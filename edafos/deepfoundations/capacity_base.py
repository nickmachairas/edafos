""" Provide the ``CapacityMethod`` class.

"""

# -- Imports -----------------------------------------------------------------
import numpy as np
import pandas as pd
from edafos.data import english_hpiles, olson90_data


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

        # Create data frame for tabular results
        if self.project.unit_system == 'English':
            col_names = ['Depth (ft)', 'Rs_o (kip)', 'Rs_i (kip)',
                         'Rp_p (kip)',  'Rp_u (kip)', 'Rn_p (kip)',
                         'Rn_u (kip)']
        else:
            col_names = ['Depth (m)', 'Rs_o (kN)', 'Rs_i (kN)',
                         'Rp_p (kN)', 'Rp_u (kN)', 'Rn_p (kN)',
                         'Rn_u (kN)']
        self.tab_results = pd.DataFrame(columns=col_names)
        self.capacity = None
        self.plugged = None

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
            list: Two lists of depths, :math:`z` (unitless). The first list is
                at the bottom, the second list is at mid point for average
                effective stress calculations.
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

        # mid_z_list = []
        # for i, ii in zip(z_list[:-1], z_list[1:]):
        #     mid = (ii - i)/2
        #     mid_z_list.append(i + mid)
        #
        # return z_list, [0.0] + mid_z_list
        return z_list

    # -- Method for shaft resistance (general) -------------------------------
    @staticmethod
    def shaft_resistance(fs, area):
        """ Method that calculates shaft resistance, :math:`R_s`, as per
        equation :eq:`R_s-api`.

        Args:
            fs (float): unit shaft resistance, :math:`f_s`
            area (float): side surface area, :math:`A_s`

        Returns:
            Quantity: Shaft resistance with units.
        """
        return fs * area

    # -- Method for toe resistance (general) ---------------------------------
    def toe_resistance(self, qp, area):
        """ Method that calculates toe resistance, :math:`R_p`, as per
        equation :eq:`R_p-api`.

        Args:
            qp (float): Unit toe resistance, :math:`q_p`
            area (float): pile toe cross-sectional area, :math:`A_p` or
                :math:`A_{pp}`

        Returns:
            Quantity: Toe resistance with units.
        """
        res = qp * area
        return res.to(self.project._set_units('capacity'))

    # -- Method for unit shaft resistance (cohesive) -------------------------
    @staticmethod
    def unit_shaft_res_clay(a, su):
        """ Method that calculates unit shaft resistance for cohesive soils, as
        per equation :eq:`f_s-api-clay`.

        Args:
            a (float): :math:`\\alpha` factor (unitless)
            su (float): undrained shear strength of soil

        Returns:
            Quantity: Unit shaft resistance with units.
        """
        return a * su

    # -- Method for alpha factor (Revised API, cohesive) ---------------------
    @staticmethod
    def a_factor_rev_api(sigma, su):
        """ Method that calculates the :math:`\\alpha` factor for cohesionless
        soils, as per equation :eq:`a-rev-api-clay`.

        Args:
            sigma (float): average effective stress
            su (float): undrained shear strength of soil

        Returns:
            float or dimensionless Quantity: The :math:`\\alpha` factor
        """
        psi = su / sigma
        if psi <= 1:
            alpha = max(0.0, (min(0.5 * (psi ** -0.5), 1.0)))
        else:
            alpha = max(0.0, (min(0.5 * (psi ** -0.25), 1.0)))

        return alpha

    # -- Method for unit toe resistance (cohesive) ---------------------------
    @staticmethod
    def unit_toe_res_clay(su):
        """ Method that calculates the unit toe resistance, :math:`q_p` for
        cohesionless soils, as per equation :eq:`q_p-api-clay`.

        The average, :math:`su`, is implemented in the
        :meth:`~edafos.deepfoundations.capacity_base.CapacityMethod.average_toe_su`
        method.

        Args:
            su (float): undrained shear strength of soil

        Returns:
            Quantity: Unit toe resistance with units.
        """
        return 9 * su

    # -- Method for average toe su (cohesive) --------------------------------
    def average_toe_su(self):
        """ API RP2A guidelines, as also shown in equation :eq:`q_p-api-clay`,
        recommend that for bearing capacity calculations, the undrained shear
        strength, :math:`s_u`, should be taken as the average over a distance
        of two pile diameters below the tip of the pile. This method calculates
        this average if there is available information.

        Returns:
            Quantity: Average
        """
        # TODO: What about tapered piles?
        toe_z = self.project.pile.pen_depth
        pile_side = self.project.pile.side
        pile_diameter = self.project.pile.diameter
        pile_shape = self.project.pile.shape
        if pile_side is None:
            if self.project.pile.pile_type == 'h-pile':
                d = english_hpiles[pile_shape]['flange_width']
                two_d_z = toe_z + 2 * d * (self.project._set_units('pile_diameter'))
            else:
                two_d_z = toe_z + 2 * pile_diameter
        else:
            if pile_shape in ['square-solid', 'square-hollow']:
                two_d_z = toe_z + 2 * pile_side
            else:
                # TODO: n = 5 here is not correct, must fix for hex and octa
                two_d_z = toe_z + 2 * (pile_side/np.tan(np.pi/5))

        two_d_range = np.arange(toe_z.magnitude, two_d_z.magnitude, 0.2)

        count = 0
        added = 0
        for i in two_d_range:
            try:
                su = self.project.sp.get_soil_prop(i, 'su')
                added = added + su
                count = count + 1
            except ValueError:
                pass

        return added / count

    # -- Method for unit shaft resistance (cohesionless) ---------------------
    @staticmethod
    def unit_shaft_res_sand(k, sigma, delta):
        """ TODO: add...

        Returns:

        """
        return k * sigma * np.tan(np.deg2rad(delta))

    # -- Method for lateral earth K ------------------------------------------
    @staticmethod
    def lateral_k(corr_n, full_displ=True):
        """ TODO: add...

        Args:
            corr_n:
            full_displ:

        Returns:

        """
        if full_displ:
            k = 0.70 + 0.015 * corr_n
        else:
            k = 0.16 + 0.015 * corr_n

        return k

    # -- Method that returns Olson 90 guidelines -----------------------------
    def olson90_table(self, soil_desc, corr_n, req):
        """ TODO: add...

        Args:
            soil_desc:
            corr_n:
            req:

        Returns:

        """
        allowed_soil = ['gravel', 'sand-gravel', 'sand', 'sand-silt', 'silt']
        if soil_desc not in allowed_soil:
            raise ValueError("'{}' not a valid input for `soil_desc`. Valid "
                             "inputs are {}.".format(soil_desc, allowed_soil))

        allowed_req = ['delta', 'f_lim', 'N_q', 'q_lim']
        if req not in allowed_req:
            raise ValueError("'{}' not a valid input for `req`. Valid inputs "
                             "are {}.".format(req, allowed_req))

        if soil_desc in ['gravel', 'sand-gravel']:
            if 0 <= corr_n <= 4:
                res = olson90_data[soil_desc]['very_loose'][req]
            elif 5 <= corr_n <= 10:
                res = olson90_data[soil_desc]['loose'][req]
            elif 11 <= corr_n <= 30:
                res = olson90_data[soil_desc]['medium'][req]
            else:
                res = olson90_data[soil_desc]['dense'][req]
        elif soil_desc == 'sand':
            if 0 <= corr_n <= 4:
                res = olson90_data[soil_desc]['very_loose'][req]
            elif 5 <= corr_n <= 10:
                res = olson90_data[soil_desc]['loose'][req]
            elif 11 <= corr_n <= 30:
                res = olson90_data[soil_desc]['medium'][req]
            elif 31 <= corr_n <= 50:
                res = olson90_data[soil_desc]['dense'][req]
            elif 51 <= corr_n <= 100:
                res = olson90_data[soil_desc]['very_dense'][req]
            else:
                res = olson90_data[soil_desc]['very_dense+'][req]
        elif soil_desc == 'sand-silt':
            if 0 <= corr_n <= 4:
                res = olson90_data[soil_desc]['very_loose'][req]
            elif 5 <= corr_n <= 10:
                res = olson90_data[soil_desc]['loose'][req]
            elif 11 <= corr_n <= 30:
                res = olson90_data[soil_desc]['medium'][req]
            elif 31 <= corr_n <= 50:
                res = olson90_data[soil_desc]['dense'][req]
            elif 51 <= corr_n <= 100:
                res = olson90_data[soil_desc]['very_dense'][req]
            elif 101 <= corr_n <= 200:
                res = olson90_data[soil_desc]['very_dense+'][req]
            else:
                res = olson90_data[soil_desc]['very_dense++'][req]
        else:  # silt
            if 0 <= corr_n <= 4:
                res = olson90_data[soil_desc]['very_loose'][req]
            elif 5 <= corr_n <= 10:
                res = olson90_data[soil_desc]['loose'][req]
            elif 11 <= corr_n <= 30:
                res = olson90_data[soil_desc]['medium'][req]
            elif 31 <= corr_n <= 50:
                res = olson90_data[soil_desc]['dense'][req]
            else:
                res = olson90_data[soil_desc]['very_dense'][req]

        if req in ['f_lim', 'q_lim']:
            res = res * self.project._set_units('stress')

        return res
