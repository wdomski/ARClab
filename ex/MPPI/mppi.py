import numpy as np

from simulator import Circle, obstacle_center


class MovingCircle(Circle):
    def __init__(self, center, velocity, **kwargs):
        super().__init__(np.array(center, dtype=float), **kwargs)
        self.velocity = np.array(velocity, dtype=float)

    def center_at(self, time):
        # TODO Task 3.1: predict the center at absolute time; do not mutate it.
        return self.center.copy()


class MPPI:
    def __init__(self, model, T=4.0, dt=0.2, samples=128,
                 temperature=0.5, noise=(0.6, 1.0), seed=0):
        self.model = model
        self.dt = dt
        self.samples = samples
        self.temperature = temperature
        self.noise = np.array(noise)
        self.rng = np.random.default_rng(seed)
        self.u = np.zeros((round(T / dt), model.m))
        self.lower = np.array([-1.0, -1.0])
        self.upper = np.array([1.0, 1.0])

    def command(self, state, goal, obstacles=(), time=0.0):
        perturbations = np.zeros((self.samples, *self.u.shape))
        # TODO Task 1.1: replace zeros with Gaussian noise using self.rng and self.noise.

        candidates = np.clip(self.u + perturbations, self.lower, self.upper)
        costs = np.empty(self.samples)
        for sample in range(self.samples):
            costs[sample] = self.cost(candidates[sample], state, goal,
                                      obstacles, time)
            costs[sample] += self.temperature * np.sum(
                self.u * perturbations[sample] / self.noise**2)

        weights = np.full(self.samples, 1.0 / self.samples)
        # TODO Task 1.2: use exp(-(cost - min(costs)) / temperature), then normalize.

        # TODO Task 1.3: add weighted perturbations to self.u and clip its bounds.
        self.u = np.clip(self.u, self.lower, self.upper)

        cost = self.cost(self.u, state, goal, obstacles, time)
        control = self.u[0].copy()
        # TODO Task 1.4: shift self.u by one row; set the last row to zero.
        self.u[-1] = 0.0
        return control, cost

    def cost(self, controls, state, goal, obstacles=(), time=0.0):
        saved_state = self.model.state.copy()
        self.model.state = state.copy()
        try:
            cost = 0.0
            for step, control in enumerate(controls):
                # TODO Task 1.5: propagate the model and add dt * 10 * position error squared.
                state = self.model.state
                cost += 0.0

                # TODO Task 3.2: replace time with time + (step + 1) * dt.
                predicted_time = time
                for obstacle in obstacles:
                    center = obstacle_center(obstacle, predicted_time)
                    # TODO Task 2: add a finite safety-margin and collision penalty.
                    cost += 0.0

            # TODO Task 1.6: add terminal position and wrapped orientation error costs.
            cost += 0.0
            return cost
        finally:
            self.model.state = saved_state