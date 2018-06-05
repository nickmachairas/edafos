""" Provide the ``SoilProfile`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.project import Project
import numpy as np
import pandas as pd
import pint
units = pint.UnitRegistry()


# -- SoilProfile Class -------------------------------------------------------

class SoilProfile(Project):
    """ Class to represent a new soil profile.

    .. warning::

       Pay attention to the base units for each unit system that you
       choose to use. Refer to the parameter definition below or the
       :ref:`base_units` page.

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
        if self.unit_system == 'SI':
            self.water_table = float(water_table) * units.meter
        else:
            self.water_table = float(water_table) * units.feet

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
                     'Corrected N', 'Field Phi', 'Calc. Phi', 'Shear Strength']
        unit_list = [
            '(coh/coless)',                                        # Soil Type
            '(m)' if self.unit_system == 'SI' else '(ft)',         # Depth
            '(m)' if self.unit_system == 'SI' else '(ft)',         # Height
            '(kN/m3)' if self.unit_system == 'SI' else '(lbf/ft3)',  # TUW
            '(bl/0.3m)' if self.unit_system == 'SI' else '(bpf)',  # Field N
            '(bl/0.3m)' if self.unit_system == 'SI' else '(bpf)',  # Corrected N
            '(deg)',                                               # Field Phi
            '(deg)',                                               # Calc. Phi
            '(kN/m2)' if self.unit_system == 'SI' else '(lbf/ft2)'  # Shear Su
        ]
        arrays = [name_list, unit_list]
        tuples = list(zip(*arrays))
        header = pd.MultiIndex.from_tuples(tuples, names=['Property', 'Units'])
        self.layers = pd.DataFrame(columns=header)
        self.layers.index.name = 'Layer'

        return self

    # -- Method to add layers ------------------------------------------------

    def add_layer(self, soil_type, height, tuw, **kwargs):
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

            tuw (float): Total unit weight of soil.

                - For **SI**: Enter TUW in **kN/m**\ :sup:`3`.
                - For **English**: Enter TUW in **lbf/ft**\ :sup:`3`.

        Keyword Args:
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
        for column in self.layers.columns.levels[0]:
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
                Allowed values are ``pore_water``, ``total``, ``effective``
                and ``all``. The last value, ``all``, returns all three
                stresses in the same order.

        Returns:
            Quantity: A physical quantity with associated units.

        """


    def __str__(self):
        return "Unit system: {0.unit_system}\nDepth to Water Table: " \
               "{0.water_table}\n\n{0.layers}".format(self)
