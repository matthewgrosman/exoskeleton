import numpy as np

# Spherical 4R constants
S4R_ALPHA = 35.005
S4R_BETA = 35.005
S4R_GAMMA = 35
S4R_ETA = 35
S4R_THETA_INITIAL = 98.489

# Theta calculation constants
THETA_1_INITIAL = -49.296
THETA_5_INITIAL = 23.97

# DH constants
DH_D = np.array([-122.98, 0, 0, 0, 85.06])
DH_ALPHA = np.array([35, 35, 35, 35, 0])
DH_A = np.array([0, 0, 0, 0, 0])

# G and H static arrays
G = np.array([[0.1949, 0.8851, -0.4227, -14.3574],
                  [0.9787, -0.1468, 0.1437, 25.3417],
                  [0.0651, -0.4417, -0.8948, -121.6040],
                  [0, 0, 0, 1]])

H = np.array([[1, 0, 0, 37.623],
                  [0, 1, 0, -11.555],
                  [0, 0, 1, 77.397],
                  [0, 0, 0, 1]])
