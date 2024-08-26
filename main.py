import os
import pybullet as p
import pybullet_data
import signal
import time

# Global flag for loop control
running = True

def signal_handler(sig, frame):
    global running
    print("SIGINT received, stopping the simulation.")
    running = False

# Associate SIGINT (Ctrl+C) with the handler function
signal.signal(signal.SIGINT, signal_handler)

# Ref: https://hackmd.io/@ziFYLStXQ765oLFwA4JjRg/rk1mqoY2_
# Connect to PyBullet GUI
"""
There are two modes to start the PyBullet simulator.
- p.GUI: Use for debugging and observing the motion of the robot.
- p.DIRECT: Faster execution speed. Use for model training.
The return value of `connect()` is an integer, representing the
ID of the simulation environment. If there are multiple environments,
then you can specific the environment via this ID.
"""
physicsClient = p.connect(
    p.GUI,
    options="--background_color_red=0.8 --background_color_green=1 --background_color_blue=0.9"
)
# Connect to pybullet_data path
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set Acceleration of Gravity
p.setGravity(0, 0, -9.8)

# Load the default plain
planeId = p.loadURDF("plane.urdf")

# Load our robot
robot_urdf = os.path.join(
    os.getcwd(),
    "Robot_v3_description",
    "urdf",
    "Robot_v3.xacro"
)
print(robot_urdf)
robot_id = p.loadURDF(robot_urdf, useFixedBase=True)

# Keep the simulation running for observation
while running:
    p.stepSimulation()
    number_of_joints = p.getNumJoints(robot_id)
    if os.getenv("DEBUG") is not None:
        os.system("clear")
        for joint_number in range(number_of_joints):
            info = p.getJointInfo(robot_id, joint_number)
            print(info[0], ": ", info[1])
    time.sleep(1 / 240)

# Disconnect
p.disconnect()
print("Simulation stopped.")
