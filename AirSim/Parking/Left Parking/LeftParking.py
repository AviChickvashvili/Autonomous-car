# use open cv to create point cloud from depth image.
from __future__ import division
import airsim

import cv2
import time
import sys
import math
import numpy as np
import camera as cam






# file will be saved in PythonClient folder (i.e. same folder as script)
# point cloud ASCII format, use viewers like CloudCompare http://www.danielgm.net/cc/ or see http://www.geonext.nl/wp-content/uploads/2014/05/Point-Cloud-Viewers.pdf
outputFile = "cloud.asc"
color = (0, 255, 0)
rgb = "%d %d %d" % color
projectionMatrix = np.array([[-0.501202762, 0.000000000, 0.000000000, 0.000000000],
                             [0.000000000, -0.501202762, 0.000000000, 0.000000000],
                             [0.000000000, 0.000000000, 10.00000000, 100.00000000],
                             [0.000000000, 0.000000000, -10.0000000, 0.000000000]])


client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

global_front = 1
global_left = 1
global_right = 1
while True:
    car_state = client.getCarState()
    camera_pose_l = airsim.Pose(airsim.Vector3r(0.4, -2, 0.5), airsim.to_quaternion(0, 0, -1.3))  # PRY in radians
    client.simSetCameraPose(0, camera_pose_l);
    rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)

    if (rawImage is None):
        print("Camera is not returning image, please check airsim for error messages")
        airsim.wait_key("Press any key to exit")
        sys.exit(0)
    else:

        # left
        left=cam.get_left_camera1(client)
        # print("saved " + outputFile)
        car_controls.throttle = 0.4
        car_controls.steering = 0
        client.setCarControls(car_controls)
        #PARK
        if (left <2650) :
            print("turn left")
            print("turn left")
            # while (left > 18950 or left>20000):
            #     print("turning right\n")
            #     if left > 300:
            car_controls.steering = -2.95
            car_controls.throttle = 0.2
            #     else:
            #         print("right close")
            #
            #         car_controls.steering = 0.4
            #         car_controls.throttle = 0.25
            client.setCarControls(car_controls)
            time.sleep(2.4)



            front=cam.get_front_camera(client)
            while front<500 or front <20000:
                car_controls.steering = 0
                car_controls.throttle = 0.25
                client.setCarControls(car_controls)
                time.sleep(0.5)
                front = cam.get_front_camera(client)

            print("parking complete")
            car_controls.steering = 0
            car_controls.throttle = 0.2
            time.sleep(2.5)
            car_controls.brake = 1
            car_controls.throttle = 0
            client.setCarControls(car_controls)
            break



            # while(1):
            #     print("park")
            #     car_controls.steering = 0
            #     car_controls.throttle = 0.25
            #     client.setCarControls(car_controls)
            #     time.sleep(0.50)
            #     car_state = client.getCarState()
            #     camera_pose_l = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, 0))  # PRY in radians
            #     client.simSetCameraPose(0, camera_pose_l);
            #     rawImage = client.simGetImage("front_center", airsim.ImageType.DepthPerspective)
            #     png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
            #     gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
            #     Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
            #     front = savePointCloud(Image3D, outputFile, 0)
                # if (front < 100):
                #     client.enableApiControl(True)
                #     print("Emergancy Brake")
                #     car_controls.brake = 1
                #     car_controls.throttle = 0
                #     client.setCarControls(car_controls)
            #     camera_pose_l = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, -1.2))  # PRY in radians
            #     client.simSetCameraPose(0, camera_pose_l);
            #     rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
            #     png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
            #     gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
            #     Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
            #     left = savePointCloud(Image3D, outputFile, 1)
            # #     try
            #     camera_pose_r = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, 1.2))  # PRY in radians
            #     client.simSetCameraPose(0, camera_pose_r);
            #     rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
            #     png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
            #     gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
            #     Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
            #     right = savePointCloud(Image3D, outputFile, 2)
            #     if right < 600:
            #         client.enableApiControl(True)
            #         print("Caution left!!")
            #         # car_controls.brake = 1
            #         car_controls.throttle = 0
            #         client.setCarControls(car_controls)
            #         time.sleep(1)
            #         car_controls.brake = 0
            #         car_controls.throttle = 0.2
            #         client.setCarControls(car_controls)
            #     else:
            #         car_controls.steering = 0.1
            #         car_controls.throttle = 0.2
            #         client.setCarControls(car_controls)
            #         time.sleep(0.50)

