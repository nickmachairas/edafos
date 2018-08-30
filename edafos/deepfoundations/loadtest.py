""" Provide the ``LoadTest`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.deepfoundations import Pile
import numpy as np


# -- LoadTest Class ----------------------------------------------------------

class LoadTest(Pile):
    """ Class to represent a new pile load test.

    .. warning::

       Pay attention to the input units for each unit system that you
       choose to use. Refer to the parameter definition below or the
       :ref:`input_units` page.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, unit_system, **kwargs):
        """
        Args:
            unit_system (str): The unit system for the load test. Can only be
                'English', or 'SI'. Properties inherited from the ``Project``
                class.

        Keyword Args:
            loadtest_type (str): Type of load test. Available options are:

                - ``static``: TODO: a lot more to add here

        """
        super().__init__(unit_system=unit_system)

        # -- Check for valid kwargs ------------------------------------------
        allowed_keys = ['loadtest_type']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # -- Assign values ---------------------------------------------------
        self.loadtest_type = kwargs.get('loadtest_type', None)

        # -- Check for valid loadtest type -----------------------------------
        allowed_loadtest_type = ['static']
        if self.loadtest_type in allowed_loadtest_type:
            pass
        elif self.loadtest_type is None:
            raise ValueError("Must specify `loadtest_type`.")
        else:
            raise ValueError("'{}' not recognized. Pile load test type can "
                             "only be {}.".format(self.pile_type,
                                                  allowed_loadtest_type))
