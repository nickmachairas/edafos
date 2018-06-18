.. _pile-capacity:

##########################
Pile Capacity Calculations
##########################

The following examples detail the steps required to run pile capacity
calculations in ``edafos``.


*************
Piles in Sand
*************

Consider the example in :numref:`ex_capacity_sand`.


.. _ex_capacity_sand:
.. figure:: ../_static/figures/ex_capacity_sand.png
   :alt: ex_capacity_sand.png
   :align: center
   :width: 400px

   Closed-ended steel pipe pile in sand.


The calculated capacity, :math:`R_n`, (aka *nominal resistance*) is the sum of
the frictional (aka *shaft*) resistance, :math:`R_s`, and the end-bearing
(aka *toe*) resistance, :math:`R_p`, of the pile. Hence,

.. math::

   R_n = R_s + R_p


.. rubric:: Project setup

In ``edafos``, this example is set up as follows:

.. code-block:: python

   # Import the Project, SoilProfile and Pile classes
   from edafos.project import Project
   from edafos.soil import SoilProfile
   from edafos.deepfoundations import Pile

   # Create the project object
   project = Project(unit_system='English', project_name='Example 1')

   # Create a SoilProfile object with initial parameters
   profile = SoilProfile(unit_system='English', water_table=10)

   # Add layer properties
   profile.add_layer(soil_type='cohesionless',
                     height=40,
                     tuw=100,
                     field_phi=35,
                     corr_n=20)

   # Attach the soil profile to the project
   project.attach_sp(profile)

   # Create a pile
   pile = Pile(unit_system='English',
               pile_type='pipe-closed',
               length=32,
               pen_depth=30,
               diameter=14,
               thickness=0.75)

   # Attach the pile to the project
   project.attach_pile(pile)

   # Why not get the effective stress at say 15-ft??...
   project.sp.calculate_stress(15)

|

And this is the output:

.. ipython:: python

   # Import the Project, SoilProfile and Pile classes
   from edafos.project import Project
   from edafos.soil import SoilProfile
   from edafos.deepfoundations import Pile

   # Create the project object
   project = Project(unit_system='English', project_name='Example 1')

   # Create a SoilProfile object with initial parameters
   profile = SoilProfile(unit_system='English', water_table=10)

   # Add layer properties
   profile.add_layer(soil_type='cohesionless',
                     height=40,
                     tuw=100,
                     field_phi=35,
                     corr_n=20)

   # Attach the soil profile to the project
   project.attach_sp(profile)

   # Create a pile
   pile = Pile(unit_system='English',
               pile_type='pipe-closed',
               length=32,
               pen_depth=30,
               diameter=14,
               thickness=0.75)

   # Attach the pile to the project
   project.attach_pile(pile)

   # Why not get the effective stress at say 15-ft??...
   project.sp.calculate_stress(15)

   print(project)
