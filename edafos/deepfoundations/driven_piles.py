""" Provide the ``DrivenPiles`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.project import Project
from edafos.data import english_hpiles, si_hpiles
# from tabulate import tabulate
# import numpy as np
# import pandas as pd
# import pint
# units = pint.UnitRegistry()


# -- SoilProfile Class -------------------------------------------------------

class DrivenPile(Project):
    """ Class to represent a new driven pile.

    .. warning::

       Pay attention to the input units for each unit system that you
       choose to use. Refer to the parameter definition below or the
       :ref:`input_units` page.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, unit_system, pile_type, **kwargs):
        """
        Args:
            unit_system (str): The unit system for the project. Can only be
                'English', or 'SI'. Properties inherited from the ``Project``
                class.

            pile_type (str): Type of driven pile. Available options are:

                - ``concrete``: A rectangular (normally square) concrete pile.
                    Requires different keyword arguments depending on ``shape``.
                    Always requires ``length``.
                - ``pipe_open``: An open-ended circular steel pipe pile.
                    Requires keyword arguments ``diameter``, ``thickness``,
                    ``length``.
                - ``pipe_closed``: A closed-ended circular steel pipe pile.
                    Requires keyword argument ``diameter``, ``length``.
                - ``h_pile``: An H shape steel beam used as a pile.
                    Requires keyword argument ``shape``, ``length``.
                - ``timber``: A circular timber pile.
                    Requires keyword argument ``diameter``, ``length``.

        Keyword Args:
            shape (str): Pile shape given pile type. For concrete piles the
                options are ``square-solid``, ``square-hollow``,
                ``circle-closed``, ``circle-open``, ``hexagon`` and ``octagon``.
                For H-piles see documentation for stored sections.
                TODO: Add reference to table with sections.

            side (float): :math:`\\alpha`: Side length of square, hexagonal and
                octagonal piles, at the top.

                - For **SI**: Enter side length in **centimeters**.
                - For **English**: Enter side length in **inches**.

            diameter (float): :math:`d`: Outer diameter at the top for circular
                piles and inner diameter of concrete square hollow piles.

                - For **SI**: Enter diameter in **centimeters**.
                - For **English**: Enter diameter in **inches**.

            thickness (float): :math:`t`: Wall thickness of steel pipe piles
                and concrete circular open-ended piles.

                - For **SI**: Enter thickness in **centimeters**.
                - For **English**: Enter thickness in **inches**.

            length (float): :math:`L_t`: Total length of pile.

                - For **SI**: Enter length in **meters**.
                - For **English**: Enter length in **feet**.

            pen_depth (float): :math:`D_p`: Penetration depth, the part of the
                pile that is embedded in the ground. **Important:** if a
                penetration depth is not entered, it will be assumed equal to
                the total length of the pile.

                - For **SI**: Enter depth in **meters**.
                - For **English**: Enter depth in **feet**.

            nf_zone (float): :math:`D_{nf}`: No-friction zone; this is the
                length of a segment measured from ground level where frictional
                resistance does not contribute to pile capacity.

                - For **SI**: Enter depth in **meters**.
                - For **English**: Enter depth in **feet**.

            taper_dims (list of tuples): :math:`(d_i,l_i)`: For tapered piles,
                enter the width of the pile, :math:`d_i`, at a length,
                :math:`l_i`, measured from the top of the pile. The program
                allows for multiple tapered sections. Enter as a list, for
                example: [(12,4), (10,4),]

                - For **SI**: Enter width in **centimeters** and length
                  in **meters**.
                - For **English**: Enter width in **inches** and length
                  in **feet**.


        """
        super().__init__(unit_system=unit_system)

        # Check for valid pile type
        allowed_piles = ['concrete', 'pipe-open', 'pipe-closed', 'h-pile',
                         'timber']
        if pile_type in allowed_piles:
            self.pile_type = pile_type
        else:
            raise ValueError("'{}' not recognized. Pile type can only be {}."
                             "".format(pile_type, allowed_piles))

        # Check for valid kwargs
        allowed_keys = ['shape', 'side', 'diameter', 'thickness', 'length',
                        'pen_depth', 'nf_zone', 'taper_dims']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # Assign values
        self.shape = kwargs.get('shape', None)
        self.side = kwargs.get('side', None)
        self.diameter = kwargs.get('diameter', None)
        self.thickness = kwargs.get('thickness', None)
        self.length = kwargs.get('length', None)
        self.pen_depth = kwargs.get('pen_depth', self.length)
        self.nf_zone = kwargs.get('nf_zone', None)
        self.taper_dims = kwargs.get('taper_dims', None)

        # TODO: Fix these checks so they return the missing required attr only
        # TODO: Also throw a warning if additional, unnecessary attr are given
        # Checks for concrete piles
        if self.pile_type == 'concrete':
            allowed_shape = ['square-solid', 'square-hollow', 'circle-closed',
                             'circle-open', 'hexagon', 'octagon']
            if self.shape not in allowed_shape:
                raise ValueError("'{}' is not a valid value for concrete pile "
                                 "shape.\nThe allowed values are: {}"
                                 "".format(self.shape, allowed_shape))
            else:
                pass
            shape_reqs = {
                'square-solid': [self.side, self.length],
                'square-hollow': [self.side, self.diameter, self.length],
                'circle-closed': [self.diameter, self.length],
                'circle-open': [self.diameter, self.thickness, self.length],
                'hexagon': [self.side, self.length],
                'octagon': [self.side, self.length],
            }
            shape_kwgs = {
                'square-solid': ['side', 'length'],
                'square-hollow': ['side', 'diameter', 'length'],
                'circle-closed': ['diameter', 'length'],
                'circle-open': ['diameter', 'thickness', 'length'],
                'hexagon': ['side', 'length'],
                'octagon': ['side', 'length'],
            }
            for shape in allowed_shape:
                if (self.shape == shape) and (None in shape_reqs[shape]):
                    raise ValueError("Missing required properties for pile "
                                     "shape: '{}'.\nEnter values for: {}."
                                     "".format(shape, shape_kwgs[shape]))
                else:
                    pass
            # Fix assignments and units
            self.side = (self.side * self._set_units('pile_diameter')
                         if self.side is not None else None)
            self.diameter = (self.diameter * self._set_units('pile_diameter')
                             if self.diameter is not None else None)
            self.thickness = (self.thickness * self._set_units('pile_diameter')
                              if self.thickness is not None else None)
            self.length = self.length * self._set_units('pile_length')
            self.pen_depth = self.pen_depth * self._set_units('pile_length')
            self.nf_zone = (self.nf_zone * self._set_units('pile_length')
                            if self.nf_zone is not None else None)

        # Checks for pipe open piles
        elif self.pile_type == 'pipe-open':
            if (self.diameter is None) or (self.thickness is None) or \
                    (self.length is None):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: ['diameter', "
                                 "'thickness', 'length]."
                                 "".format(self.pile_type))
            else:
                pass
            # Fix assignments and units
            self.shape = 'circular'
            self.side = None
            self.diameter = self.diameter * self._set_units('pile_diameter')
            self.thickness = self.thickness * self._set_units('pile_diameter')
            self.length = self.length * self._set_units('pile_length')
            self.pen_depth = self.pen_depth * self._set_units('pile_length')
            self.nf_zone = (self.nf_zone * self._set_units('pile_length')
                            if self.nf_zone is not None else None)

        # Checks for pipe closed piles
        elif self.pile_type == 'pipe-closed':
            if (self.diameter is None) or (self.length is None):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: ['diameter', "
                                 "'length'].".format(self.pile_type))
            else:
                pass
            # Fix assignments and units
            self.shape = 'circular'
            self.side = None
            self.diameter = self.diameter * self._set_units('pile_diameter')
            self.thickness = None
            self.length = self.length * self._set_units('pile_length')
            self.pen_depth = self.pen_depth * self._set_units('pile_length')
            self.nf_zone = (self.nf_zone * self._set_units('pile_length')
                            if self.nf_zone is not None else None)

        # Checks for H-Piles
        # TODO: Add logic for custom H-pile shapes
        elif self.pile_type == 'h-pile':
            if self.length is None:
                raise ValueError("Enter value for 'length'.")
            elif self.unit_system == 'English':
                if self.shape not in english_hpiles:
                    raise ValueError(
                        "'{}' is not a valid shape for English H-Piles."
                        "\nThe allowed values are: {}"
                        "".format(self.shape, english_hpiles.keys()))
                else:
                    pass
            elif self.unit_system == 'SI':
                if self.shape not in si_hpiles:
                    raise ValueError(
                        "'{}' is not a valid shape for S.I. H-Piles."
                        "\nThe allowed values are: {}"
                        "".format(self.shape, si_hpiles.keys()))
                else:
                    pass
            # Fix assignments and units
            self.side = None
            self.diameter = None
            self.thickness = None
            self.length = self.length * self._set_units('pile_length')
            self.pen_depth = self.pen_depth * self._set_units('pile_length')
            self.nf_zone = (self.nf_zone * self._set_units('pile_length')
                            if self.nf_zone is not None else None)

        # Checks for timber piles
        elif self.pile_type == 'timber':
            if (self.diameter is None) or (self.length is None):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: ['diameter', "
                                 "'length].".format(self.pile_type))
            else:
                pass
            # Fix assignments and units
            self.shape = 'circular'
            self.side = None
            self.diameter = self.diameter * self._set_units('pile_diameter')
            self.thickness = None
            self.length = self.length * self._set_units('pile_length')
            self.pen_depth = self.pen_depth * self._set_units('pile_length')
            self.nf_zone = (self.nf_zone * self._set_units('pile_length')
                            if self.nf_zone is not None else None)

    # -- Method for string representation ------------------------------------

    def __str__(self):
        return "Pile Details:\n------------\n" \
               "Type: {0.pile_type}\n" \
               "Shape: {0.shape}\n" \
               "Side: {0.side}\n" \
               "Diameter: {0.diameter}\n" \
               "Thickness: {0.thickness}\n" \
               "Total Length: {0.length}\n" \
               "Penetration Depth: {0.pen_depth}\n" \
               "No-Friction Zone: {0.nf_zone}".format(self)
