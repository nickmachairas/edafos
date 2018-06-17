""" Provide the ``Project`` class.

As of this writing (v.0.1.0) ``Project`` classes will be required for all
actions.

"""

# -- Imports -----------------------------------------------------------------
from datetime import datetime
from random import randint
import pint
units = pint.UnitRegistry()


# -- Project Class -----------------------------------------------------------

class Project(object):
    """ Class to represent a new project.

    """

    def __init__(self, unit_system, **kwargs):
        """
        Args:
            unit_system (str): The unit system for the project. Can only be
                'English', or 'SI'.
        Keyword Args:
            project_id (int): The unique id for the project. If one is not
                provided, a random 8-digit number will be assigned.
            project_name (str): The project name. If none is entered it
                defaults to "New Project".
            date (timestamp): The date and time of the analysis. If it is not
                provided, the current time when the object was instantiated
                is stored.

        """

        # Check for valid attributes
        allowed_keys = ['project_id', 'project_name', 'date']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute. The "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # Check for Unit System
        if unit_system in ['English', 'SI']:
            self.unit_system = unit_system
        else:
            raise ValueError("Unit system can only be 'English' or 'SI'.")

        # Assign values
        self.project_id = kwargs.get('project_id', randint(10e6, 10e7-1))
        self.project_name = kwargs.get('project_name', 'New Project')
        self.date = kwargs.get('date', datetime.now())

    # -- A Helper Method to set units (Private) ------------------------------

    def _set_units(self, dim):
        """ A private helper method that returns the Pint units to be attached
        to a variable based on the set unit system and dimensionality (dim).
        Since this is a private method, the stored values will not be shown
        in the docstring. Refer to the `unit_dict` in the code.

        Args:
            dim (str): The dimensionality for the variable. For example, layer
                height is 'length'.

        Returns:
            Pint units.

        """
        unit_dict = {
            'length': {'SI': units.meter, 'English': units.feet},
            'tuw': {'SI': units.kN / units.meter ** 3,
                    'English': (units.kip/1000) / units.feet ** 3},
            'stress': {'SI': units.kN / units.meter ** 2,
                       'English': units.kip / units.feet ** 2},
            'pile_diameter': {'SI': units.cm, 'English': units.inches},
            'pile_length': {'SI': units.meter, 'English': units.feet},
            'pile_xarea': {'SI': units.cm ** 2, 'English': units.inches ** 2},
            'pile_side_area': {'SI': units.meter ** 2,
                               'English': units.feet ** 2},
        }

        return unit_dict[dim][self.unit_system]

    # -- Method for string representation ------------------------------------

    def __str__(self):
        return "Project ID: {0.project_id}\nProject Name: {0.project_name}" \
               "\nDatetime: {0.date}\nUnit System: {0.unit_system}".format(self)
