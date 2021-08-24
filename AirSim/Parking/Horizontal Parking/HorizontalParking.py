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
    camera_pose_r = airsim.Pose(airsim.Vector3r(0.4, 0.9, 0.5), airsim.to_quaternion(0, 0, 1.3))  # PRY in radians
    client.simSetCameraPose(0, camera_pose_r);
    rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)

    if (rawImage is None):
        print("Camera is not returning image, please check airsim for error messages")
        airsim.wait_key("Press any key to exit")
        sys.exit(0)
    else:

        # right
        right=cam.get_right_camera2(client)
        # print("saved " + outputFile)
        car_controls.throttle = 0.4
        car_controls.steering = 0
        client.setCarControls(car_controls)

        if(right>20000 or right<2000):
            bool1 = True
            print("bool1 True")

        #parking detected
        if(bool1 and right>6000 and right<8000):
            bool2 = True
            print("bool2 True")
            car_controls.throttle = 0.2
            car_controls.steering = 0
            client.setCarControls(car_controls)

        if(bool1 and bool2 and (right>20000 or right<2000)):
            bool3 = True
            print("bool3 True")
            #slowdown


        if(bool1 and bool2 and bool3):
            print("start parking")
            time.sleep(1.75)
            car_controls.brake = 1
            car_controls.throttle = 0
            client.setCarControls(car_controls)
            back = cam.get_back_camera(client)
            right = cam.get_right_camera2(client)
            time.sleep(1)

            while (True):
            # while(right>7400 or right<7000) and (back>9400 or back<9200):
                #reverse rgiht

                car_controls.brake=0
                client.setCarControls(car_controls)
                car_controls.throttle = -0.3
                car_controls.is_manual_gear = True
                car_controls.manual_gear = -1
                car_controls.steering = 2.95
                client.setCarControls(car_controls)

                time.sleep(3.8)
                print("end right rev")
                back = cam.get_back_camera(client)
                right = cam.get_right_camera2(client)
            # print("****GOODVALUES****")
            # back = cam.get_back_camera(client)
            # right = cam.get_right_camera2(client)
            # while(right > 3100 or right < 2700 and back > 6950 or back < 6550):

                #drive reverse
                client.setCarControls(car_controls)
                car_controls.throttle = -0.3
                car_controls.is_manual_gear = True
                car_controls.manual_gear = -1
                car_controls.steering = 0
                client.setCarControls(car_controls)
                time.sleep(3.1)
                print("end forward rev")
                back = cam.get_back_camera(client)
                right = cam.get_right_camera2(client)
            #     # back = cam.get_back_camera(client)
            #     # right = cam.get_right_camera2(client)
            #
                #reverse left
                client.setCarControls(car_controls)
                car_controls.throttle = -0.3
                car_controls.is_manual_gear = True
                car_controls.manual_gear = -1
                car_controls.steering = -2.95
                client.setCarControls(car_controls)
                time.sleep(1.75)
                print("end left rev")

                # back = cam.get_back_camera(client)
                # right = cam.get_right_camera2(client)

                #breaks
                car_controls.brake = 1
                car_controls.throttle = 0
                client.setCarControls(car_controls)
                back = cam.get_back_camera(client)
                right = cam.get_right_camera2(client)
                time.sleep(2)
                car_controls.brake = 0

                car_controls.is_manual_gear = True
                car_controls.manual_gear = 1

                car_controls.steering = 3.1
                car_controls.throttle = 0.25
                client.setCarControls(car_controls)
                time.sleep(2.7)
                car_controls.brake = 1
                car_controls.throttle = 0
                client.setCarControls(car_controls)

                time.sleep(2)

                car_controls.brake = 0
                car_controls.steering = 0
                car_controls.throttle = 0
                client.setCarControls(car_controls)
                time.sleep(3)

                ########
                # check front > value
                # check back > value
                # drive forward
                print("start fixing")

                back = cam.get_back_camera1(client)
                front=cam.get_front_camera2(client)
                bool_1 = False
                bool_2 = False
                while back <2000 or back>20000 or front <2000 or front>20000:
                    print("in the while")
                    if back <2000 or back>20000:
                        print("in the 1")
                        back = cam.get_back_camera1(client)
                        front = cam.get_front_camera2(client)
                        while front >2000 and front<20000:
                            print("drive forward")
                            client.setCarControls(car_controls)
                            bool_2 = True
                            car_controls.throttle = 0.17

                            car_controls.is_manual_gear = True
                            car_controls.manual_gear = 1
                            car_controls.steering = 0
                            client.setCarControls(car_controls)
                            front = cam.get_front_camera2(client)
                            time.sleep(0.5)

                    if (bool_1 or bool_2):
                        car_controls.brake = 1
                        car_controls.throttle = 0
                        client.setCarControls(car_controls)
                        sys.exit(0)

                    if front <2000 or front>20000:
                        print("in the 2")
                        front = cam.get_front_camera2(client)
                        back = cam.get_back_camera1(client)
                        while back >2000 and back<20000:
                            print("drive backwards")
                            bool_1 = True
                            client.setCarControls(car_controls)
                            car_controls.throttle = -0.17
                            car_controls.is_manual_gear = True
                            car_controls.manual_gear = -1
                            car_controls.steering = 0
                            client.setCarControls(car_controls)
                            back = cam.get_back_camera1(client)
                            time.sleep(0.5)


                    if(bool_1 or bool_2):
                        car_controls.brake = 1
                        car_controls.throttle = 0
                        client.setCarControls(car_controls)
                        sys.exit(0)


                print("**** done parking ****")
                front = cam.get_front_camera2(client)
                back = cam.get_back_camera1(client)

                sys.exit(0)

            # if back<900:
                #     while(back<900):
                #         if(front<1000):
                #             car_controls.brake = 1
                #             car_controls.throttle = 0
                #             client.setCarControls(car_controls)
                #             break
                #     client.setCarControls(car_controls)
                #     car_controls.throttle = 0.1
                #     car_controls.is_manual_gear = True
                #     car_controls.manual_gear = 1
                #     car_controls.steering = 0
                #     client.setCarControls(car_controls)
                #     front = cam.get_front_camera2(client)
                #     back = cam.get_back_camera1(client)
                # ########
                # if front<1000:
                #     while front<1000:
                #         if(back<600):
                #             car_controls.brake = 1
                #             car_controls.throttle = 0
                #             client.setCarControls(car_controls)
                #             break
                #
                #     client.setCarControls(car_controls)
                #     car_controls.throttle = -0.1
                #     car_controls.is_manual_gear = True
                #     car_controls.manual_gear = -1
                #     car_controls.steering = 0
                #     client.setCarControls(car_controls)
                #     back = cam.get_back_camera1(client)
                #     front = cam.get_front_camera2(client)










                # back = cam.get_back_camera(client)
                # client.setCarControls(car_controls)
                # car_controls.throttle = -0.3
                # car_controls.is_manual_gear = True
                # car_controls.manual_gear = -1
                # car_controls.steering = 0
                # client.setCarControls(car_controls)
                # time.sleep(1)

                # break



        #PARK
        # if (right >9450) :
        #     print("turn right")
        #     print("turn right")
        #     # while (left > 18950 or left>20000):
        #     #     print("turning right\n")
        #     #     if left > 300:
        #     car_controls.steering = 2.95
        #     car_controls.throttle = 0.2
        #     #     else:
        #     #         print("right close")
        #     #
        #     #         car_controls.steering = 0.4
        #     #         car_controls.throttle = 0.25
        #     client.setCarControls(car_controls)
        #     time.sleep(2.4)



            # front=cam.get_front_camera1(client)
            # # while front<500 or front <20000:
            #
            # while front <10900:
            #     car_controls.steering = 0
            #     car_controls.throttle = 0.25
            #     client.setCarControls(car_controls)
            #     time.sleep(0.5)
            #     front = cam.get_front_camera(client)

            # print("parking complete")
            # car_controls.steering = 0
            # car_controls.throttle = 0.2
            # time.sleep(2)
            # car_controls.brake = 1
            # car_controls.throttle = 0
            # client.setCarControls(car_controls)
            # break

