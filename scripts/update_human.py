#!/usr/bin/env python

import rospy
import sys
from cr_cw2_gaze_based_prediction.msg import human_info
from std_msgs.msg import Int64
import numpy as np
from prob_funcs import p_grip_given_target, p_gaze_given_target

def generate_human(runtime: int, timestep: int, hand_delay: int, movement_time: int, full_random: bool) -> None:
	"""
	
	:runtime    : Time to execute movement to object (ms)
	:timestep   : Timestep of simulation (ms)
	:hand_delay : Number of milliseconds before hand is shown to robot
	:full_random:
	"""
	assert runtime <= movement_time, "Runtime must be less than or equal to movement time";
	
	pub = rospy.Publisher('human_info', human_info, queue_size = 10);
	pub_truth = rospy.Publisher('target_truth', Int64, queue_size = 10);
	rospy.init_node('human', anonymous = False);
	
	rate = rospy.Rate(1000/timestep);
	
	_id = 1;
	while not rospy.is_shutdown() and _id <= 500:
		
		# desired_object_x: 1 = big ball, 2 = small ball
		# object positions: big ball (2.0, 1.0), small ball (4.0, 1.0)
		# grip: 1 = all fingers (AF), 2 = thumb & index (TI), 3 = index only (I)
		# gaze: 1 = at big ball, 2 = at small ball, 3 = blind
		
		print("--------------------------------------------");
		print("Generating New %s Scenario"%("Random" if full_random else "Realistic"));
		
		hand_x = 3.0;#np.random.uniform(2.9, 3.1);
		hand_y = 5.0;
		desired_object = np.random.randint(1, 3, dtype = int);
		
		print("Target is: Object %s"%("1" if desired_object == 1 else "2"), end = "\n\n");
		pub_truth.publish(desired_object);
		
		if full_random:
			grip = np.random.randint(1, 4, dtype = int);
			gaze = np.random.randint(1, 4, dtype = int);
		else:
			grip_choices = [p_grip_given_target(desired_object, i) for i in range(1,4)];
			gaze_choices = [p_gaze_given_target(desired_object, i) for i in range(1,4)];
			grip = np.random.choice(range(1,4), p = grip_choices);
			gaze = np.random.choice(range(1,4), p = gaze_choices);
		
		xf = 2.0 if desired_object == 1 else 4.0;
		
		xtraj = list(np.geomspace(xf, hand_x, movement_time/timestep, True));
		ytraj = list(np.geomspace(1.0, hand_y, movement_time/timestep, True));
		
		xtraj.reverse();
		ytraj.reverse();
		
		t = 0;
		while not rospy.is_shutdown() and t < runtime:
			# Send human info and update hand position
			t_reached = t == runtime - timestep;
			
			if t <= hand_delay:
				rospy.loginfo("\n id:%s\n grip:%s\n gaze:%s\n hand_x:%s\n hand_y:%s\n t:%s\n t_reached:%s"%(_id, 0, gaze, 3.0, hand_y, t, t_reached));
				pub.publish(_id, t, gaze, hand_x, hand_y, 0, t_reached);
			else:
				traj_i = round((t-hand_delay)/timestep) - 1;
				rospy.loginfo("\n id:%s\n grip:%s\n gaze:%s\n hand_x:%s\n hand_y:%s\n t:%s\n t_reached:%s"%(_id, grip, gaze, xtraj[traj_i], ytraj[traj_i], t, t_reached));
				pub.publish(_id, t, gaze, xtraj[traj_i], ytraj[traj_i], grip, t_reached);
			
			rate.sleep();
			t += timestep;
		_id += 1;
	
if __name__ == "__main__":
	try:
		generate_human(2000, 100, 1000, 2000, sys.argv[0]);
	except rospy.ROSInterruptException:
		pass;	
