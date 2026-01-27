from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

from .math_utils import norm360


@dataclass(frozen=True)
class EphemerisPaths:
    ephe_dir: Path


def find_environment_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "environment" and (parent / "SOP.md").exists():
            return parent
    raise RuntimeError(f"Could not locate environment root from {here}")


def default_ephemeris_paths() -> EphemerisPaths:
    env_root = find_environment_root()
    ephe_dir = env_root / "data" / "sweph"
    return EphemerisPaths(ephe_dir=ephe_dir)


def configure_swisseph(ephe_dir: Path) -> None:
    swe.set_ephe_path(str(ephe_dir))


def _require_swisseph(retflags: int, *, what: str) -> None:
    # In strict forensic mode, falling back to Moshier is a hard failure.
    if int(retflags) & int(swe.FLG_SWIEPH) == 0:
        raise RuntimeError(
            f"{what}: Swiss Ephemeris files not in use (retflags={retflags}). "
            "Expected FLG_SWIEPH; refusing fallback."
        )


def julian_day_ut(year: int, month: int, day: int, hour_ut: float) -> float:
    return float(swe.julday(year, month, day, hour_ut))


def calc_ecliptic_ut(jd_ut: float, body: int, *, topocentric: bool, sidereal: bool) -> tuple[dict[str, float], int]:
    flags = int(swe.FLG_SWIEPH | swe.FLG_SPEED)
    if topocentric:
        flags |= int(swe.FLG_TOPOCTR)
    if sidereal:
        flags |= int(swe.FLG_SIDEREAL)
    xx, retflags = swe.calc_ut(jd_ut, body, flags)
    _require_swisseph(int(retflags), what=f"calc_ut(body={body})")
    return (
        {
            "lon": norm360(float(xx[0])),
            "lat": float(xx[1]),
            "dist_au": float(xx[2]),
            "speed_lon": float(xx[3]),
            "speed_lat": float(xx[4]),
            "speed_dist": float(xx[5]),
        },
        int(retflags),
    )


def calc_declination_ut(jd_ut: float, body: int, *, topocentric: bool) -> float:
    flags = int(swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL)
    if topocentric:
        flags |= int(swe.FLG_TOPOCTR)
    xx, retflags = swe.calc_ut(jd_ut, body, flags)
    _require_swisseph(int(retflags), what=f"calc_ut_equatorial(body={body})")
    # xx[1] is declination (degrees) in equatorial mode
    return float(xx[1])


def calc_true_obliquity_ut(jd_ut: float) -> float:
    xx, _ = swe.calc_ut(jd_ut, swe.ECL_NUT)
    return float(xx[0])


def houses_ut(jd_ut: float, lat: float, lon: float, hsys: bytes) -> tuple[tuple[float, ...], tuple[float, ...]]:
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys)
    return tuple(float(x) for x in cusps), tuple(float(x) for x in ascmc)


def house_position(
    *,
    armc: float,
    geolat: float,
    eps: float,
    lon: float,
    lat: float,
    hsys: bytes,
) -> float:
    return float(swe.house_pos(armc, geolat, eps, (lon, lat), hsys))


def fixstar_ut(jd_ut: float, name: str, *, sidereal: bool) -> dict[str, float]:
    flags = int(swe.FLG_SWIEPH | swe.FLG_SPEED)
    if sidereal:
        flags |= int(swe.FLG_SIDEREAL)
    xx, stnam, retflags = swe.fixstar2_ut(name, jd_ut, flags)
    _require_swisseph(int(retflags), what=f"fixstar2_ut({name!r})")
    return {
        "name": stnam,
        "lon": norm360(float(xx[0])),
        "lat": float(xx[1]),
        "dist_au": float(xx[2]),
    }


def jd_ut_to_datetime_utc(jd_ut: float) -> datetime:
    y, m, d, hour = swe.revjul(jd_ut)
    hh = int(hour)
    mm = int((hour - hh) * 60)
    ss_float = (((hour - hh) * 60) - mm) * 60
    ss = int(ss_float)
    us = int(round((ss_float - ss) * 1_000_000))
    if us == 1_000_000:
        ss += 1
        us = 0
    return datetime(y, m, d, hh, mm, ss, us, tzinfo=timezone.utc)


def rise_set_ut(
    jd_ut: float,
    *,
    body: int,
    lon: float,
    lat: float,
    alt_m: float,
    rsmi: int,
    atpress: float = 0.0,
    attemp: float = 0.0,
) -> float:
    res, tret = swe.rise_trans(jd_ut, body, rsmi, (lon, lat, alt_m), atpress, attemp)
    if res != 0:
        raise RuntimeError(f"rise_trans failed with code {res}")
    return float(tret[0])

