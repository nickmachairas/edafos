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
        'perimeter': 47.77,  # = 2*depth + 4*flange_width - 2*web_thickness
        'box_area': 65.40,  # = depth * flange_width
        'box_perimeter': 32.35,  # = 2*depth + 2*flange_width
        'depth': 8.02,  # d
        'web_thickness': 0.445,  # tw
        'flange_width': 8.155,  # bf
        'flange_thickness': 0.445,  # tf
    },
    'HP10X42': {
        'area': 12.4,
        'perimeter': 58.87,
        'box_area': 97.73,
        'box_perimeter': 39.55,
        'depth': 9.7,
        'web_thickness': 0.415,
        'flange_width': 10.075,
        'flange_thickness': 0.42,
    },
    'HP10X57': {
        'area': 16.8,
        'perimeter': 59.75,
        'box_area': 102.1,
        'box_perimeter': 40.43,
        'depth': 9.99,
        'web_thickness': 0.565,
        'flange_width': 10.225,
        'flange_thickness': 0.565,
    },
    'HP12X53': {
        'area': 15.5,
        'perimeter': 70.87,
        'box_area': 141.9,
        'box_perimeter': 47.65,
        'depth': 11.78,
        'web_thickness': 0.435,
        'flange_width': 12.045,
        'flange_thickness': 0.435,
    },
    'HP12X63': {
        'area': 18.4,
        'perimeter': 71.35,
        'box_area': 144.8,
        'box_perimeter': 48.13,
        'depth': 11.94,
        'web_thickness': 0.515,
        'flange_width': 12.125,
        'flange_thickness': 0.515,
    },
    'HP12X74': {
        'area': 21.8,
        'perimeter': 71.91,
        'box_area': 148.2,
        'box_perimeter': 48.69,
        'depth': 12.13,
        'web_thickness': 0.605,
        'flange_width': 12.215,
        'flange_thickness': 0.61,
    },
    'HP12X84': {
        'area': 24.6,
        'perimeter': 72.37,
        'box_area': 151,
        'box_perimeter': 49.15,
        'depth': 12.28,
        'web_thickness': 0.685,
        'flange_width': 12.295,
        'flange_thickness': 0.685,
    },
    'HP14X73': {
        'area': 21.4,
        'perimeter': 84.55,
        'box_area': 198.5,
        'box_perimeter': 56.39,
        'depth': 13.61,
        'web_thickness': 0.505,
        'flange_width': 14.585,
        'flange_thickness': 0.505,
    },
    'HP14X89': {
        'area': 26.1,
        'perimeter': 85.21,
        'box_area': 203.2,
        'box_perimeter': 57.05,
        'depth': 13.83,
        'web_thickness': 0.615,
        'flange_width': 14.695,
        'flange_thickness': 0.615,
    },
    'HP14X102': {
        'area': 30,
        'perimeter': 85.75,
        'box_area': 207.1,
        'box_perimeter': 57.59,
        'depth': 14.01,
        'web_thickness': 0.705,
        'flange_width': 14.785,
        'flange_thickness': 0.705,
    },
    'HP14X117': {
        'area': 34.4,
        'perimeter': 86.35,
        'box_area': 211.5,
        'box_perimeter': 58.19,
        'depth': 14.21,
        'web_thickness': 0.805,
        'flange_width': 14.885,
        'flange_thickness': 0.805,
    },
}

si_piles = {
    # TODO: Add SI pile details
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
