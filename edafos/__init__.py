import pint
units = pint.UnitRegistry()


# -- A helper function to set units ------------------------------------------

def set_units(dim, unit_system):
    """ A private helper function that returns the Pint units to be attached
    to a variable based on the set unit system and dimensionality (dim).

    Args:
        dim (str): The dimensionality for the variable. For example, layer
            height is 'length'.

        unit_system (str): The unit system, 'SI' or 'English'.

    Returns:
        Pint units.

    """
    unit_dict = {
        'degrees': {'SI': units.degree, 'English': units.degree},
        'length': {'SI': units.meter, 'English': units.feet},
        'tuw': {'SI': units.kN / units.meter ** 3,
                'English': (units.kip / 1000) / units.feet ** 3},
        'stress': {'SI': units.kN / units.meter ** 2,
                   'English': units.kip / units.feet ** 2},
        'capacity': {'SI': units.kN, 'English': units.kip},
        'pile_diameter': {'SI': units.cm, 'English': units.inches},
        'pile_length': {'SI': units.meter, 'English': units.feet},
        'pile_xarea': {'SI': units.cm ** 2, 'English': units.inches ** 2},
        'pile_xarea_alt': {'SI': units.meter ** 2,
                           'English': units.feet ** 2},
        'pile_side_area': {'SI': units.meter ** 2,
                           'English': units.feet ** 2},
        'modulus': {'SI': 10e9 * units.pascal,
                    'English': units.kip / units.inches ** 2},
        'aeol': {'SI': units.kN / units.meter,
                 'English': units.kip / units.inches},
        'pile_settlement': {'SI': units.mm, 'English': units.inches},
    }

    return unit_dict[dim][unit_system]
