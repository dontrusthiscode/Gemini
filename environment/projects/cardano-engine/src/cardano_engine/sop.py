from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SopConfig:
    # House systems
    HORARY_HOUSES: bytes = b"R"  # Regiomontanus
    NATAL_HOUSES: bytes = b"P"  # Placidus

    # Ayanamsa
    SIDEREAL_MODE: int = 1  # swe.SIDM_LAHIRI (resolved at runtime to avoid importing swe here)

    # Nodes
    DEFAULT_NODE: str = "mean"

    # Aspect policy
    MAJOR_ASPECTS_DEG: tuple[tuple[str, float], ...] = (
        ("conjunction", 0.0),
        ("sextile", 60.0),
        ("square", 90.0),
        ("trine", 120.0),
        ("opposition", 180.0),
    )
    STRICT_WEAK_ASPECT_ORB_DEG: float = 3.0

    # Lilly moieties (half-orbs)
    MOIETIES_DEG: dict[str, float] = None  # initialized below

    # Declination parallels
    PARALLEL_ORB_DEG: float = 1.0
    NUCLEAR_LOCK_ORB_DEG: float = 0.2

    # Combustion
    COMBUSTION_ORB_DEG: float = 8.5

    # Antiscia contact orb
    ANTISCIA_CONTACT_ORB_DEG: float = 1.0

    # Fixed stars
    FIXED_STAR_ORB_DEFAULT_DEG: float = 1.0
    FIXED_STAR_ORB_EXCEPTIONS_DEG: dict[str, float] = None  # initialized below
    FIXED_STARS_DEFAULT: tuple[str, ...] = (
        "Algol",
        "Alcyone",  # Pleiades
        "Aldebaran",
        "Sirius",
        "Castor",
        "Pollux",
        "Regulus",
        "Spica",
        "Arcturus",
        "Antares",
        "Vega",
        "Altair",
        "Fomalhaut",
        "Markab",
        "Scheat",
        "Alphard",
    )


_DEFAULT_MOIETIES: dict[str, float] = {
    "Sun": 7.5,
    "Moon": 6.0,
    "Saturn": 4.5,
    "Jupiter": 4.5,
    "Mars": 3.5,
    "Venus": 3.5,
    "Mercury": 3.5,
}

_DEFAULT_FIXED_STAR_EXCEPTIONS: dict[str, float] = {
    "Regulus": 1.5,
    "Spica": 1.5,
    "Algol": 1.5,
    "Sirius": 1.5,
}

# Attach defaults to frozen dataclass (since default dicts are not hashable).
SOP = SopConfig(MOIETIES_DEG=_DEFAULT_MOIETIES, FIXED_STAR_ORB_EXCEPTIONS_DEG=_DEFAULT_FIXED_STAR_EXCEPTIONS)

