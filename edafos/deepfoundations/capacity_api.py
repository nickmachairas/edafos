""" Provide the ``API`` class.

"""

# -- Imports -----------------------------------------------------------------
from .capacity_base import CapacityMethod
import pint
units = pint.UnitRegistry()


# -- API Class ---------------------------------------------------------------

class API(CapacityMethod):
    """ Class to represent the Revised API method for capacity calculations of
    driven or drilled piles.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, project):
        """
        Args:
            project (class): Provide the ``Project`` object as defined in the
                :class:`~edafos.project.Project` class.
        """
        super().__init__(project=project)

        self.method_name = 'Revised API'

        # Run pre check
        self._pre_check(['tuw', 'corr_n', 'su'])

    # -- Method for unit shaft resistance ------------------------------------
    @staticmethod
    def unit_shaft_res_clay(a, su):
        """ Method that calculates unit shaft resistance for cohesive soils, as
        per equation :eq:`f_s-api-clay`.

        Args:
            a (float): :math:`\\alpha` factor (unitless)
            su (float): undrained shear strength of soil

        Returns:
            Quantity: The unit shaft resistance with units.
        """
        return a * su

    # -- Method for alpha factor as per Revised API --------------------------
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
