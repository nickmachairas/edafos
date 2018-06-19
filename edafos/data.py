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
