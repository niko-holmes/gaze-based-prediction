#!/usr/bin/env python

def p_target_given_grip(target: int, grip: int) -> float:
	if grip in [1,2]:
		if grip == target:
			return 0.8;
		elif grip != target:
			return 0.2;
	return 0.5;
		
def p_target_given_gaze(target: int, gaze: int) -> float:
	if gaze in [1,2]:
		if gaze == target:
			return 0.7;
		elif gaze != target:
			return 0.3;
	return 0.5;
	
def p_target_given_gazegrip(target: int, gaze: int, grip: int) -> float:
	return (p_target_given_grip(target, grip) + p_target_given_gaze(target, gaze))/2;
	
def p_gaze() -> float:
	return 1.0/3;
	
def p_grip() -> float:
	return 1.0/3;
	
def p_target() -> float:
	return 1.0/2;

def p_gaze_given_target(target: int, gaze: int) -> float:
	return (p_target_given_gaze(target, gaze) * p_gaze()) / p_target();
	
def p_grip_given_target(target: int, grip: int) -> float:
	return (p_target_given_grip(target, grip) * p_grip()) / p_target();
