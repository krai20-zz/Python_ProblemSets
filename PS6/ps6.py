# -*- coding: utf-8 -*-
# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """ 

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """

    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}
        for x in range(0, width):
            for y in range(0, height):
                self.tiles[(x, y)] = 'NotClean'

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        self.tiles[(x, y)] = 'Clean'

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.tiles[(m, n)] == 'Clean':
            return True
        else:
            return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.tiles)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        NumCleanTiles = 0
        for tile in self.tiles:
            if self.tiles[tile] == 'Clean':
                NumCleanTiles += 1
        return NumCleanTiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # return random.choice(self.tiles.keys())
        return Position(random.random() * self.width, random.random() * self.height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        return ((0<=x<self.width) and (0<=y<self.height))

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """

    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.direction = random.choice(range(361))
        self.position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.choice(range(361))


# test_robot = StandardRobot((5, 5), 1).updatePositionAndClean()
# print test_robot

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
   Runs NUM_TRIALS trials of the simulation and returns the mean number of
   time-steps needed to clean the fraction MIN_COVERAGE of the room.

   The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
   speed SPEED, in a room of dimensions WIDTH x HEIGHT.

   num_robots: an int (num_robots > 0)
   speed: a float (speed > 0)
   width: an int (width > 0)
   height: an int (height > 0)
   min_coverage: a float (0 <= min_coverage <= 1.0)
   num_trials: an int (num_trials > 0)
   robot_type: class of robot to be instantiated (e.g. Robot or
               RandomWalkRobot)
   """
    t = 0
    for trials in range(num_trials):     
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        Room = RectangularRoom(width, height)
        robots_collection = []
        for robots in range(num_robots):
            robots_collection.append(robot_type(Room, speed))
        while Room.getNumCleanedTiles() < min_coverage * float(Room.getNumTiles()):
            for i in robots_collection:
                i.updatePositionAndClean()
            t += 1
            #anim.update(Room, robots_collection)
        #anim.done()
    return t/num_trials

#print runSimulation(1, 1.0, 5, 5, 0.8, 30, StandardRobot)

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20�20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions
# 20�20, 25�16, 40�10, 50�8, 80�5, and 100�4?

def showPlot1(n=10):
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    n: an int (showing number of robots)
    """
    robots_collection = []
    for robots in range(1, n+1):
        robots_collection.append(robots)

    mean_simulation = []
    for robots in range(1, n+1):
        mean_simulation.append(runSimulation(robots, 1.0, 5, 5, 0.8, 30, StandardRobot))
    pylab.title("mean cleaning time depending on number of robots")
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Mean Cleaning Time")
    pylab.plot(robots_collection,mean_simulation)
    pylab.show()

def showPlot2():
    """
Produces a plot showing dependence of cleaning time on room shape.
"""
    area = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    mean_simulation = []
    ratio = []
    for width, height in area:
        mean_simulation.append(runSimulation(2, 1.0, width, height, 0.8, 30, StandardRobot))
        ratio.append(width/height)
    pylab.title("mean cleaning time depending on width/height ratio")
    pylab.xlabel("width/height ratio")
    pylab.ylabel("Mean Cleaning Time")
    pylab.plot(ratio, mean_simulation)
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
A RandomWalkRobot is a robot with the "random walk" movement strategy: it
chooses a new direction at random after each time-step.
"""

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        rand_dir = random.choice(range(361))
        self.setRobotDirection(rand_dir)
        new_position = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(self.position)

#print runSimulation(1, 1.0, 5, 5, 0.8, 10, RandomWalkRobot)

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3(n=10):
    """
Produces a plot comparing the two robot strategies.
"""
    robots_collection = []
    for robots in range(1, n+1):
        robots_collection.append(robots)

    mean_simulation_standardrobot = []
    for robots in range(1, n+1):
        mean_simulation_standardrobot.append(runSimulation(robots, 1.0, 5, 5, 0.8, 30, StandardRobot))

    mean_simulation_randomrobot = []
    for robots in range(1, n+1):
        mean_simulation_randomrobot.append(runSimulation(robots, 1.0, 5, 5, 0.8, 30, RandomWalkRobot))

    pylab.title("comparison of mean cleaning time depending on number of robots")
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Mean Cleaning Time for Standard and Random Walk Robot")
    pylab.plot(robots_collection, mean_simulation_standardrobot,label = 'StandardRobot')
    pylab.plot(robots_collection,mean_simulation_randomrobot, color = 'r',label = 'RandomWalkRobot')
    pylab.legend()
    pylab.show()

print showPlot3(5)