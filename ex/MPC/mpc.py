from abc import ABCMeta
from abc import abstractmethod
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial

class Model:
    __metaclass__ = ABCMeta
    
    def __init__(self, state: np.array, dt: float) -> None:
        self._state = state     # vehicle state
        self._dt = dt           # time step
        
    @abstractmethod
    def step(self, u: np.array):
        pass
    
    @property
    def n(self):
        return len(self.state)
    
    @property
    @abstractmethod
    def m(self):
        pass
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state   
        
class UnicycleModel(Model):
    def __init__(self, state: np.array, dt: float, R: float, L: float) -> None:
        # state is vehicle state: x, y, theta
        super().__init__(state, dt)
        self.R = R             # wheel radius
        self.L = L             # half of axle length
    
    def step(self, u: np.array):
        # TODO given current state (self._state) and control inputs u
        # evaluate new state after time self._dt
        
        return self._state
        
    @property
    def m(self):
        return 2


class AckermanModel(Model):
    def __init__(self, state: np.array, dt: float, l: float) -> None:
        # state is vehicle state: x, y, theta
        super().__init__(state, dt)
        self.l = l             # wheel base
    
    def step(self, u: np.array):
        # TODO given current state (self._state) and control inputs u
        # evaluate new state after time self._dt
        
        return self._state
        
    @property
    def m(self):
        return 2

        
class Obstacle:
    __metaclass__ = ABCMeta
    
    def __init__(self, safe_margin=0.2) -> None:
        self._safe_margin = safe_margin
    
    @abstractmethod
    def distance(self, point: np.array):
        return 0
    
    @abstractmethod
    def inside(self, point: np.array):
        return False
    
    @abstractmethod
    def inside_safe(self, point: np.array):
        return False    
    
    @abstractmethod
    def plotType(self):
        return ""  
    
    @property
    def safe_margin(self):
        return self._safe_margin  
    
class Circle(Obstacle):
    
    def __init__(self, center: np.array, radius = 0.5, **kwargs) -> None:
        super().__init__(**kwargs)
        self._radius = radius
        self._center = center

    def distance(self, point: np.array):
        # TODO calculate distance to the center of circular obstacle
        distance = 0
        return distance
    
    def _inside(self, point: np.array, radius):
        distance =  self.distance(point)
        if distance <= radius:
            return True, distance
        return False, distance
    
    def inside(self, point: np.array):
        return self._inside(point, self._radius)
    
    def inside_safe(self, point: np.array):
        return self._inside(point, self._radius + self._safe_margin)
    
    def plotType(self):
        return "circle"
    
    @property
    def center(self):
        return self._center
    
    @property
    def radius(self):
        return self._radius
    
    @property
    def radius_safe(self):
        return self._radius + self._safe_margin
    
class Rectangle(Obstacle):
    
    def __init__(self, center: np.array, width=1, height=0.5, orientationDeg = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self._center = center
        self._width = width
        self._height = height
        self._orientationRad = orientationDeg * np.pi / 180
        
        self._points = self._calc_points()
        self._points_margin = self._calc_points(self._safe_margin)
        
    def _calc_points(self, margin = 0):
        half_width = (self._width + margin) / 2
        half_height = (self._height + margin) / 2
        points = np.zeros((4,2))
        points[0, 0] = self._center[0] + half_width * np.cos(self._orientationRad) - half_height * np.sin(self._orientationRad)
        points[0, 1] = self._center[1] + half_width * np.sin(self._orientationRad) + half_height * np.cos(self._orientationRad)
        points[1, 0] = self._center[0] - half_width * np.cos(self._orientationRad) - half_height * np.sin(self._orientationRad)
        points[1, 1] = self._center[1] - half_width * np.sin(self._orientationRad) + half_height * np.cos(self._orientationRad)
        points[2, 0] = self._center[0] - half_width * np.cos(self._orientationRad) + half_height * np.sin(self._orientationRad)
        points[2, 1] = self._center[1] - half_width * np.sin(self._orientationRad) - half_height * np.cos(self._orientationRad)
        points[3, 0] = self._center[0] + half_width * np.cos(self._orientationRad) + half_height * np.sin(self._orientationRad)
        points[3, 1] = self._center[1] + half_width * np.sin(self._orientationRad) - half_height * np.cos(self._orientationRad)
        return points
    
    def get_bottom_left(self):
        return self._points[2,:]
    
    def get_bottom_left_margin(self):
        return self._points_margin[2,:]

    def distance(self, point: np.array):
        diff = self._center - point[0:2]
        return np.sqrt(np.dot(diff, diff))
    
    def _inside(self, point: np.array, margin = 0):
        distance =  self.distance(point)
        
        # TODO
        # check if there is collision with the rectangle
        # for this you can use points, center of the rectangle 
        # or other technique

        return False, distance
    
    def inside(self, point: np.array):
        return self._inside(point)
    
    def inside_safe(self, point: np.array):
        return self._inside(point, self._safe_margin)
    
    def plotType(self):
        return "rectangle"
    
    @property
    def center(self):
        return self._center
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def orientationDeg(self):
        return self._orientationRad * 180 / np.pi  
    
    @property
    def orientationRad(self):
        return self._orientationRad

class MPC:
    def __init__(self, model: Model, T: float, dt: float) -> None:
        self.model = model
        self.T = T
        self.dt = dt
        
        self.model_state = None
        self._obstacles = []
        self._stats = {}
        
    def run(self, start: np.array, goal: np.array, obstacles = [], maxiter=100):
        """Run MPC algorithm

        Args:
            start (np.array): Initial point of dimension 3 (x, y, theta)
            goal (np.array): Goal pose of dimension 3 (x, y, theta)
            obstacles (list, optional): List of obstacles (derivatives of 
                Obstacle class). Defaults to [].
            maxiter (int, optional): Maximum number of iterations. Defaults to 100.

        Returns:
            tuple: Solution (control signals, path, statistic)
        """
        n = int(self.T / self.dt)
        u = np.zeros((n, self.model.m))
        self._goal = goal
        solution = []
        solution.append(u)
        path = []
        path.append(start)
        
        stats = {'step': [0], 'robot': [start], 'goal': goal, 'dt': self.dt, 
                 'distance': [0], 'angle': [0],
                 'cost': [0]}
        
        self._obstacles = obstacles
        
        m = self.model.m        
        # define bounds for control signals, upper and lower limit
        bounds = Bounds([-1, -0.5]*int(n//m), [1, 0.5]*int(n//m))
        
        state = start
        u = [0]*n
        
        previous_cost = np.inf
        earlyStop = -1
        
        for i in range(1, maxiter):
            self.model_state = state
            result = minimize(self.cost, u, method='SLSQP',
                constraints=[], options={'ftol': 1e-3, 'disp': False},
                bounds=bounds)
            # TODO
            # 1. Append m first points from the optimization solution
            # to the solution list
            
            
            # 2. Update model's state with current state
            
            
            # 3. Calculate next state of the model given 
            # latest control signals (at the end of solution list
            # which was updated in point 1.
            
            
            # 4. Save new state as new point on path
            # Append it to path list
            
            
            # 5. Preserve last vector of control input by
            # removing first m values from optimization result and 
            # assigning it to control input list u
            
            
            # 6. Extend control input list with m  
            # values, e.g. with m zeros
            
            # Statistics
            diff = state[0:2] - goal[0:2]
            distance = np.sqrt(np.dot(diff, diff))
            angle = (state[2] - goal[2]) / np.pi * 180
            stats['step'].append(i)
            stats['cost'].append(result.fun)
            stats['robot'].append(state)
            stats['distance'].append(distance)
            stats['angle'].append(angle)
            print(f"Step {i:05d}, cost {result.fun:.2f}\n"
                  f"robot: {state}, goal: {goal}\n"
                  f"distance: {distance:.2f}, angle diff: {angle:.2f}")
            
            # If the cost function is not dropping faster 
            # than some given value terminate calculation
            cost_diff = np.abs(previous_cost - result.fun)
            if cost_diff < 0.01:
                print("Early stop")
                earlyStop = i
                break
            previous_cost = result.fun
            
        # returning solution (list of control inputs)
        # and path (robot poses) and stats
        self._stats = stats
        return solution, path, stats 
            
        
    def cost(self, u: np.array) -> float:
        """Calculates cost function at given time
        provided control signals

        Args:
            u (np.array): Control signals

        Returns:
            float: Value of cost function
        """
        self.model.state = self.model_state
        
        m = self.model.m
        steps = len(u) // m
        cost = 0
        
        for i in range(0, steps):
            # iterate new state of the model
            # TODO: 1. run step on the model 
            # providing control signals
            
            # calculate distance to the goal
            # TODO: 2. calculate distance to goal based on 
            # newly evaluated state, and evaluate angle difference 
            # between current orientation and goal orientation
            
            # TODO: 3. using the distance to goal 
            # calculate cost and add it to overall 'cost'
            
            for obstacle in self._obstacles:
                pass
                # TODO: 4. evaluate possible collision with obstacles
                
        return cost
    
    def plot(self, path: list, goal: np.array, dt: float, animationFile=''):
        """Plot animated evolution of robot's state

        Args:
            path (list): List containing robot poses
            goal (np.array): Goal position
            dt (float): Time step

        Returns:
            _type_: None
        """
        path = np.array(path)
        frames = path.shape[0]
        fig, ax = plt.subplots()
        line_path, = ax.plot([], [], 'bo')
        line_safety, = ax.plot([], [], 'yo')
        line_collision, = ax.plot([], [], 'ko')
        line_vector = ax.quiver([0], [0], [0], [0], angles='xy', scale=1, scale_units='xy')
        line_stats = ax.text(-0.8,1.4, "Statistics")
        ax.plot(goal[0], goal[1], 'bx')
        ax.quiver(goal[0], goal[1], np.cos(goal[2]) * 0.5, np.sin(goal[2]) * 0.5, angles='xy', scale=1, scale_units='xy')
        ax.grid('both')

        def init():
            """Initialize plots

            Returns:
                _type_: None
            """
            ax.set_xlim(np.minimum(path[:,0].min(), goal[0]) - 1, np.maximum(path[:,0].max(), goal[0]) + 1)
            ax.set_ylim(np.minimum(path[:,1].min(), goal[1]) - 1, np.maximum(path[:,1].max(), goal[1]) + 1)
            ax.set_aspect('equal')
            
            for obstacle in self._obstacles:
                if obstacle.plotType() == "circle":
                    ax.add_patch(plt.Circle(obstacle.center, obstacle.radius + obstacle.safe_margin, color='pink'))
                    ax.add_patch(plt.Circle(obstacle.center, obstacle.radius, color='red'))
                elif obstacle.plotType() == "rectangle":
                    ax.add_patch(plt.Rectangle(obstacle.get_bottom_left_margin(), 
                                                obstacle.width + obstacle.safe_margin, 
                                                obstacle.height + obstacle.safe_margin, 
                                                obstacle.orientationDeg, color='pink'))
                    ax.add_patch(plt.Rectangle(obstacle.get_bottom_left(), 
                            obstacle.width, obstacle.height, obstacle.orientationDeg, color='red'))
                
            return line_path, line_vector, line_safety, line_collision, line_stats

        def update(frame, data):
            """Called every iteration
            Updates plots

            Args:
                frame (_type_): Frame time
                data (_type_): Dictionary of curves and datapoints.

            Returns:
                _type_: _description_
            """
            frame = int(frame)
            if frame == 0:
                # clear path
                data['path_x'].clear()
                data['path_y'].clear()
                data['safety_x'].clear()
                data['safety_y'].clear()
                data['collision_x'].clear()
                data['collision_y'].clear()
                
            safety = False
            collision = False
            for obstacle in self._obstacles:
                collision_local, _ = obstacle.inside(path[frame, :])
                safety_local, _ = obstacle.inside_safe(path[frame, :])
                
                if collision_local:
                    collision = True
                    break
                if safety_local:
                    safety = True
            
            violation_text = "No violation"
            if collision:
                data['collision_x'].append(path[frame, 0])
                data['collision_y'].append(path[frame, 1])
                violation_text = "Collision"
            elif not collision and safety:
                data['safety_x'].append(path[frame, 0])
                data['safety_y'].append(path[frame, 1])
                violation_text = "Safety margin"
            else:
                data['path_x'].append(path[frame, 0])
                data['path_y'].append(path[frame, 1])            
            
            data['path'].set_data(data['path_x'], data['path_y'])
            data['collision'].set_data(data['collision_x'], data['collision_y'])
            data['safety'].set_data(data['safety_x'], data['safety_y'])
            
            point = path[frame, 0:2]
            if frame < len(path)-1:
                point2 = path[frame+1, 0:2] 
            else:
                point2 = point
            scale = (point2 - point) * 4
            
            data['vector'].set_offsets(point)
            data['vector'].set_UVC([scale[0]], [scale[1]])
            
            if self._stats:
                data['stats'].set_text(f"Step: {frame}\n"
                                       f"Distance: {self._stats['distance'][frame]:.2f}, "
                                       f"Angle diff: {self._stats['angle'][frame]:.1f}\n"
                                       f"{violation_text}")
            
            return data['path'], data['vector'], data['safety'], data['collision'], data['stats']

        data = {'path': line_path, 'path_x': [], 'path_y' : [],
                'safety': line_safety, 'safety_x': [], 'safety_y': [],
                'collision': line_collision, 'collision_x': [], 'collision_y': [],
                'vector': line_vector,
                'stats': line_stats}
        
        repeat = True
        if animationFile:
           repeat = False 
        animation = FuncAnimation(fig, partial(update, data=data), 
                            frames=np.linspace(0, frames-1, frames),
                            init_func=init, blit=True,
                            interval = dt,
                            repeat = repeat)
        if animationFile:
            animation.save(animationFile, fps=1)
        plt.show()
            