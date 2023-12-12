#!/usr/bin/env python

import rospy
from cr_cw2_gaze_based_prediction.msg import prediction_results
from std_msgs.msg import Int64, Float64

global truth;
global result_sum;
global result_amo;
global pub;

def log_data(data) -> None:
	"""
	"""
	global truth;
	global result_sum;
	global result_amo;
	global pub;
	
	guessed_target = 1 if max(data.P_t1, data.P_t2) == data.P_t1 else 2;
	
	result_sum += 1 if guessed_target == truth else 0;
	result_amo += 1;
	
	lifetime_accuracy = result_sum / result_amo;
	
	print("| {:^5} | {:^13f} | {:^13f} | {:^14} | {:^11} | {:^17%} |".format(data.id, data.P_t1, data.P_t2, guessed_target, truth, lifetime_accuracy));
	
	pub.publish(lifetime_accuracy);
	

def get_truth(data) -> None:
	global truth;
	
	truth = data.data;

def logger() -> None:
	"""
	"""
	global pub;
	
	pub = rospy.Publisher('lifetime_accuracy', Float64, queue_size = 10);
	rospy.init_node('data_logger', anonymous = False);
	rospy.Subscriber('target_truth', Int64, get_truth);
	rospy.Subscriber('prediction_results', prediction_results, log_data);
	
	print("____________________________________________________________________________________________");
	print("| Trial | Object 1 Prob | Object 2 Prob | Guessed Target | True Target | Lifetime Accuracy |");
	
	rospy.spin();
	
	
if __name__ == "__main__":
	result_sum = 0;
	result_amo = 0;
	truth = 0;
	
	logger();
