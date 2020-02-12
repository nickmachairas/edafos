""" Functions for calculating in-situ stresses.
"""

# -- Imports ------------------------------------------------------------------


# -- Functions ----------------------------------------------------------------

def effective_stress(z: float, gwt: float):
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

    Returns:
        float: The calculated stress

    """
    zw = max(z - gwt, 0)

    return zw
