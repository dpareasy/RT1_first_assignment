#Research Track I -first assignment
================================
Parisi Davide Leo 4329668 

This assignment requires the development of a sofware architecture, in python language, for constraintly drive a robot around a particular enviroment. To help the it in the navigation, the architecture relies on the `R.see` method. 

The architecture should be able to:

* Drive in loop the robot in the counterclockwise direction

* Make the robot avoid touching golden tokens (which constitute the circuit)

* Drives the robot close to any silver token inside the enviroment, enables it to grab and move them behind itself

![Simulator_enviroment](https://user-images.githubusercontent.com/92155300/141161356-d32612af-46de-41c6-9e6b-ca522cfc54a3.png)



## How to run ##

in order to run the the script in the simulator use `run.py` and pass the file name `assignment.py` as follow:

```
$ python2 run.py assignment.py
```

## Robot behaviour ##

When the simulation is launched, the robot is generated in a pre-built environment where it can distinguish golden tokens from silver.
Once generated, it immediately begins its drive counterclockwise by constantly detecting the distances from each of the two types of tokens. If the distance from the golden tokens drops below a certain threshold it turns, so as to avoid collisions, otherwise it moves forward. When it detects a silver token, the robot must point at it and, once close, grabs it and releases it behind itself, turning in the direction of the farther wall. 


https://user-images.githubusercontent.com/92155300/141161108-8a0ffc14-e9c9-4793-a906-5d992e1b456e.mp4




### Equipment ###

#### Motors ####

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

#### The Grabber ####

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.


#### Vision ####

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/


## About software architecture ##

To implement the code for this project I decided to use 8 different functions. In the following lines there is an explanation of each one.

### The drive function ###

The drive function makes use of the two motors mentioned in "Equipment" section. If both are setted with a positive speed, the simulated robot assume a linear velocity and can drive forward. 

Parameters:
* The linear velocity 
* The time interval

Equipment:
* Motors

### The turn function ###

The turn function uses the same motors of the above mentioned one, but this time, one of them is set with a positive speed while the other with a negative one. This way, when the function is called, the simulated robot assume an angular velocity which makes it turn either left or right. 

Parameters:
* The angular velocity 
* The time interval

Equipment:
* Motors


### The find_golden_token function ###

This function enables the robot to recognise golden tokens. In this function I decided to set an angular threshold that allows a rather wide frontal view for golden tokens. 

Return:
* The frontal distance from golden token
* The alignment with golden tokens

Equipment:
* `R.see` method


### The find_silver_token function ###

This function enables the robot to recognise silver token. In this function I decided to set an angular threshol in order to reduce the robot visual field, forcing it to look forward, to be sure that it did not go back to grab the token just released. 

Return:
* The frontal distance from silver token
* The alignment with silver tokens

Equipment:
* `R.see` method

### The right_side_distance function ###

This is the function to detect right side distance from the wall made of golden tokens. It detects the right distance in an angular range between 80° and 100°.

Return: 
* The right side distance from golden tokens

Equipment:
* `R.see` method

### The left_side_distance function ###

This is the function to detect left side distance from the wall made of golden token. It detects the left distance in an angular range between -100° and -80°.

Return: 
* The left side distance from golden tokens

Equipment:
* `R.see` method


### The avoid_golden_token function ###

This is the function used to avoid collisions with golden token. The idea developed there is to compute left and right distances from golden tokens. This way, when the robot gets too close to the wall, it can decide to turn in the direction where the distance from it is greater. Then, when tokens in its field of vision appear sufficiently far away it resumes its run. 

Parameters:
* The frontal distance from golden tokens
* The left side distance from golden tokens
* The right side distance from golden tokens


![avoid_golden](https://user-images.githubusercontent.com/92155300/141161232-7f7ab7e3-3546-4f9a-953d-c91d082092be.gif)



### The grab_silver_token function ###

This function allows the simulated robot to grab silver tokens. This action is allowed only when the distance from the silver tokens is less than a preset value and if the robot is aligned with them. After grabbing, it computes the left and right distances from the wall and decides to turn in the direction of the farthest. Then, after having released the token, it spins again following the same logic used before. 

This function has 5 parameters: the position with respect to silver tokens, the alignment with respect to silver tokens, the position with respect to golden tokens, left and right distance from golden tokens.

Equipment:
* `R.grab` method of the grabber
* `R.release` method of the grabber

used function:
* The `find_silver_token` function
* The `right_side_distance` function
* The `left_side_distance` function

![grab_function](https://user-images.githubusercontent.com/92155300/141161262-f0dda653-4ea0-434d-b751-2472a41eba88.gif)



## Pseudocode ##

In the following lines there is the pseudocode of the code used to manage the behaviour of the robot:

```
while 1
	update all cordinates
	
	if dist from golden is less than a pre-established threshold
		if right distance from the wall is greater than left distance
			turn right
		else 
			turn left
	else 
		drive forward
		print "move forward"
		
	if can see silver token	
		while 1	
			if the robot is close enough to the silver token
				print "I found it"
				grab the token
				print "Gotcha!"
			
				if distance from right wall is grater than left distance
					turn right
				else
					turn left
						
				release the token
					
				if distance from right wall is grater than left distance
					turn right
				else
					turn left
				exit from the loop
				
			elif distance less than 1.5		
				if the robot is well aligned with the silver token
					print "Ah, here we are!"
					drive forward
				elif the robot is misaligned to the right
					while it is misaligned
						print "left a bit..."
						turn left
					
				elif the robot is misaligned to the left
					while it is misaligned 				
						print "right a bit..."
						turn right
```

## Possible improvements ##

A possible improvement could be a control, in grab_silver_token function, that allows the robot to ignore silver tokens if there are golden tokens between it and the silver. Doing this allows to avoid reducing the viewing distance range. This decrement must be done because otherwise the robot will move in the direction of silver tokens despite the presence of the wall between it and its target.  
