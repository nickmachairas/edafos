""" This file contains stored data.

"""

# -- H-Pile Dictionaries -----------------------------------------------------

english_hpiles = {
    'HP8X36': {
        'area': 10.6,
        'perimeter': 47.77,  # = 2*depth + 4*flange_width - 2*web_thickness
        'box_area': 65.40,  # = depth * flange_width
        'box_perimeter': 32.35,  # = 2*depth + 2*flange_width
        'depth': 8.02,  # d
        'web_thickness': 0.445,  # tw
        'flange_width': 8.155,  # bf
        'flange_thickness': 0.445,  # tf
    },
    'HP10X42': {
        'area': 12.4,
        'perimeter': 58.87,
        'box_area': 97.73,
        'box_perimeter': 39.55,
        'depth': 9.7,
        'web_thickness': 0.415,
        'flange_width': 10.075,
        'flange_thickness': 0.42,
    },
    'HP10X57': {
        'area': 16.8,
        'perimeter': 59.75,
        'box_area': 102.1,
        'box_perimeter': 40.43,
        'depth': 9.99,
        'web_thickness': 0.565,
        'flange_width': 10.225,
        'flange_thickness': 0.565,
    },
    'HP12X53': {
        'area': 15.5,
        'perimeter': 70.87,
        'box_area': 141.9,
        'box_perimeter': 47.65,
        'depth': 11.78,
        'web_thickness': 0.435,
        'flange_width': 12.045,
        'flange_thickness': 0.435,
    },
    'HP12X63': {
        'area': 18.4,
        'perimeter': 71.35,
        'box_area': 144.8,
        'box_perimeter': 48.13,
        'depth': 11.94,
        'web_thickness': 0.515,
        'flange_width': 12.125,
        'flange_thickness': 0.515,
    },
    'HP12X74': {
        'area': 21.8,
        'perimeter': 71.91,
        'box_area': 148.2,
        'box_perimeter': 48.69,
        'depth': 12.13,
        'web_thickness': 0.605,
        'flange_width': 12.215,
        'flange_thickness': 0.61,
    },
    'HP12X84': {
        'area': 24.6,
        'perimeter': 72.37,
        'box_area': 151,
        'box_perimeter': 49.15,
        'depth': 12.28,
        'web_thickness': 0.685,
        'flange_width': 12.295,
        'flange_thickness': 0.685,
    },
    'HP14X73': {
        'area': 21.4,
        'perimeter': 84.55,
        'box_area': 198.5,
        'box_perimeter': 56.39,
        'depth': 13.61,
        'web_thickness': 0.505,
        'flange_width': 14.585,
        'flange_thickness': 0.505,
    },
    'HP14X89': {
        'area': 26.1,
        'perimeter': 85.21,
        'box_area': 203.2,
        'box_perimeter': 57.05,
        'depth': 13.83,
        'web_thickness': 0.615,
        'flange_width': 14.695,
        'flange_thickness': 0.615,
    },
    'HP14X102': {
        'area': 30,
        'perimeter': 85.75,
        'box_area': 207.1,
        'box_perimeter': 57.59,
        'depth': 14.01,
        'web_thickness': 0.705,
        'flange_width': 14.785,
        'flange_thickness': 0.705,
    },
    'HP14X117': {
        'area': 34.4,
        'perimeter': 86.35,
        'box_area': 211.5,
        'box_perimeter': 58.19,
        'depth': 14.21,
        'web_thickness': 0.805,
        'flange_width': 14.885,
        'flange_thickness': 0.805,
    },
}

si_hpiles = {
    # TODO: Add SI H-Pile details
}

# -- API Guidelines for Shaft and Toe Resistance -----------------------------

api_data = {
    'very_loose': {
        'Ncor': '0 - 4',  # bpf
        'delta': 15,      # deg
        'f_lim': 1.0,     # ksf
        'N_q': 8,
        'q_lim': 40,      # ksf
    },
    'loose': {
        'Ncor': '5 - 10',
        'delta': 20,
        'f_lim': 1.4,
        'N_q': 12,
        'q_lim': 60,
    },
    'medium': {
        'Ncor': '11 - 30',
        'delta': 25,
        'f_lim': 1.7,
        'N_q': 20,
        'q_lim': 100,
    },
    'dense': {
        'Ncor': '31 - 50',
        'delta': 30,
        'f_lim': 2.0,
        'N_q': 40,
        'q_lim': 200,
    },
    'very_dense': {
        'Ncor': 'over 50',
        'delta': 35,
        'f_lim': 2.4,
        'N_q': 50,
        'q_lim': 250,
    },
}

# -- Olson 90 Guidelines for Shaft and Toe Resistance ------------------------

olson90_data = {
    'gravel': {
        'very_loose': {
            'Ncor': '0 - 4',
            'delta': 20,
            'f_lim': 1.4,
            'N_q': 12,
            'q_lim': 60,
        },
        'loose': {
            'Ncor': '5 - 10',
            'delta': 25,
            'f_lim': 1.7,
            'N_q': 20,
            'q_lim': 100,
        },
        'medium': {
            'Ncor': '11 - 30',
            'delta': 30,
            'f_lim': 2.0,
            'N_q': 40,
            'q_lim': 200,
        },
        'dense': {
            'Ncor': 'over 30',
            'delta': 35,
            'f_lim': 2.4,
            'N_q': 60,
            'q_lim': 250,
        },
    },
    'sand-gravel': {
        'very_loose': {
            'Ncor': '0 - 4',
            'delta': 20,
            'f_lim': 1.4,
            'N_q': 12,
            'q_lim': 60,
        },
        'loose': {
            'Ncor': '5 - 10',
            'delta': 25,
            'f_lim': 1.7,
            'N_q': 20,
            'q_lim': 100,
        },
        'medium': {
            'Ncor': '11 - 30',
            'delta': 30,
            'f_lim': 2.0,
            'N_q': 40,
            'q_lim': 200,
        },
        'dense': {
            'Ncor': 'over 30',
            'delta': 35,
            'f_lim': 2.4,
            'N_q': 60,
            'q_lim': 250,
        },
    },
    'sand': {
        'very_loose': {
            'Ncor': '0 - 4',
            'delta': 20,
            'f_lim': 1.0,
            'N_q': 50,
            'q_lim': 40,
        },
        'loose': {
            'Ncor': '5 - 10',
            'delta': 30,
            'f_lim': 1.1,
            'N_q': 120,
            'q_lim': 120,
        },
        'medium': {
            'Ncor': '11 - 30',
            'delta': 35,
            'f_lim': 1.9,
            'N_q': 120,
            'q_lim': 190,
        },
        'dense': {
            'Ncor': '31 - 50',
            'delta': 40,
            'f_lim': 2.6,
            'N_q': 120,
            'q_lim': 190,
        },
        'very_dense': {
            'Ncor': '51 - 100',
            'delta': 40,
            'f_lim': 3.7,
            'N_q': 130,
            'q_lim': 200,
        },
        'very_dense+': {
            'Ncor': 'over 100',
            'delta': 40,
            'f_lim': 3.8,
            'N_q': 220,
            'q_lim': 530,
        },
    },
    'sand-silt': {
        'very_loose': {
            'Ncor': '0 - 4',
            'delta': 10,
            'f_lim': 1.0,
            'N_q': 10,
            'q_lim': 10,
        },
        'loose': {
            'Ncor': '5 - 10',
            'delta': 10,
            'f_lim': 1.0,
            'N_q': 20,
            'q_lim': 40,
        },
        'medium': {
            'Ncor': '11 - 30',
            'delta': 15,
            'f_lim': 1.4,
            'N_q': 50,
            'q_lim': 110,
        },
        'dense': {
            'Ncor': '31 - 50',
            'delta': 20,
            'f_lim': 2.0,
            'N_q': 100,
            'q_lim': 160,
        },
        'very_dense': {
            'Ncor': '51 - 100',
            'delta': 30,
            'f_lim': 2.0,
            'N_q': 100,
            'q_lim': 200,
        },
        'very_dense+': {
            'Ncor': '101 - 200',
            'delta': 34,
            'f_lim': 20,
            'N_q': 100,
            'q_lim': 200,
        },
        'very_dense++': {
            'Ncor': 'over 200',
            'delta': 40,
            'f_lim': 20,
            'N_q': 100,
            'q_lim': 200,
        },
    },
    'silt': {
        'very_loose': {
            'Ncor': '0 - 4',
            'delta': 10,
            'f_lim': 1.0,
            'N_q': 10,
            'q_lim': 40,
        },
        'loose': {
            'Ncor': '5 - 10',
            'delta': 15,
            'f_lim': 1.0,
            'N_q': 10,
            'q_lim': 40,
        },
        'medium': {
            'Ncor': '11 - 30',
            'delta': 20,
            'f_lim': 1.4,
            'N_q': 10,
            'q_lim': 40,
        },
        'dense': {
            'Ncor': '31 - 50',
            'delta': 20,
            'f_lim': 1.4,
            'N_q': 12,
            'q_lim': 60,
        },
        'very_dense': {
            'Ncor': 'over 50',
            'delta': 25,
            'f_lim': 1.4,
            'N_q': 12,
            'q_lim': 60,
        },
    },
}

# -- USCS --------------------------------------------------------------------

uscs_dict = {
    'GW': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Gravels (More than 50% of '
                    'coarse fraction larger than No. 4 sieve size) > Clean '
                    'Gravels (Less than 5% fines)',
        'long_desc': 'Well-graded gravels, gravel-sand mixtures, little or no '
                     'fines',
        'short_desc': 'Gravel (WG)',
    },
    'GP': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Gravels (More than 50% of '
                    'coarse fraction larger than No. 4 sieve size) > Clean '
                    'Gravels (Less than 5% fines)',
        'long_desc': 'Poorly-graded gravels, gravel-sand mixtures, little or no'
                     ' fines',
        'short_desc': 'Gravel (PG)',
    },
    'GM': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Gravels (More than 50% of '
                    'coarse fraction larger than No. 4 sieve size) > Gravels '
                    'with Fines (More than 12% fines)',
        'long_desc': 'Silty gravels, gravel-sand-silt mixtures',
        'short_desc': 'Silty gravel',
    },
    'GC': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Gravels (More than 50% of '
                    'coarse fraction larger than No. 4 sieve size) > Gravels '
                    'with Fines (More than 12% fines)',
        'long_desc': 'Clayey gravels, gravel-sand-clay mixtures',
        'short_desc': 'Clayey gravel',
    },
    'GW-GM': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Gravels (More than 50% of '
                    'coarse fraction larger than No. 4 sieve size) > Gravels '
                    'with Fines (More than 12% fines)',
        'long_desc': 'Well-graded gravels, gravel-sand mixtures, with fines',
        'short_desc': 'Gravel (WG, w/ fines)',
    },
    'GP-GM': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Gravels (More than 50% of '
                    'coarse fraction larger than No. 4 sieve size) > Gravels '
                    'with Fines (More than 12% fines)',
        'long_desc': 'Poorly-graded gravels, gravel-sand mixtures, with fines',
        'short_desc': 'Gravel (PG, w/ fines)',
    },
    'SW': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Clean Sands '
                    '(Less than 5% fines)',
        'long_desc': 'Well-graded sands, gravelly sands, little or no fines',
        'short_desc': 'Sand (WG)',
    },
    'SP': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Clean Sands '
                    '(Less than 5% fines)',
        'long_desc': 'Poorly-graded sands, gravelly sands, little or no fines',
        'short_desc': 'Sand (PG)',
    },
    'SM': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Sands with Fines '
                    '(More than 12% fines)',
        'long_desc': 'Silty sands, sand-silt mixtures',
        'short_desc': 'Silty sand',
    },
    'SC': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Sands with Fines '
                    '(More than 12% fines)',
        'long_desc': 'Clayey sands, sand-clay mixtures',
        'short_desc': 'Clayey sand',
    },
    'SW-SM': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Sands with Fines '
                    '(More than 12% fines)',
        'long_desc': 'Well-graded sands, gravelly sands, with silt',
        'short_desc': 'Sand (WG, w/ silt)',
    },
    'SW-SC': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Sands with Fines '
                    '(More than 12% fines)',
        'long_desc': 'Well-graded sands, gravelly sands, with clay',
        'short_desc': 'Sand (WG, w/ clay)',
    },
    'SP-SM': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Sands with Fines '
                    '(More than 12% fines)',
        'long_desc': 'Poorly-graded sands, gravelly sands, with silt',
        'short_desc': 'Sand (PG, w/ silt)',
    },
    'SP-SC': {
        'soil_type': 'cohesionless',
        'category': 'Coarse-grained soils (more than 50% of material is larger '
                    'than No. 200 sieve size) > Sands 50% or more of coarse '
                    'fraction smaller than No. 4 sieve size > Sands with Fines '
                    '(More than 12% fines)',
        'long_desc': 'Poorly-graded sands, gravelly sands, with clay',
        'short_desc': 'Sand (PG, w/ clay)',
    },
    'ML': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    'less than 50%)',
        'long_desc': 'Inorganic silts and very fine sands, rock flour, silty '
                     'of clayey fine sands or clayey silts with slight '
                     'plasticity',
        'short_desc': 'Sandy/Clayey Silt (LP)',
    },
    'CL': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    'less than 50%)',
        'long_desc': 'Inorganic clays of low to medium plasticity, gravelly '
                     'clays, sandy clays, silty clays, lean clays',
        'short_desc': 'Clay (LP)',
    },
    'OL': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    'less than 50%)',
        'long_desc': 'Organic silts and organic silty clays of low plasticity',
        'short_desc': 'Organic silt/clay (LP)',
    },
    'CL-ML': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    'less than 50%)',
        'long_desc': '',
        'short_desc': 'Silty Clay (LP)',
    },
    'SM-ML': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    'less than 50%)',
        'long_desc': '',
        'short_desc': 'Sandy/Clayey Silt (LP)',
    },
    'MH': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    '50% or greater)',
        'long_desc': 'Inorganic silts, micaceous or diatomaceous fine sandy or '
                     'silty soils, elastic silts',
        'short_desc': 'Sandy/Clayey Silt (HP)',
    },
    'CH': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    '50% or greater)',
        'long_desc': 'Inorganic clays of high plasticity, fat clays',
        'short_desc': 'Clay (HP)',
    },
    'OH': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    '50% or greater)',
        'long_desc': 'Organic clays of medium to high plasticity, organic '
                     'silts',
        'short_desc': 'Organic silt/clay (HP)',
    },
    'OL-OH': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    '50% or greater)',
        'long_desc': '',
        'short_desc': '',
    },
    'CL-CH': {
        'soil_type': 'cohesive',
        'category': 'Fine-graned soils (50% or more of material is smaller '
                    'than No. 200 sieve size) > Silts and Clays (Liquid limit '
                    '50% or greater)',
        'long_desc': '',
        'short_desc': '',
    },
    'PT': {
        'soil_type': 'cohesive',
        'category': 'Highly organic soils',
        'long_desc': 'Peat and other highly organic soils',
        'short_desc': 'Peat',
    },
    'ROCK': {
        'soil_type': 'rock',
        'category': 'Rocks',
        'long_desc': '',
        'short_desc': 'Rock',
    },
}
