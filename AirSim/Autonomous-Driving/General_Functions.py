# use open cv to create point cloud from depth image.
from __future__ import division
import airsim

import cv2
import time
import sys
import math
import numpy as np

############################################
########## This is work in progress! #######
############################################

def distance(point_cloud,num):
    global global_front
    global global_left
    global global_right

    x_avg = 0
    y_avg = 0
    z_avg = 0
    # for i in range (len(point_cloudX)):
    #     x_avg+= point_cloudX[i]
    #     y_avg += point_cloudY[i]
    #     z_avg += point_cloudZ[i]
    for i in range (len (point_cloud) -3):
        x_avg += point_cloud[i]
        y_avg += point_cloud[i+1]
        z_avg += point_cloud[i+2]
        i+=3
    if (len (point_cloud))==0 and num==0:
        return global_front
    elif (len (point_cloud))==0 and num==1:
        return global_left
    elif (len (point_cloud))==0 and num==2:
        return global_right

    ans = ((x_avg/3) ** 2 +  (y_avg/3)** 2 + (z_avg/3) ** 2 )
    # ans = ((x_avg / 3) ** 2 + (y_avg / 3) ** 2)

    f_ans = math.sqrt(ans)
    if num == 0:
        global_front = f_ans
    elif num == 1:
        global_left = f_ans
        print("left  ",f_ans)
        return f_ans
    elif num == 2:
        global_right = f_ans
        print("right  ",f_ans)
        return f_ans
    print("front  ",f_ans)
    return f_ans





# file will be saved in PythonClient folder (i.e. same folder as script)
# point cloud ASCII format, use viewers like CloudCompare http://www.danielgm.net/cc/ or see http://www.geonext.nl/wp-content/uploads/2014/05/Point-Cloud-Viewers.pdf
outputFile = "cloud.asc"
color = (0, 255, 0)
rgb = "%d %d %d" % color
projectionMatrix = np.array([[-0.501202762, 0.000000000, 0.000000000, 0.000000000],
                             [0.000000000, -0.501202762, 0.000000000, 0.000000000],
                             [0.000000000, 0.000000000, 10.00000000, 100.00000000],
                             [0.000000000, 0.000000000, -10.0000000, 0.000000000]])


def printUsage():
    print("Usage: python point_cloud.py [cloud.txt]")


def savePointCloud(image, fileName,num):
    xarr =[]
    yarr=[]
    zarr=[]

    f = open(fileName, "w")
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            pt = image[x, y]
            if (math.isinf(pt[0]) or math.isnan(pt[0])):
                # skip it
                None
            else:
                xarr.append(pt[0])
                xarr.append(pt[1])
                xarr.append(pt[2])
                # yarr.append(pt[1])
                # zarr.append(pt[2]-1)

                f.write("%f %f %f %s\n" % (pt[0], pt[1], pt[2] - 1, rgb))
    f.close()
    return distance(xarr,num)



for arg in sys.argv[1:]:
    avi = arg

client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

global_front = 1
global_left = 1
global_right = 1
while True:
    car_state = client.getCarState()
    camera_pose_l = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, 0))  # PRY in radians
    client.simSetCameraPose(0, camera_pose_l);
    rawImage = client.simGetImage("front_center", airsim.ImageType.DepthPerspective)
    if (rawImage is None):
        print("Camera is not returning image, please check airsim for error messages")
        airsim.wait_key("Press any key to exit")
        sys.exit(0)
    else:
        png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
        Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
        front=savePointCloud(Image3D, outputFile,0)

        # right
        camera_pose_r = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, 1.2))  # PRY in radians
        client.simSetCameraPose(0, camera_pose_r);
        rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
        png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
        Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
        right=savePointCloud(Image3D, outputFile,2)

        # left
        camera_pose_l = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, -1.2))  # PRY in radians
        client.simSetCameraPose(0, camera_pose_l);
        rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
        png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
        Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
        left=savePointCloud(Image3D, outputFile,1)
        # print("saved " + outputFile)
        car_controls.throttle = 0.4
        car_controls.steering = 0
        client.setCarControls(car_controls)

        if (left < 600) or (left>20000):
            while (left < 600 or left>20000):
                print("turning right\n")
                if left > 300:
                    car_controls.steering = 0.2
                    car_controls.throttle = 0.3
                else:
                    print("right close")

                    car_controls.steering = 0.4
                    car_controls.throttle = 0.25
                client.setCarControls(car_controls)
                time.sleep(0.50)
                camera_pose_l = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, -1.2))  # PRY in radians
                client.simSetCameraPose(0, camera_pose_l);
                rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
                png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
                gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
                Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
                left = savePointCloud(Image3D, outputFile, 1)
            #     try
                camera_pose_r = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, 1.2))  # PRY in radians
                client.simSetCameraPose(0, camera_pose_r);
                rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
                png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
                gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
                Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
                right = savePointCloud(Image3D, outputFile, 2)
                if right < 600:
                    client.enableApiControl(True)
                    print("Caution left!!")
                    # car_controls.brake = 1
                    car_controls.throttle = 0
                    client.setCarControls(car_controls)
                    time.sleep(1)
                    car_controls.brake = 0
                    car_controls.throttle = 0.2
                    client.setCarControls(car_controls)
                else:
                    car_controls.steering = 0.1
                    car_controls.throttle = 0.2
                    client.setCarControls(car_controls)
                    time.sleep(0.50)

        if (right < 600) or (right>20000):
            while (right < 600 or right>20000):
                print("turning left\n")
                if right > 300:
                    car_controls.steering = -0.2
                    car_controls.throttle = 0.3
                else:
                    print("left close")
                    car_controls.steering = -0.4
                    car_controls.throttle = 0.25
                client.setCarControls(car_controls)
                time.sleep(0.50)
                camera_pose_r = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, 1.2))  # PRY in radians
                client.simSetCameraPose(0, camera_pose_r);
                rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
                png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
                gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
                Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
                right = savePointCloud(Image3D, outputFile, 2)
            #     try
                camera_pose_l = airsim.Pose(airsim.Vector3r(0.8, 0, 0), airsim.to_quaternion(0, 0, -1.2))  # PRY in radians
                client.simSetCameraPose(0, camera_pose_l);
                rawImage = client.simGetImage("0", airsim.ImageType.DepthPerspective)
                png = cv2.imdecode(np.frombuffer(rawImage, np.uint8), cv2.IMREAD_UNCHANGED)
                gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
                Image3D = cv2.reprojectImageTo3D(gray, projectionMatrix)
                left = savePointCloud(Image3D, outputFile, 1)
                if left < 600:
                    client.enableApiControl(True)
                    print("Caution right!!")
                    # car_controls.brake = 1
                    car_controls.throttle = 0
                    client.setCarControls(car_controls)
                    time.sleep(1)
                    car_controls.brake = 0
                    car_controls.throttle = 0.2
                    client.setCarControls(car_controls)
                else:
                    car_controls.steering = -0.1
                    car_controls.throttle = 0.2
                    client.setCarControls(car_controls)
                    time.sleep(0.50)
        if (front < 200):
            client.enableApiControl(True)
            print("Emergancy Brake")
            car_controls.brake = 1
            car_controls.throttle = 0
            client.setCarControls(car_controls)
            # time.sleep(2)
    # key = cv2.waitKey(1) & 0xFF;
    # if (key == 27 or key == ord('q') or key == ord('x')):
    #     break;