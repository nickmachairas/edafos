.. _capacity-methods:

########################
Capacity of Single Piles
########################

``edafos`` implements the pile capacity methods presented below.


.. _api-method:

**********
API Method
**********

American Petroleum Institute (API).


.. admonition:: Required Properties

   :Pile:

      - :math:`\alpha` or :math:`d`: side length or diameter for surface
        area, :math:`A_s` (shaft resistance)
      - :math:`\alpha` or :math:`d` (:math:`t`): side
        length or diameter (with thickness for open ended) for toe area,
        :math:`A_p, A_{pp}` (toe resistance)
      - pile type: open-ended or closed-ended for :math:`K` selection
        (cohesionless soils)

   :Soil:

      - type: cohesive/cohesionless classification
      - :math:`\gamma`: total unit weight for effective stress calculations
      - :math:`s_u`: undrained shear strength (cohesive soils)
      - :math:`N_{cor}`: SPT-N corrected to select :math:`\delta`,
        :math:`f_{s.lim}`, :math:`N_q`, :math:`q_{s.lim}` (cohesionless soils)

   **Note**: ``edafos`` runs a pre-check to verify that all required properties
   have been defined prior to running the capacity calculations. Refer to the
   :meth:`~edafos.deepfoundations.capacity_base.CapacityMethod._pre_check`
   method for more information.



Cohesive Soils
==============

The revised API method was included in RP-2A (1993) and has been widely used
in the offshore industry.


Shaft Resistance
----------------

The general equation for shaft resistance is given by:

.. math:: R_s = \sum{f_s A_s}
   :label: R_s-api

where:

- :math:`f_s`: unit shaft resistance (adhesion)
- :math:`A_s`: side surface area of pile

and,

.. math:: f_s = \alpha s_u
   :label: f_s-api-clay

where:

- :math:`\alpha`: coefficient as per revised API (1987)
- :math:`s_u`: undrained shear strength of soil


The :math:`\alpha` factor is calculated based on the conditional in equation
:eq:`a-rev-api-clay`.


.. math::
   :label: a-rev-api-clay

   \alpha = \begin{cases}
   0.5\psi^{-0.5} & \textrm{if} \quad \psi \leq 1.0 \\
   0.5\psi^{-0.25} & \textrm{if} \quad \psi > 1.0
   \end{cases} \quad \leq 1.0

where:

- :math:`\psi`: :math:`s_u/\bar{\sigma'}` at a depth, :math:`z`
- :math:`\bar{\sigma'}`: average effective stress (at midpoint)
- :math:`s_u`: undrained shear strength of soil



Toe Resistance
--------------

The toe resistance is equal to:

.. math:: R_p = q_p A_p
   :label: R_p-api

where:

- :math:`q_p`: unit toe resistance
- :math:`A_p`: pile toe cross-sectional area


**Important:** Toe resistance must always be checked against
:math:`R_p = q_p A_{pp}` where :math:`A_{pp}` is the cross sectional area of
soil plug in open end pipe or H-piles at pile toe.

The unit toe resistance, :math:`q_p`, is given by:

.. math:: q_p = 9 s_u
   :label: q_p-api-clay

where:

- :math:`s_u`: Undrained shear strength at the tip of the pile, usually taken as
  the **average over a distance of two diameters** below the tip of the pile.

|

Cohesionless Soils
==================

Following API RP2A (1987) recommendations.


Shaft Resistance
----------------

Shaft resistance is given by the general form in equation :eq:`R_s-api`. Unit
shaft resistance for piles in cohesionless soils is calculated by:

.. math:: f_s = K \sigma' \tan{\delta}
   :label: f_s-api-sand

where:

- :math:`K`: coefficient of lateral earth (ratio of horizontal to vertical
  normal effective stress)
- :math:`\bar{\sigma'}`: average effective stress (at midpoint)
- :math:`\delta`: friction angle between the soil and the pile wall


:numref:`API_K_table` offers recommended values for the coefficient of lateral
earth, :math:`K`.

.. _API_K_table:
.. table:: Values for coefficient of lateral earth, :math:`K`

   +------------------------------------------------+-----+
   | Condition                                      | K   |
   +================================================+=====+
   | unplugged, open-ended pipe piles (tens & comp) | 0.8 |
   +------------------------------------------------+-----+
   | full-displacement piles                        | 1.0 |
   +------------------------------------------------+-----+


:numref:`API_d_table` offers guidelines for :math:`\delta`, the friction angle
between the soil and the pile wall as well as limiting, :math:`f_s`.

.. _API_d_table:
.. table:: Guidelines for Side Friction in Siliceous Soil

   +----------------------------------------+----------------+-----------------------+
   | Soil                                   | :math:`\delta` | Limiting, :math:`f_s` |
   +                                        + , degrees      +-----------------------+
   |                                        |                | kips/ft2 | kPa        |
   +========================================+================+==========+============+
   | Very loose to medium, sand to silt     | 15             | 1.0      | 47.8       |
   +----------------------------------------+----------------+----------+------------+
   | Loose to dense, sand to silt           | 20             | 1.4      | 67.0       |
   +----------------------------------------+----------------+----------+------------+
   | Medium to dense, sand to sand-silt     | 25             | 1.7      | 81.4       |
   +----------------------------------------+----------------+----------+------------+
   | Dense to very dense, sand to sand-silt | 30             | 2.0      | 95.8       |
   +----------------------------------------+----------------+----------+------------+
   | Dense to very dense, gravel to sand    | 35             | 2.4      | 114.9      |
   +----------------------------------------+----------------+----------+------------+


Toe Resistance
--------------

Toe resistance is given by the general form in equation :eq:`R_p-api`. Unit
toe resistance for piles in cohesionless soils is calculated by:

.. math:: q_p = \sigma' N_q
   :label: q_p-api-sand

where:

- :math:`\sigma'`: effective stress at pile tip (not average)
- :math:`N_q`: bearing capacity factor


:numref:`API_q_table` offers guidelines for :math:`N_q`, bearing capacity factor
as well as limiting, :math:`q_p`.


.. _API_q_table:
.. table:: Guidelines for Toe Resistance in Siliceous Soil

   +----------------------------------------+-------------+--------------------------+
   | Soil                                   | :math:`N_q` | Limiting, :math:`q_p`    |
   +                                        +             +--------------------------+
   |                                        |             | kips/ft\ :sup:`2` | MPa  |
   +========================================+=============+===================+======+
   | Very loose to medium, sand to silt     | 8           | 40                | 1.9  |
   +----------------------------------------+-------------+-------------------+------+
   | Loose to dense, sand to silt           | 12          | 60                | 2.9  |
   +----------------------------------------+-------------+-------------------+------+
   | Medium to dense, sand to sand-silt     | 20          | 100               | 4.8  |
   +----------------------------------------+-------------+-------------------+------+
   | Dense to very dense, sand to sand-silt | 40          | 200               | 9.6  |
   +----------------------------------------+-------------+-------------------+------+
   | Dense to very dense, gravel to sand    | 50          | 250               | 12.0 |
   +----------------------------------------+-------------+-------------------+------+


In order to interpret :numref:`API_d_table` and :numref:`API_q_table`
algorithmically, the correlation in :numref:`API_SPT_corr_table` is employed
in ``edafos``.


.. _API_SPT_corr_table:
.. table:: SPT-N corrected Correlations

   +--------------+-----------------------+--------------------+
   | Density      | :math:`N_{cor}` (bpf) | :math:`\phi` (deg) |
   +==============+=======================+====================+
   | Very loose   | 0 - 4                 | < 28               |
   +--------------+-----------------------+--------------------+
   | Loose        | 5 - 10                | 28 - 30            |
   +--------------+-----------------------+--------------------+
   | Medium dense | 11 - 30               | 30 - 36            |
   +--------------+-----------------------+--------------------+
   | Dense        | 31 - 50               | 36 - 41            |
   +--------------+-----------------------+--------------------+
   | Very Dense   | over 50               | > 41               |
   +--------------+-----------------------+--------------------+


In which case :numref:`API_d_table`, :numref:`API_q_table` and
:numref:`API_SPT_corr_table` can be consolidated as in
:numref:`API_d_q_SPT_table`.


.. _API_d_q_SPT_table:
.. table:: Guidelines for Shaft and Toe Resistance in Siliceous Soil with
   SPT-N values

   +----------------------------------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Soil                                   | :math:`N_{cor}` (bpf) | :math:`\delta` (deg) | :math:`f_{s.lim}` (ksf) | :math:`N_q` | :math:`q_{p.lim}` (ksf) |
   +========================================+=======================+======================+=========================+=============+=========================+
   | Very loose to medium, sand to silt     | 0 - 4                 | 15                   | 1.0                     | 8           | 40                      |
   +----------------------------------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Loose to dense, sand to silt           | 5 - 10                | 20                   | 1.4                     | 12          | 60                      |
   +----------------------------------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Medium to dense, sand to sand-silt     | 11 - 30               | 25                   | 1.7                     | 20          | 100                     |
   +----------------------------------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Dense to very dense, sand to sand-silt | 31 - 50               | 30                   | 2.0                     | 40          | 200                     |
   +----------------------------------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Dense to very dense, gravel to sand    | over 50               | 35                   | 2.4                     | 50          | 250                     |
   +----------------------------------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+



|


.. _olson90-method:

***************
Olson 90 Method
***************

The Olson 90 method is for cohesionless soils only. It was created from a
database of 31 load tests on steel pipe piles.


.. admonition:: Required Properties

   :Pile:

      - :math:`\alpha` or :math:`d`: side length or diameter for surface
        area, :math:`A_s` (shaft resistance)
      - :math:`\alpha` or :math:`d` (:math:`t`): side
        length or diameter (with thickness for open ended) for toe area,
        :math:`A_p, A_{pp}` (toe resistance)
      - pile type: open-ended or closed-ended for :math:`K` selection
        (cohesionless soils)

   :Soil:

      - type: cohesive/cohesionless classification
      - :math:`\gamma`: total unit weight for effective stress calculations
      - :math:`s_u`: undrained shear strength (cohesive soils)
      - desc, :math:`N_{cor}`: soil description and SPT-N corrected to select
        :math:`\delta`, :math:`f_{s.lim}`, :math:`N_q`, :math:`q_{s.lim}`
        (cohesionless soils)

   **Note**: ``edafos`` runs a pre-check to verify that all required properties
   have been defined prior to running the capacity calculations. Refer to the
   :meth:`~edafos.deepfoundations.capacity_base.CapacityMethod._pre_check`
   method for more information.



Cohesionless Soils
==================

Olson 90 is similar to the Revised API method with two main differences. First,
the coefficient of lateral earth, :math:`K`, is calculated rather than taken
from :numref:`API_K_table`. In Olson 90, :math:`K` is:

.. math::
   :label: olson90-K

   K = \begin{cases}
   0.16 + 0.015 \, N_{cor} & \textrm{non-displacement piles}\\
   0.70 + 0.015 \, N_{cor} & \textrm{full displacement piles}
   \end{cases}

where:

- :math:`N_{cor}`: SPT-N values corrected for overburden pressure


Next, Olson 90 provides revised guidelines for shaft and tow resistances which
are offered in :numref:`Olson90_table`.


.. _Olson90_table:
.. table:: Olson 90 guidelines for Shaft and Toe Resistance

   +---------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Soil          | :math:`N_{cor}` (bpf) | :math:`\delta` (deg) | :math:`f_{s.lim}` (ksf) | :math:`N_q` | :math:`q_{p.lim}` (ksf) |
   +===============+=======================+======================+=========================+=============+=========================+
   | Gravel        | 0 - 4                 | [20]                 | [1.4]                   | [12]        | [60]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 5 - 10                | [25]                 | [1.7]                   | [20]        | [100]                   |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 11 - 30               | [30]                 | [2.0]                   | [40]        | [200]                   |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | over 30               | [35]                 | [2.4]                   | [60]        | [250]                   |
   +---------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Sand / Gravel | 0 - 4                 | [20]                 | [1.4]                   | [12]        | [60]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 5 - 10                | [25]                 | [1.7]                   | [20]        | [100]                   |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 11 - 30               | [30]                 | [2.0]                   | [40]        | [200]                   |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | over 30               | [35]                 | [2.4]                   | [60]        | [250]                   |
   +---------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Sand          | 0 - 4                 | [20]                 | [1.0]                   | [50]        | [40]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 5 - 10                | 30                   | 1.1                     | 120         | 120                     |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 11 - 30               | 35                   | 1.9                     | 120         | 190                     |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 31 - 50               | 40                   | 2.6                     | 120         | 190                     |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 51 - 100              | 40                   | 3.7                     | 130         | 200                     |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | over 100              | 40                   | 3.8                     | 220         | 530                     |
   +---------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Sand / Silt   | 0 - 4                 | 10                   | [1.0]                   | [10]        | [10]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 5 - 10                | 10                   | [1.0]                   | [20]        | [40]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 11 - 30               | 15                   | [1.4]                   | 50          | 110                     |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 31 - 50               | 20                   | 2.0                     | 100         | 160                     |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 51 - 100              | [30]                 | [2.0]                   | [100]       | [200]                   |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 101 - 200             | [34]                 | [20]                    | [100]       | [200]                   |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | over 200              | 40                   | 20                      | [100]       | [200]                   |
   +---------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+
   | Silt          | 0 - 4                 | [10]                 | [1.0]                   | [10]        | [40]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 5 - 10                | 15                   | [1.0]                   | [10]        | [40]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 11 - 30               | 20                   | [1.4]                   | [10]        | [40]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | 31 - 50               | 20                   | [1.4]                   | [12]        | [60]                    |
   +               +-----------------------+----------------------+-------------------------+-------------+-------------------------+
   |               | over 50               | [25]                 | [1.4]                   | [12]        | [60]                    |
   +---------------+-----------------------+----------------------+-------------------------+-------------+-------------------------+


**Note:**

- Must not interpolate. In using values in :numref:`Olson90_table`, use the
  line corresponding to N = 4 for any layer with N less than or equal to 4,
  the line corresponding to 10 for N = 5 - 10, and so on.
- Number in brackets were extrapolated, no supporting data.

