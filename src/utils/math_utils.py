"""
Math utility functions.
"""

import math
from typing import Tuple


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        x1, y1: First point
        x2, y2: Second point

    Returns:
        Distance
    """
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max.

    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value

    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))


def lerp(a: float, b: float, t: float) -> float:
    """
    Linear interpolation between two values.

    Args:
        a: Start value
        b: End value
        t: Interpolation factor (0-1)

    Returns:
        Interpolated value
    """
    return a + (b - a) * t


def normalize_vector(x: float, y: float) -> Tuple[float, float]:
    """
    Normalize a 2D vector.

    Args:
        x: X component
        y: Y component

    Returns:
        (nx, ny) normalized vector
    """
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def angle_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate angle between two points in radians.

    Args:
        x1, y1: First point
        x2, y2: Second point

    Returns:
        Angle in radians
    """
    return math.atan2(y2 - y1, x2 - x1)
