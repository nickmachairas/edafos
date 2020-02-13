""" Functions for calculating in-situ stresses.
"""

# -- Imports ------------------------------------------------------------------
import numpy as np
from edafos import units


# -- Functions ----------------------------------------------------------------

def _gamma_avg(z: float, heights: list, gammas: list):
    """

    Args:
        z:
        heights:
        gammas:

    Returns:

    """
    if z <= 0:
        return 0

    if z > sum(heights):
        raise ValueError('Depth (z) is out of bounds.')

    z_heights = []

    if len(heights) == 1:
        z_heights.append(heights[0])
    else:
        for i, v in enumerate(heights):
            if sum(heights[:i+1]) < z:
                z_heights.append(v)
            else:
                z_heights.append(z - sum(heights[:i]))
                break

    z_gammas = [gammas[i] for i in range(len(z_heights))]

    weighted_gamma = np.average(z_gammas, weights=z_heights)

    return weighted_gamma


def effective_stress(z: float, gwt: float, heights: list, gammas: list):
    """
    Example:
        This is an example.

        >>> from edafos.stresses import effective_stress
        >>> effective_stress(1, 3)
        4


    Args:
        z (float): Depth to point of interest, in feet (default) or meters.
        gwt (float): Ground water table, measured from ground level. Must be
            positive if below ground level or negative for offshore. In feet
            (default) or meters.
        heights (list): An array of soil layer heights from top to bottom. In
            feet (default) or meters.
        gammas (list): An array of soil layer unit weights from top to bottom.
            In pcf (default) or kN/m3.

    Returns:
        Quantity: The calculated effective stress, in psf (default) or kN/m2.

    """
    gwt = max(gwt, 0)
    zw = max(z - gwt, 0)

    gamma_avg = _gamma_avg(z, heights, gammas)
    stress = gamma_avg * (z - zw) + (gamma_avg - 62.4) * zw

    return stress * units['psf']
