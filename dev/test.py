# from edafos.project import Project
from edafos.soil import SoilProfile
from edafos.deepfoundations import DrivenPile
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
    pile = DrivenPile(unit_system='English',
                      pile_type='concrete',
                      shape='square-solid',
                      length=10,
                      side=12,
                      diameter=12,
                      thickness=1,
                      pen_depth=0.5,
                      nf_zone=2,
                      taper_dims=[[10, 10], ],
                      #taper_dims=[[10, 5], [10, 5], ]
                      )

    print(pile)


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
    test_pile()
