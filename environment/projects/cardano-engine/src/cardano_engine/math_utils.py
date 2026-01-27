from __future__ import annotations


def norm360(deg: float) -> float:
    """Normalize degrees to [0, 360)."""
    return deg % 360.0


def wrap180(deg: float) -> float:
    """Wrap degrees to (-180, 180]."""
    x = (deg + 180.0) % 360.0 - 180.0
    # Prefer +180 over -180 for determinism.
    return 180.0 if x == -180.0 else x


def angular_separation_deg(a: float, b: float) -> float:
    """Return the smallest angular separation between two longitudes (0..180)."""
    return abs(wrap180(a - b))


