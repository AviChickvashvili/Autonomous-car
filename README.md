# Autonomous-car

# Overview

In our final project we decided to create our own version of automonous car. <br>                                                            Our goals were to impart the car self-driving and self-parking abilities. <br>   The project was created by AirSim simulatur.



# AirSim

AirSim is a simulator for drones, cars and more, built on Unreal Engine. It is open-source, cross platform, and supports software-in-the-loop simulation with popular flight controllers such as PX4 & ArduPilot and hardware-in-loop with PX4 for physically and visually realistic simulations. It is developed as an Unreal plugin that can simply be dropped into any Unreal environment. 


We developed a way to control the car by using Airsim simulator cameras(such as DepthPerspective).
We impart abilities to the car such as self parking, Identify people who cross Pedestrian crossing, obstacle avoidanse and we test our code on new maps that we created.



# examples:


Identify people who cross Pedestrian crossing and emergency braking of the vehicle:

![crossroad](https://user-images.githubusercontent.com/57869913/130615178-372a3934-56d3-4a33-b50f-e83f90a29ef9.gif)


Identification of available parking (horizntal parking):

![horizontal](https://user-images.githubusercontent.com/57869913/130614000-14cc98d5-7884-4a8c-87d6-ea9c83cd42eb.gif)



# Prerequisites

* [Recommended hardware](https://wiki.unrealengine.com/Recommended_Hardware) for running UnrealEngine4, required
for AirSim.  Although it is possible build AirSim on OS X and Linux.

* [Python3](https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe) for 64-bit Windows


# Instructions

1. Clone this repository.
2. Open AirSim simulator.  
3. Choose the default car simulation. 
4. From the repository, choose a script that you want to run from "AirSim" folder (this folder, contains all the algorithem / script)
5. Run the script from pycharm and the car should start moving.






Example of using tensorflow app:

![3333333333333](https://user-images.githubusercontent.com/57190914/121053497-1c76d780-c7c4-11eb-9c5c-7448eaf7fae3.gif)


# participants

This code represents the final project at Ariel University:

* Meir Rozenfeld
* Avi Chickvashvili 
* Tomer Dvir 
