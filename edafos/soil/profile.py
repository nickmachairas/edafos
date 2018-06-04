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

       Pay attention to the base units for each unit system that you will
       choose to use. Refer to the parameter definition below or the
       :ref:`base_units` page.

    """

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

    def _create_profile(self):
        """ A private method that instantiates the soil profile data frame.

        Returns:
            An empty Pandas DataFrame with two headers, one for the column
            names and another for the column units.

        """
        name_list = ['Soil Type', 'Depth', 'Height', 'TUW', 'Field N',
                     'Corrected N', 'Field Phi', 'Calc. Phi', 'Shear Strength']
        unit_list = [
            '(S/C)',                                               # Soil Type
            '(m)' if self.unit_system == 'SI' else '(ft)',         # Depth
            '(m)' if self.unit_system == 'SI' else '(ft)',         # Height
            '(kN/m3)' if self.unit_system == 'SI' else '(lbf/ft3)',  # TUW
            '(bl/0.3m)' if self.unit_system == 'SI' else '(bpf)',  # Field N
            '(bl/0.3m)' if self.unit_system == 'SI' else '(bpf)',  # Corrected N
            '(deg)',                                               # Field Phi
            '(deg)',                                               # Calc. Phi
            '(kN/m2)' if self.unit_system == 'SI' else '(lbf/ft2)'  # Shear Strength
        ]
        arrays = [name_list, unit_list]
        tuples = list(zip(*arrays))
        header = pd.MultiIndex.from_tuples(tuples, names=['Property', 'Units'])
        self.layers = pd.DataFrame(columns=header)

        return self

    def add_layer(self, soil_type, height, tuw, field_n=None, corr_n=None,
                  field_phi=None, calc_phi=None, su=None):
        """ Adds a new layer to the profile with the given parameters.

        Args:
            soil_type (str): Allowed values are 'cohesive' for clays and
                'cohesionless' for sands.
            height (float): Height of soil layer.

                - For **SI**: Enter height in **meters**.
                - For **English**: Enter height in **feet**.

            tuw (float): Total unit weight of soil.

                - For **SI**: Enter TUW in **kN/m**\ :sup:`3`.
                - For **English**: Enter TUW in **lbf/ft**\ :sup:`3`.

            field_n (int, optional): Field SPT-N values.
            corr_n (int, optional): Corrected Field SPT-N values.

                .. note::

                   If field SPT-N value is given without the corrected SPT-N,
                   the corrected value will be automatically calculated.

            field_phi (float, optional): Field internal angle of friction, *φ*,
                in degrees.
            calc_phi (float, optional): Calculated internal angle of friction,
                *φ*, from SPT-N values.
            su (float, optional): Undrained shear strength, *s*\ :sub:`u`.

                - For **SI**: Enter *s*\ :sub:`u` in **kN/m**\ :sup:`2`.
                - For **English**: Enter *s*\ :sub:`u` in **lbf/ft**\ :sup:`2`.


        """
        if len(self.layers) == 0:
            depth = height
        else:
            depth = self.layers.loc[len(self.layers) - 1, 'Depth'] + height

        # self.layers = self.layers.append({'Soil Type': soil_type,
        #                                   'Depth': 12,
        #                                   'Height': height,
        #                                   'TUW': tuw
        #                                   }, ignore_index=True)

        self.layers.loc[len(self.layers)] = [
            soil_type, depth, height, tuw, field_n, corr_n, field_phi,
            calc_phi, su]

        return self

    def __str__(self):
        return "Unit system: {0.unit_system}\nDepth to Water Table: " \
               "{0.water_table}\n\nLayers:\n{0.layers}".format(self)
