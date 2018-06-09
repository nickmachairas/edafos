from edafos.project import Project
from edafos.soil import SoilProfile
# import pandas as pd
# from tabulate import tabulate

if __name__ == "__main__":
    # project1 = Project(unit_system='English')
    # print(project1)
    # print("-----------")
    caseB = SoilProfile(unit_system='English', water_table=10)
    caseB.add_layer(soil_type='cohesionless', height=5, tuw=90)
    caseB.add_layer(soil_type='cohesive', height=11, tuw=110)
    #print(caseB)
    print(caseB.calculate_stress(6, kind='pore_water'))
    print(caseB.calculate_stress(14))
    # print(profile1.layers[['Depth', 'Height', 'TUW']])
    # print(profile1.water_table)
    # print(profile1.layers['Depth'].isnull().all().values[0])
    # print(profile1.layers['Field N'].isnull().all().values[0])
    # print(profile1.calculate_stress(6))
