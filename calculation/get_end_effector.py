"""
All credit for these calculations goes to: https://drive.google.com/drive/folders/18XZ3T8iQ1MzVMngPpcYfKfxNLCJTCkb_

I've converted the MATLAB code from the linked folder into Python so it's easier
to package/distribute for this project. All of the logic comes from the MATLAB folder.

Here is the original research paper that these calculations were used in: https://cctomm.ca/2023/CCToMM_M3_Symposium_paper_13.pdf
"""

import numpy as np

from calculation.constants import S4R_ALPHA, S4R_BETA, S4R_GAMMA, S4R_ETA, S4R_THETA_INITIAL, \
    THETA_1_INITIAL, THETA_5_INITIAL, DH_A, DH_ALPHA, DH_D, G, H


def get_end_effector(sensor1: float, sensor2: float, sensor3: float) -> (float, float):
    """
    Function that calculates and returns two angles... [TK]

    :param sensor1: [TK]
    :param sensor2: [TK]
    :param sensor3: [TK]
    :return: [TK]
    """
    # Calculate S4R values
    s4r_theta = S4R_THETA_INITIAL - sensor2
    s4r_psi = _get_output_angle(s4r_theta)
    s4r_phi = _get_coupler_angle(s4r_theta, s4r_psi)
    S4R_zeta = _get_transmission_angle(s4r_theta)

    # Calculate theta values
    theta_1 = THETA_1_INITIAL + sensor1
    theta_2 = -s4r_psi
    theta_3 = S4R_THETA_INITIAL - sensor2
    theta_4 = s4r_phi
    theta_5 = -S4R_zeta - THETA_5_INITIAL + sensor3

    # Create dh_theta
    dh_theta = np.array([np.array([theta_1, theta_2, theta_3, theta_4, theta_5])])

    # Initialize empty/eye structures to hold calculation results
    T = np.zeros((4, 4, dh_theta.shape[0]))
    output = np.eye(4)

    # Perform calculations to compute output angles
    for i in range(dh_theta.shape[1]):
        a, d = DH_A[i], DH_D[i]
        A_j = _get_dh_link_jl(dh_theta, i, a, d)
        output = np.dot(output, A_j)

    T[:, :, 0] = np.dot(np.dot(G, output), np.linalg.inv(H))

    new_theta_1 = np.rad2deg(np.arctan2(T[0, 2, 0], -T[1, 2, 0]))
    new_theta_2 = np.rad2deg(np.arctan2(T[2, 0, 0], T[2, 1, 0]))

    return new_theta_1, new_theta_2


def _get_output_angle(theta: float) -> float:
    """
    Function that calculates and returns the output angle. The output angle is... [TK]

    :param theta: [TK]
    :return: [TK]
    """
    A1 = np.cos(np.radians(theta)) * np.sin(np.radians(S4R_ALPHA)) * np.cos(np.radians(S4R_GAMMA)) * np.sin(
        np.radians(S4R_BETA)) - \
         np.cos(np.radians(S4R_ALPHA)) * np.sin(np.radians(S4R_GAMMA)) * np.sin(np.radians(S4R_BETA))
    B1 = np.sin(np.radians(theta)) * np.sin(np.radians(S4R_ALPHA)) * np.sin(np.radians(S4R_BETA))
    C1 = np.cos(np.radians(S4R_ETA)) - np.cos(np.radians(theta)) * np.sin(np.radians(S4R_ALPHA)) * np.sin(
        np.radians(S4R_GAMMA)) * np.cos(np.radians(S4R_BETA)) - \
         np.cos(np.radians(S4R_ALPHA)) * np.cos(np.radians(S4R_GAMMA)) * np.cos(np.radians(S4R_BETA))

    psi_p1 = np.degrees(np.arctan2(B1, A1))
    psi_p2 = np.degrees(np.arccos(C1 / np.sqrt(A1 ** 2 + B1 ** 2)))

    return psi_p1 - psi_p2


def _get_coupler_angle(theta: float, s4r_psi: float) -> float:
    """
    Function that calculates and returns the coupler angle. The coupler angle is... [TK]

    :param theta: [TK]
    :param s4r_psi: [TK]
    :return: [TK]
    """
    cos_phi = (np.sin(np.radians(S4R_BETA)) * np.cos(np.radians(theta)) * np.cos(np.radians(S4R_GAMMA)) * np.cos(
        np.radians(s4r_psi)) +
               np.cos(np.radians(theta)) * np.sin(np.radians(S4R_GAMMA)) * np.cos(np.radians(S4R_BETA)) +
               np.sin(np.radians(S4R_BETA)) * np.sin(np.radians(theta)) * np.sin(np.radians(s4r_psi)) -
               np.sin(np.radians(S4R_ALPHA)) * np.cos(np.radians(S4R_ETA))) / \
              (np.cos(np.radians(S4R_ALPHA)) * np.sin(np.radians(S4R_ETA)))

    sin_phi = (-np.sin(np.radians(S4R_BETA)) * np.sin(np.radians(theta)) * np.cos(np.radians(S4R_GAMMA)) * np.cos(
        np.radians(s4r_psi)) -
               np.sin(np.radians(theta)) * np.sin(np.radians(S4R_GAMMA)) * np.cos(np.radians(S4R_BETA)) +
               np.sin(np.radians(S4R_BETA)) * np.cos(np.radians(theta)) * np.sin(np.radians(s4r_psi))) / \
              np.sin(np.radians(S4R_ETA))

    return np.degrees(np.arctan2(sin_phi, cos_phi))


def _get_transmission_angle(theta: float) -> float:
    """
    Function that calculates and returns the transmission angle. The transmission angle is... [TK]

    :param theta: [TK]
    :return: [TK]
    """
    return np.degrees(np.arccos((np.cos(np.radians(S4R_BETA)) * np.cos(np.radians(S4R_ETA)) - np.cos(
        np.radians(S4R_GAMMA)) * np.cos(np.radians(S4R_ALPHA)) - np.sin(np.radians(S4R_GAMMA)) * np.sin(
        np.radians(S4R_ALPHA)) * np.cos(np.radians(theta))) / (
                                 np.sin(np.radians(S4R_BETA)) * np.sin(np.radians(S4R_ETA)))))


def _get_dh_link_jl(dh_theta, i, a, d):
    """
    Function that calculates and returns the... [TK]

    :param dh_theta: [TK]
    :param i: [TK]
    :param a: [TK]
    :param d: [TK]
    :return: [TK]
    """
    return np.array([[np.cos(np.radians(dh_theta[0, i])), -np.sin(np.radians(dh_theta[0, i])) * np.cos(np.radians(DH_ALPHA[i])),
                         np.sin(np.radians(dh_theta[0, i])) * np.sin(np.radians(DH_ALPHA[i])), a * np.cos(np.radians(dh_theta[0, i]))],
                        [np.sin(np.radians(dh_theta[0, i])), np.cos(np.radians(dh_theta[0, i])) * np.cos(np.radians(DH_ALPHA[i])),
                         -np.cos(np.radians(dh_theta[0, i])) * np.sin(np.radians(DH_ALPHA[i])), a * np.sin(np.radians(dh_theta[0, i]))],
                        [0, np.sin(np.radians(DH_ALPHA[i])), np.cos(np.radians(DH_ALPHA[i])), d],
                        [0, 0, 0, 1]])
