This repository contains Python scripts showing how you can use AirSim and create your own Autonomous car -
from moving vehicle by itself, then use the built in cameras images (such as Scene, DepthPerspective, Segmentation) and use the data for Autonomous parking.  

# Prerequisites

* [Recommended hardware](https://wiki.unrealengine.com/Recommended_Hardware) for running UnrealEngine4, required
for AirSim.  Although it is possible build AirSim on OS X and Linux.

* [Python3](https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe) for 64-bit Windows


# Instructions

1. Clone this repository.
2. Open AirSim simulator.  
3. When prompted, go with the default car simulation. 
4. From the repository, run the <b>image_collection.py</b> script.  It will start the car moving and stop when the
car collides with the fence, creating a <b>carpix</b> folder containing the images on which you will train 
the network in the next step.
5. From the repository, run the <b>collision_training.py</b> script.  Running on an HP Z440 workstation with 
NVIDIA GeForce GTX 1080 Ti GPU, we were able to complete the 500 training iterations in a few seconds.
6. From the repository, run the <b>collision_testing.py</b> script.  This should drive the car forward as before, but 
but the car should stop right before it hits the fence, based on the collision predicted by the neural net.

# How it works

The <b>image_collection</b> script maintains a queue of the ten most recent images and saves them to numbered
files in the <b>carpix</b> folder.  The <b>collision_training</b> script converts these color images to
grayscale, then builds a training set in which all images but the final one are labeled as safe (no
collision; code <tt>[1 0]</tt>), and the final one is labeled as a collision (code <tt>[0 1]</tt>).  
Finally, this training script uses Python's built-in <tt>pickle</tt> library to 
[save](https://github.com/simondlevy/AirSimTensorFlow/blob/master/collision_training.py#L111-L113)
the trained network parameters (weights and biases).  The <b>collision_testing</b> script uses <tt>pickle</tt> to
[restore](https://github.com/simondlevy/AirSimTensorFlow/blob/master/collision_testing.py#L42-L45)
these parameters, then reconstructs the TensorFlow [neural net](https://github.com/simondlevy/AirSimTensorFlow/blob/master/tf_softmax_layer.py#L18-L28) from them.  (We found this approach easier than
using TensorFlow's [save-and-restore](https://www.tensorflow.org/programmers_guide/saved_model) API.)
Finally, the <b>collision_testing</b> script moves the vehicle forward, converting the live 
image into grayscale and running it through the network to make a collision/no-collision prediction.
When the value of the &ldquo;collision bit&rdquo; exceeds 0.5, the script stops the vehicle by applying the brakes.

# Future work

Our single-layer logistic regression network provides a simple proof-of-concept
example; however, for a more realistic data set involving collisions with
different types of objects, a convolutional network would make more sense.
AirSim also provides access to depth images (just press the <b>1</b> key during
the simulation) which, like the Lidar on today's self-driving cars, would
provide a valuable additional source of information for avoiding collisions.

# participants

This code represents the final project at Ariel University:

* Meir Rozenfeld
* Avi Chickvashvili 
* Tomer Dvir 

