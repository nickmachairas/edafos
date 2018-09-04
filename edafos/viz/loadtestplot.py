""" Provide the ``LoadTestPlot`` class.

"""

# -- Imports -----------------------------------------------------------------
import matplotlib.pyplot as plt


# -- LoadTestPlot Class ------------------------------------------------------

class LoadTestPlot(object):
    """ Class to represent a new load test plot using the `Bokeh
    <https://bokeh.pydata.org/>`_ and the the `Matplotlib
    <https://matplotlib.org/>`_ libraries.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, unit_system, **kwargs):
        """
        Args:
            unit_system (str): The unit system for the load test. Can only be
                'English', or 'SI'.

        Keyword Args:
            library (str): Define the library that sill be used to draw the
                plot. Options are 'matplotlib' or 'bokeh'. Default is
                'matplotlib'.

            title (str): Title of the plot.

            q (list): List of load values.

                - For **SI**: Enter load, :math:`Q`, in **kN**.
                - For **English**: Enter load, :math:`Q`, in **kip**.

            s (list): List of displacement values.

                - For **SI**: Enter displacement, :math:`S`, in **centimeters**.
                - For **English**: Enter displacement, :math:`S`, in **inches**.

        """

        # -- Check for Unit System -------------------------------------------
        if unit_system in ['English', 'SI']:
            self.unit_system = unit_system
        else:
            raise ValueError("Unit system can only be 'English' or 'SI'.")

        # -- Check for valid kwargs ------------------------------------------
        allowed_keys = ['library', 'title', 'q', 's']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # -- Assign values ---------------------------------------------------
        self.title = kwargs.get('title', None)
        self.library = kwargs.get('library', 'matplolib')
        if self.library not in ['matplotlib', 'bokeh']:
            raise ValueError("Plotting library can only be 'matplotlib' or "
                             "'bokeh'")
        self.q = kwargs.get('q', None)
        self.s = kwargs.get('s', None)
        if len(self.q) != len(self.s):
            raise ValueError("'q' and 's' lists must be of equal length")
        if (self.q is None) or (self.s is None):
            raise ValueError("Can't plot without data, can I?")

    # -- Method that produces the Matplotlib plot ----------------------------
    def pltplot(self):
        """ Method that produces the Matplotlib plot

        Returns:
            A load test plot.
        """
        fig = plt.figure(1, figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.plot(self.q, self.s)
        ax.set_ylabel('Displacement, S (inches)')
        ax.set_xlabel('Load, Q (kips)')
        ax.invert_yaxis()
        ax.grid(color='k', linestyle='--', linewidth=0.75, alpha=0.5, zorder=-1)
        plt.title(self.title, weight='bold')

        return plt.show()

    # -- Method that produces the Bokeh plot ---------------------------------
    def bokehplot(self):
        """ Method that produces the Matplotlib plot

        Returns:
            A load test plot.
        """

    # -- Final step to produce the plot --------------------------------------
    def draw(self):
        """ Method that produces the Matplotlib or Bokeh plot based on the
        selection.

        Returns:
            A load test plot.
        """
        if self.library == 'matplotlib':
            return self.pltplot()
        else:
            return self.bokehplot()
