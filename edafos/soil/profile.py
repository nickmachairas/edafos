""" Provide the ``SoilProfile`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.project import Project
from tabulate import tabulate
import numpy as np
import pandas as pd


# -- SoilProfile Class -------------------------------------------------------

class SoilProfile(Project):
    """ Class to represent a new soil profile.

    .. warning::

       Pay attention to the base units for each unit system that you
       choose to use. Refer to the parameter definition below or the
       :ref:`input_units` page.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, unit_system, water_table):
        """
        Args:
            water_table (float): Depth to water table measured from ground
                elevation.

                - For **SI**: Enter value in **meters**.
                - For **English**: Enter value in **feet**.

            unit_system (str): The unit system for the project. Can only be
                'English', or 'SI'. Properties inherited from the ``Project``
                class.

        """
        super().__init__(unit_system=unit_system)

        # Set units for the water table
        self.water_table = float(water_table) * self._set_units('length')

        # Call function to instantiate the soil profile data frame
        self._create_profile()

    # -- Soil Profile Instantiation Method (Private) -------------------------

    def _create_profile(self):
        """ A private method that instantiates the soil profile data frame.

        Returns:
            An empty Pandas DataFrame with two headers, one for the column
            names and another for the column units.

        """
        name_list = ['Soil Type', 'Depth', 'Height', 'TUW', 'Field N',
                     'Corr. N', 'Field Phi', 'Calc. Phi', 'Shear Su']
        self.layers = pd.DataFrame(columns=name_list)
        self.layers.index.name = 'Layer'

        return self

    # -- Method to add layers ------------------------------------------------

    def add_layer(self, soil_type, height, **kwargs):
        """ Method to add a new layer to the soil profile.

        .. todo::

           Run parameter checks for allowable ranges and required info, for
           example, raise a warning for a cohesionless layer without shear
           strength.

        Args:
            soil_type (str): Allowed values are 'cohesive' for clays and
                'cohesionless' for sands.
            height (float): Height of soil layer.

                - For **SI**: Enter height in **meters**.
                - For **English**: Enter height in **feet**.


        Keyword Args:
            tuw (float): Total unit weight of soil.

                - For **SI**: Enter TUW in **kN/m**\ :sup:`3`.
                - For **English**: Enter TUW in **lbf/ft**\ :sup:`3`.

            field_n (int): Field SPT-N values.
            corr_n (int): Corrected Field SPT-N values.

                .. note::

                   If field SPT-N value is given without the corrected SPT-N,
                   the corrected value will be automatically calculated.

            field_phi (float): Field internal angle of friction, *φ*,
                in degrees.
            calc_phi (float): Calculated internal angle of friction,
                *φ*, from SPT-N values.
            su (float): Undrained shear strength, *s*\ :sub:`u`.

                - For **SI**: Enter *s*\ :sub:`u` in **kN/m**\ :sup:`2`.
                - For **English**: Enter *s*\ :sub:`u` in **lbf/ft**\ :sup:`2`.

        """

        # Check for valid attributes
        allowed_keys = ['soil_type', 'height', 'tuw', 'field_n', 'corr_n',
                        'field_phi', 'calc_phi', 'su']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute. The "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # Assign values
        tuw = kwargs.get('tuw', None)
        field_n = kwargs.get('field_n', None)
        corr_n = kwargs.get('corr_n', None)
        field_phi = kwargs.get('field_phi', None)
        calc_phi = kwargs.get('calc_phi', None)
        su = kwargs.get('su', None)

        # Check for soil type
        if soil_type in ['cohesive', 'cohesionless']:
            soil_type = soil_type
        else:
            raise ValueError("Soil type can only be 'cohesive' or "
                             "'cohesionless'.")

        # Check that all inputs are positive numbers
        for i in [height, tuw, field_n, corr_n, field_phi, calc_phi, su]:
            if (i is not None) and (type(i) not in [int, float]):
                raise TypeError("Value '{}' is of type {} and is not "
                                "permissible. \nEnter only positive numbers "
                                "(int or float) for soil properties."
                                "".format(i, type(i)))
            elif (i is not None) and (i < 0):
                raise ValueError("Value '{}' is not permissible. Enter positive"
                                 " numbers only for soil properties.".format(i))
            else:
                pass

        # Calculate depth from layers heights
        if len(self.layers) == 0:
            depth = height
        else:
            depth = self.layers.loc[len(self.layers), 'Depth'] + height

        # Store values in data frame
        self.layers.loc[len(self.layers)+1] = [
            soil_type, depth, height, tuw, field_n, corr_n, field_phi,
            calc_phi, su]

        # Reset index to start at 1
        if self.layers.index[0] == 0:
            self.layers.index = self.layers.index + 1

        # Enforce proper data types
        # TODO: Repeated every time a layer is added. Is there a better way?
        self.layers.fillna(np.nan, inplace=True)
        # for column in self.layers.columns.levels[0]:
        for column in self.layers.columns:
            if column != 'Soil Type':
                self.layers[column] = self.layers[column].astype(float)

        return self

    # -- Method to calculate stresses ----------------------------------------

    def calculate_stress(self, z, kind='effective'):
        """ Method to calculate stresses (pore water, total, effective). It
        defaults to 'effective'. Change the ``kind`` parameter to get the
        other stresses.

        Args:
            z (float): Vertical depth to the point of interest, measured from
                the top of the soil profile.

                - For **SI**: Enter depth, *z*, in **meters**.
                - For **English**: Enter depth, *z*, in **feet**.

            kind (str): Parameter that controls the output of the function.
                Allowed values are ``total``, ``pore_water``, ``effective``
                and ``all``. The last value, ``all``, returns all three
                stresses in the same order.

        Returns:
            Quantity: A physical quantity with associated units.

        """

        # Check for kind values
        allowed = ['effective', 'total', 'pore_water', 'all']
        if kind in allowed:
            kind = kind
        else:
            raise ValueError("'{}' entry is invalid. Choose from {}."
                             "".format(kind, allowed))

        # Check that z is within limits
        max_depth = self.layers['Height'].sum()
        if z > max_depth:
            raise ValueError("Depth z = {0} {2}, is beyond the total defined "
                             "soil profile depth, {1} {2}."
                             "".format(z, max_depth, self._set_units('length')))
        elif ((z < 0) and (self.water_table.magnitude >= 0)) \
                or (z < self.water_table.magnitude < 0):
            raise ValueError("Nothing but thin air at z = {} {}. Try lower."
                             "".format(z, self._set_units('length')))
        else:
            pass

        # Set units for input parameter, z
        z = float(z) * self._set_units('length')

        # Define zw, the vertical distance below the water table.
        zw = z - self.water_table
        if zw.magnitude < 0:
            zw = 0 * zw.units

        # Define pore water pressure
        if self.unit_system == 'SI':
            gamma_w = 9.81 * self._set_units('tuw')
        else:
            gamma_w = 62.4 * self._set_units('tuw')
        pore_water = zw * gamma_w

        # -- Define total stress ---------------------------------------------
        h1 = self.layers['Height'][1] * self._set_units('length')
        g1 = self.layers['TUW'][1] * self._set_units('tuw')

        # Prepare for Takeaway No 4
        if (z.magnitude >= 0) and (self.water_table.magnitude < 0):
            stress_from_water_body = abs(self.water_table) * gamma_w
        else:
            stress_from_water_body = 0 * self._set_units('stress')

        # Main if statement
        if (z.magnitude < 0) and (self.water_table.magnitude < 0):
            total_stress = pore_water
        elif z < h1:
            total_stress = z * g1 + stress_from_water_body

        elif z.magnitude in self.layers['Depth'].values:

            # Get the layer index where z is at the interface
            ix = self.layers[self.layers['Depth'] == z.magnitude].index[0]

            # Multiply and sum the data frame columns of relevant layers
            # total_stress = (sum(self.layers['Height'][0:ix] *
            #                     self.layers['TUW'][0:ix]
            #                     ) * self._set_units('stress')
            #                 ) + stress_from_water_body
            total_stress = sum((self.layers['Height'][0:ix].values
                                * self._set_units('length')) *
                               (self.layers['TUW'][0:ix].values *
                                self._set_units('tuw'))
                               ) + stress_from_water_body

        else:
            # Get the previous layer index where z is in
            ixp = self.layers[self.layers['Depth'] < z.magnitude].index[-1]

            # Get the current layer index where z is in
            ixc = self.layers[self.layers['Depth'] > z.magnitude].index[0]

            # Multiply and sum the data frame columns of relevant layers
            # total_stress = ((sum(self.layers['Height'][0:ixp] *
            #                      self.layers['TUW'][0:ixp]
            #                      ) + (
            #                      (z.magnitude - self.layers['Depth'][ixp]) *
            #                      self.layers['TUW'][ixc])
            #                  ) * self._set_units('stress')
            #                 ) + stress_from_water_body
            total_stress = (sum((self.layers['Height'][0:ixp].values *
                                 self._set_units('length')) *
                                (self.layers['TUW'][0:ixp].values *
                                 self._set_units('tuw'))
                                ) + (
                                ((z.magnitude - self.layers['Depth'][ixp]) *
                                 self._set_units('length')) *
                                (self.layers['TUW'][ixc] *
                                 self._set_units('tuw')))

                            ) + stress_from_water_body

        # Define effective stress
        effective_stress = total_stress - pore_water

        if kind == 'effective':
            return effective_stress
        elif kind == 'total':
            return total_stress
        elif kind == 'pore_water':
            return pore_water
        else:
            return total_stress, pore_water, effective_stress

    # -- Method for string representation ------------------------------------

    def __str__(self):

        layer_tbl = tabulate(self.layers, headers='keys', tablefmt='simple')

        unit_list = [
            ['Depth', '(m)' if self.unit_system == 'SI' else '(ft)'],
            ['Height', '(m)' if self.unit_system == 'SI' else '(ft)'],
            ['TUW', '(kN/m3)' if self.unit_system == 'SI' else '(lbf/ft3)'],
            ['Field N', '(bl/0.3m)' if self.unit_system == 'SI' else '(bpf)'],
            ['Corrected N', '(bl/0.3m)' if self.unit_system == 'SI' else
                '(bpf)'],
            ['Field Phi', '(deg)'],
            ['Calculated Phi', '(deg)'],
            ['Shear Strength', '(kN/m2)' if self.unit_system == 'SI' else
                '(lbf/ft2)']
        ]
        unit_tbl = tabulate(unit_list, tablefmt='plain')

        return "\n" \
               "Unit System: {0.unit_system}\n" \
               "Water Table: {0.water_table}\n\n" \
               "{1}\n\n" \
               "Units:\n" \
               "------\n" \
               "{2}".format(self, layer_tbl, unit_tbl)
