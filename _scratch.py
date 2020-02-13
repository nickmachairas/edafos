from edafos import effective_stress

heights1 = [4.5, 4.5]
gammas1 = [90, 110]

heights2 = [3.3, 82, 9.8, 311.7, 42.7]
gammas2 = [65, 95, 130, 140, 140]

if __name__ == '__main__':
    print(effective_stress(7, -7, heights1, gammas1))
    print(effective_stress(7, -7, heights1, gammas1).to('ksf'))
    print(effective_stress(7, -7, heights1, gammas1).to('kN_m2'))
    print('---')
    print(effective_stress(1.65, -1.64, heights2, gammas2).to('ksf'))
    print(effective_stress(44.3, -1.64, heights2, gammas2).to('ksf'))
    print(effective_stress(90.2, -1.64, heights2, gammas2).to('ksf'))
    print(effective_stress(250.95, -1.64, heights2, gammas2).to('ksf'))
    print(effective_stress(428.15, -1.64, heights2, gammas2).to('ksf'))
