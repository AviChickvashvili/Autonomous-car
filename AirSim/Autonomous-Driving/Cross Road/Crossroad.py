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

bool1 = False
bool2 = False
bool3 = False


global_front = 1
global_left = 1
global_right = 1
while True:
    car_state = client.getCarState()
    camera_pose_r = airsim.Pose(airsim.Vector3r(0.8, 0, 0.5), airsim.to_quaternion(0, 0, 0))  # PRY in radians
    client.simSetCameraPose(0, camera_pose_r);
    rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)

    if (rawImage is None):
        print("Camera is not returning image, please check airsim for error messages")
        airsim.wait_key("Press any key to exit")
        sys.exit(0)
    else:
        # right
         flag = False
         while True and flag==False:

            front=cam.get_front_camera(client)
            # print("saved " + outputFile)
            if front >= 3550 :
                car_controls.brake = 0
                car_controls.throttle = 0.4
                car_controls.steering = 0
                client.setCarControls(car_controls)
                # time.sleep(12)
                # sys.exit(0)
            else:
                print("emergency brake! people in the front")
                car_controls.brake = 1
                car_controls.throttle = 0
                client.setCarControls(car_controls)
                front = cam.get_front_camera(client)
                flag =True

         while True :
            time.sleep(15)
            front = cam.get_front_camera(client)
            print("The road is clear , please continue")
            if front>3000:
                car_controls.brake = 0
                car_controls.throttle = 0.4
                car_controls.steering = 0
                client.setCarControls(car_controls)
                time.sleep(1.5)

            # front = cam.get_front_camera(client)
            # if front >10700:
            #     car_controls.steering = -2.95
            #     car_controls.throttle = 0.4
            #     client.setCarControls(car_controls)
            #     time.sleep(2.1)
            #     car_controls.steering = 0
            #     car_controls.throttle = 0.4
            #     client.setCarControls(car_controls)
            #     time.sleep(100)
                # time.sleep(5)
                # car_controls.throttle = 0.4
                # car_controls.steering = 0
                # client.setCarControls(car_controls)

    # while True:
        #     front=cam.get_front_camera(client)
        #     # sys.exit(0)
















        #
        #
        #
        # if(right>20000 or right<2000):
        #     bool1 = True
        #     print("bool1 True")
        #
        # #parking detected
        # if(bool1 and right>7000 and right<9000):
        #     bool2 = True
        #     print("bool2 True")
        #     car_controls.throttle = 0.2
        #     car_controls.steering = 0
        #     client.setCarControls(car_controls)
        #
        # if(bool1 and bool2 and (right>20000 or right<2000)):
        #     bool3 = True
        #     print("bool3 True")
        #     #slowdown
        #
        #
        # if(bool1 and bool2 and bool3):
        #     print("start parking")
        #     time.sleep(1.6)
        #     car_controls.brake = 1
        #     car_controls.throttle = 0
        #     client.setCarControls(car_controls)
        #     time.sleep(1)
        #     back = cam.get_back_camera(client)
        #     right = cam.get_right_camera2(client)
        #
        #     while (right > 4500 or right<7600) and back>9386 :
        #         #reverse rgiht
        #
        #         car_controls.brake=0
        #         client.setCarControls(car_controls)
        #         car_controls.throttle = -0.3
        #         car_controls.is_manual_gear = True
        #         car_controls.manual_gear = -1
        #         car_controls.steering = 2.95
        #         client.setCarControls(car_controls)
        #
        #         # time.sleep(3.7)
        #         print("end right rev")
        #         back = cam.get_back_camera(client)
        #         right = cam.get_right_camera2(client)
        #     # print("****GOODVALUES****")
        #     # back = cam.get_back_camera(client)
        #     # right = cam.get_right_camera2(client)
        #
        #     print("2ND while")
        #     while right > 3500  and back > 6400 :
        #
        #         #drive reverse
        #
        #
        #         client.setCarControls(car_controls)
        #         car_controls.throttle = -0.3
        #         car_controls.is_manual_gear = True
        #         car_controls.manual_gear = -1
        #         car_controls.steering = 0
        #         client.setCarControls(car_controls)
        #         # time.sleep(3)
        #         print("end reverse rev")
        #         back = cam.get_back_camera(client)
        #         right = cam.get_right_camera2(client)
        #     #     # back = cam.get_back_camera(client)
        #     #     # right = cam.get_right_camera2(client)
        #     #
        #
        #     print("3RD while")
        #     while (right<5000 or right > 2900)  and back > 5120 :
        #
        #         #reverse left
        #         client.setCarControls(car_controls)
        #         car_controls.throttle = -0.3
        #         car_controls.is_manual_gear = True
        #         car_controls.manual_gear = -1
        #         car_controls.steering = -2.95
        #         client.setCarControls(car_controls)
        #         # time.sleep(1.6)
        #         print("end left rev")
        #         back = cam.get_back_camera(client)
        #         right = cam.get_right_camera2(client)
        #         # back = cam.get_back_camera(client)
        #         # right = cam.get_right_camera2(client)
        #
        #         #breaks
        #     car_controls.brake = 1
        #     car_controls.throttle = 0
        #     client.setCarControls(car_controls)
        #     time.sleep(1.5)
        #     sys.exit(0)
        #
        #     ########
        #         # check front > value
        #         # check back > value
        #         # drive forward
        #         ########
        #
        #
        #         # back = cam.get_back_camera(client)
        #         # client.setCarControls(car_controls)
        #         # car_controls.throttle = -0.3
        #         # car_controls.is_manual_gear = True
        #         # car_controls.manual_gear = -1
        #         # car_controls.steering = 0
        #         # client.setCarControls(car_controls)
        #         # time.sleep(1)
        #
        #         # break
        #
        #
        #
        # #PARK
        # # if (right >9450) :
        # #     print("turn right")
        # #     print("turn right")
        # #     # while (left > 18950 or left>20000):
        # #     #     print("turning right\n")
        # #     #     if left > 300:
        # #     car_controls.steering = 2.95
        # #     car_controls.throttle = 0.2
        # #     #     else:
        # #     #         print("right close")
        # #     #
        # #     #         car_controls.steering = 0.4
        # #     #         car_controls.throttle = 0.25
        # #     client.setCarControls(car_controls)
        # #     time.sleep(2.4)
        #
        #
        #
        #     # front=cam.get_front_camera1(client)
        #     # # while front<500 or front <20000:
        #     #
        #     # while front <10900:
        #     #     car_controls.steering = 0
        #     #     car_controls.throttle = 0.25
        #     #     client.setCarControls(car_controls)
        #     #     time.sleep(0.5)
        #     #     front = cam.get_front_camera(client)
        #
        #     # print("parking complete")
        #     # car_controls.steering = 0
        #     # car_controls.throttle = 0.2
        #     # time.sleep(2)
        #     # car_controls.brake = 1
        #     # car_controls.throttle = 0
        #     # client.setCarControls(car_controls)
        #     # break

