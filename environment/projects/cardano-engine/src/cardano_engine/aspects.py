from __future__ import annotations

from dataclasses import dataclass

from .math_utils import angular_separation_deg
from .sop import SOP


@dataclass(frozen=True)
class AspectHit:
    a: str
    b: str
    aspect: str
    exact_deg: float
    separation_deg: float
    orb_deg: float
    allowed_orb_deg: float
    partile: bool
    weak_wide: bool


def allowed_orb_deg(a: str, b: str) -> float | None:
    ma = SOP.MOIETIES_DEG.get(a)
    mb = SOP.MOIETIES_DEG.get(b)
    if ma is None or mb is None:
        return None
    return (ma + mb) / 2.0


def aspect_hits(longitudes: dict[str, float]) -> list[AspectHit]:
    bodies = [b for b in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn") if b in longitudes]
    hits: list[AspectHit] = []
    for i, a in enumerate(bodies):
        for b in bodies[i + 1 :]:
            sep = angular_separation_deg(longitudes[a], longitudes[b])
            for aspect_name, exact in SOP.MAJOR_ASPECTS_DEG:
                orb = abs(sep - exact)
                ao = allowed_orb_deg(a, b)
                if ao is None:
                    continue
                if orb <= ao:
                    hits.append(
                        AspectHit(
                            a=a,
                            b=b,
                            aspect=aspect_name,
                            exact_deg=exact,
                            separation_deg=sep,
                            orb_deg=orb,
                            allowed_orb_deg=ao,
                            partile=orb < 1.0,
                            weak_wide=orb > SOP.STRICT_WEAK_ASPECT_ORB_DEG,
                        )
                    )
    hits.sort(key=lambda h: (h.orb_deg, h.a, h.b, h.aspect))
    return hits


@dataclass(frozen=True)
class ParallelHit:
    a: str
    b: str
    kind: str  # parallel | contra-parallel
    decl_a: float
    decl_b: float
    orb_deg: float
    nuclear: bool


def parallels(declinations: dict[str, float]) -> list[ParallelHit]:
    bodies = [b for b in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn") if b in declinations]
    hits: list[ParallelHit] = []
    for i, a in enumerate(bodies):
        for b in bodies[i + 1 :]:
            da = declinations[a]
            db = declinations[b]

            orb_parallel = abs(da - db)
            if orb_parallel <= SOP.PARALLEL_ORB_DEG:
                hits.append(
                    ParallelHit(
                        a=a,
                        b=b,
                        kind="parallel",
                        decl_a=da,
                        decl_b=db,
                        orb_deg=orb_parallel,
                        nuclear=orb_parallel <= SOP.NUCLEAR_LOCK_ORB_DEG,
                    )
                )

            orb_contra = abs(da + db)
            if orb_contra <= SOP.PARALLEL_ORB_DEG:
                hits.append(
                    ParallelHit(
                        a=a,
                        b=b,
                        kind="contra-parallel",
                        decl_a=da,
                        decl_b=db,
                        orb_deg=orb_contra,
                        nuclear=orb_contra <= SOP.NUCLEAR_LOCK_ORB_DEG,
                    )
                )

    hits.sort(key=lambda h: (h.orb_deg, h.kind, h.a, h.b))
    return hits


