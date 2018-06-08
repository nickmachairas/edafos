from edafos.project import Project
from edafos.soil import SoilProfile
# import pandas as pd
# from tabulate import tabulate

if __name__ == "__main__":
    project1 = Project(unit_system='English')
    print(project1)
    print("-----------")
    profile1 = SoilProfile(unit_system='English', water_table=10)
    profile1.add_layer(soil_type='cohesionless', height=16, tuw=90)
    # profile1.add_layer(soil_type='cohesionless', height=1.5, tuw=102)
    # profile1.add_layer(soil_type='cohesionless', height=15, tuw=102, su=999)
    # print(profile1.layers.info())
    # print(profile1)
    # print(profile1.layers[['Depth', 'Height', 'TUW']])
    # print(profile1.water_table)
    # print(profile1.layers['Depth'].isnull().all().values[0])
    # print(profile1.layers['Field N'].isnull().all().values[0])
    print(profile1.calculate_stress(6))
