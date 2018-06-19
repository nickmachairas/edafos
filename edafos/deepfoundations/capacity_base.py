""" Provide the ``CapacityMethod`` class.

"""

# -- Imports -----------------------------------------------------------------
import numpy as np
import pandas as pd


# -- CapacityMethod Class ----------------------------------------------------

class CapacityMethod(object):
    """ Class to represent the base methods shared by all Capacity Methods. It
    is not anticipated that users will interact with this class.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, project):
        """
        Args:
            project (class): Provide the ``Project`` object as defined in the
                :class:`~edafos.project.Project` class.
        """
        # Type check
        if str(type(project)) == "<class 'edafos.project.Project'>":
            self.project = project
        else:
            raise TypeError("Wrong input. Attach `Project` objects only.")

        self.method_name = 'Base Capacity Method'

    # -- Private method for pre-checks ---------------------------------------
    def _pre_check(self, req):
        """ Private method that goes through all defined soil and pile
        properties and compares against the requested properties to ensure they
        are available.

        Pile objects cannot be created without the required properties, hence,
        at the moment this method focuses mostly on soil properties.

        Args:
            req (list): A list of required properties by their corresponding
                argument names (i.e. ``[soil_type, tuw, corr_n]``).

        Returns:
            pass/fail (TODO- with recommendations for missing properties)
        """
        # Input check
        if type(req) is not list:
            raise ValueError("Input for 'req' is not a list as it should.")
        # Note and TODO:
        # pile properties ['pile_type', 'side', 'diameter', 'thickness'] are not
        # checked because the Pile object cannot be created without them
        allowed = ['soil_desc', 'tuw', 'corr_n', 'su']

        # One more input check
        for prop in req:
            if prop not in allowed:
                raise ValueError("Invalid property '{}'. Allowed properties are"
                                 " {}.".format(prop, allowed))

        # Shorthand for convenience
        df = self.project.sp.layers

        # -- Soil checks -----------------------------------------------------
        if len(df.index) == 0:
            raise ValueError("No layers in soil profile.")

        # Create an empty dictionary
        missing = {}
        for i in df.index:
            missing[i] = []

        # Loop through layers
        for i in df.index:
            for prop in req:
                if prop == 'tuw':
                    if np.isnan(df['TUW'][i]):
                        missing[i].append('tuw')
                elif prop == 'corr_n':
                    if df['Soil Type'][i] == 'cohesionless':
                        if np.isnan(df['Corr. N'][i]):
                            missing[i].append('corr_n')
                elif prop == 'su':
                    if df['Soil Type'][i] == 'cohesive':
                        if np.isnan(df['Shear Su'][i]):
                            missing[i].append('su')
                elif prop == 'soil_desc':  # This accommodates Olson 90 only!!!
                    if df['Soil Type'][i] == 'cohesionless':
                        if pd.isnull(df['Soil Desc'][i]):
                            missing[i].append('soil_desc')

        msg = "ANALYSIS PRE-CHECK:\n"
        for i in missing:
            if len(missing[i]) > 0:
                msg = msg + "Layer {} ({}) is missing these properties: " \
                            "{}\n".format(i, df['Soil Type'][i], missing[i])

        if len(msg) > 20:
            raise ValueError("{} ".format(self.method_name.upper()) + msg)
        else:
            print("\n***** {} ANALYSIS PRE-CHECK COMPLETE - NO REQUIRED "
                  "PROPERTIES MISSING *****\n".format(self.method_name.upper()))

    # -- Private method for expanded list of z's -----------------------------

    def _z_for_analysis(self):
        """ Private method that expands the
        :meth:`~edafos.project.Project.z_layer_pile` list to produce smaller
        intervals that the analysis will run on. These intervals are:

        - For **SI**: 0.2 meters
        - For **English**: 0.5 feet

        Returns:
            list: A list of depths, :math:`z` (unitless).
        """
        last_z = self.project.sp.layers['Depth'].max()
        if self.project.unit_system == 'SI':
            iz = list(np.arange(0, last_z, 0.2))
        else:
            iz = list(np.arange(0, last_z, 0.5))

        # Compile list
        z_list = iz + self.project.z_layer_pile()
        # Remove duplicates and sort
        z_list = list(set(z_list))
        z_list.sort()

        return z_list
