""" Provide the ``API`` class.

"""

# -- Imports -----------------------------------------------------------------


# -- API Class ---------------------------------------------------------------

class API(object):
    """ Class to represent the API method for capacity calculations of driven
    or drilled piles.

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

    # -- Private method for expanded list of z's -----------------------------

    def _z_analysis(self):
        """ Private method that expands the
        :meth:`~edafos.project.Project.z_layer_pile` list to produce smaller
        intervals that the analysis will run on. These intervals are:

        - For **SI**: 0.2 meters
        - For **English**: 0.5 feet

        Returns:
            list: A list of depths, :math:`z` (unitless).
        """

