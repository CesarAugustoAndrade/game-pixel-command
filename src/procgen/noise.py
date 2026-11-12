"""
Noise generation utilities for procedural generation.
Simple implementation without external dependencies.
"""

import math
import random


class SimpleNoise:
    """
    Simple noise generator for procedural generation.
    Simplified implementation without numpy/noise libraries.
    """

    def __init__(self, seed: int = None):
        """
        Initialize noise generator.

        Args:
            seed: Random seed
        """
        if seed is not None:
            random.seed(seed)

        # Generate permutation table
        self.perm = list(range(256))
        random.shuffle(self.perm)
        self.perm *= 2

    def noise2d(self, x: float, y: float) -> float:
        """
        Generate 2D noise value.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Noise value between -1 and 1
        """
        # Grid cell coordinates
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255

        # Fractional part
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        # Fade curves
        u = self._fade(xf)
        v = self._fade(yf)

        # Hash coordinates
        aa = self.perm[self.perm[xi] + yi]
        ab = self.perm[self.perm[xi] + yi + 1]
        ba = self.perm[self.perm[xi + 1] + yi]
        bb = self.perm[self.perm[xi + 1] + yi + 1]

        # Gradients
        g1 = self._gradient(aa, xf, yf)
        g2 = self._gradient(ba, xf - 1, yf)
        g3 = self._gradient(ab, xf, yf - 1)
        g4 = self._gradient(bb, xf - 1, yf - 1)

        # Interpolate
        x1 = self._lerp(g1, g2, u)
        x2 = self._lerp(g3, g4, u)

        return self._lerp(x1, x2, v)

    def _fade(self, t: float) -> float:
        """Fade function for smooth interpolation."""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a: float, b: float, t: float) -> float:
        """Linear interpolation."""
        return a + t * (b - a)

    def _gradient(self, hash_val: int, x: float, y: float) -> float:
        """Calculate gradient."""
        h = hash_val & 3
        if h == 0:
            return x + y
        elif h == 1:
            return -x + y
        elif h == 2:
            return x - y
        else:
            return -x - y
