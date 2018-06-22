""" Provide the ``Olson 90`` class.

"""

# -- Imports -----------------------------------------------------------------
from .capacity_base import CapacityMethod


# -- Olson 90 Class ----------------------------------------------------------

class Olson90(CapacityMethod):
    """ Class to represent the Olson 90 method for capacity calculations of
    driven or drilled piles. For the engineering background refer to the section
    on the :ref:`olson90-method`.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, project):
        """
        Args:
            project (class): Provide the ``Project`` object as defined in the
                :class:`~edafos.project.Project` class.
        """
        super().__init__(project=project)

        self.method_name = 'Olson 90'

        # Run pre check
        self._pre_check(['soil_desc', 'tuw', 'corr_n', 'su'])

        # Run analysis
        self.run()

    # -- Method for shaft resistance -----------------------------------------
    def shaft_res_per_z(self, z1, z2):
        """ Method that follows the Olson 90 method for pile shaft resistance
        and calculates :math:`R_s` for a section defined by ``z1`` and ``z2``.

        Args:
            z1 (float): Vertical depth to the highest point of interest,
                measured from the top of the soil profile.

                - For **SI**: Enter depth, *z1*, in **meters**.
                - For **English**: Enter depth, *z1*, in **feet**.

            z2 (float): Vertical depth to the lowest point of interest,
                measured from the top of the soil profile.

                - For **SI**: Enter depth, *z1*, in **meters**.
                - For **English**: Enter depth, *z1*, in **feet**.

        Returns:
            Quantity: Two values with units depending on pile type. The first
            for **plugged** conditions, the second for **unplugged** conditions.

        """
        # Input check
        if z2 <= z1:
            raise ValueError("'z2' must be larger than 'z1', please correct.")

        # Get soil type (cohesive/cohesionless)
        soil_type = self.project.sp.get_soil_prop(z2, 'soil_type')

        # Get Average Effective Stress
        mid_z = z1 + ((z2 - z1) / 2)
        eff_stress = self.project.sp.calculate_stress(mid_z)

        # -- Cohesive Soils --------------------------------------------------
        if soil_type == 'cohesive':
            # Get the shear strength
            su = self.project.sp.get_soil_prop(z2, 'su')

            # Get the alpha factor
            a_factor = self.a_factor_rev_api(eff_stress, su)

            # Calculate unit shaft resistance
            f_s = self.unit_shaft_res_clay(a_factor, su)

        pass

    # -- Method that follows the recipe --------------------------------------
    def run(self):
        """ Method where the method "recipe" is compiled and all calculations
        are performed.

        Returns:

        """
        # z_list = self._z_for_analysis()
        z_list = self.project.z_layer_pile()

        plugged = True
        total_r_s_out = 0
        total_r_s_in = 0

        for top_z, bot_z in zip(z_list[:-1], z_list[1:]):
            # Effective stress
            mid_z = top_z + ((bot_z - top_z)/2)
            eff_sigma = self.project.sp.calculate_stress(mid_z)
            bot_sigma = self.project.sp.calculate_stress(bot_z)

            # Get soil type (cohesive/cohesionless)
            soil_type = self.project.sp.get_soil_prop(bot_z, 'soil_type')

            # Plugged conditions
            side_area_out = self.project.pile.side_area(top_z, bot_z,
                                                        box_area=True)
            toe_area_pl = self.project.pile.xsection_area(bot_z, box_area=True,
                                                          soil_plug=True)

            # Unplugged conditions
            if self.project.pile.pile_type in ['pipe-open', 'h-pile']:
                side_area_in = self.project.pile.side_area(top_z, bot_z,
                                                           inside=True)
                toe_area_upl = self.project.pile.xsection_area(bot_z)
            else:
                side_area_in = 0 * self.project.set_units('pile_side_area')
                toe_area_upl = 0 * self.project.set_units('pile_xarea_alt')

            if soil_type == 'cohesive':
                # Side Friction
                su = self.project.sp.get_soil_prop(bot_z, 'su')
                a_factor = self.a_factor_rev_api(eff_sigma, su)
                f_s = self.unit_shaft_res_clay(a_factor, su)

                # End bearing
                toe_su = self.average_toe_su()
                q_p = self.unit_toe_res_clay(toe_su)
            else:
                # Side Friction
                corr_n = self.project.sp.get_soil_prop(bot_z, 'corr_n')
                soil_desc = self.project.sp.get_soil_prop(bot_z, 'soil_desc')
                if self.project.pile.pile_type in ['pipe-open', 'h-pile']:
                    k = self.lateral_k_olson90(corr_n, False)
                else:
                    k = self.lateral_k_olson90(corr_n, True)
                delta = self.olson90_table(soil_desc, corr_n, 'delta')
                f_lim = self.olson90_table(soil_desc, corr_n, 'f_lim')
                f_s = min(self.unit_shaft_res_sand(k, eff_sigma, delta), f_lim)

                # End bearing
                n_q = self.olson90_table(soil_desc, corr_n, 'N_q')
                q_lim = self.olson90_table(soil_desc, corr_n, 'q_lim')
                q_p = min((bot_sigma * n_q), q_lim)

            r_s_out = self.shaft_resistance(f_s, side_area_out)
            r_s_in = self.shaft_resistance(f_s, side_area_in)

            total_r_s_out = total_r_s_out + r_s_out
            total_r_s_in = total_r_s_in + r_s_in

            r_p_pl = self.toe_resistance(q_p, toe_area_pl)
            r_p_upl = self.toe_resistance(q_p, toe_area_upl)

            # Plugged total resistance
            r_n_pl = total_r_s_out + r_p_pl

            # Unplugged total resistance
            if self.project.pile.pile_type in ['pipe-open', 'h-pile']:
                r_n_upl = total_r_s_out + total_r_s_in + r_p_upl
            else:
                r_n_upl = 0 + total_r_s_in + r_p_upl

            # Store values in data frame
            self.tab_results.loc[len(self.tab_results) + 1] = [
                bot_z, total_r_s_out.magnitude, total_r_s_in.magnitude,
                r_p_pl.magnitude, r_p_upl.magnitude, r_n_pl.magnitude,
                r_n_upl.magnitude]

        max_unplugged = self.tab_results.iloc[:, -1].max()
        max_pluged = self.tab_results.iloc[:, -2].max()

        if self.project.pile.pile_type in ['pipe-open', 'h-pile']:
            if max_unplugged < max_pluged:
                plugged = False
            result = min(max_unplugged, max_pluged)
        else:
            result = max_pluged

        self.capacity = result
        self.plugged = plugged

        return self
