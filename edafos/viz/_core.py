""" Provide the `` ... `` class.

"""

# -- Imports -----------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.colors import to_rgba
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
    def soil_patch(axis, h_top, h_bot, soil_type, label, width=4):
        """

        Returns:

        """
        if soil_type == 'cohesive':
            soil_color = '#EC9777'
        elif soil_type == 'cohesionless':
            soil_color = '#F4D77E'
        elif soil_type == 'rock':
            soil_color = '#D6D6D6'
        else:
            soil_color = 'white'

        ax = axis.fill([0, 0, width, width],
                       [h_top, h_bot, h_bot, h_top],
                       facecolor=soil_color,
                       edgecolor='black',
                       # ls='solid',
                       lw=0.5,
                       # fill=False,
                       # hatch='*',
                       # alpha=0.5,
                       zorder=-1,
                       label=label
                       )
        return ax

    # -- Matplotlib patch for water ------------------------------------------

    @staticmethod
    def water_patch(axis, wt, lowest, width=4):
        """

        Returns:

        """
        ax = axis.fill([0, 0, width, width],
                       [wt.magnitude, lowest, lowest, wt.magnitude],
                       facecolor=to_rgba('LightSeaGreen', alpha=0.15),
                       edgecolor=to_rgba('LightSeaGreen', alpha=1.0),
                       lw=1.0,
                       ls='-.',
                       zorder=0,
                       label='GW @ {:.1f}'.format(wt)
                       )
        return ax

    # -- Matplotlib table for layers dataframe -------------------------------
    def layer_table(self, axis):
        """

        Args:
            axis:

        Returns:

        """
        df = self.obj.layers
        df = df.round(2)
        tbl = axis.table(cellText=df.values,
                         rowLabels=df.index,
                         colLabels=df.columns,
                         loc='bottom',
                         bbox=[0.0, -0.38, 1, 0.35],  # left, bot, width, height
                         )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(6)

        for key, cell in tbl.get_celld().items():
            cell.set_linewidth(0.25)

        return tbl

    # -- Matplotlib SPT-N plot -----------------------------------------------
    def spt_plot(self, axis, ax1_ymin, ax1_ymax):
        """

        Args:
            axis:

        Returns:

        """
        ax = axis.scatter(x=self.obj.spt_data['SPT-N'],
                          y=self.obj.spt_data['Depth'],
                          s=3,
                          c='k')

        axis.invert_yaxis()
        axis.set_ylim(ymin=ax1_ymin,
                      ymax=ax1_ymax)
        axis.xaxis.tick_top()
        axis.xaxis.set_label_position('top')
        axis.get_yaxis().set_visible(False)
        axis.set_xlabel('Field SPT-N', fontsize=9)
        axis.xaxis.set_tick_params(labelsize=8)

        return ax

    # -- Construct figure from parts -----------------------------------------

    def construct(self):
        """

        Returns:
            A plot

        """
        # Initialize figure and axes
        fig = plt.figure(figsize=(9, 7.5), dpi=150)
        # ax1 is for the layer plot
        ax1 = fig.add_subplot(111)
        # ax2 is for the SPT plot
        ax2 = fig.add_subplot(122)

        # Get soil layer depths
        depths = self.obj.layers['Depth'].values
        # Add zero at the beginning of the array
        depths = np.insert(depths, 0, 0)
        # Get soil type
        soil_type = self.obj.layers['Soil Type']
        # Loop through layer depth array and add fills to the axis
        s_type_list = []
        for h_top, h_bot, s_t in zip(depths[:-1], depths[1:], soil_type):
            self.soil_patch(axis=ax1,
                            h_top=h_top,
                            h_bot=h_bot,
                            soil_type=s_t,
                            label=s_t if s_t not in s_type_list
                            else '')
            self.soil_patch(axis=ax2,
                            h_top=h_top,
                            h_bot=h_bot,
                            soil_type=s_t,
                            label='',
                            width=20)

            if s_t not in s_type_list:
                s_type_list.append(s_t)

        # Add ground water
        self.water_patch(axis=ax1,
                         wt=self.obj.water_table,
                         lowest=depths.max())

        # Add a pile for now
        ax1.fill([1.75, 2, 2, 1.75],
                 [-5, -5, 70, 70],
                 facecolor='gray',
                 edgecolor='black',
                 )

        # Try to add a table
        self.layer_table(ax1)

        # Invert the y axis
        ax1.invert_yaxis()
        ax1.set_xlim(xmin=0, xmax=4.0)
        ax1.set_ylim(ymin=depths.max())

        # Hide x labels
        # ax1.set_xticklabels([])
        ax1.get_xaxis().set_visible(False)

        # Add minot ticks for depth
        ax1.yaxis.set_minor_locator(AutoMinorLocator())

        # Pick up correct units for depth label
        if self.obj.unit_system == 'S.I.':
            y_units = '(m)'
        else:
            y_units = '(ft)'

        # Set depth label
        ax1.set_ylabel('Depth ' + y_units, weight='bold')

        # Add a title
        ax1.set_title(self.obj.name, weight='bold', y=1.08)

        # Add the layer legend
        ax1.legend()

        plt.subplots_adjust(bottom=0.3)

        # -- SPT Plot
        # ax2.invert_yaxis()
        ax1_ymin, ax1_ymax = ax1.get_ylim()
        self.spt_plot(ax2, ax1_ymin, ax1_ymax)
        # ax2.set_ylim(ymin=ax1_ymin,
        #              ymax=ax1_ymax)
        # ax2.xaxis.tick_top()
        # ax2.xaxis.set_label_position('top')
        # ax2.get_yaxis().set_visible(False)
        # ax2.set_xlabel('Field SPT-N', fontsize=9)
        # ax2.xaxis.set_tick_params(labelsize=8)

        return plt.show()
