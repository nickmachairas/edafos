""" Provide the ``LoadTestPlot`` class.

"""

# -- Imports -----------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from bokeh.plotting import figure, output_file, show
from bokeh.models import DataRange1d, LinearAxis


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

            web_embed (bool): If True, the plot is returned but not shown or
                saved. Used to embed the plot in websites, tested with Flask.
                Default is False. Currently only works with the Bokeh library.

            title (str): Title of the plot.

            q (list): List of load values.

                - For **SI**: Enter load, :math:`Q`, in **kN**.
                - For **English**: Enter load, :math:`Q`, in **kip**.

            s (list): List of displacement values.

                - For **SI**: Enter displacement, :math:`S`, in **millimeters**.
                - For **English**: Enter displacement, :math:`S`, in **inches**.

            filename (str): Define the filename of the saved image (png format)
                of the load test plot. Default is ``None`` and no image is
                exported. Note: when the filename is defined, the image is
                exported but not shown. Also, plots are exported for the
                'matplotlib' library only, the 'bokeh' library (v.0.13.0)
                required far to many dependencies to export.

            elastic_deflection (dict): The points defining the elastic
            deflection line. Input must be a dictionary:
            ``{'S': [min_s, max_s], 'Q': [min_q, max_q]}``.

                - For **SI**: Enter settlement in **millimeters** and load
                  in **kilonewtons**.
                - For **English**: Enter settlement in **inches** and load
                  in **kip**.

        """

        # -- Check for Unit System -------------------------------------------
        if unit_system in ['English', 'SI']:
            self.unit_system = unit_system
        else:
            raise ValueError("Unit system can only be 'English' or 'SI'.")

        # -- Check for valid kwargs ------------------------------------------
        allowed_keys = ['library', 'web_embed', 'title', 'q', 's', 'filename',
                        'elastic_deflection']
        for key in kwargs:
            if key not in allowed_keys:
                raise AttributeError("'{}' is not a valid attribute.\nThe "
                                     "allowed attributes are: {}"
                                     "".format(key, allowed_keys))

        # -- Assign values ---------------------------------------------------
        self.title = kwargs.get('title', None)
        self.library = kwargs.get('library', 'matplolib')
        self.web_embed = kwargs.get('web_embed', False)
        if self.library not in ['matplotlib', 'bokeh']:
            raise ValueError("Plotting library can only be 'matplotlib' or "
                             "'bokeh'")
        self.q = kwargs.get('q', None)
        self.s = kwargs.get('s', None)
        if len(self.q) != len(self.s):
            raise ValueError("'q' and 's' lists must be of equal length")
        if (self.q is None) or (self.s is None):
            raise ValueError("Can't plot without data, can I?")
        self.filename = kwargs.get('filename', None)
        self.elastic_deflection = kwargs.get('elastic_deflection', None)

    # -- Method that produces the Matplotlib plot ----------------------------
    def pltplot(self):
        """ Method that produces the Matplotlib plot

        Returns:
            A load test plot.
        """
        # TODO: Add logic for when input units are SI

        fig = plt.figure(1, figsize=(6, 6), dpi=150)
        ax = fig.add_subplot(111)
        ax.plot(self.q, self.s, lw=2)
        ax.set_ylabel('Head Displacement, S (inches)', weight='semibold',
                      size=9)
        ax.set_xlabel('Axial Load, Q (kip)', weight='semibold', size=9)
        ax.invert_yaxis()
        ax.grid(color='grey', linestyle='--', linewidth=0.75, alpha=0.5,
                zorder=-1)
        plt.title(self.title, weight='bold', y=1.10)

        ax2 = ax.twinx()
        ax2.invert_yaxis()
        ymin, ymax = ax.get_ylim()
        ax2.set_ylim(ymin * 25.4, ymax * 25.4)
        ax2.set_ylabel('Head Displacement, S (mm)', weight='semibold', size=9)

        ax3 = ax.twiny()
        xmin, xmax = ax.get_xlim()
        ax3.set_xlim(xmin * 4.4482216, xmax * 4.4482216)
        ax3.set_xlabel('Axial Load, Q (kilonewton)', weight='semibold', size=9)

        ax.tick_params(axis='both', which='major', labelsize=9)
        ax2.tick_params(axis='both', which='major', labelsize=9)
        ax3.tick_params(axis='both', which='major', labelsize=9)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax2.yaxis.set_minor_locator(AutoMinorLocator())
        ax3.xaxis.set_minor_locator(AutoMinorLocator())

        if self.filename:
            return plt.savefig(fname=self.filename, dpi=150, format='png')
        else:
            return plt.show()

    # -- Method that produces the Bokeh plot ---------------------------------
    def bokehplot(self):
        """ Method that produces the Bokeh plot

        Returns:
            A load test plot.
        """
        # TODO: Add logic for when input units are SI

        p = figure(plot_width=500,
                   plot_height=500,
                   title=self.title,
                   x_axis_label='Axial Load, Q (kip)',
                   y_axis_label='Head Displacement, S (inches)')

        p.toolbar_location = None
        p.toolbar.active_drag = None
        p.grid.grid_line_dash = 'dotted'
        p.grid.grid_line_alpha = 0.75
        p.grid.grid_line_color = 'grey'
        p.x_range = DataRange1d(start=0, end=max(self.q)*1.08)
        p.y_range = DataRange1d(flipped=True, end=0, start=max(self.s)*1.08)
        p.extra_y_ranges = {"y2": DataRange1d(flipped=True, end=0,
                                              start=max(self.s)*1.08*25.4)}
        p.add_layout(LinearAxis(y_range_name="y2",
                                axis_label='Head Displacement, S (mm)'),
                     'right')
        p.extra_x_ranges = {"x2": DataRange1d(start=0,
                                              end=max(self.q)*1.08*4.4482216)}
        p.add_layout(LinearAxis(x_range_name="x2",
                                axis_label='Axial Load, Q (kilonewton)'),
                     'above')

        p.line(self.q, self.s, line_width=2)
        p.line(self.elastic_deflection['Q'],
               self.elastic_deflection['S'],
               line_width=2)

        if self.web_embed:
            return p
        else:
            output_file("lt_plot.html")
            show(p)

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
