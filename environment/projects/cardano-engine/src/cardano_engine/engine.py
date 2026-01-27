from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import swisseph as swe

from . import dignity
from .aspects import aspect_hits, parallels
from .dignity import almuten_of_degree, essential_dignity
from .math_utils import angular_separation_deg, norm360
from .sop import SOP
from .swisseph_utils import (
    EphemerisPaths,
    calc_declination_ut,
    calc_ecliptic_ut,
    calc_true_obliquity_ut,
    configure_swisseph,
    default_ephemeris_paths,
    find_environment_root,
    fixstar_ut,
    house_position,
    houses_ut,
    jd_ut_to_datetime_utc,
    rise_set_ut,
)


@dataclass(frozen=True)
class ChartInput:
    chart_type: str
    dt: datetime
    lat: float
    lon: float
    alt_m: float = 0.0
    question: str | None = None
    context: object | None = None
    chart_id: str | None = None


def _parse_datetime(value: str, timezone_name: str | None) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        if not timezone_name:
            raise ValueError(
                "datetime must include timezone offset (ISO 8601), e.g. 2026-01-18T16:06:00-08:00, "
                "or provide a separate timezone field (IANA name, e.g. America/Los_Angeles)."
            )
        dt = dt.replace(tzinfo=ZoneInfo(timezone_name))
    return dt


def load_input(path: Path) -> ChartInput:
    payload = json.loads(path.read_text(encoding="utf-8"))
    chart_type = str(payload["chart_type"]).strip().lower()
    tz_name = payload.get("timezone")
    dt_raw = payload.get("datetime") or payload.get("datetime_local")
    if dt_raw is None:
        raise ValueError("Missing datetime. Provide 'datetime' (ISO) or 'datetime_local' + 'timezone'.")
    dt = _parse_datetime(str(dt_raw), str(tz_name) if tz_name else None)
    loc = payload["location"]
    lat = float(loc["lat"])
    lon = float(loc["lon"])
    alt_m = float(loc.get("alt_m", 0.0))
    question = payload.get("question")
    context = payload.get("context")
    chart_id = payload.get("chart_id")
    return ChartInput(
        chart_type=chart_type,
        dt=dt,
        lat=lat,
        lon=lon,
        alt_m=alt_m,
        question=question,
        context=context,
        chart_id=chart_id,
    )


def _dt_to_jd_ut(dt: datetime) -> tuple[datetime, float]:
    dt_utc = dt.astimezone(timezone.utc)
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0 + dt_utc.microsecond / 3_600_000_000.0
    jd_ut = float(swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour))
    return dt_utc, jd_ut


def _sect_from_sun_house(sun_house_pos: float) -> str:
    # house_pos returns [1,13); houses 7-12 are above horizon.
    return "day" if 7.0 <= sun_house_pos < 13.0 else "night"


def _planetary_day_ruler(dt_local: datetime) -> str:
    # Python weekday(): Monday=0..Sunday=6
    weekday = dt_local.weekday()
    # Chaldean weekday rulers: Monday Moon, Tuesday Mars, Wednesday Mercury,
    # Thursday Jupiter, Friday Venus, Saturday Saturn, Sunday Sun
    mapping = {0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter", 4: "Venus", 5: "Saturn", 6: "Sun"}
    return mapping[weekday]


CHALDEAN_HOUR_SEQUENCE: tuple[str, ...] = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")


def _planetary_hour(dt_local: datetime, *, lat: float, lon: float, alt_m: float) -> dict:
    """
    Compute planetary hour ruler from local datetime + location.

    - Planetary day starts at sunrise.
    - Daytime hours: sunrise -> sunset split into 12 unequal hours.
    - Night hours: sunset -> next sunrise split into 12 unequal hours.
    """
    dt_utc, jd_ut = _dt_to_jd_ut(dt_local)

    rs_rise = int(swe.CALC_RISE | swe.BIT_DISC_CENTER)
    rs_set = int(swe.CALC_SET | swe.BIT_DISC_CENTER)

    eps = 1e-6  # ~0.086s; ensures “next” event queries don’t return the same instant

    # Sunrise that begins the current planetary day (always <= jd_ut, unless circumpolar).
    sunrise = rise_set_ut(jd_ut - 1.0, body=swe.SUN, lon=lon, lat=lat, alt_m=alt_m, rsmi=rs_rise)
    sunset = rise_set_ut(sunrise + eps, body=swe.SUN, lon=lon, lat=lat, alt_m=alt_m, rsmi=rs_set)
    sunrise_next = rise_set_ut(sunrise + 0.5, body=swe.SUN, lon=lon, lat=lat, alt_m=alt_m, rsmi=rs_rise)

    if sunrise <= jd_ut < sunset:
        is_day = True
        segment_start = sunrise
        segment_end = sunset
    else:
        is_day = False
        segment_start = sunset
        segment_end = sunrise_next

    hour_len = (segment_end - segment_start) / 12.0
    if hour_len <= 0:
        raise RuntimeError("Invalid planetary hour length computed")

    hour_index = int((jd_ut - segment_start) // hour_len)
    hour_index = max(0, min(11, hour_index))

    sunrise_dt_utc = jd_ut_to_datetime_utc(sunrise)
    sunrise_dt_local = sunrise_dt_utc.astimezone(dt_local.tzinfo or timezone.utc)
    day_ruler = _planetary_day_ruler(sunrise_dt_local)

    start_idx = CHALDEAN_HOUR_SEQUENCE.index(day_ruler)
    seq = [CHALDEAN_HOUR_SEQUENCE[(start_idx + i) % 7] for i in range(24)]

    ruler = seq[hour_index] if is_day else seq[12 + hour_index]

    return {
        "ruler": ruler,
        "day_ruler": day_ruler,
        "is_day": is_day,
        "hour_index": hour_index + (0 if is_day else 12),
        "hour_index_in_segment": hour_index,
        "sunrise_utc": sunrise_dt_utc.isoformat(),
        "sunset_utc": jd_ut_to_datetime_utc(sunset).isoformat(),
        "sunrise_next_utc": jd_ut_to_datetime_utc(sunrise_next).isoformat(),
        "segment_start_utc": jd_ut_to_datetime_utc(segment_start).isoformat(),
        "segment_end_utc": jd_ut_to_datetime_utc(segment_end).isoformat(),
        "hour_length_minutes": hour_len * 24.0 * 60.0,
        "dt_utc": dt_utc.isoformat(),
    }


def _whole_sign_house_number(asc_lon: float, body_lon: float) -> int:
    asc_sign = int(norm360(asc_lon) // 30.0)
    body_sign = int(norm360(body_lon) // 30.0)
    return int(((body_sign - asc_sign) % 12) + 1)


def _antiscia_solstice(lon: float) -> float:
    # Reflection across 0 Cancer / 0 Capricorn axis.
    return norm360(180.0 - lon)


def _antiscia_reverse(lon: float) -> float:
    # Alternate formula seen in operator notes: reverse longitude.
    return norm360(360.0 - lon)


def _contra(lon: float) -> float:
    return norm360(lon + 180.0)


def _dodecatemoria(lon: float) -> float:
    lon = norm360(lon)
    start = float(int(lon // 30.0) * 30)
    return norm360(lon + 12.0 * (lon - start))


def compute_chart(inp: ChartInput, *, eph: EphemerisPaths | None = None) -> dict:
    if eph is None:
        eph = default_ephemeris_paths()

    configure_swisseph(eph.ephe_dir)

    # Sidereal mode: Lahiri / Chitra Paksha.
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    dt_utc, jd_ut = _dt_to_jd_ut(inp.dt)
    ayanamsa = float(swe.get_ayanamsa_ut(jd_ut))

    # Always set topo (altitude defaults to 0 if unknown).
    swe.set_topo(inp.lon, inp.lat, inp.alt_m)

    bodies = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "MeanNode": swe.MEAN_NODE,
        "TrueNode": swe.TRUE_NODE,
    }

    # Houses + angles (tropical)
    if inp.chart_type in ("horary", "crow"):
        hsys = SOP.HORARY_HOUSES
    else:
        hsys = SOP.NATAL_HOUSES
    cusps, ascmc = houses_ut(jd_ut, inp.lat, inp.lon, hsys)
    asc = norm360(ascmc[0])
    mc = norm360(ascmc[1])
    armc = float(ascmc[2])
    eps = calc_true_obliquity_ut(jd_ut)

    # Sun house position for sect
    sun_geo, _ = calc_ecliptic_ut(jd_ut, swe.SUN, topocentric=False, sidereal=False)
    sun_house_pos = house_position(armc=armc, geolat=inp.lat, eps=eps, lon=sun_geo["lon"], lat=sun_geo["lat"], hsys=hsys)
    sect = _sect_from_sun_house(sun_house_pos)

    # Planetary hour
    planetary_hour = _planetary_hour(inp.dt, lat=inp.lat, lon=inp.lon, alt_m=inp.alt_m)
    hour_ruler = str(planetary_hour["ruler"])

    # Compute longitudes / declinations
    bodies_out: dict[str, dict] = {}
    tropical_lons: dict[str, float] = {}
    decls: dict[str, float] = {}

    for name, body_id in bodies.items():
        # Topocentric tropical
        topo_trop, topo_trop_rf = calc_ecliptic_ut(jd_ut, body_id, topocentric=True, sidereal=False)
        # Geocentric tropical for audit
        geo_trop, geo_trop_rf = calc_ecliptic_ut(jd_ut, body_id, topocentric=False, sidereal=False)
        # Sidereal topo
        topo_sid, topo_sid_rf = calc_ecliptic_ut(jd_ut, body_id, topocentric=True, sidereal=True)

        lon_trop = topo_trop["lon"]
        tropical_lons[name] = lon_trop

        dec = calc_declination_ut(jd_ut, body_id, topocentric=True)
        decls[name] = dec

        sign = dignity.SIGNS[int(lon_trop // 30.0)]
        deg_in = lon_trop - float(int(lon_trop // 30.0) * 30)

        # House number: for horary/natal use computed house_pos; overlays use whole sign elsewhere.
        hpos = house_position(
            armc=armc, geolat=inp.lat, eps=eps, lon=topo_trop["lon"], lat=topo_trop["lat"], hsys=hsys
        )
        house_num = int(hpos) if hpos < 13.0 else 12

        ed = None
        if name in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
            ed = essential_dignity(name, lon_trop, sect=sect)

        bodies_out[name] = {
            "tropical": {
                "lon": topo_trop["lon"],
                "lat": topo_trop["lat"],
                "deg_in_sign": deg_in,
                "sign": sign,
                "speed_lon": topo_trop["speed_lon"],
                "geocentric_lon": geo_trop["lon"],
                "retflags_topocentric": topo_trop_rf,
                "retflags_geocentric": geo_trop_rf,
            },
            "sidereal_lahiri": {
                "lon": topo_sid["lon"],
                "lat": topo_sid["lat"],
                "retflags_topocentric": topo_sid_rf,
            },
            "draconic": {},  # filled below
            "declination": dec,
            "house": {
                "system": hsys.decode("ascii"),
                "position": hpos,
                "number": house_num,
            },
            "essential_dignity": None if ed is None else {"score": ed.score, "breakdown": ed.breakdown},
        }

    mean_node_lon = tropical_lons["MeanNode"]
    for name in bodies_out:
        bodies_out[name]["draconic"] = {
            "lon": norm360(bodies_out[name]["tropical"]["lon"] - mean_node_lon),
        }

    # Whole sign overlays for sidereal/draconic (per SOP)
    asc_sid = norm360(asc - ayanamsa)
    mc_sid = norm360(mc - ayanamsa)
    asc_drac = norm360(asc - mean_node_lon)
    mc_drac = norm360(mc - mean_node_lon)

    for name in bodies_out:
        lon_t = float(bodies_out[name]["tropical"]["lon"])
        lon_s = float(bodies_out[name]["sidereal_lahiri"]["lon"])
        lon_d = float(bodies_out[name]["draconic"]["lon"])
        bodies_out[name]["whole_sign_houses"] = {
            "tropical": _whole_sign_house_number(asc, lon_t),
            "sidereal_lahiri": _whole_sign_house_number(asc_sid, lon_s),
            "draconic": _whole_sign_house_number(asc_drac, lon_d),
        }

    # Angles as pseudo-bodies (tropical + shifted overlays)
    bodies_out["Asc"] = {
        "tropical": {"lon": asc},
        "sidereal_lahiri": {"lon": asc_sid},
        "draconic": {"lon": asc_drac},
    }
    bodies_out["MC"] = {
        "tropical": {"lon": mc},
        "sidereal_lahiri": {"lon": mc_sid},
        "draconic": {"lon": mc_drac},
    }

    # Essential dignity of Asc degree (almuten) + ASC ruler
    asc_sign = dignity.SIGNS[int(asc // 30.0)]
    asc_ruler = dignity.DOMICILE_RULER_BY_SIGN[asc_sign]
    asc_almuten_scores = almuten_of_degree(asc, sect=sect)
    max_score = max(asc_almuten_scores.values())
    asc_almuten = sorted([p for p, s in asc_almuten_scores.items() if s == max_score])

    # Flags (compute-only)
    flags: list[str] = []
    asc_deg = asc - float(int(asc // 30.0) * 30)
    if asc_deg < 3.0:
        flags.append("ASC too early (< 3°)")
    if asc_deg > 27.0:
        flags.append("ASC too late (> 27°)")

    # Saturn in 7th (horary/crow only)
    if inp.chart_type in ("horary", "crow"):
        sat_house = int(bodies_out["Saturn"]["house"]["number"])
        if sat_house == 7:
            flags.append("Saturn in 7th (flag)")

    # Planetary hour mismatch
    if hour_ruler != asc_ruler and hour_ruler not in asc_almuten:
        flags.append("Planetary Hour mismatch (flag: not radical)")

    # Combustion checks
    sun_lon = bodies_out["Sun"]["tropical"]["lon"]
    for name in ("Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
        sep = angular_separation_deg(bodies_out[name]["tropical"]["lon"], sun_lon)
        bodies_out[name]["combustion"] = {"sep_deg": sep, "combust": sep <= SOP.COMBUSTION_ORB_DEG}

    # Major aspects (tropical topo)
    aspect_list = [a.__dict__ for a in aspect_hits({k: v for k, v in tropical_lons.items() if k in SOP.MOIETIES_DEG})]

    # Parallels
    parallel_list = [p.__dict__ for p in parallels({k: v for k, v in decls.items() if k in SOP.MOIETIES_DEG})]

    # Fixed star conjunctions (tropical)
    fixed_hits: list[dict] = []
    for star in SOP.FIXED_STARS_DEFAULT:
        try:
            s = fixstar_ut(jd_ut, star, sidereal=False)
        except Exception:
            continue
        orb_limit = SOP.FIXED_STAR_ORB_EXCEPTIONS_DEG.get(star, SOP.FIXED_STAR_ORB_DEFAULT_DEG)
        for body in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
            sep = angular_separation_deg(s["lon"], bodies_out[body]["tropical"]["lon"])
            if sep <= orb_limit:
                fixed_hits.append({"star": s["name"], "body": body, "orb_deg": sep, "limit_deg": orb_limit, "star_lon": s["lon"]})
        for angle in ("Asc", "MC"):
            sep = angular_separation_deg(s["lon"], bodies_out[angle]["tropical"]["lon"])
            if sep <= orb_limit:
                fixed_hits.append({"star": s["name"], "body": angle, "orb_deg": sep, "limit_deg": orb_limit, "star_lon": s["lon"]})
    fixed_hits.sort(key=lambda x: (x["orb_deg"], x["star"], x["body"]))

    # Antiscia / contra contacts (tropical)
    antiscia_contacts: list[dict] = []
    bodies_for_antiscia = ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Asc", "MC")
    lon_map = {b: bodies_out[b]["tropical"]["lon"] for b in bodies_for_antiscia}
    for a in bodies_for_antiscia:
        a_lon = lon_map[a]
        anti = _antiscia_solstice(a_lon)
        contra = _contra(anti)
        anti_alt = _antiscia_reverse(a_lon)
        contra_alt = _contra(anti_alt)
        for b in bodies_for_antiscia:
            if a == b:
                continue
            b_lon = lon_map[b]
            for kind, point in (
                ("antiscia", anti),
                ("contra_antiscia", contra),
                ("antiscia_alt", anti_alt),
                ("contra_antiscia_alt", contra_alt),
            ):
                sep = angular_separation_deg(point, b_lon)
                if sep <= SOP.ANTISCIA_CONTACT_ORB_DEG:
                    antiscia_contacts.append({"a": a, "b": b, "kind": kind, "orb_deg": sep})
    antiscia_contacts.sort(key=lambda x: (x["orb_deg"], x["kind"], x["a"], x["b"]))

    # Dodecatemoria positions (tropical)
    dodec: dict[str, dict] = {}
    for name in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
        lon = bodies_out[name]["tropical"]["lon"]
        dlon = _dodecatemoria(lon)
        dsign = dignity.SIGNS[int(dlon // 30.0)]
        ddeg = dlon - float(int(dlon // 30.0) * 30)
        dodec[name] = {"lon": dlon, "sign": dsign, "deg_in_sign": ddeg}

    # Moon sequence + VOC flag (simple scan + refinement)
    moon_sequence: list[dict] = []
    moon_lon0 = bodies_out["Moon"]["tropical"]["lon"]
    moon_sign_start = float(int(moon_lon0 // 30.0) * 30)
    moon_sign_end = moon_sign_start + 30.0

    # Rough end time: step forward until Moon leaves sign (max 4 days).
    jd_end = jd_ut
    for _ in range(0, 96):  # 96 hours
        jd_end += 1.0 / 24.0
        moon_pos, _ = calc_ecliptic_ut(jd_end, swe.MOON, topocentric=True, sidereal=False)
        if moon_pos["lon"] < moon_sign_start or moon_pos["lon"] >= moon_sign_end:
            break

    def sep_minus_aspect(jd: float, aspect_deg: float, body_id: int) -> float:
        m, _ = calc_ecliptic_ut(jd, swe.MOON, topocentric=True, sidereal=False)
        p, _ = calc_ecliptic_ut(jd, body_id, topocentric=True, sidereal=False)
        return angular_separation_deg(m["lon"], p["lon"]) - aspect_deg

    # Scan for crossings for each planet/aspect.
    scan_step = 1.0 / 24.0  # 1 hour
    targets = {"Sun": swe.SUN, "Mercury": swe.MERCURY, "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN}
    for body_name, body_id in targets.items():
        for aspect_name, aspect_deg in SOP.MAJOR_ASPECTS_DEG:
            t0 = jd_ut
            f0 = sep_minus_aspect(t0, aspect_deg, body_id)
            t = t0
            while t < jd_end:
                t1 = min(t + scan_step, jd_end)
                f1 = sep_minus_aspect(t1, aspect_deg, body_id)
                if f0 == 0.0:
                    bracket = (t, t)
                elif f0 * f1 <= 0.0:
                    bracket = (t, t1)
                else:
                    bracket = None

                if bracket is not None:
                    lo, hi = bracket
                    # Refine by bisection to ~1 second.
                    for _ in range(0, 40):
                        mid = (lo + hi) / 2.0
                        fm = sep_minus_aspect(mid, aspect_deg, body_id)
                        if abs(fm) < 1e-6:
                            lo = hi = mid
                            break
                        if f0 * fm <= 0.0:
                            hi = mid
                            f1 = fm
                        else:
                            lo = mid
                            f0 = fm
                    jd_hit = (lo + hi) / 2.0
                    mpos, _ = calc_ecliptic_ut(jd_hit, swe.MOON, topocentric=True, sidereal=False)
                    ppos, _ = calc_ecliptic_ut(jd_hit, body_id, topocentric=True, sidereal=False)
                    sep = angular_separation_deg(mpos["lon"], ppos["lon"])
                    orb = abs(sep - aspect_deg)
                    moon_sequence.append({"jd_ut": jd_hit, "body": body_name, "aspect": aspect_name, "orb_deg": orb})
                    break

                t = t1
                f0 = f1

    moon_sequence.sort(key=lambda ev: ev["jd_ut"])
    if not moon_sequence:
        flags.append("Moon Void of Course (flag)")

    # Convert moon sequence times to ISO UTC for the report
    moon_seq_out: list[dict] = []
    for ev in moon_sequence:
        dt_ev = jd_ut_to_datetime_utc(float(ev["jd_ut"]))
        moon_seq_out.append(
            {"datetime_utc": dt_ev.isoformat(), "body": ev["body"], "aspect": ev["aspect"], "orb_deg": ev["orb_deg"]}
        )

    # Dispositors (domicile + exaltation) for each classical planet
    dispositor: dict[str, dict] = {}
    for name in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
        sign = bodies_out[name]["tropical"]["sign"]
        dispositor[name] = {
            "domicile_ruler": dignity.DOMICILE_RULER_BY_SIGN[sign],
            "exaltation_ruler": dignity.EXALTATION_RULER_BY_SIGN.get(sign),
        }

    env_root = find_environment_root()
    planet_file, planet_start, planet_end, planet_denum = swe.get_current_file_data(0)
    moon_file, moon_start, moon_end, moon_denum = swe.get_current_file_data(1)
    asteroid_file, asteroid_start, asteroid_end, asteroid_denum = swe.get_current_file_data(2)
    star_file, star_start, star_end, star_denum = swe.get_current_file_data(4)

    result = {
        "meta": {
            "engine": "cardano-engine",
            "engine_version": "0.1.0",
            "python": f"{swe.__file__}",
            "swisseph_version": getattr(swe, "__version__", None),
            "ephemeris_dir": str(eph.ephe_dir),
            "environment_root": str(env_root),
            "swe_files": {
                "planet": {"path": planet_file, "start_jd": planet_start, "end_jd": planet_end, "denum": planet_denum},
                "moon": {"path": moon_file, "start_jd": moon_start, "end_jd": moon_end, "denum": moon_denum},
                "asteroid": {
                    "path": asteroid_file,
                    "start_jd": asteroid_start,
                    "end_jd": asteroid_end,
                    "denum": asteroid_denum,
                },
                "stars": {"path": star_file, "start_jd": star_start, "end_jd": star_end, "denum": star_denum},
            },
        },
        "chart": {
            "chart_type": inp.chart_type,
            "datetime_input": inp.dt.isoformat(),
            "datetime_utc": dt_utc.isoformat(),
            "location": {"lat": inp.lat, "lon": inp.lon, "alt_m": inp.alt_m},
            "house_system": hsys.decode("ascii"),
            "sect": sect,
            "asc_ruler": asc_ruler,
            "asc_almuten": {"winners": asc_almuten, "scores": asc_almuten_scores},
            "planetary_hour": planetary_hour,
            "ayanamsa_lahiri": ayanamsa,
            "question": inp.question,
            "context": inp.context,
            "angles": {
                "tropical": {"Asc": asc, "MC": mc},
                "sidereal_lahiri": {"Asc": asc_sid, "MC": mc_sid},
                "draconic": {"Asc": asc_drac, "MC": mc_drac},
            },
            "houses": {"cusps": cusps, "ascmc": ascmc},
        },
        "flags": flags,
        "bodies": bodies_out,
        "dispositors": dispositor,
        "aspects": aspect_list,
        "parallels": parallel_list,
        "antiscia_contacts": antiscia_contacts,
        "dodecatemoria": dodec,
        "fixed_stars": fixed_hits,
        "moon_sequence": moon_seq_out,
    }
    return result
