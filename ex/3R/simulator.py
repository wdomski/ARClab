import numpy as np
from scipy.integrate import solve_ivp


class Simulator:
    def __init__(self, parameters, model_ode_fn, print_interval=0.5):
        self._parameters = parameters
        self._model_ode_fn = model_ode_fn
        self._print_interval = print_interval
        self._next_print_time = 0.0

    def _ode_wrapper(self, t, y):
        output, additional = self._model_ode_fn(t, y, self._parameters)

        if t >= self._next_print_time:
            qr = y[3:6]
            qr_d1 = y[0:3]
            k = additional['k']
            print(f"t: {t:7.2f} | "
                  f"q: [{qr[0]:7.3f}, {qr[1]:7.3f}, {qr[2]:7.3f}] | "
                  f"q': [{qr_d1[0]:7.3f}, {qr_d1[1]:7.3f}, {qr_d1[2]:7.3f}] | "
                  f"eff: [{k[0]:7.3f}, {k[1]:7.3f}, {k[2]:7.3f}]")
            self._next_print_time = t + self._print_interval

        return output

    def run(self, ic, tEnd, sample_time):
        t_eval = np.arange(0, tEnd + sample_time, sample_time)
        self._next_print_time = 0.0

        solver = solve_ivp(
            self._ode_wrapper,
            [0, tEnd], ic, method='RK45',
            rtol=1e-6, atol=1e-6, t_eval=t_eval)

        tLength = len(solver.t)
        additional = {
            'qchd': np.zeros((3, tLength)),
            'qchd_d1': np.zeros((3, tLength)),
            'qchd_d2': np.zeros((3, tLength)),
            'dets': np.zeros((2, tLength)),
            'k': np.zeros((3, tLength)),
        }
        for i in range(tLength):
            _, add_new = self._model_ode_fn(solver.t[i], solver.y[:, i], self._parameters)
            additional['qchd'][:, i] = add_new['qchd']
            additional['qchd_d1'][:, i] = add_new['qchd_d1']
            additional['qchd_d2'][:, i] = add_new['qchd_d2']
            additional['dets'][:, i] = add_new['dets']
            additional['k'][:, i] = add_new['k']

        sim_data = {
            'time': solver.t,
            'out_qr_d1': solver.y[0:3, :].T,
            'out_qr_d0': solver.y[3:6, :].T,
        }

        return sim_data, additional
