from edafos.stresses import effective_stress

heights = [4.5, 4.5]
gammas = [90, 110]

if __name__ == '__main__':
    print(effective_stress(7, -7, heights, gammas))
    print(effective_stress(7, -7, heights, gammas).to('kN_m2'))
