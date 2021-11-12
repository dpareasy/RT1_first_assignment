from __future__ import print_function

import time
from sr.robot import *


a_th = 4.0 
""" float: Threshold for the control of the orientation"""

d_th = 0.4 
""" float: Threshold for the control of the linear distance"""

ath_s= 50 
"""angular field of view for silver token"""

ath_g= 45 
"""angular field of view for golden token"""

dist_min=0.9 
"""threshold of the minimum distance from golden token"""

R = Robot() 
"""instance of the class robot"""


def drive(speed, seconds): 
	
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    """
	function for setting a linear velocity
	Parameters:
				-The speed of the wheels
  				-The time interval
  				
  	No values returned
	"""

def turn(speed, seconds):
 	
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    """
	function for setting an angular velocity.
	Parameters:
				-The speed of the wheels
  				-The time interval
  				
 	No values returned
	"""   

def find_silver_token():
	  
    dist=1.5
    for token in R.see(): 
        if token.dist < dist and -ath_s<token.rot_y<ath_s and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==1.5:
	return -1, -1
    else:
   	return dist, rot_y
   	"""
	function to find silver token around the arena
	
	Returns: 
			-The frontal distance from silver token
			- The alignment with the silver token
	"""	
   	
def right_side_distance():

	dist=100
	for token in R.see():
			if token.dist < dist and 80<token.rot_y<100 and token.info.marker_type is MARKER_TOKEN_GOLD:
				dist=token.dist
			
	if dist==100:
		return -1
	else:
		return dist
	"""
	function to detect the right distance from golden token.
	
	No parameters passed
	
	Returns:
    		-The right distance from golden token
	"""		

def left_side_distance():
	
	dist=100
	for token in R.see():
			if token.dist < dist and -100<token.rot_y<-80 and token.info.marker_type is MARKER_TOKEN_GOLD:
				dist=token.dist
			
	if dist==100:
		return -1
	else:
		return dist
	"""
	function to detect the left distance from golden token.
	
	No parameters passed
	
	Returns:
			-The left distance from golden token
	"""	
   	
def find_golden_token():
	 
    dist=100
    for token in R.see():
        if token.dist < dist and -ath_g<token.rot_y<ath_g and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100 :
	return -1, -1
    else:
   	return dist, rot_y
   	"""
	function to find golden token around the arena.
	
	No parameters passed
	
	Returns: 
		- The frontal distance from golden token
		- The alignment with golden token
	"""	   

def avoid_golden_token(dist_g, r_side_dist, l_side_dist):
  
	if dist_g<dist_min:
		if r_side_dist>l_side_dist:
			print("turn right")
			turn(12, 0.3)
		else:
			print("turn left")
			turn(-12, 0.3)
	else:
    		drive(75, 0.2)
    		print("move forward!")
    	"""
    	function to avoid touching golden token in the arena.
    	Parameters: 
    			-The frontal distance from golden token
    			-The right distance from golden token
    			-The left side distance from golden token
    	No return values
    	"""
def grab_silver_token():
		
		
	while 1:
		
		dist_s, rot_y_s = find_silver_token() 
		r_side_dist = right_side_distance()
		l_side_dist = left_side_distance()
					
		if dist_s <=d_th: #if distance from silver token is less than d_th threshold
	
	        	print("I found it!")
	        	R.grab() #grab silver token
	        	print("Gotcha!") 
		        
			if r_side_dist>l_side_dist: #if right side distance is greater than left side distance
	        		turn(25, 2.5) #turn right in order to avoid touching the wall while moving the silver token behind
	        	else:
				turn(-25, 2.5) #in the other case, turn left
	        
	        	R.release() #release silver token 
	        	
	        	print("Released!")		 	        
		       
	        	if r_side_dist>l_side_dist: #comparign the two distances in order to decide turning in the direction of the greater distance from the wall
	        		turn(-25, 2.5)
			else:
				turn(25, 2.5)
			return
		        
		elif dist_s<1.5:
					        
			if -a_th<= rot_y_s <= a_th: # if the robot is well aligned with the token, we go forward
				print("Ah, here we are!.")
				drive(50, 0.1)
			elif rot_y_s < -a_th: # if the robot is misaligned with the silver token on the right
				while rot_y_s < -a_th: #turn left until it is aligned
					dist_s, rot_y_s=find_silver_token()
	        			print("Left a bit...")
	        			turn(-6, 0.1)
			elif rot_y_s > a_th:
				while rot_y_s > a_th: # if the robot is misaligned with the silvertoken on the left
					dist_s, rot_y_s=find_silver_token() #turn right until it is aligned
	        			print("Right a bit...") 
	        			turn(+6, 0.1)
    	"""
    	function to grab, move behind and release silver token.
    	No parameters.
    	No return values.
    	"""
	
   	
def main():

	while 1:
		dist_s, rot_y_s=find_silver_token() #updating all cordinates
		dist_g, rot_y_g = find_golden_token()
		r_side_dist = right_side_distance()
		l_side_dist = left_side_distance()
    		
		avoid_golden_token(dist_g, r_side_dist, l_side_dist) #avoid collision function
			
		if dist_s!=-1: #if the robot can see the silver token
				
			grab_silver_token() #call the grab silver token function
		
main()
