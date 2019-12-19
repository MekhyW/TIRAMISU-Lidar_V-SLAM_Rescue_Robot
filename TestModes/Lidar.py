import time
import math
import PyLidar3
Sweeper = PyLidar3.YdLidarX4('COM6', 6000)
Sweeper.Connect()
SWEEPER_GENERATOR = Sweeper.StartScanning()
t = time.time()
while time.time()-t < 2:
    lidardata = next(SWEEPER_GENERATOR)
    for angle in range(0, 360):
        print(lidardata[angle], angle)
Sweeper.StopScanning()
Sweeper.Disconnect()