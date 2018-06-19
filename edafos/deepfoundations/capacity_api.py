""" Provide the ``API`` class.

"""

# -- Imports -----------------------------------------------------------------
from .capacity_base import CapacityMethod


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
