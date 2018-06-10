.. _soil-stresses:

#############
Soil Stresses
#############


Calculation of soil stresses (total, porewater, effective) are implemented in
the :meth:`~edafos.soil.profile.SoilProfile.calculate_stress` method. This
section outlines the approach in creating a method that covers most cases
(multiple layers, varying water table) and allows to calculate stresses at any
vertical depth of interest, :math:`z`.

For more on soil stresses refer to the excellent book by `Reese et al. (2006)`_.

.. _Reese et al. (2006): https://www.wiley.com/en-us/Analysis+and+Design+of+Shallow+and+Deep+Foundations-p-9780471431596


.. note::

   For all cases presented below, positive (+) is upwards and reference (0)
   is at ground level.



.. rubric:: Case A - single layer, stresses above and below water table

Consider the soil profile in :numref:`soilstresses_caseA`. A 16-ft sand layer
with total unit weight of 90 lbf/ft\ :sup:`3` and the water table at a depth
of 10-ft. Point A is at depth, :math:`z`, of 6-ft and point B is at a depth,
:math:`z`, of 14-ft below ground level.


.. _soilstresses_caseA:
.. figure:: ../_static/figures/soilstresses_caseA.png
   :alt: soilstresses_caseA.png
   :align: center
   :width: 300 px

   Single layer, stresses above and below water table.


The first takeaway comes with the introduction of the term :math:`z_w`, the
vertical distance below the water table.


.. admonition:: Takeaway No 1

   .. math::

      z_w = z - WT

   Always calculate :math:`z_w` and if negative, set :math:`z_w=0`. Hence:

   .. math::

      z_w = \begin{cases}
      0 & \textrm{if} \quad z_w < 0 \\
      z - WT & \textrm{otherwise}
      \end{cases}


**Total stress** at point A:

.. math::

   \sigma_A = \gamma z_A = (90 \textrm{ pcf})(6 \textrm{ ft}) = 540 \textrm{ psf}



**Pore water pressure** at point A:

.. math::

   z_w = z_A - WT = 6 - 10 = -4 \textrm{ ft} = 0

.. math::

   u_A = z_w \, \gamma_w = 0 \textrm{ psf}



**Effective stress** at point A:

.. math::

   \sigma'_A = \sigma_A - u_A = 540 - 0 = 540 \textrm{ psf}



**Total stress** at point B:

.. math::

   \sigma_B = \gamma z_B = (90 \textrm{ pcf})(14 \textrm{ ft}) = 1260 \textrm{ psf}



**Pore water pressure** at point B:

.. math::

   z_w = z_B - WT = 14 - 10 = 4 \textrm{ ft}

.. math::

   u_A = z_w \, \gamma_w = (62.4 \textrm{ pcf})(4 \textrm{ ft}) = 249.6 \textrm{ psf}



**Effective stress** at point B:

.. math::

   \sigma'_B = \sigma_B - u_B = 1260 - 249.6 = 1010.4 \textrm{ psf}

|

The same example can be implemented in ``edafos`` as follows.

.. ipython:: python

   # Import the `SoilProfile` class
   from edafos.soil import SoilProfile

   # Create a SoilProfile object with initial parameters
   caseA = SoilProfile(unit_system='English', water_table=10)

   # Add layer properties
   caseA.add_layer(soil_type='cohesionless', height=16, tuw=90)

   # Stresses at point A
   total, pore, effective = caseA.calculate_stress(6, kind='all')
   print("Total Stress: {:0.3f}\nPore Water Pressure: {:0.3f}\n"
         "Effective Stress: {:0.3f}".format(total, pore, effective))

   # Stresses at point B
   total, pore, effective = caseA.calculate_stress(14, kind='all')
   print("Total Stress: {:0.3f}\nPore Water Pressure: {:0.3f}\n"
         "Effective Stress: {:0.3f}".format(total, pore, effective))

|

You can also create a stress distribution plot:

.. plot::

   import numpy as np
   import matplotlib.pyplot as plt
   from edafos.soil import SoilProfile

   caseA = SoilProfile(unit_system='English', water_table=10)
   caseA.add_layer(soil_type='cohesionless', height=16, tuw=90)

   z = np.arange(0,17,1)
   t = []; p = []; s = [];
   for i in z:
      total, pore, eff = caseA.calculate_stress(i, kind='all')
      t.append(total.magnitude)
      p.append(pore.magnitude)
      s.append(eff.magnitude)
   plt.plot(p, z, label="Pore Water Pressure")
   plt.plot(t, z, label="Total Stress")
   plt.plot(s, z, label="Effective Stress")
   plt.title("Stress Distribution for Case A")
   plt.xlabel("(kip/ft2)")
   plt.ylabel("Depth (ft)")
   plt.gca().invert_yaxis()
   plt.grid()
   plt.legend()
   plt.show()


----

.. rubric:: Case B - two layers, stresses above and below water table

Consider the soil profile in :numref:`soilstresses_caseB`. A 5-ft sand layer
with total unit weight of 90 lbf/ft\ :sup:`3`, an 11-ft clay layer with total
unit weight of 110 lbf/ft\ :sup:`3` and the water table at a depth of 10-ft.
Point A is at depth, :math:`z`, of 6-ft and point B is at a depth, :math:`z`,
of 14-ft below ground level.


.. _soilstresses_caseB:
.. figure:: ../_static/figures/soilstresses_caseB.png
   :alt: soilstresses_caseB.png
   :align: center
   :width: 300 px

   Two layers, stresses above and below water table.



.. admonition:: Takeaway No 2

   Total stress in terms of :math:`z`:

   .. math::

      \sigma(z) =
      \begin{cases}
      z \, \gamma_1 & \textrm{if} \quad z < H_1 \\
      \sum\limits_{i=1}^n {H_i \, \gamma_i} &
         \textrm{if} \quad z = \sum\limits_{i=1}^n {H_i} \\
      \sum\limits_{i=1}^{n-1} {H_i \, \gamma_i} +
         \Big(z-\sum\limits_{i=1}^{n-1} {H_i}\Big) \, \gamma_n &
         \textrm{if} \quad \sum\limits_{i=1}^{n-1} {H_i} < z <
         \sum\limits_{i=1}^n {H_i}
      \end{cases}



**Total stress** at point A:

.. math::

   \sigma_A = H_1 \, \gamma_1 + (z_A-H_1) \, \gamma_2
      = (5 \textrm{ ft})(90 \textrm{ pcf})
      + (6-5 \textrm{ ft})(110 \textrm{ pcf})
      = 560 \textrm{ psf}


**Pore water pressure** at point A:

.. math::

   z_w = z_A - WT = 6 - 10 = -4 \textrm{ ft} = 0

.. math::

   u_A = z_w \, \gamma_w = 0 \textrm{ psf}


**Effective stress** at point A:

.. math::

   \sigma'_A = \sigma_A - u_A = 560 - 0 = 560 \textrm{ psf}


**Total stress** at point B:

.. math::

   \sigma_B = H_1 \, \gamma_1 + (z_B-H_1) \, \gamma_2
      = (5 \textrm{ ft})(90 \textrm{ pcf})
      + (14-5 \textrm{ ft})(110 \textrm{ pcf})
      = 1440 \textrm{ psf}


**Pore water pressure** at point B:

.. math::

   z_w = z_B - WT = 14 - 10 = 4 \textrm{ ft}

.. math::

   u_A = z_w \, \gamma_w = (62.4 \textrm{ pcf})(4 \textrm{ ft}) = 249.6 \textrm{ psf}



**Effective stress** at point B:

.. math::

   \sigma'_B = \sigma_B - u_B = 1440 - 249.6 = 1190.4 \textrm{ psf}


|

Case B can be implemented in ``edafos`` as follows.

.. ipython:: python

   # Import the `SoilProfile` class
   from edafos.soil import SoilProfile

   # Create a SoilProfile object with initial parameters
   caseB = SoilProfile(unit_system='English', water_table=10)

   # Add layer properties
   caseB.add_layer(soil_type='cohesionless', height=5, tuw=90)
   caseB.add_layer(soil_type='cohesive', height=11, tuw=110)

   # Stresses at point A
   total, pore, effective = caseB.calculate_stress(6, kind='all')
   print("Total Stress: {:0.3f}\nPore Water Pressure: {:0.3f}\n"
         "Effective Stress: {:0.3f}".format(total, pore, effective))

   # Stresses at point B
   total, pore, effective = caseB.calculate_stress(14, kind='all')
   print("Total Stress: {:0.3f}\nPore Water Pressure: {:0.3f}\n"
         "Effective Stress: {:0.3f}".format(total, pore, effective))


|

You can also create a stress distribution plot:

.. plot::

   import numpy as np
   import matplotlib.pyplot as plt
   from edafos.soil import SoilProfile

   caseB = SoilProfile(unit_system='English', water_table=10)
   caseB.add_layer(soil_type='cohesionless', height=5, tuw=90)
   caseB.add_layer(soil_type='cohesive', height=11, tuw=110)

   z = np.arange(0,17,1)
   t = []; p = []; s = [];
   for i in z:
      total, pore, eff = caseB.calculate_stress(i, kind='all')
      t.append(total.magnitude)
      p.append(pore.magnitude)
      s.append(eff.magnitude)
   plt.plot(p, z, label="Pore Water Pressure")
   plt.plot(t, z, label="Total Stress")
   plt.plot(s, z, label="Effective Stress")
   plt.title("Stress Distribution for Case B")
   plt.xlabel("(kip/ft2)")
   plt.ylabel("Depth (ft)")
   plt.gca().invert_yaxis()
   plt.grid()
   plt.legend()
   plt.show()


----

.. rubric:: Case C - two layers, under water

Consider the soil profile in :numref:`soilstresses_caseC`. A 4.5-ft sand layer
with total unit weight of 90 lbf/ft\ :sup:`3` and a 4.5-ft clay layer with total
unit weight of 110 lbf/ft\ :sup:`3` are under 7-ft of water. Point A is 3-ft
above soil grade and point B is at a depth, :math:`z`, of 7-ft below soil grade.


.. _soilstresses_caseC:
.. figure:: ../_static/figures/soilstresses_caseC.png
   :alt: soilstresses_caseC.png
   :align: center
   :width: 300 px

   Two layers, under water.



**Total stress** at point A:

.. math::

   z_w = z_A - WT = -3 - (-7) = 4 \textrm{ ft}

.. math::

   \sigma_A = z_w \, \gamma_w = (4 \textrm{ ft})(62.4 \textrm{ pcf})
      = 249.6 \textrm{ psf}


**Pore water pressure** at point A:

.. math::

   u_A = z_w \, \gamma_w = (4 \textrm{ ft})(62.4 \textrm{ pcf})
      = 249.6 \textrm{ psf}

**Effective stress** at point A:

.. math::

   \sigma'_A = \sigma_A - u_A = 249.6 - 249.6 = 0 \textrm{ psf}

|

.. admonition:: Takeaway No 3

   If :math:`z<0` and :math:`WT<0`, then:

   .. math::

      \sigma = u = z_w \, \gamma_w

|

**Total stress** at point B:

.. math::

   \sigma_B = | WT | \, \gamma_w + H_1 \, \gamma_1 + (z_B-H_1) \, \gamma_2
      = (7 \textrm{ ft})(62.4 \textrm{ pcf})
      + (4.5 \textrm{ ft})(90 \textrm{ pcf})
      + (7-4.5 \textrm{ ft})(110 \textrm{ pcf})
      = 1116.8 \textrm{ psf}


**Pore water pressure** at point B:

.. math::

   z_w = z_B - WT = 7 - (-7) = 14 \textrm{ ft}

.. math::

   u_B = z_w \, \gamma_w = (14 \textrm{ ft})(62.4 \textrm{ pcf})
      = 873.6 \textrm{ psf}


**Effective stress** at point B:

.. math::

   \sigma'_B = \sigma_B - u_B = 1116.8 - 873.6 = 243.2 \textrm{ psf}


|

.. admonition:: Takeaway No 4

   If :math:`z>0` and :math:`WT<0`, adjust the total stress equation to
   include above grade stresses due to water pressure.


|

Case C can be implemented in ``edafos`` as follows.

.. ipython:: python

   # Import the `SoilProfile` class
   from edafos.soil import SoilProfile

   # Create a SoilProfile object with initial parameters
   caseC = SoilProfile(unit_system='English', water_table=-7)

   # Add layer properties
   caseC.add_layer(soil_type='cohesionless', height=4.5, tuw=90)
   caseC.add_layer(soil_type='cohesive', height=4.5, tuw=110)

   # Stresses at point A
   total, pore, effective = caseC.calculate_stress(-3, kind='all')
   print("Total Stress: {:0.3f}\nPore Water Pressure: {:0.3f}\n"
         "Effective Stress: {:0.3f}".format(total, pore, effective))

   # Stresses at point B
   total, pore, effective = caseC.calculate_stress(7, kind='all')
   print("Total Stress: {:0.3f}\nPore Water Pressure: {:0.3f}\n"
         "Effective Stress: {:0.3f}".format(total, pore, effective))


|

You can also create a stress distribution plot:

.. plot::

   import numpy as np
   import matplotlib.pyplot as plt
   from edafos.soil import SoilProfile

   caseC = SoilProfile(unit_system='English', water_table=-7)
   caseC.add_layer(soil_type='cohesionless', height=4.5, tuw=90)
   caseC.add_layer(soil_type='cohesive', height=4.5, tuw=110)

   z = np.arange(-7,10,1)
   t = []; p = []; s = [];
   for i in z:
      total, pore, eff = caseC.calculate_stress(i, kind='all')
      t.append(total.magnitude)
      p.append(pore.magnitude)
      s.append(eff.magnitude)
   plt.plot(p, z, label="Pore Water Pressure")
   plt.plot(t, z, label="Total Stress")
   plt.plot(s, z, label="Effective Stress")
   plt.title("Stress Distribution for Case C")
   plt.xlabel("(kip/ft2)")
   plt.ylabel("Depth (ft)")
   plt.gca().invert_yaxis()
   plt.grid()
   plt.legend()
   plt.show()

