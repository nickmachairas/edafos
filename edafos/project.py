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
        self.sp = None
        self.pile = None

    # -- A Helper Method to set units ----------------------------------------

    def set_units(self, dim):
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
            'degrees': {'SI': units.degree, 'English': units.degree},
            'length': {'SI': units.meter, 'English': units.feet},
            'tuw': {'SI': units.kN / units.meter ** 3,
                    'English': (units.kip/1000) / units.feet ** 3},
            'stress': {'SI': units.kN / units.meter ** 2,
                       'English': units.kip / units.feet ** 2},
            'capacity': {'SI': units.kN, 'English': units.kip},
            'pile_diameter': {'SI': units.cm, 'English': units.inches},
            'pile_length': {'SI': units.meter, 'English': units.feet},
            'pile_xarea': {'SI': units.cm ** 2, 'English': units.inches ** 2},
            'pile_xarea_alt': {'SI': units.meter ** 2,
                               'English': units.feet ** 2},
            'pile_side_area': {'SI': units.meter ** 2,
                               'English': units.feet ** 2},
            'modulus': {'SI': 10e9 * units.pascal,
                        'English': units.kip / units.inches ** 2},
            'aeol': {'SI': units.kN / units.meter,
                     'English': units.kip / units.inches},
        }

        return unit_dict[dim][self.unit_system]

    # -- Method to attach a soil profile -------------------------------------
    def attach_sp(self, obj):
        """ Method that attaches a ``SoilProfile`` object to the ``Project``
        object. The ``Project`` class supports adding **one** ``SoilProfile``
        object. If you run the ``attach_sp`` more than once, it will replace
        the previous ``SoilProfile`` object.

        Args:
            obj (class): A :class:`~edafos.soil.profile.SoilProfile` class.

        Returns:
            self
        """
        # Type check
        if str(type(obj)) == "<class 'edafos.soil.profile.SoilProfile'>":
            self.sp = obj
        else:
            raise TypeError("Wrong input. Attach `SoilProfile` objects only.")

        # Unit system check
        # TODO: This needs more work for what happens when units are different
        if self.unit_system != self.sp.unit_system:
            raise AttributeError("Inconsistent unit systems.")
        else:
            pass

        return self

    # -- Method to attach a pile ---------------------------------------------
    def attach_pile(self, obj):
        """ Method that attaches a ``Pile`` object to the ``Project`` object.
        The ``Project`` class supports adding **one** ``Pile`` object. If you
        run the ``attach_pile`` more than once, it will replace the previous
        ``Pile`` object.

        Args:
            obj (class): A :class:`~edafos.deepfoundations.piles.Pile` class.

        Returns:
            self
        """
        # Type check
        if str(type(obj)) == "<class 'edafos.deepfoundations.piles.Pile'>":
            self.pile = obj
        else:
            raise TypeError("Wrong input. Attach `Pile` objects only.")

        # Unit system check
        # TODO: This needs more work for what happens when units are different
        if self.unit_system != self.pile.unit_system:
            raise AttributeError("Inconsistent unit systems.")
        else:
            pass

        # Check if the pile is longer than the soil profile
        if self.sp is None:
            pass
        else:
            if self.sp.layers['Depth'].max() < self.pile.pen_depth.magnitude:
                raise ValueError("Pile penetration depth is larger than "
                                 "total soil profile depth.")
            else:
                pass

        return self

    # -- Method for list of relevant z's -------------------------------------

    def z_layer_pile(self):
        """ Method that analyzes the defined soil layers, water table, pile
        tapered sections (if any) and produces a list of depths, :math:`z`,
        where there is a change in soil conditions or pile properties.

        Returns:
            list: A list of depths, :math:`z` (unitless).
        """
        # Check if SoilProfile and Pile are attached
        if (self.sp is None) or (self.pile is None):
            raise ValueError("No SoilProfile or Pile attached to Project.")
        else:
            pass

        # Fix for negative water table (offshore)
        wt = self.sp.water_table.magnitude
        if wt < 0:
            wt = 0

        # Compile list
        z_list = self.sp.z_of_layers() + self.pile.z_of_pile() + [wt]
        # Remove duplicates and sort
        z_list = list(set(z_list))
        z_list.sort()

        return z_list

    # -- Method for string representation ------------------------------------

    def __str__(self):
        return "Project ID: {0.project_id}\nProject Name: {0.project_name}" \
               "\nDatetime: {0.date}\nUnit System: {0.unit_system}\n" \
               "{1}\n" \
               "Soil Profile WT: {0.sp.water_table}\n" \
               "Pile Type: {0.pile.pile_type}".format(self, 12*'-')
