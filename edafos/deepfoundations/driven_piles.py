""" Provide the ``DrivenPiles`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.project import Project
# from tabulate import tabulate
# import numpy as np
# import pandas as pd
# import pint
# units = pint.UnitRegistry()


# -- H-Pile Dictionaries -----------------------------------------------------

english_piles = {
    'HP8X36': {
        'area': 10.6,
        'perimeter': 47.77,
        'box_area': 65.40,
        'box_perimeter': 32.35,
        'depth': 8.02,
        'web_thickness': 0.445,
        'flange_width': 8.155,
        'flange_thickness': 0.445,
    }
}

si_piles = {

}


# -- SoilProfile Class -------------------------------------------------------

class DrivenPile(Project):
    """ Class to represent a new driven pile.

    .. warning::

       Pay attention to the input units for each unit system that you
       choose to use. Refer to the parameter definition below or the
       :ref:`input_units` page.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, unit_system, pile_type, **kwargs):
        """
        Args:
            unit_system (str): The unit system for the project. Can only be
                'English', or 'SI'. Properties inherited from the ``Project``
                class.

            pile_type (str): Type of driven pile. Available options are:

                - ``pipe_open``: An open-ended circular steel pipe pile.
                    Requires keyword arguments ``diameter``, ``thickness``.
                - ``pipe_closed``: A closed-ended circular steel pipe pile.
                    Requires keyword argument ``diameter``.
                - ``concrete``: A rectangular (normally square) concrete pile.
                    Requires keyword argument ``side``.
                - ``h_pile``: An H shape steel beam used as a pile.
                    Requires keyword argument ``h_type``.

        Keyword Args:
            diameter (float): Pile diameter for circular piles.

                - For **SI**: Enter diameter in **centimeters**.
                - For **English**: Enter diameter in **inches**.

            thickness (float): Wall thickness of steel pipe piles.

                - For **SI**: Enter thickness in **centimeters**.
                - For **English**: Enter thickness in **inches**.

            side (float): Side length of rectangular (normally square) piles.

                - For **SI**: Enter side length in **centimeters**.
                - For **English**: Enter side length in **inches**.

            h_type (str): See... TODO: Add reference to table with sections.


        """
        super().__init__(unit_system=unit_system)

        # Check for valid pile type
        allowed_piles = ['pipe_open', 'pipe_closed', 'concrete', 'h_pile']
        if pile_type in allowed_piles:
            self.pile_type = pile_type
        else:
            raise ValueError("'{}' not recognized. Pile type can only be {}."
                             "".format(pile_type, allowed_piles))

        # Check for valid kwargs
        allowed_keys = ['diameter', 'thickness', 'side']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # Assign values
        self.diameter = kwargs.get('diameter', None)
        self.thickness = kwargs.get('thickness', None)
        self.side = kwargs.get('side', None)

        # Check that the selected pile type also has the required arguments
        pile_reqs = {
            'pipe_open': [self.diameter, self.thickness],
            'pipe_closed': [self.diameter],
            'concrete': [self.side],
        }
        pile_kwgs = {
            'pipe_open': ['diameter', 'thickness'],
            'pipe_closed': ['diameter'],
            'concrete': ['side'],
        }
        for pile in allowed_piles:
            if (self.pile_type == pile) and (None in pile_reqs[pile]):
                raise ValueError("Missing required properties for pile type: "
                                 "'{}'.\nEnter values for: {}."
                                 "".format(pile, pile_kwgs[pile]))
            else:
                pass
