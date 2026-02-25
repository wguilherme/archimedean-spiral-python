import math
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class SpiralParams:
    r_start: float          # inner radius (mm)
    r_end: float            # outer radius (mm)
    turns: int              # number of full turns
    points_per_turn: int = 360  # angular resolution


def generate_spiral(params: SpiralParams) -> List[Tuple[float, float]]:
    """
    Generate an Archimedean spiral as a list of (x, y) points in mm.

    The spiral follows the law:
        r(t) = r_start + (r_end - r_start) * t,  t in [0, 1]

    where t is the normalized progress over the full arc.
    Angle sweeps from 0 to turns * 2π.
    """
    total_points = params.turns * params.points_per_turn
    points: List[Tuple[float, float]] = []

    for i in range(total_points + 1):
        t = i / total_points
        angle = params.turns * 2 * math.pi * t
        r = params.r_start + (params.r_end - params.r_start) * t
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))

    return points
