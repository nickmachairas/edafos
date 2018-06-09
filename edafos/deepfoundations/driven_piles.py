""" Provide the ``DrivenPiles`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.project import Project
# from tabulate import tabulate
# import numpy as np
# import pandas as pd
# import pint
# units = pint.UnitRegistry()


# -- SoilProfile Class -------------------------------------------------------

class DrivenPile(Project):
    """ Class to represent a new driven pile.

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

        # Set units for the water table
        self.water_table = float(water_table) * self._set_units('length')

        # Call function to instantiate the soil profile data frame
        self._create_profile()
