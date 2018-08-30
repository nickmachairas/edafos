""" Provide the ``Pile`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.project import Project
from edafos.data import english_hpiles, si_hpiles
import numpy as np


# -- SoilProfile Class -------------------------------------------------------

class Pile(Project):
    """ Class to represent a new driven or drilled pile.

    .. warning::

       Pay attention to the input units for each unit system that you
       choose to use. Refer to the parameter definition below or the
       :ref:`input_units` page.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, unit_system, **kwargs):
        """
        Args:
            unit_system (str): The unit system for the project. Can only be
                'English', or 'SI'. Properties inherited from the ``Project``
                class.

        Keyword Args:
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
                - ``cast-in-place``: A concrete cast-in-place pile.
                  Requires keyword argument ``diameter``, ``length``.

            shape (str): Pile shape given pile type. For concrete piles the
                options are ``square-solid``, ``square-hollow``,
                ``circle-closed``, ``circle-open``, ``hexagon`` and ``octagon``.
                For H-piles, see :numref:`english_hpile_table` for stored
                sections.

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

            taper_dims (list of lists): [:math:`d_i,l_i`]: For tapered piles,
                enter the width of the pile, :math:`d_i`, at a length,
                :math:`l_i`, measured from the top of the pile. The program
                allows for multiple tapered sections. Enter as a list, for
                example: [[12,4], [10,4],]

                - For **SI**: Enter width in **centimeters** and length
                  in **meters**.
                - For **English**: Enter width in **inches** and length
                  in **feet**.

        """
        super().__init__(unit_system=unit_system)

        # -- Check for valid kwargs ------------------------------------------
        allowed_keys = ['pile_type', 'shape', 'side', 'diameter', 'thickness',
                        'length', 'pen_depth', 'nf_zone', 'taper_dims']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # -- Assign values ---------------------------------------------------
        self.pile_type = kwargs.get('pile_type', None)
        self.shape = kwargs.get('shape', None)
        self.side = kwargs.get('side', None)
        self.diameter = kwargs.get('diameter', None)
        self.thickness = kwargs.get('thickness', None)
        self.length = kwargs.get('length', None)
        self.pen_depth = kwargs.get('pen_depth', self.length)
        self.nf_zone = kwargs.get('nf_zone', None)
        self.taper_dims = kwargs.get('taper_dims', None)

        # -- Check for valid pile type ---------------------------------------
        allowed_piles = ['concrete', 'pipe-open', 'pipe-closed', 'h-pile',
                         'timber', 'cast-in-place']
        if self.pile_type in allowed_piles:
            pass
        else:
            raise ValueError("'{}' not recognized. Pile type can only be {}."
                             "".format(self.pile_type, allowed_piles))

        # -- Reject negative or zero values ----------------------------------
        for i in [self.side, self.diameter, self.thickness, self.length,
                  self.pen_depth, self.nf_zone]:
            if i is None:
                pass
            elif type(i) not in [int, float]:
                raise ValueError("Cannot parse non-numerical pile properties. "
                                 "Did you enter a string?")
            try:
                if i <= 0:
                    raise ValueError("Cannot parse negative or zero pile "
                                     "properties.")
            except TypeError:
                pass

        # TODO: Fix these checks so they return the missing required attr only
        # TODO: Also throw a warning if additional, unnecessary attr are given
        # -- Checks for concrete piles ---------------------------------------
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
            self.side = (self.side * self.set_units('pile_diameter')
                         if self.side is not None else None)
            self.diameter = (self.diameter * self.set_units('pile_diameter')
                             if self.diameter is not None else None)
            self.thickness = (self.thickness * self.set_units('pile_diameter')
                              if self.thickness is not None else None)
            self.length = self.length * self.set_units('pile_length')
            self.pen_depth = self.pen_depth * self.set_units('pile_length')
            self.nf_zone = (self.nf_zone * self.set_units('pile_length')
                            if self.nf_zone is not None else None)
            if self.shape in ['square-solid', 'hexagon', 'octagon']:
                self.diameter = None
                self.thickness = None
            elif self.shape == 'square-hollow':
                self.thickness = None
            elif self.shape == 'circle-closed':
                self.side = None
                self.thickness = None
            else:
                self.side = None

            # Check for taper dims diameters
            if self.taper_dims is None:
                pass
            else:
                if len(self.taper_dims) > 1:
                    for i, ii in zip(self.taper_dims[:-1], self.taper_dims[1:]):
                        if ii[0] > i[0]:
                            raise ValueError("Subsequent taper diameters "
                                             "cannot be larger than preceding "
                                             "taper diameters. Please correct.")
                        else:
                            pass
                else:
                    pass
                diam_list = []
                if self.shape in ['circle-closed', 'circle-open']:
                    for i in self.taper_dims:
                        if i[0] > self.diameter.magnitude:
                            raise ValueError("Cannot have taper diameter larger"
                                             " than top pile diameter.")
                        else:
                            diam_list.append(i[0])
                            i[0] = i[0] * self.set_units('pile_diameter')
                    if (len(set(diam_list)) == 1) and (diam_list[0] ==
                                                       self.diameter.magnitude):
                        raise ValueError("This is not a tapered pile. All "
                                         "tapered diameters are the same and "
                                         "equal to the top diameter.")
                else:
                    for i in self.taper_dims:
                        if i[0] > self.side.magnitude:
                            raise ValueError("Cannot have taper diameter larger"
                                             " than top pile diameter.")
                        else:
                            diam_list.append(i[0])
                            i[0] = i[0] * self.set_units('pile_diameter')
                    if (len(set(diam_list)) == 1) and (diam_list[0] ==
                                                       self.side.magnitude):
                        raise ValueError("This is not a tapered pile. All "
                                         "tapered diameters are the same and "
                                         "equal to the top diameter.")

        # -- Checks for pipe open piles --------------------------------------
        elif self.pile_type == 'pipe-open':
            if (self.diameter is None) or (self.thickness is None) or \
                    (self.length is None):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: ['diameter', "
                                 "'thickness', 'length]."
                                 "".format(self.pile_type))
            else:
                pass
            if self.taper_dims is not None:
                raise ValueError("Open-ended steel pipe piles cannot be "
                                 "tapered.")
            else:
                pass
            # Fix assignments and units
            self.shape = 'circular'
            self.side = None
            self.diameter = self.diameter * self.set_units('pile_diameter')
            self.thickness = self.thickness * self.set_units('pile_diameter')
            self.length = self.length * self.set_units('pile_length')
            self.pen_depth = self.pen_depth * self.set_units('pile_length')
            self.nf_zone = (self.nf_zone * self.set_units('pile_length')
                            if self.nf_zone is not None else None)

        # -- Checks for pipe closed piles ------------------------------------
        elif self.pile_type == 'pipe-closed':
            if (self.diameter is None) or (self.length is None) \
                    or (self.thickness is None):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: ['diameter', "
                                 "'thickness', 'length']."
                                 "".format(self.pile_type))
            else:
                pass
            if self.taper_dims is not None:
                raise ValueError("Closed-ended steel pipe piles cannot be "
                                 "tapered.")
            else:
                pass
            # Fix assignments and units
            self.shape = 'circular'
            self.side = None
            self.diameter = self.diameter * self.set_units('pile_diameter')
            self.thickness = self.thickness * self.set_units('pile_diameter')
            self.length = self.length * self.set_units('pile_length')
            self.pen_depth = self.pen_depth * self.set_units('pile_length')
            self.nf_zone = (self.nf_zone * self.set_units('pile_length')
                            if self.nf_zone is not None else None)

        # -- Checks for H-Piles ----------------------------------------------
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
            if self.taper_dims is not None:
                raise ValueError("H-Piles cannot be tapered.")
            else:
                pass
            # Fix assignments and units
            self.side = None
            self.diameter = None
            self.thickness = None
            self.length = self.length * self.set_units('pile_length')
            self.pen_depth = self.pen_depth * self.set_units('pile_length')
            self.nf_zone = (self.nf_zone * self.set_units('pile_length')
                            if self.nf_zone is not None else None)

        # -- Checks for timber and cast-in-place piles -----------------------
        # TODO: Most likely cast-in-place will have their own checks
        elif self.pile_type in ['timber', 'cast-in-place']:
            if (self.diameter is None) or (self.length is None):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: ['diameter', "
                                 "'length].".format(self.pile_type))
            else:
                pass
            # Fix assignments and units
            self.shape = 'circular'
            self.side = None
            self.diameter = self.diameter * self.set_units('pile_diameter')
            self.thickness = None
            self.length = self.length * self.set_units('pile_length')
            self.pen_depth = self.pen_depth * self.set_units('pile_length')
            self.nf_zone = (self.nf_zone * self.set_units('pile_length')
                            if self.nf_zone is not None else None)

            # Check for taper dims diameters
            if self.taper_dims is None:
                pass
            else:
                if len(self.taper_dims) > 1:
                    for i, ii in zip(self.taper_dims[:-1], self.taper_dims[1:]):
                        if ii[0] > i[0]:
                            raise ValueError("Subsequent taper diameters "
                                             "cannot be larger than preceding "
                                             "taper diameters. Please correct.")
                        else:
                            pass
                else:
                    pass
                diam_list = []
                for i in self.taper_dims:
                    if i[0] > self.diameter.magnitude:
                        raise ValueError("Cannot have taper diameter larger"
                                         " than top pile diameter.")
                    else:
                        diam_list.append(i[0])
                        i[0] = i[0] * self.set_units('pile_diameter')
                if (len(set(diam_list)) == 1) and (diam_list[0] ==
                                                   self.diameter.magnitude):
                    raise ValueError("This is not a tapered pile. All "
                                     "tapered diameters are the same and "
                                     "equal to the top diameter.")
        else:
            pass

        # -- Taper dims checks -----------------------------------------------
        if self.taper_dims is None:
            pass
        else:
            if type(self.taper_dims) is not list:
                raise ValueError("Taper dims must be a list of lists.")
            elif len(self.taper_dims) == 0:
                raise ValueError("Taper dims list cannot be empty.")
            else:
                pass

            taper_length = 0
            for i in self.taper_dims:
                if (type(i) is not list) or (len(i) != 2):
                    raise ValueError("Taper dims must be a list of lists, "
                                     "i.e. [[d,l],].")
                elif (type(i[0].magnitude) not in [int, float]) \
                        or (type(i[1]) not in [int, float]):
                    raise ValueError("Cannot parse non-numerical taper "
                                     "dimensions. Did you enter a string?")
                elif (i[0].magnitude <= 0) or (i[1] <= 0):
                    raise ValueError("Cannot parse negative or zero taper "
                                     "dimensions. Please correct.")
                else:
                    taper_length = taper_length + i[1]
                    i[1] = i[1] * self.set_units('pile_length')
            if taper_length != self.length.magnitude:
                raise ValueError("Sum of lengths of tapered portions does "
                                 "not equal total pile length")
            else:
                pass

    # -- Static method for rectangle area ------------------------------------

    @staticmethod
    def area_of_shape(ad, shape, t=None, ad2=None, h=None):
        """ Static method that calculates the area of a given shape.

        Args:
            ad (float): Length of side or diameter.
            shape (str): Options are ``square``, ``hexagon``, ``octagon``,
                ``circle``, ``ring``, ``trapezoid``, ``cone``.
            t (float): Thickness of pile wall.
            ad2 (float): Additional length of side or diameter to obtain
                side area.
            h (float): Segment height to obtain side area.

        Returns:
            float: Area of shape (unitless)

        """
        allowed = ['square', 'hexagon', 'octagon', 'circle', 'ring',
                   'trapezoid', 'cone']
        if shape not in allowed:
            raise ValueError("Shape can be {} only.".format(allowed))
        else:
            pass

        if shape == 'square':
            area = ad ** 2
        elif shape == 'hexagon':
            area = (3/2) * np.sqrt(3) * (ad**2)
        elif shape == 'octagon':
            area = 2 * (1 + np.sqrt(2)) * (ad**2)
        elif shape == 'circle':
            area = np.pi * (ad ** 2) / 4
        elif shape == 'ring':
            area = np.pi * ((ad ** 2) - (ad - 2 * t) ** 2) / 4
        elif shape == 'trapezoid':
            area = ((ad + ad2) / 2) * h
        else:  # Cone -- http://mathworld.wolfram.com/ConicalFrustum.html
            s = np.sqrt((((ad - ad2)/2) ** 2) + (h ** 2))
            area = np.pi * ((ad + ad2)/2) * s

        return area

    # -- Private method for pile a/d at z ------------------------------------

    def _pile_a_d(self, z):
        """ A private method that returns the side, :math:`a`, or diameter,
        :math:`d`, of a pile at a depth :math:`z`.

        Args:
            z (float): Vertical depth to the point of interest, measured from
                the top of the soil profile.

                - For **SI**: Enter depth, *z*, in **meters**.
                - For **English**: Enter depth, *z*, in **feet**.

        Returns:
            Quantity: Side :math:`a`, or diameter, :math:`d`.
        """
        z = z * self.set_units('length')
        # The length x from the top of the pile is defined as
        x = self.length - self.pen_depth + z

        if self.pile_type == 'concrete':
            if self.shape in ['square-solid', 'square-hollow', 'hexagon',
                              'octagon']:
                if self.taper_dims is None:
                    di = [self.side.magnitude, self.side.magnitude]
                    li = [0, self.length.magnitude]
                else:
                    di = [self.side.magnitude] + [i[0].magnitude for i in
                                                  self.taper_dims]
                    li = [0] + [i[1].magnitude for i in self.taper_dims]
                    li = np.cumsum(li)
            else:
                if self.taper_dims is None:
                    di = [self.diameter.magnitude, self.diameter.magnitude]
                    li = [0, self.length.magnitude]
                else:
                    di = [self.diameter.magnitude] + [i[0].magnitude for i in
                                                      self.taper_dims]
                    li = [0] + [i[1].magnitude for i in self.taper_dims]
                    li = np.cumsum(li)
        elif self.pile_type in ['pipe-open', 'pipe-closed']:
            di = [self.diameter.magnitude, self.diameter.magnitude]
            li = [0, self.length.magnitude]
        else:  # Timber and cast-in-place piles
            if self.taper_dims is None:
                di = [self.diameter.magnitude, self.diameter.magnitude]
                li = [0, self.length.magnitude]
            else:
                di = [self.diameter.magnitude] + [i[0].magnitude for i in
                                                  self.taper_dims]
                li = [0] + [i[1].magnitude for i in self.taper_dims]
                li = np.cumsum(li)

        return np.interp(x.magnitude, li, di) * self.set_units('pile_diameter')

    # -- Method for cross sectional area at z --------------------------------

    def xsection_area(self, z, soil_plug=False, box_area=False):
        """ Method that returns the pile cross sectional area at a depth,
        :math:`z`, from ground surface.

        .. warning::

           This method was made for bearing capacity calculations.
           As such, it returns the relevant cross sectional area. For example,
           for steel pipe closed-ended piles, it will return the circle and not
           the ring area.

        TODO: For concrete square hollow piles it currently returns solid area

        Args:
            z (float): Vertical depth to the point of interest, measured from
                the top of the soil profile.

                - For **SI**: Enter depth, *z*, in **meters**.
                - For **English**: Enter depth, *z*, in **feet**.

            soil_plug (bool): If ``TRUE``, the method returns the full area of
                open-ended piles.

            box_area (bool): For H-piles, if set to ``TRUE``, the method
                returns the box area.

        Returns:
            Quantity: The cross sectional area of the pile w/ units.

        """
        if z < 0:
            raise ValueError("Depth z cannot be negative here.")
        else:
            pass

        # The length x from the top of the pile is defined as
        x = self.length.magnitude - self.pen_depth.magnitude + z

        if (x < 0) or (x > self.length.magnitude):
            area = 0 * self.set_units('pile_xarea')
        elif self.pile_type == 'concrete':
            if self.shape in ['square-solid', 'square-hollow']:
                area = self.area_of_shape(self._pile_a_d(z), 'square')
            elif self.shape == 'hexagon':
                area = self.area_of_shape(self._pile_a_d(z), 'hexagon')
            elif self.shape == 'octagon':
                area = self.area_of_shape(self._pile_a_d(z), 'octagon')
            elif self.shape == 'circle-closed':
                area = self.area_of_shape(self._pile_a_d(z), 'circle')
            else:  # circle-open
                if soil_plug:
                    area = self.area_of_shape(self._pile_a_d(z), 'circle')
                else:
                    area = self.area_of_shape(self._pile_a_d(z), 'ring',
                                              self.thickness)

        elif self.pile_type == 'pipe-open':
            if soil_plug:
                area = self.area_of_shape(self._pile_a_d(z), 'circle')
            else:
                area = self.area_of_shape(self._pile_a_d(z), 'ring',
                                          self.thickness)

        elif self.pile_type == 'pipe-closed':
            area = self.area_of_shape(self._pile_a_d(z), 'circle')

        elif self.pile_type == 'h-pile':
            if box_area:
                area = english_hpiles[self.shape]['box_area'] \
                       * self.set_units('pile_xarea')
            else:
                area = english_hpiles[self.shape]['area'] \
                       * self.set_units('pile_xarea')

        else:  # Timber and cast-in-place piles
            area = self.area_of_shape(self._pile_a_d(z), 'circle')

        # Had to convert area from in2 to ft2 because unit toe resistance units
        # were not correctly formatted
        return area.to(self.set_units('pile_xarea_alt'))

    # -- Method for side area between z1, z2 ---------------------------------

    def side_area(self, z1, z2, box_area=False, inside=False):
        """ Method that returns the side area for a section of the pile defined
        by z1 and z2.

        Args:
            z1 (float): Vertical depth to the highest point of interest,
                measured from the top of the soil profile.

                - For **SI**: Enter depth, *z1*, in **meters**.
                - For **English**: Enter depth, *z1*, in **feet**.

            z2 (float): Vertical depth to the lowest point of interest,
                measured from the top of the soil profile.

                - For **SI**: Enter depth, *z1*, in **meters**.
                - For **English**: Enter depth, *z1*, in **feet**.

            box_area (bool): For H-piles, if set to ``TRUE``, the method
                returns the box area.

            inside (bool): For open steel pipe piles only. If TRUE, it returns
                the inside area of the pile for plugged calculations.

        Returns:
            Quantity: The side area of the pile w/ units between z1 and z2.
        """
        if (z1 < 0) or (z2 < 0):
            raise ValueError("Depth z cannot be negative here.")
        elif z2 <= z1:
            raise ValueError("z2 must be larger than z1")
        else:
            pass

        # The length x from the top of the pile is defined as
        x1 = self.length.magnitude - self.pen_depth.magnitude + z1
        x2 = self.length.magnitude - self.pen_depth.magnitude + z2

        h = (z2 - z1) * self.set_units('pile_length')

        # TODO: Give these limits another thought, maybe not return zero.
        if (x1 < 0) or (x1 > self.length.magnitude) or (x2 < 0) or \
                (x2 > self.length.magnitude):
            area = 0 * self.set_units('pile_xarea')
        elif self.pile_type == 'concrete':
            if self.shape in ['square-solid', 'square-hollow']:
                area = 4 * self.area_of_shape(ad=self._pile_a_d(z1),
                                              shape='trapezoid',
                                              ad2=self._pile_a_d(z2), h=h)
            elif self.shape == 'hexagon':
                area = 6 * self.area_of_shape(ad=self._pile_a_d(z1),
                                              shape='trapezoid',
                                              ad2=self._pile_a_d(z2), h=h)
            elif self.shape == 'octagon':
                area = 8 * self.area_of_shape(ad=self._pile_a_d(z1),
                                              shape='trapezoid',
                                              ad2=self._pile_a_d(z2), h=h)
            else:  # circle-closed and circle-open
                area = self.area_of_shape(ad=self._pile_a_d(z1),
                                          shape='cone',
                                          ad2=self._pile_a_d(z2), h=h)

        elif self.pile_type in ['pipe-open', 'pipe-closed']:
            if (self.pile_type == 'pipe-open') and inside:
                t = self.thickness.magnitude
                area = self.area_of_shape(ad=(self._pile_a_d(z1) - 2*t *
                                              self.set_units('pile_diameter')
                                              ),
                                          shape='cone',
                                          ad2=(self._pile_a_d(z2) - 2*t *
                                               self.set_units('pile_diameter')
                                               ),
                                          h=h)
            else:
                area = self.area_of_shape(ad=self._pile_a_d(z1), shape='cone',
                                          ad2=self._pile_a_d(z2), h=h)
        # TODO: adjust to accept si piles as well
        elif self.pile_type == 'h-pile':
            if box_area:
                area = (english_hpiles[self.shape]['box_perimeter']
                        * self.set_units('pile_diameter')) * h
            else:
                area = (english_hpiles[self.shape]['perimeter']
                        * self.set_units('pile_diameter')) * h

        else:  # Timber and cast-in-place piles
            area = self.area_of_shape(ad=self._pile_a_d(z1), shape='cone',
                                      ad2=self._pile_a_d(z2), h=h)

        return area.to(self.set_units('pile_side_area'))

    # -- Method that returns list of relevant z's ----------------------------

    def z_of_pile(self):
        """ Method that returns a list of depths, :math:`z`, for the pile that
        correspond to the top of the pile (if below ground), the tip of the
        pile and inflection points if tapered.

        The assumption here is that :math:`z = x - L_t + D_p`, where :math:`x`
        is a point along the length of the pile. Therefore, for :math:`x = 0`
        we get the depth :math:`z_{pile.top}` at the top of the pile (if
        :math:`D_p > L_t`) and for :math:`x = L_t`, we get the depth
        :math:`z_{pile.toe}` at the toe (aka tip) of the pile. If the pile is
        tapered, :math:`x` along inflection points will produce the
        corresponding :math:`z`.

        Returns:
            A list of depths, :math:`z` (unitless).
        """
        z_list = []
        # Get z_pile-top if Dp > Lt
        if self.pen_depth.magnitude > self.length.magnitude:
            z = self.pen_depth.magnitude - self.length.magnitude
            z_list.append(z)
        else:
            pass
        # Get the remaining z's
        if self.taper_dims is None:
            z = self.pen_depth.magnitude
            z_list.append(z)
        else:
            taper_l = []
            for i in self.taper_dims:
                taper_l.append(i[1].magnitude)
            taper_l = np.cumsum(taper_l)
            for ii in taper_l:
                z = ii - self.length.magnitude + self.pen_depth.magnitude
                if z > 0:
                    z_list.append(z)
                else:
                    pass

        return z_list

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
               "No-Friction Zone: {0.nf_zone}\n" \
               "Taper Dims [[d,l],]: {0.taper_dims}".format(self)
