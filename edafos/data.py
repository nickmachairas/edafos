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
