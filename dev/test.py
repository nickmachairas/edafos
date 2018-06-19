from edafos.project import Project
from edafos.soil import SoilProfile
from edafos.deepfoundations import Pile, API
# import pandas as pd
# from tabulate import tabulate


def olson_009():
    profile = SoilProfile(unit_system='English', water_table=5)
    profile.add_layer(soil_type='cohesive', height=8, tuw=103)
    profile.add_layer(soil_type='cohesive', height=22.5, tuw=109)
    profile.add_layer(soil_type='cohesionless', height=10.5, tuw=120)
    profile.add_layer(soil_type='cohesive', height=32.6, tuw=107)
    profile.add_layer(soil_type='cohesive', height=10, tuw=107)

    mids = []
    for i in profile.layers.index:
        if i == 1:
            mids.append(profile.layers['Height'][i]/2)
        else:
            mids.append(profile.layers['Depth'][i-1] +
                        profile.layers['Height'][i]/2)
    print(mids)
    mids = [4.0, 19.25, 35.75, 57.3, 73.6]
    for i in mids:
        res = profile.calculate_stress(i)
        print(i, res)


def test_pile():
    pile = Pile(unit_system='English',
                pile_type='cast-in-place',
                shape='HP8X36',
                length=10,
                side=12,
                diameter=12,
                thickness=1,
                # pen_depth=15,
                nf_zone=2,
                # taper_dims=[[6, 10], ],
                # taper_dims=[[10, 5], [8, 5], ]
                )

    print(pile)
    print(pile.xsection_area(10))
    print(pile.side_area(0, 10))


def example1():
    # Create the project object
    project = Project(unit_system='English', project_name='Example 1')

    # Create the soil profile object
    profile = SoilProfile(unit_system='English', water_table=10)
    profile.add_layer(soil_type='cohesionless',
                      height=40,
                      tuw=100,
                      field_phi=35,
                      corr_n=20)
    profile.add_layer(soil_type='cohesionless',
                      height=20,
                      tuw=100,
                      field_phi=35,
                      corr_n=20)
    profile.add_layer(soil_type='cohesionless',
                      height=30,
                      tuw=100,
                      field_phi=35,
                      corr_n=20)

    # Attach the soil profile to the project
    project.attach_sp(profile)

    # Create a pile
    pile = Pile(unit_system='English',
                pile_type='concrete',
                shape='square-solid',
                length=32.99,
                side=14,
                #pen_depth=30,
                diameter=14,
                thickness=0.75,
                #taper_dims=[[12, 32]]
                )

    # Attach the pile to the project
    project.attach_pile(pile)

    # Why not get the effective stress at say 15-ft??...
    project.sp.calculate_stress(15)

    # Start a pile capacity analysis
    api = API(project)

    # print(project)
    # print("*************")
    # print(profile)
    # print(project.sp.calculate_stress(15))
    # print(project.sp.z_of_layers())
    # print(project.z_layer_pile())
    # print(api._z_analysis())
    print(api.get_soil_prop(40, 'su'))


if __name__ == "__main__":
    # project1 = Project(unit_system='English')
    # print(project1)
    # print("-----------")
    # caseB = SoilProfile(unit_system='English', water_table=-7)
    # caseB.add_layer(soil_type='cohesionless', height=4.5, tuw=90)
    # caseB.add_layer(soil_type='cohesive', height=4.5, tuw=110)
    # print(caseB)
    # print(caseB.calculate_stress(-3, kind='all'))
    # print(caseB.calculate_stress(7, kind='all'))
    # print(profile1.layers[['Depth', 'Height', 'TUW']])
    # print(profile1.water_table)
    # print(profile1.layers['Depth'].isnull().all().values[0])
    # print(profile1.layers['Field N'].isnull().all().values[0])
    # print(profile1.calculate_stress(6))
    # olson_009()
    # test_pile()
    example1()
