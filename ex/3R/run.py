import numpy as np
import matplotlib.pyplot as plt

from inputOutputDecoupling import model_ode
from simulator import Simulator


def main():
    tEnd = 100

    np.random.seed(123456789)

    m1 = 1
    m2 = 1
    m3 = 1
    mc = m1 + m2 + m3

    l1 = 1
    l2 = 1
    l3 = 1

    a = 0
    b = 0
    c = 0

    g = -10

    Tv = 0.01
    Ts = 0.01
    Tk = 5

    Kp = 10 * np.eye(3)
    Kd = 50 * np.eye(3)

    # define initial conditions for the manipulator
    init_qr_d1 = np.array([0.0, 0.0, 0.0])
    init_qr = np.array([0.0, 0.0, 0.0])

    # set sample time
    sample_time = 0.1

    # parameters for the model
    parameters = {
        'm1': m1, 'm2': m2, 'm3': m3, 'mc': mc,
        'l1': l1, 'l2': l2, 'l3': l3,
        'a': a, 'b': b, 'c': c,
        'g': g,
        'Tv': Tv, 'Ts': Ts, 'Tk': Tk,
        'Kp': Kp, 'Kd': Kd,
    }

    print('Starting ...')

    ic = np.zeros(6)
    ic[0:3] = init_qr_d1
    ic[3:6] = init_qr

    sim = Simulator(parameters, model_ode)
    sim_data, additional = sim.run(ic, tEnd, sample_time)

    # Plot errors: difference between real and desired end-effector trajectory
    plt.subplot(2, 2, 1)
    plt.plot(sim_data['time'], additional['k'][0, :] - additional['qchd'][0, :],
             sim_data['time'], additional['k'][1, :] - additional['qchd'][1, :],
             sim_data['time'], additional['k'][2, :] - additional['qchd'][2, :])
    plt.title("End-effector trajectory errors")
    plt.legend(["x", "y", "z"])

    # Plot real vs desired trajectory in 3D
    ax = plt.subplot(2, 2, 2, projection='3d')
    ax.plot(additional['k'][0, :], additional['k'][1, :], additional['k'][2, :], 'r')
    ax.plot(additional['qchd'][0, :], additional['qchd'][1, :], additional['qchd'][2, :], 'b')
    ax.legend(['Real', 'Desired'])
    ax.set_title("Real vs. desired trajectory")

    # Plot joint trajectory
    plt.subplot(2, 2, 3)
    plt.plot(sim_data['time'], sim_data['out_qr_d0'])
    plt.title("Joint positions")
    plt.legend(["q1", "q2", "q3"])

    # Plot joint velocities
    plt.subplot(2, 2, 4)
    plt.plot(sim_data['time'], sim_data['out_qr_d1'])
    plt.title("Joint velocities")
    plt.legend(["q1'", "q2'", "q3'"])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
