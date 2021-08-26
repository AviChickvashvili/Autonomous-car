This repository contains Python scripts showing how you can use AirSim and create your own Autonomous car -
from moving vehicle by itself, then use the built in cameras images (such as Scene, DepthPerspective, Segmentation) and use the data for Autonomous parking.  


# Instructions

1. Clone this repository.
2. Open AirSim simulator.  
3. Choose the default car simulation. 
4. From the repository, choose a script that you want to run from "AirSim" folder (this folder, contains all the algorithem / script)
5. Run the script from pycharm and the car should start moving.

# Project process

First, we placed three cameras on the vehicle in the relevant locations for environmental detection (right, left, and straight).
The image was processed using opencv (to convert the images to point cloud).
Using point cloud, we used a distance formula to estimate the distance of the objects from the vehicle.
In this method, we were able to identify available parking, autonomous capabilities, and emergency braking at a crosswalk.



In the first step, we estimated the distance by the front camera, so the vehicle brakes when close to the object:

![brake_front](https://user-images.githubusercontent.com/57869913/130597386-016d217d-1dc1-43a1-b24f-48e95a01f2a5.gif)

![crossroad](https://user-images.githubusercontent.com/57869913/130615178-372a3934-56d3-4a33-b50f-e83f90a29ef9.gif)


Then, using the side cameras (right and left), we estimated the distance from the sides, and if necessary a correction was made:

![ezgif com-gif-maker](https://user-images.githubusercontent.com/57869913/130595095-b2ac7603-7634-4293-870e-24e7dd42a554.gif)

# Parking process

Once the vehicle was fitted with autonomous capabilities, the next step was to impart self-parking capability.


In the first stage, the vehicle detects available parking (right and left) and parks forward: <br>
![right park](https://user-images.githubusercontent.com/57869913/130614997-d20b8228-c98d-4006-86c6-56c5ba6ed54e.gif) ![left park](https://user-images.githubusercontent.com/57869913/130614516-51fc4e8b-9974-4511-aa79-7693df35bfdc.gif)



Then, based on the availability of available parking, the vehicle enters a parking lot in reverse: <br>
![ezgif com-gif-maker](https://user-images.githubusercontent.com/57869913/130614870-6a9cd96b-11d6-472c-b61c-8687e3e95484.gif)


Once vertical parking has been achieved, it now remains to park horizontally to the road: <br>
![horizontal](https://user-images.githubusercontent.com/57869913/130614000-14cc98d5-7884-4a8c-87d6-ea9c83cd42eb.gif)





