import numpy as np


def effector_trajectory_generator_3d(t, parameters=None):
    """Generates prime function, first and second derivative for
    end effector trajectory"""
    w = 0.015 * 2 * np.pi
    k = 0.5
    dx = 2.3
    dy = 0.1
    dz = 0.0

    qchd = np.array([k * np.cos(w * t) + dx,
                     k * np.sin(w * t) + dy,
                     0.1 * k * np.cos(w * t) + dz])

    # TODO: calculate first and second derivative based on the qchd vector
    qchd_d1 = np.array([0.0, 0.0, 0.0])
    qchd_d2 = np.array([0.0, 0.0, 0.0])

    return qchd, qchd_d1, qchd_d2


def model_ode(t, input_args, parameters):
    # get input values

    # manipulator joint velocities
    qr_d1 = input_args[0:3]
    q_d1 = qr_d1.copy()
    # manipulator joint position
    qr = input_args[3:6]
    q = qr.copy()

    m1 = parameters['m1']
    m2 = parameters['m2']
    m3 = parameters['m3']
    mc = parameters['mc']

    l1 = parameters['l1']
    l2 = parameters['l2']
    l3 = parameters['l3']

    a = parameters['a']
    b = parameters['b']
    c = parameters['c']

    g = parameters['g']

    Tv = parameters['Tv']
    Ts = parameters['Ts']
    Tk = parameters['Tk']

    Kp = parameters['Kp']
    Kd = parameters['Kd']

    # calculate position of the end-effector
    xch = (a + l1 * np.cos(qr[0])
           - l2 * (np.sin(qr[0]) * np.sin(qr[1]) - np.cos(qr[0]) * np.cos(qr[1]))
           - l3 * np.cos(qr[2]) * (np.sin(qr[0]) * np.sin(qr[1]) - np.cos(qr[0]) * np.cos(qr[1])))
    ych = (b + l1 * np.sin(qr[0])
           + l2 * (np.cos(qr[0]) * np.sin(qr[1]) + np.cos(qr[1]) * np.sin(qr[0]))
           + l3 * np.cos(qr[2]) * (np.cos(qr[0]) * np.sin(qr[1]) + np.cos(qr[1]) * np.sin(qr[0])))
    zch = c + l3 * np.sin(qr[2])

    xch_d1 = (
        - l3 * (np.cos(qr[2]) * (np.cos(qr[0]) * np.sin(qr[1]) * qr_d1[0]
        + np.cos(qr[1]) * np.sin(qr[0]) * qr_d1[0]
        + np.cos(qr[0]) * np.sin(qr[1]) * qr_d1[1]
        + np.cos(qr[1]) * np.sin(qr[0]) * qr_d1[1])
        - np.sin(qr[2]) * (np.sin(qr[0]) * np.sin(qr[1]) - np.cos(qr[0]) * np.cos(qr[1])) * qr_d1[2])
        - l2 * (np.cos(qr[0]) * np.sin(qr[1]) * qr_d1[0]
        + np.cos(qr[1]) * np.sin(qr[0]) * qr_d1[0]
        + np.cos(qr[0]) * np.sin(qr[1]) * qr_d1[1]
        + np.cos(qr[1]) * np.sin(qr[0]) * qr_d1[1])
        - l1 * np.sin(qr[0]) * qr_d1[0])

    ych_d1 = (
        l3 * (np.cos(qr[2]) * (np.cos(qr[0]) * np.cos(qr[1]) * qr_d1[0]
        + np.cos(qr[0]) * np.cos(qr[1]) * qr_d1[1]
        - np.sin(qr[0]) * np.sin(qr[1]) * qr_d1[0]
        - np.sin(qr[0]) * np.sin(qr[1]) * qr_d1[1])
        - np.sin(qr[2]) * (np.cos(qr[0]) * np.sin(qr[1]) + np.cos(qr[1]) * np.sin(qr[0])) * qr_d1[2])
        + l2 * (np.cos(qr[0]) * np.cos(qr[1]) * qr_d1[0]
        + np.cos(qr[0]) * np.cos(qr[1]) * qr_d1[1]
        - np.sin(qr[0]) * np.sin(qr[1]) * qr_d1[0]
        - np.sin(qr[0]) * np.sin(qr[1]) * qr_d1[1])
        + l1 * np.cos(qr[0]) * qr_d1[0])

    zch_d1 = l3 * np.cos(qr[2]) * qr_d1[2]

    # calculate dynamics
    M = np.array([
        [(l1**2 * m1) / 3 + l1**2 * m2 + l1**2 * m3 + (l2**2 * m2) / 3 + l2**2 * m3 + (l3**2 * m3 * np.cos(qr[2])**2) / 3 + l1 * l2 * m2 * np.cos(qr[1]) + 2 * l1 * l2 * m3 * np.cos(qr[1]) + l2 * l3 * m3 * np.cos(qr[2]) + l1 * l3 * m3 * np.cos(qr[1]) * np.cos(qr[2]),
         (l2**2 * m2) / 3 + l2**2 * m3 + (l3**2 * m3 * np.cos(qr[2])**2) / 3 + (l1 * l2 * m2 * np.cos(qr[1])) / 2 + l1 * l2 * m3 * np.cos(qr[1]) + l2 * l3 * m3 * np.cos(qr[2]) + (l1 * l3 * m3 * np.cos(qr[1]) * np.cos(qr[2])) / 2,
         -(l1 * l3 * m3 * np.sin(qr[1]) * np.sin(qr[2])) / 2],
        [(l2**2 * m2) / 3 + l2**2 * m3 + (l3**2 * m3 * np.cos(qr[2])**2) / 3 + (l1 * l2 * m2 * np.cos(qr[1])) / 2 + l1 * l2 * m3 * np.cos(qr[1]) + l2 * l3 * m3 * np.cos(qr[2]) + (l1 * l3 * m3 * np.cos(qr[1]) * np.cos(qr[2])) / 2,
         (l2**2 * m2) / 3 + l2**2 * m3 + (l3**2 * m3 * np.cos(qr[2])**2) / 3 + l2 * l3 * m3 * np.cos(qr[2]),
         0],
        [-(l1 * l3 * m3 * np.sin(qr[1]) * np.sin(qr[2])) / 2,
         0,
         (l3**2 * m3) / 3]])

    C = np.array([
        [- qr_d1[1] * ((l1 * l2 * m2 * np.sin(qr[1])) / 2 + l1 * l2 * m3 * np.sin(qr[1]) + (l1 * l3 * m3 * np.cos(qr[2]) * np.sin(qr[1])) / 2) - qr_d1[2] * ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2 + (l1 * l3 * m3 * np.cos(qr[1]) * np.sin(qr[2])) / 2),
         - qr_d1[0] * ((l1 * l2 * m2 * np.sin(qr[1])) / 2 + l1 * l2 * m3 * np.sin(qr[1]) + (l1 * l3 * m3 * np.cos(qr[2]) * np.sin(qr[1])) / 2) - qr_d1[1] * ((l1 * l2 * m2 * np.sin(qr[1])) / 2 + l1 * l2 * m3 * np.sin(qr[1]) + (l1 * l3 * m3 * np.cos(qr[2]) * np.sin(qr[1])) / 2) - qr_d1[2] * ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2 + (l1 * l3 * m3 * np.cos(qr[1]) * np.sin(qr[2])) / 2),
         - qr_d1[0] * ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2 + (l1 * l3 * m3 * np.cos(qr[1]) * np.sin(qr[2])) / 2) - qr_d1[1] * ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2 + (l1 * l3 * m3 * np.cos(qr[1]) * np.sin(qr[2])) / 2) - (l1 * l3 * m3 * np.cos(qr[2]) * np.sin(qr[1]) * qr_d1[2]) / 2],
        [qr_d1[0] * ((l1 * l2 * m2 * np.sin(qr[1])) / 2 + l1 * l2 * m3 * np.sin(qr[1]) + (l1 * l3 * m3 * np.cos(qr[2]) * np.sin(qr[1])) / 2) - ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[2],
         -((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[2],
         - ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[0] - ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[1]],
        [((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[1] + qr_d1[0] * ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2 + (l1 * l3 * m3 * np.cos(qr[1]) * np.sin(qr[2])) / 2),
         ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[0] + ((l3**2 * m3 * np.cos(qr[2]) * np.sin(qr[2])) / 3 + (l2 * l3 * m3 * np.sin(qr[2])) / 2) * qr_d1[1],
         0]])

    D = np.array([0, 0, -(g * l3 * m3 * np.cos(qr[2])) / 2])

    J = np.array([
        [- l1 * np.sin(qr[0]) - l2 * np.sin(qr[0] + qr[1]) - l3 * np.cos(qr[2]) * np.sin(qr[0] + qr[1]),
         - l2 * np.sin(qr[0] + qr[1]) - l3 * np.cos(qr[2]) * np.sin(qr[0] + qr[1]),
         -l3 * np.sin(qr[2]) * np.cos(qr[0] + qr[1])],
        [l1 * np.cos(qr[0]) + l2 * np.cos(qr[0] + qr[1]) + l3 * np.cos(qr[2]) * np.cos(qr[0] + qr[1]),
         l2 * np.cos(qr[0] + qr[1]) + l3 * np.cos(qr[2]) * np.cos(qr[0] + qr[1]),
         -l3 * np.sin(qr[2]) * np.sin(qr[0] + qr[1])],
        [0, 0, l3 * np.cos(qr[2])]])

    J_d1 = np.array([
        [- l3 * (np.cos(qr[2]) * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - np.sin(qr[2]) * np.sin(qr[0] + qr[1]) * qr_d1[2]) - l2 * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - l1 * np.cos(qr[0]) * qr_d1[0],
         - l3 * (np.cos(qr[2]) * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - np.sin(qr[2]) * np.sin(qr[0] + qr[1]) * qr_d1[2]) - l2 * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]),
         l3 * (np.sin(qr[2]) * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - np.cos(qr[2]) * np.cos(qr[0] + qr[1]) * qr_d1[2])],
        [- l3 * (np.sin(qr[2]) * np.cos(qr[0] + qr[1]) * qr_d1[2] + np.cos(qr[2]) * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])) - l2 * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - l1 * np.sin(qr[0]) * qr_d1[0],
         - l3 * (np.sin(qr[2]) * np.cos(qr[0] + qr[1]) * qr_d1[2] + np.cos(qr[2]) * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])) - l2 * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]),
         - l3 * np.cos(qr[2]) * np.sin(qr[0] + qr[1]) * qr_d1[2] - l3 * np.sin(qr[2]) * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])],
        [0, 0, -l3 * np.sin(qr[2]) * qr_d1[2]]])

    P = np.array([
        l3 * (np.sin(qr[2]) * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - np.cos(qr[2]) * np.cos(qr[0] + qr[1]) * qr_d1[2]) * qr_d1[2] - qr_d1[0] * (l3 * (np.cos(qr[2]) * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - np.sin(qr[2]) * np.sin(qr[0] + qr[1]) * qr_d1[2]) + l2 * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) + l1 * np.cos(qr[0]) * qr_d1[0]) - qr_d1[1] * (l3 * (np.cos(qr[2]) * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) - np.sin(qr[2]) * np.sin(qr[0] + qr[1]) * qr_d1[2]) + l2 * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])),
        - qr_d1[1] * (l3 * (np.sin(qr[2]) * np.cos(qr[0] + qr[1]) * qr_d1[2] + np.cos(qr[2]) * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])) + l2 * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])) - (l3 * np.cos(qr[2]) * np.sin(qr[0] + qr[1]) * qr_d1[2] + l3 * np.sin(qr[2]) * np.cos(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])) * qr_d1[2] - qr_d1[0] * (l3 * (np.sin(qr[2]) * np.cos(qr[0] + qr[1]) * qr_d1[2] + np.cos(qr[2]) * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1])) + l2 * np.sin(qr[0] + qr[1]) * (qr_d1[0] + qr_d1[1]) + l1 * np.sin(qr[0]) * qr_d1[0]),
        -l3 * np.sin(qr[2]) * qr_d1[2]**2])

    B = np.eye(3)

    T = np.array([0.0, 0.0, 0.0])
    # TODO: calculate friction in manipulator joints
    # use Tustin model with Tv, Ts and Tk coefficients
    # velocities for each joints are in vector q_d1

    # generate trajectory for end effector
    # remember to calculate 1st and 2nd derivative of desired end-effector
    # trajectory
    qchd, qchd_d1, qchd_d2 = effector_trajectory_generator_3d(t, parameters)

    MInv = np.linalg.inv(M)

    #     y'' = P - J M^-1 C q' + J M^-1 u

    detJ = np.linalg.det(J)

    # calculate F
    # F = P - J M^-1 C q' - J M^-1 D - J M^-1 T
    F = np.zeros(3)

    # calculate G
    # G = J M^-1
    G = np.zeros((3, 3))

    qch = np.array([xch, ych, zch])
    qch_d1 = np.array([xch_d1, ych_d1, zch_d1])

    # calculate errors: e and e'
    # for e' keep e_d1 notation
    # e = qch - qchd
    # e' = qch' - qchd'
    e = np.zeros(3)
    e_d1 = np.zeros(3)

    # calculate new input to the system v
    # v = qd'' - Kd e' - Kp e
    v = np.zeros(3)

    detG = np.linalg.det(G)
    # calculate inverse of G as below
    # Ginv = np.linalg.inv(G)

    # calculate control input u
    # u = G^-1 * (v - F)
    u = np.zeros(3)

    # calculate state
    qr_d2 = MInv @ (B @ u - C @ q_d1 - D - T)

    dets = np.array([detG, detJ])

    output_args = np.zeros(6)
    output_args[0:3] = qr_d2
    output_args[3:6] = qr_d1

    additional = {
        'qchd': qchd,
        'qchd_d1': qchd_d1,
        'qchd_d2': qchd_d2,
        'dets': dets,
        'k': qch,
    }

    return output_args, additional
