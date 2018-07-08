""" Provide the `` ... `` class.

"""

# -- Imports -----------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np


# -- ... Class -------------------------------------------------------

class ProfilePlot(object):
    """ Class to represent a profile plot.

    """

    # -- Constructor ---------------------------------------------------------

    def __init__(self, obj):
        """
        Args:
            obj (class): An object of class
                :class:`~edafos.soil.profile.SoilProfile` class.

        """
        self.obj = obj

    # -- Matplotlib patch for a layer ----------------------------------------

    @staticmethod
    def soil_patch(axis, h_top, h_bot, soil_type, width=4):
        """

        Returns:

        """
        if soil_type == 'cohesive':
            soil_color = '#F4D77E'
        elif soil_type == 'cohesionless':
            soil_color = '#EC9777'
        else:
            soil_color = 'white'

        return axis.fill([0, 0, width, width],
                         [h_top, h_bot, h_bot, h_top],
                         facecolor=soil_color,
                         edgecolor='black',
                         # ls='solid',
                         lw=0.75,
                         # fill=False,
                         # hatch='*',
                         # alpha=0.5,
                         zorder=-1
                         )

    # -- Construct figure from parts -----------------------------------------

    def construct(self):
        """

        Returns:
            A plot

        """
        fig = plt.figure(dpi=150)
        ax1 = fig.add_subplot(111)

        # Get soil layer depths
        depths = self.obj.layers['Depth'].values
        # Add zero at the beginning of the array
        depths = np.insert(depths, 0, 0)
        # Get soil type
        soil_type = self.obj.layers['Soil Type']
        # Loop through layer depth array and add fills to the axis
        for h_top, h_bot, s_t in zip(depths[:-1], depths[1:], soil_type):
            self.soil_patch(ax1, h_top, h_bot, s_t)

        # Add a pile for now
        ax1.fill([1.75, 2, 2, 1.75],
                 [-5, -5, 70, 70],
                 facecolor='gray',
                 edgecolor='black',
                 )

        ax1.invert_yaxis()
        # ax1.set_ylim(ymax=0)
        ax1.set_xlim(xmin=0)

        ax1.yaxis.set_minor_locator(AutoMinorLocator())

        if self.obj.unit_system == 'S.I.':
            y_units = '(m)'
        else:
            y_units = '(ft)'

        ax1.set_ylabel('Depth ' + y_units, weight='bold')

        print(self.obj.layers['Depth'])

        return plt.show()
