#!/usr/bin/env python

import rospy
from cr_cw2_gaze_based_prediction.srv import prediction
import numpy as np
from prob_funcs import p_target_given_gazegrip

def predict_target(req) -> tuple:
	"""
	"""

	# Calculate hand to objs distance
	dist_obj1 = ((req.hand_x - 2.0)**2 + (req.hand_y - 1.0)**2)**0.5;
	dist_obj2 = ((req.hand_x - 4.0)**2 + (req.hand_y - 1.0)**2)**0.5;
	
	print("====================================================");
	print("Object 1 Dist: %s"%(dist_obj1));
	print("Object 2 Dist: %s"%(dist_obj2));
	
	# Get target prediction based on obj distance
	# Convert hand to object distances to a probability.
	# Probability N approaches 1 as hand approaches object N.
	
	P_t1_dist = 1 - (dist_obj1 / (dist_obj1 + dist_obj2));
	P_t2_dist = 1 - (dist_obj2 / (dist_obj1 + dist_obj2));
	
	print("====================================================");
	print("Target probability based on distance");
	print("----------------------------------------------------");
	print("Target is 1: %s"%(P_t1_dist));
	print("Target is 2: %s"%(P_t2_dist));
	
	# Predict hand trajectory?
	
	# Get target prediction based on gaze and grip
	P_t1_gg = p_target_given_gazegrip(1, req.gaze, req.grip);
	P_t2_gg = p_target_given_gazegrip(2, req.gaze, req.grip);
	
	print("====================================================");
	print("Target probability based on gaze & grip");
	print("----------------------------------------------------");
	print("Target is 1: %s"%(P_t1_gg));
	print("Target is 2: %s"%(P_t2_gg));
	print("====================================================");
	
	# Use Kalman filter to generate final prediction
	P_t1 = (P_t1_dist + P_t1_gg)/2# + req.P_t1_old) / 3;
	P_t2 = (P_t2_dist + P_t2_gg)/2# + req.P_t2_old) / 3;
	
	# Publish predicted target info
	return (P_t1, P_t2)

def prediction_server() -> None:
	"""
	"""
	
	rospy.init_node("target_prediction");
	s = rospy.Service("target_prediction", prediction, predict_target);
	print("Server Ready");
	rospy.spin();
	
if __name__ == "__main__":
	prediction_server();
	
