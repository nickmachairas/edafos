from edafos.project import Project
from edafos.soil import SoilProfile
from tabulate import tabulate

if __name__ == "__main__":
    project1 = Project(unit_system="English")
    print(project1)
    print("-----------")
    profile1 = SoilProfile(unit_system="English", water_table=1)
    profile1.add_layer(soil_type='C', height=10, tuw=90)
    profile1.add_layer(soil_type='S', height=1.5, tuw=102)
    profile1.add_layer(soil_type='S', height=15, tuw=102)
    #print(profile1)
    print(profile1)
    print(tabulate(profile1.layers[['Depth','Height']], headers='keys', tablefmt='psql'))
