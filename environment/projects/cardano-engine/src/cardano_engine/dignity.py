from __future__ import annotations

from dataclasses import dataclass

from .math_utils import norm360


SIGNS: tuple[str, ...] = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)


def sign_index(longitude: float) -> int:
    return int(norm360(longitude) // 30.0)


def sign_start(longitude: float) -> float:
    return float(sign_index(longitude) * 30)


def degree_in_sign(longitude: float) -> float:
    return norm360(longitude) - sign_start(longitude)


DOMICILE_RULER_BY_SIGN: dict[str, str] = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

EXALTATION_RULER_BY_SIGN: dict[str, str] = {
    "Aries": "Sun",
    "Taurus": "Moon",
    "Cancer": "Jupiter",
    "Virgo": "Mercury",
    "Libra": "Saturn",
    "Capricorn": "Mars",
    "Pisces": "Venus",
}

EXALTATION_SIGN_BY_PLANET: dict[str, str] = {v: k for (k, v) in EXALTATION_RULER_BY_SIGN.items()}


def opposite_sign(sign: str) -> str:
    idx = SIGNS.index(sign)
    return SIGNS[(idx + 6) % 12]


# Dorothean triplicity rulers.
# Each entry: (day_ruler, night_ruler, participating_ruler)
TRIPLICITY_BY_ELEMENT: dict[str, tuple[str, str, str]] = {
    "fire": ("Sun", "Jupiter", "Saturn"),
    "earth": ("Venus", "Moon", "Mars"),
    "air": ("Saturn", "Mercury", "Jupiter"),
    "water": ("Venus", "Mars", "Moon"),
}

ELEMENT_BY_SIGN: dict[str, str] = {
    "Aries": "fire",
    "Leo": "fire",
    "Sagittarius": "fire",
    "Taurus": "earth",
    "Virgo": "earth",
    "Capricorn": "earth",
    "Gemini": "air",
    "Libra": "air",
    "Aquarius": "air",
    "Cancer": "water",
    "Scorpio": "water",
    "Pisces": "water",
}


# Egyptian bounds/terms table.
# Each sign is a list of (end_degree, ruler). Degrees are within sign (0..30).
EGYPTIAN_TERMS: dict[str, list[tuple[float, str]]] = {
    "Aries": [(6, "Jupiter"), (14, "Venus"), (21, "Mercury"), (26, "Mars"), (30, "Saturn")],
    "Taurus": [(8, "Venus"), (14, "Mercury"), (22, "Jupiter"), (27, "Saturn"), (30, "Mars")],
    "Gemini": [(7, "Mercury"), (14, "Jupiter"), (21, "Venus"), (25, "Mars"), (30, "Saturn")],
    "Cancer": [(7, "Mars"), (13, "Venus"), (19, "Mercury"), (26, "Jupiter"), (30, "Saturn")],
    "Leo": [(6, "Saturn"), (13, "Mercury"), (19, "Venus"), (25, "Jupiter"), (30, "Mars")],
    "Virgo": [(7, "Mercury"), (13, "Venus"), (18, "Jupiter"), (24, "Mars"), (30, "Saturn")],
    "Libra": [(6, "Saturn"), (14, "Mercury"), (21, "Jupiter"), (28, "Venus"), (30, "Mars")],
    "Scorpio": [(7, "Mars"), (13, "Venus"), (19, "Mercury"), (24, "Jupiter"), (30, "Saturn")],
    "Sagittarius": [(12, "Jupiter"), (17, "Venus"), (21, "Mercury"), (26, "Saturn"), (30, "Mars")],
    "Capricorn": [(7, "Mercury"), (14, "Jupiter"), (22, "Venus"), (26, "Saturn"), (30, "Mars")],
    "Aquarius": [(7, "Mercury"), (13, "Venus"), (20, "Jupiter"), (25, "Mars"), (30, "Saturn")],
    "Pisces": [(12, "Venus"), (19, "Jupiter"), (24, "Mercury"), (27, "Mars"), (30, "Saturn")],
}


CHALDEAN_DECAN_SEQUENCE: tuple[str, ...] = ("Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter")


def face_ruler(sign: str, deg_in_sign: float) -> str:
    # Aries 0-10 starts with Mars, then follow Chaldean order continuously through the zodiac.
    sign_idx = SIGNS.index(sign)
    decan_idx_in_sign = int(deg_in_sign // 10.0)  # 0,1,2
    global_decan_index = sign_idx * 3 + decan_idx_in_sign
    return CHALDEAN_DECAN_SEQUENCE[global_decan_index % len(CHALDEAN_DECAN_SEQUENCE)]


def term_ruler(sign: str, deg_in_sign: float) -> str:
    for end_deg, ruler in EGYPTIAN_TERMS[sign]:
        if deg_in_sign < end_deg:
            return ruler
    # Defensive fallback
    return EGYPTIAN_TERMS[sign][-1][1]


@dataclass(frozen=True)
class EssentialDignity:
    sign: str
    deg_in_sign: float
    domicile: bool
    exaltation: bool
    triplicity: bool
    term: bool
    face: bool
    detriment: bool
    fall: bool
    peregrine: bool
    score: int
    breakdown: dict[str, int]


def essential_dignity(planet: str, longitude: float, *, sect: str) -> EssentialDignity:
    """
    Essential dignity per locked SOP:
    - Triplicity: Dorothean (sect ruler only) scored +3 when applicable.
    - Terms: Egyptian (+2), Faces: Chaldean (+1)
    - Domicile +5, Exalt +4; Detriment -5, Fall -4; Peregrine -5 when no other dignity and not in detriment/fall.
    """
    lon = norm360(longitude)
    sign = SIGNS[int(lon // 30.0)]
    deg = lon - float(SIGNS.index(sign) * 30)

    domicile_ruler = DOMICILE_RULER_BY_SIGN[sign]
    exalt_ruler = EXALTATION_RULER_BY_SIGN.get(sign)
    element = ELEMENT_BY_SIGN[sign]
    trip_day, trip_night, _trip_part = TRIPLICITY_BY_ELEMENT[element]
    trip_ruler = trip_day if sect == "day" else trip_night

    term = term_ruler(sign, deg)
    face = face_ruler(sign, deg)

    breakdown: dict[str, int] = {}

    is_domicile = planet == domicile_ruler
    if is_domicile:
        breakdown["domicile"] = 5

    is_exalt = planet == exalt_ruler
    if is_exalt:
        breakdown["exaltation"] = 4

    is_triplicity = planet == trip_ruler
    if is_triplicity:
        breakdown["triplicity"] = 3

    is_term = planet == term
    if is_term:
        breakdown["term"] = 2

    is_face = planet == face
    if is_face:
        breakdown["face"] = 1

    # Detriment / fall
    is_detriment = DOMICILE_RULER_BY_SIGN[opposite_sign(sign)] == planet
    if is_detriment:
        breakdown["detriment"] = -5

    exalt_sign = EXALTATION_SIGN_BY_PLANET.get(planet)
    is_fall = exalt_sign is not None and opposite_sign(exalt_sign) == sign
    if is_fall:
        breakdown["fall"] = -4

    has_any_positive = any(k in breakdown for k in ("domicile", "exaltation", "triplicity", "term", "face"))
    is_peregrine = (not has_any_positive) and (not is_detriment) and (not is_fall)
    if is_peregrine:
        breakdown["peregrine"] = -5

    score = int(sum(breakdown.values()))

    return EssentialDignity(
        sign=sign,
        deg_in_sign=deg,
        domicile=is_domicile,
        exaltation=is_exalt,
        triplicity=is_triplicity,
        term=is_term,
        face=is_face,
        detriment=is_detriment,
        fall=is_fall,
        peregrine=is_peregrine,
        score=score,
        breakdown=breakdown,
    )


def almuten_of_degree(longitude: float, *, sect: str) -> dict[str, int]:
    """
    Compute almuten scores for a single zodiac degree using SOP weights.
    Returns a dict planet->score (can be tied).
    """
    lon = norm360(longitude)
    sign = SIGNS[int(lon // 30.0)]
    deg = lon - float(SIGNS.index(sign) * 30)

    scores: dict[str, int] = {p: 0 for p in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn")}

    # Domicile
    scores[DOMICILE_RULER_BY_SIGN[sign]] += 5

    # Exaltation
    exalt = EXALTATION_RULER_BY_SIGN.get(sign)
    if exalt:
        scores[exalt] += 4

    # Triplicity (sect ruler)
    element = ELEMENT_BY_SIGN[sign]
    day_ruler, night_ruler, _ = TRIPLICITY_BY_ELEMENT[element]
    scores[day_ruler if sect == "day" else night_ruler] += 3

    # Term
    scores[term_ruler(sign, deg)] += 2

    # Face
    scores[face_ruler(sign, deg)] += 1

    return scores


