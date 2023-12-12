#!/usr/bin/env python

import rospy
from cr_cw2_gaze_based_prediction.msg import human_info, prediction_results
from cr_cw2_gaze_based_prediction.srv import prediction

global P_t1_old
global P_t2_old

def get_prediction(data) -> None:
	"""
	"""
	global P_t1_old
	global P_t2_old
	
	pub = rospy.Publisher("prediction_results", prediction_results, queue_size = 10);
	
	rospy.loginfo(rospy.get_caller_id() + " Message received");
	
	rospy.wait_for_service("target_prediction");
	try:
		server_proxy = rospy.ServiceProxy("target_prediction", prediction);
		preds = server_proxy(	data.t, data.gaze, data.hand_x, data.hand_y,
					data.grip, P_t1_old, P_t2_old);
		if data.target_reached:
			pub.publish(data.id, preds.P_t1, preds.P_t2);
			
		P_t1_old, P_t2_old = preds.P_t1, preds.P_t2;
		
		rospy.loginfo("\n P(obj1):%s \n P(obj2):%s"%(preds.P_t1, preds.P_t2));
		
	except rospy.ServiceException as e:
		print("Service call failed: %s"%e);

def controller() -> None:
	"""
	"""
	global P_t1_old
	global P_t2_old
	
	P_t1_old, P_t2_old = 0.5, 0.5;
	
	rospy.init_node('controller', anonymous = False);
	rospy.Subscriber('human_info', human_info, get_prediction);
	
	rospy.spin();
	
	
if __name__ == "__main__":
	controller();
