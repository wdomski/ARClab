import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "MPC"))
try:
    from ex.MPC.mpcFull import Circle, UnicycleModel
except ImportError:
    from ex.MPC.mpc import Circle, UnicycleModel


def obstacle_center(obstacle, time):
    return obstacle.center_at(time) if hasattr(obstacle, "center_at") else obstacle.center


def clearance(state, obstacles, time, safe=False):
    return min((np.linalg.norm(state[:2] - obstacle_center(obstacle, time))
                - (obstacle.radius_safe if safe else obstacle.radius)
                for obstacle in obstacles), default=np.inf)


def run(controller, start, goal, obstacles=(), max_steps=150):
    state = start.copy()
    path = [state.copy()]
    solution = []
    stats = {"time": [0.0], "cost": [], "reached": False,
             "clearance": [clearance(state, obstacles, 0.0)],
             "safe_clearance": [clearance(state, obstacles, 0.0, safe=True)]}
    for step in range(max_steps):
        angle = np.arctan2(np.sin(state[2] - goal[2]),
                           np.cos(state[2] - goal[2]))
        if np.linalg.norm(state[:2] - goal[:2]) < 0.15 and abs(angle) < 0.2:
            stats["reached"] = True
            break
        control, cost = controller.command(state, goal, obstacles,
                                           step * controller.dt)
        controller.model.state = state.copy()
        state = controller.model.step(control).copy()
        solution.append(control)
        path.append(state.copy())
        stats["time"].append((step + 1) * controller.dt)
        stats["cost"].append(cost)
        stats["clearance"].append(clearance(state, obstacles, stats["time"][-1]))
        stats["safe_clearance"].append(clearance(state, obstacles, stats["time"][-1],
                             safe=True))

    angle = np.arctan2(np.sin(state[2] - goal[2]),
                       np.cos(state[2] - goal[2]))
    stats["reached"] = (np.linalg.norm(state[:2] - goal[:2]) < 0.15
                        and abs(angle) < 0.2)
    return np.array(solution).reshape(-1, controller.model.m), np.array(path), stats


def plot(path, goal, obstacles, stats):
    fig, ax = plt.subplots()
    ax.plot(goal[0], goal[1], "bx")
    ax.quiver(goal[0], goal[1], np.cos(goal[2]), np.sin(goal[2]),
              angles="xy", scale_units="xy", scale=3)
    line, = ax.plot([], [], "b.-")
    warning, = ax.plot([], [], "yo")
    collision, = ax.plot([], [], "ko")
    robot = ax.quiver([0], [0], [0], [0],
                      angles="xy", scale_units="xy", scale=3)
    label = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")
    patches = []
    points = [path[:, :2], goal[None, :2]]
    for obstacle in obstacles:
        margin = plt.Circle(obstacle.center, obstacle.radius_safe, color="pink")
        body = plt.Circle(obstacle.center, obstacle.radius, color="red")
        ax.add_patch(margin)
        ax.add_patch(body)
        patches.append((obstacle, margin, body))
        points.append(np.array([obstacle_center(obstacle, time)
                                for time in stats["time"]]))
    points = np.vstack(points)
    padding = max([1.0] + [obstacle.radius_safe for obstacle in obstacles])
    ax.set_xlim(points[:, 0].min() - padding, points[:, 0].max() + padding)
    ax.set_ylim(points[:, 1].min() - padding, points[:, 1].max() + padding)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid(True)

    def update(frame):
        line.set_data(path[:frame + 1, 0], path[:frame + 1, 1])
        history = path[:frame + 1]
        unsafe = np.array(stats["safe_clearance"][:frame + 1]) <= 0
        collided = np.array(stats["clearance"][:frame + 1]) <= 0
        warning.set_data(history[unsafe & ~collided, 0], history[unsafe & ~collided, 1])
        collision.set_data(history[collided, 0], history[collided, 1])
        robot.set_offsets(path[frame, :2])
        robot.set_UVC([np.cos(path[frame, 2])], [np.sin(path[frame, 2])])
        for obstacle, margin, body in patches:
            center = obstacle_center(obstacle, stats["time"][frame])
            margin.center = center
            body.center = center
        label.set_text(f"t = {stats['time'][frame]:.1f} s")
        return line, warning, collision, robot, label

    interval = 1000 * (stats["time"][1] - stats["time"][0]) if len(path) > 1 else 200
    animation = FuncAnimation(fig, update, frames=len(path),
                              interval=interval, repeat=False)
    plt.show()
    return animation


def run_examples(controller_type, moving_circle_type):
    parser = argparse.ArgumentParser()
    parser.add_argument("--exercise", choices=("1", "2", "3", "all"), default="1")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--samples", type=int, default=128)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    exercises = ("1", "2", "3") if args.exercise == "all" else (args.exercise,)
    success = True
    for exercise in exercises:
        dt = 0.2
        start = np.array([0.0, 0.0, 0.0])
        goal = np.array([3.0, 1.0, 0.2])
        obstacles = []
        if exercise == "2":
            obstacles = [Circle(np.array([1.4, 0.45]), radius=0.3, safe_margin=0.25)]
        elif exercise == "3":
            obstacles = [moving_circle_type([1.5, 1.3], [0.0, -0.35],
                                             radius=0.3, safe_margin=0.25)]
        model = UnicycleModel(start.copy(), dt, R=0.05, L=0.06)
        controller = controller_type(model, dt=dt, samples=args.samples, seed=args.seed)
        solution, path, stats = run(controller, start, goal, obstacles)
        distance = np.linalg.norm(path[-1, :2] - goal[:2])
        minimum = min(stats["clearance"])
        print(f"Task {exercise}: reached={stats['reached']}, steps={len(solution)}, "
              f"distance={distance:.3f} m, min clearance={minimum:.3f} m")
        success = success and stats["reached"] and minimum > 0
        if not args.no_show:
            plot(path, goal, obstacles, stats)
    return success