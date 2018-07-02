.. _correlations:

############
Correlations
############

.. _olson-correlations:

*****
Olson
*****

Most of the values of total unit weight (TUW, a.k.a. moist unit weight),
:math:`\gamma_t`, in Prof. Roy Olson's database were assumed. If water content,
:math:`w`, was known, it was used to calculate :math:`\gamma_t`, with an
assumed specific gravity, :math:`G_s`, of 2.72. The equation for :math:`\gamma_t`
in this case was:

.. math::

   \gamma_t = \bigg( \dfrac{1 + w}{1 + w G_s} \bigg) \; G_s \gamma_w


Prof. Olson
used cases in which water contents were measured to calculate total unit weights
for all soils and then performed correlations of those values of total unit
weight with whatever other properties were available, meaning undrained shear
strength, :math:`s_u`, for cohesive soils, and SPT-N values for all soils, and
used these other properties to estimate total unit weight for cases in which
water contents were not defined. These correlations were often bad but at least
they gave a consistent basis for estimating :math:`\gamma_t`. The correlations
are shown below for cohesive and cohesionless soils.


.. rubric:: Cohesive Soils

Values for undrained shear strength may come from the following:

- Field vane shearing strength (:math:`s_{u.FV}`)
- Shearing strength from Torvane, penetrometer, etc (:math:`s_{u.MS}`)
- Shearing strength from triaxial tests (:math:`s_{u.QT}`)
- Unconfined shearing strength (:math:`s_{u.QU}`)

Priority for choosing a value for :math:`s_u` if multiple are available is:

.. math:: s_{u.QT} > s_{u.QU} > s_{u.MS} > s_{u.FV}

But use as:

.. math::

   s_u =
   \begin{cases}
   s_{u.QT} \\
   1.2 \times s_{u.QU} \\
   1.2 \times s_{u.MS} \\
   0.7 \times s_{u.FV}
   \end{cases}


For clay (``CLAY``):

.. math::

   \gamma_t =
   \begin{cases}
   113.9 + 9.276 \ln{s_u} \textrm{ in pcf} & \textrm{if } s_u > 0 \textrm{ in ksf} \\
   107.5 + 5.116 \ln{N} \textrm{ in pcf} & \textrm{if } s_u \textrm{ undef. and } N > 0 \\
   \textrm{N/A} & \textrm{if both } s_u \textrm{ and } N \textrm{ are undefined}
   \end{cases}


For silt/clay (``SICL``), clay/silt (``CLSI``) and sand/clay (``SACL``):

.. math::

   \gamma_t =
   \begin{cases}
   113 + 22 s_u \textrm{ in pcf} & \textrm{if } 0.5 < s_u < 1.5 \textrm{ in ksf} \\
   113 + 9.276 \ln{N} \textrm{ in pcf} & \textrm{if } s_u > 0 \\
   \textrm{N/A} & \textrm{if both } s_u \textrm{ and } N \textrm{ are undefined}
   \end{cases}


.. rubric:: Cohesionless Soils

For sand (``SAND``):

.. math:: \gamma_t = 126 \textrm{ pcf}

For silt/sand (``SISA``), sand/silt (``SASI``) and silt (``SILT``):

.. math:: \gamma_t = 125 + 0.15 N \textrm{ pcf} < 135 \textrm{ pcf}

For cobble/gravel (``CBGV``), gravel (``GRAV``), sand/gravel (``SAGV``),
gravel/sand (``GVSA``) and cobbles (``COBB``):

.. math:: \gamma_t = 132 \textrm{ pcf}
