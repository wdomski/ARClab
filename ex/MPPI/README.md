This course is prepared by Wojciech Domski.
All rights reserved.

# Model Predictive Path Integral control

Implement MPPI for the kinematic unicycle, then extend the same controller
with static and moving circular obstacles. Complete the numbered `TODO`
sections in `mppi.py`, replacing the placeholder values. The instructor's
working reference is `mppiFull.py`; it is not needed in student-only copies.

The state is $[x,y,\theta]$ and the input is $[v,\omega]$. The simulator first
tries the unicycle model and circular obstacle geometry from
`../MPC/mpcFull.py`, falling back to `../MPC/mpc.py` if the reference cannot
be imported. In student-only copies, the reused MPC model and geometry TODOs
must already be completed. The robot is a point; the obstacle safety margin
can account for its physical size.

## Running

From the repository root, install the existing MPC dependencies and run Task 1:

```bash
.venv/Scripts/python -m pip install -r ex/MPPI/requirements.txt
.venv/Scripts/python ex/MPPI/run.py --exercise 1
```

Use `--exercise 2` or `--exercise 3` for the subsequent tasks. Test all
reference solutions without opening plot windows with:

```bash
.venv/Scripts/python ex/MPPI/runFull.py --exercise all --seed 0 --no-show
```

Omit `--no-show` to animate the robot and obstacles. Yellow points mark safety
margin violations; black points mark collisions. The summary reports physical
clearance at simulated poses, excluding the safety margin. The runner exits
with a nonzero status if a task does not reach the goal or a sampled pose collides.
The unfinished student version runs with zero perturbations, uniform weights,
zero costs, and stationary obstacle predictions. It leaves the robot still and
reports non-convergence until the TODOs are completed, without raising TODO
exceptions.

`run.py` prefers `mppi.py` and falls back to `mppiFull.py` on an import error.
`runFull.py` tries them in the opposite order. Both runners can therefore be
used without any `Full.py` files in a student-only copy.

## MPPI algorithm

Keep a nominal input sequence $U$ of shape $(N,2)$, where $N=T/dt$.
For each of $K$ rollouts, sample independent Gaussian perturbations
$\epsilon_{k,i}\sim\mathcal{N}(0,\Sigma)$, with
$\Sigma=\operatorname{diag}(\sigma_v^2,\sigma_\omega^2)$, and simulate
$V_{k,i}=\operatorname{clip}(U_i+\epsilon_{k,i},u_{\min},u_{\max})$.
Every rollout starts from the same current robot state.

The rollout score includes the control/noise importance-sampling term:

$$S_k=\phi(x_N^k)+dt\sum_{i=0}^{N-1}q(x_{i+1}^k,t+(i+1)dt)
+\lambda\sum_{i=0}^{N-1}U_i^T\Sigma^{-1}\epsilon_{k,i}.$$

This supplied correction is part of MPPI, not an obstacle penalty. Use
numerically stable normalized weights and update the whole input sequence:

$$w_k=\frac{\exp(-(S_k-\min_j S_j)/\lambda)}
{\sum_l\exp(-(S_l-\min_j S_j)/\lambda)},\qquad
U_i\leftarrow\operatorname{clip}\left(U_i+\sum_k w_k\epsilon_{k,i},
u_{\min},u_{\max}\right).$$

Apply only the first input, shift the sequence by one row, append a zero row,
and repeat from the new measured state. This is a practical bounded MPPI
variant: clipping approximates the unconstrained Gaussian formulation.

Defaults: $dt=0.2$ s, $T=4$ s, $K=128$, $\lambda=0.5$,
$\sigma_v=0.6$, $\sigma_\omega=1.0$, $|v|\leq1$ m/s,
$|\omega|\leq1$ rad/s. Change the rollout count with `--samples` and
the random seed with `--seed`. Other parameters are in the constructor.
The controller does not call a numerical optimizer; SciPy is installed only
because the reused MPC module imports it.

# Task 1 -- unicycle in free space

Complete only the `Task 1` gaps; leave the obstacle gaps for later:

1. **1.1:** sample Gaussian perturbations using `self.rng` and `self.noise`.
2. **1.2:** compute and normalize the exponential weights.
3. **1.3:** add the weighted perturbations to `self.u` and clip the inputs.
4. **1.4:** shift the nominal sequence after selecting the first input.
5. **1.5:** propagate the supplied model and accumulate the running cost.
6. **1.6:** add the terminal cost, wrapping orientation error to $[-\pi,\pi]$.

Use the position error $e_p=[x,y]-[x_g,y_g]$ and
$e_\theta=\operatorname{atan2}(\sin(\theta-\theta_g),\cos(\theta-\theta_g))$:

$$q=10\|e_p\|^2,\qquad \phi=30\|e_p\|^2+5e_\theta^2.$$

The simulator supplies the robot step, history collection, and termination:
position error below 0.15 m and absolute orientation error below 0.2 rad.
The cost function restores the real model state after every rollout.
Compare convergence and control variation for different $K$, $\lambda$,
noise scales, and seeds. Do not stop on small changes of a random rollout cost.

# Task 2 -- static obstacles

Retain Task 1 and complete the `Task 2` block in `MPPI.cost()`.
The provided `Circle` already supplies the center, radius $r$, and inflated
radius $r_s=r+\text{safe margin}$. For distance $d$ to its center, add:

$$q_{\mathrm{obs}}=1000\max(0,r_s-d)^2+1000\mathbf{1}_{d\leq r}.$$

Include this term in the running cost with the same factor $dt$ and sum it
over all obstacles at every prediction step. It is finite even at the center.
Run Task 2 and compare the path with Task 1. Add another circle in the supplied
scenario and change the margin and penalty weights.

These are soft penalties: reaching the goal does not guarantee collision-free
motion or respect for the safety margin. Inspect the clearance and colored
trajectory points, not just the final position.

# Task 3 -- dynamic obstacles

Retain Tasks 1 and 2. The third scenario uses a circle crossing the robot's
route with a known, constant velocity.

1. **3.1:** complete `MovingCircle.center_at(time)` using
   $c(t)=c_0+v_{\mathrm{obs}}t$. Return a prediction without modifying $c_0$.
2. **3.2:** use the absolute future time $t+(i+1)dt$ when scoring the
   post-step robot state. Using only the current time freezes the obstacle
   during the rollout and does not predict a future collision.

The simulator and animation use the same prediction method and absolute
clock, starting at zero. Do not advance obstacles while sampling rollouts.
With zero obstacle velocity, the controller must reproduce static-obstacle
costs. Compare future predictions against frozen obstacle positions using the
same seed, and investigate the effect of prediction horizon and obstacle speed.

## Files

- `mppi.py` -- student controller and moving-obstacle prediction.
- `mppiFull.py` -- complete implementations of the same classes.
- `simulator.py` -- supplied MPC imports, scenarios, simulation, and animation.
- `run.py` / `runFull.py` -- student / reference runners.
- `requirements.txt` -- reuses MPC's dependency list; no new packages.