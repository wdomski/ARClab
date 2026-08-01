import numpy as np
import matplotlib.pyplot as plt

from dynamicLin import SimulatorDynamics, UnicycleModel, trajectory_generator_circle, trajectory_generator_square, trajectory_generator_hexagon

def main():
    start = np.array([0.1, 0.1, np.pi/2*0.1])
    dt = 0.01
    model = UnicycleModel(state=start, dt=dt)
    simulator = SimulatorDynamics
    sim = simulator(model=model, dt=dt)
    model.state = start
    h = model.h
    # chi1 must be nonzero for dynamic linearisation (det Kd = chi1)
    chi1_init = 1.0
    h_d1 = np.array([chi1_init * np.cos(start[2]), chi1_init * np.sin(start[2])])
    initial_condition = np.concatenate([h, h_d1, start, [chi1_init]])
    
    # TODO chose trajectory generator
    trajectory_generator = trajectory_generator_circle

    stats, solver = sim.run(initial_condition, 6, dt, trajectory_generator)
    stats = {'t': solver['t'],
             'h': solver['y'][0:2],
             'h_d1': solver['y'][2:4],
             'q': solver['y'][4:7],
             'chi1': solver['y'][7]}
    stats['hd'], stats['hd_d1'], stats['hd_d2'] = trajectory_generator(stats['t'])
    stats['eh'] = stats['h'] - stats['hd']
    stats['eh_d1'] = stats['h_d1'] - stats['hd_d1']
    
    plt.subplot(2, 3, 1)
    plt.plot(stats['t'], stats['eh'][0,:], 'b', stats['t'], stats['eh'][1,:], 'r')
    plt.title("Errors in linearized space")
    plt.subplot(2, 3, 2)
    plt.plot(np.array(stats['h'])[0,:],np.array(stats['h'])[1,:], 'r', 
             np.array(stats['hd'])[0,:],np.array(stats['hd'])[1,:], 'b')
    plt.legend(['Real', 'Desired'], loc="lower left")
    plt.title("Real vs. desired trajectory in linearized space")
    plt.gca().set_aspect('equal')
    plt.subplot(2, 3, 3)
    plt.plot(np.array(stats['q'])[0,:],np.array(stats['q'])[1,:], 'r',
             np.array(stats['h'])[0,:],np.array(stats['h'])[1,:], 'b')
    plt.title("xy vs. h trajectories")
    plt.legend(['xy', 'h1 h2'], loc="lower left")
    plt.gca().set_aspect('equal')
    plt.subplot(2, 3, 4)
    plt.plot(stats['t'],stats['h_d1'][0,:], stats['t'],stats['h_d1'][1,:])
    plt.title("Linearized velocities h'")
    plt.legend(["h1'", "h2'"])
    plt.subplot(2, 3, 5)        
    plt.plot(stats['t'],stats['q'][2,:])
    plt.title("Theta, orientation")
    plt.subplot(2, 3, 6)
    plt.plot(stats['t'],stats['chi1'])
    plt.title("chi1 (det Kd)")
    plt.show()
    
if __name__ == "__main__":
    main()
