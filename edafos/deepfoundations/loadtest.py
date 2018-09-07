""" Provide the ``LoadTest`` class.

"""

# -- Imports -----------------------------------------------------------------
from edafos.viz import LoadTestPlot
import pandas as pd


# -- LoadTest Class ----------------------------------------------------------

class LoadTest(object):
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
            name (str): Name of load test. If not specified it will be assigned
                a generic "Pile Load Test".

            loadtest_type (str): Type of load test. Available options are:

                - ``static``: TODO: a lot more to add here

            qs_data (list): A list of points where each point is represented by
                a ``(Q, S)`` tuple.

                - For **SI**: Enter load, :math:`Q`, in **kN** and
                  displacement, :math:`S`, in **millimeters**.
                - For **English**: Enter load, :math:`Q`, in **kip** and
                  displacement, :math:`S`, in **inches**.

            pile (class): Define the pile object that this load test is
                associated with.

        """

        # -- Check for Unit System -------------------------------------------
        if unit_system in ['English', 'SI']:
            self.unit_system = unit_system
        else:
            raise ValueError("Unit system can only be 'English' or 'SI'.")

        # -- Check for valid kwargs ------------------------------------------
        allowed_keys = ['name', 'loadtest_type', 'qs_data', 'pile']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # -- Assign values ---------------------------------------------------
        self.name = kwargs.get('name', 'Pile Load Test')
        self.loadtest_type = kwargs.get('loadtest_type', None)
        self.qs_data = kwargs.get('qs_data', None)
        self.pile = kwargs.get('pile', None)

        # -- Check for valid loadtest type -----------------------------------
        allowed_loadtest_type = ['static']
        if self.loadtest_type in allowed_loadtest_type:
            pass
        elif self.loadtest_type is None:
            raise ValueError("Must specify `loadtest_type`.")
        else:
            raise ValueError("'{}' not recognized. Pile load test type can "
                             "only be {}.".format(self.loadtest_type,
                                                  allowed_loadtest_type))

        # -- Convert Q/S data to DataFrame -----------------------------------
        if self.qs_data:
            self.qs_data = pd.DataFrame(data=self.qs_data, columns=['Q', 'S'])

    # -- Method that returns a plot ------------------------------------------
    def plot(self, library='matplotlib', image_name=None):
        """ Method that draws the load test plot.

        Args:
            library (str): Define the library that sill be used to draw the
                plot. Options are 'matplotlib' or 'bokeh'. Default is
                'matplotlib'.

            image_name (str): Define the filename of the saved image (png
                format) of the load test plot. Default is ``None`` and no image
                is exported. Note: when 'image_name' is defined, the image is
                exported but not shown. Also, plots are exported for the
                'matplotlib' library only, the 'bokeh' library (v.0.13.0)
                required far to many dependencies to export.

        Returns:
            A load test plot.
        """
        p = LoadTestPlot(unit_system=self.unit_system,
                         library=library,
                         title=self.name,
                         q=self.qs_data.Q.values,
                         s=self.qs_data.S.values,
                         filename=image_name)

        return p.draw()
