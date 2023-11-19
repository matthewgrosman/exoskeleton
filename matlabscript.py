import numpy as np

def gee(sensor1, sensor2, sensor3):
    S4R_alpha = 35.005
    S4R_beta = 35.005
    S4R_gamma = 35
    S4R_eta = 35

    S4R_theta = 98.489 - sensor2

    A1 = np.cos(np.radians(S4R_theta)) * np.sin(np.radians(S4R_alpha)) * np.cos(np.radians(S4R_gamma)) * np.sin(np.radians(S4R_beta)) - \
         np.cos(np.radians(S4R_alpha)) * np.sin(np.radians(S4R_gamma)) * np.sin(np.radians(S4R_beta))
    B1 = np.sin(np.radians(S4R_theta)) * np.sin(np.radians(S4R_alpha)) * np.sin(np.radians(S4R_beta))
    C1 = np.cos(np.radians(S4R_eta)) - np.cos(np.radians(S4R_theta)) * np.sin(np.radians(S4R_alpha)) * np.sin(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_beta)) - \
         np.cos(np.radians(S4R_alpha)) * np.cos(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_beta))

    psi_p1 = np.degrees(np.arctan2(B1, A1))
    psi_p2 = np.degrees(np.arccos(C1 / np.sqrt(A1**2 + B1**2)))

    S4R_psi = psi_p1 - psi_p2

    cos_phi = (np.sin(np.radians(S4R_beta)) * np.cos(np.radians(S4R_theta)) * np.cos(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_psi)) +
               np.cos(np.radians(S4R_theta)) * np.sin(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_beta)) +
               np.sin(np.radians(S4R_beta)) * np.sin(np.radians(S4R_theta)) * np.sin(np.radians(S4R_psi)) -
               np.sin(np.radians(S4R_alpha)) * np.cos(np.radians(S4R_eta))) / \
              (np.cos(np.radians(S4R_alpha)) * np.sin(np.radians(S4R_eta)))

    sin_phi = (-np.sin(np.radians(S4R_beta)) * np.sin(np.radians(S4R_theta)) * np.cos(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_psi)) -
                np.sin(np.radians(S4R_theta)) * np.sin(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_beta)) +
                np.sin(np.radians(S4R_beta)) * np.cos(np.radians(S4R_theta)) * np.sin(np.radians(S4R_psi))) / \
               np.sin(np.radians(S4R_eta))

    S4R_phi = np.degrees(np.arctan2(sin_phi, cos_phi))

    # S4R_zeta = np.degrees(np.arccos((np.cos(np.radians(S4R_beta)) * np.cos(np.radians(S4R_eta)) -
    #                                  np.cos(np.radians(S4R_gamma)) * np.cos(np.radians(S4R_alpha)) -
    #                                  np.sin(np.radians(S4R_gamma)) * np.sin(np.radians(S4R_alpha)) * np.cos(np.radians(S4R_theta))) /
    #                                 np.sin(np.radians(S4R_beta))))

    S4R_zeta = np.degrees(np.arccos((np.cos(np.radians(S4R_beta)) * np.cos(np.radians(S4R_eta)) - np.cos(
        np.radians(S4R_gamma)) * np.cos(np.radians(S4R_alpha)) - np.sin(np.radians(S4R_gamma)) * np.sin(
        np.radians(S4R_alpha)) * np.cos(np.radians(S4R_theta))) / (
                                                np.sin(np.radians(S4R_beta)) * np.sin(np.radians(S4R_eta)))))

    theta_1 = -49.296 + sensor1
    theta_2 = -S4R_psi
    theta_3 = 98.489 - sensor2
    theta_4 = S4R_phi
    theta_5 = -S4R_zeta - 23.97 + sensor3

    DH_theta = np.array([np.array([theta_1, theta_2, theta_3, theta_4, theta_5])])
    DH_d = np.array([-122.98, 0, 0, 0, 85.06])
    DH_alpha = np.array([35, 35, 35, 35, 0])
    DH_a = np.array([0, 0, 0, 0, 0])

    # DH_Table = np.column_stack((DH_theta, DH_d, DH_alpha, DH_a))

    G = np.array([[0.1949, 0.8851, -0.4227, -14.3574],
                  [0.9787, -0.1468, 0.1437, 25.3417],
                  [0.0651, -0.4417, -0.8948, -121.6040],
                  [0, 0, 0, 1]])

    H = np.array([[1, 0, 0, 37.623],
                  [0, 1, 0, -11.555],
                  [0, 0, 1, 77.397],
                  [0, 0, 0, 1]])

    A = np.zeros((4, 4, DH_theta.shape[0]))
    T = np.zeros((4, 4, DH_theta.shape[0]))
    NewTheta1 = np.zeros((DH_theta.shape[0], 1))
    NewTheta2 = np.zeros((DH_theta.shape[0], 1))

    for i in range(DH_theta.shape[0]):
        output = np.eye(4)

        for j in range(DH_theta.shape[1]):
            a = DH_a[j]
            d = DH_d[j]

            A_j = np.array([[np.cos(np.radians(DH_theta[i, j])), -np.sin(np.radians(DH_theta[i, j])) * np.cos(np.radians(DH_alpha[j])),
                             np.sin(np.radians(DH_theta[i, j])) * np.sin(np.radians(DH_alpha[j])), a * np.cos(np.radians(DH_theta[i, j]))],
                            [np.sin(np.radians(DH_theta[i, j])), np.cos(np.radians(DH_theta[i, j])) * np.cos(np.radians(DH_alpha[j])),
                             -np.cos(np.radians(DH_theta[i, j])) * np.sin(np.radians(DH_alpha[j])), a * np.sin(np.radians(DH_theta[i, j]))],
                            [0, np.sin(np.radians(DH_alpha[j])), np.cos(np.radians(DH_alpha[j])), d],
                            [0, 0, 0, 1]])

            output = np.dot(output, A_j)
            print(j, " --> ", output)
            print("------------")


        A[:, :, i] = output
        T[:, :, i] = np.dot(np.dot(G, A[:, :, i]), np.linalg.inv(H))

        # print("T: ", T)
        # print()
        # print("A: ", A)
        # print()
        # print("G: ", G)
        # print()
        # print("H: ", H)
        # print()

        NewTheta1[i, 0] = np.rad2deg(np.arctan2(T[0, 2, i], -T[1, 2, i]))
        NewTheta2[i, 0] = np.rad2deg(np.arctan2(T[2, 0, i], T[2, 1, i]))

    return NewTheta1, NewTheta2
