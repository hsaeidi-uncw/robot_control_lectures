#!/usr/bin/env python3

import rospy
import math
# import the messages for reading the joint positions and sending joint commands
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import Header

# the call back function for a shorter version of the position feedback
def pose_callback(data):
	# loop through the values for 6 joints
	for joint_no in range(6):
		# read the joint name
		joint_name = data.name[joint_no]
		# read the joint position value
		joint_pos = data.position[joint_no]
		# show the results
		monitoring_messge = joint_name + ' is at %0.2f radians'
		rospy.loginfo(monitoring_messge, joint_pos)

if __name__ == '__main__':
	# initialize the node
	rospy.init_node('simple_pose_control', anonymous = True)
	# add a subscriber to it to read the position information
	rospy.Subscriber('/joint_states', JointState, pose_callback)
	# add a publisher for sending joint position commands
	pos_pub = rospy.Publisher('/pos_joint_traj_controller/command', JointTrajectory, queue_size = 10)
	# set a 10Hz frequency for this loop
	loop_rate = rospy.Rate(10)

	# define a joint trajectory variable for sending the control commands
	pos_cmd = JointTrajectory()
	pos_cmd_point = JointTrajectoryPoint()
	# just a rouch and quick solution for complete the message template
	pos_cmd.joint_names.append('elbow_joint')
	pos_cmd.joint_names.append('shoulder_lift_joint')
	pos_cmd.joint_names.append('shoulder_pan_joint')
	pos_cmd.joint_names.append('wrist_1_joint')
	pos_cmd.joint_names.append('wrist_2_joint')
	pos_cmd.joint_names.append('wrist_3_joint')
	
	# initialize the positin command to zero
	for joint_no in range(6):
		pos_cmd_point.positions.append(0.0)
	pos_cmd_point.time_from_start = rospy.Duration(1.0)
	pos_cmd_point.positions[1] = -math.pi/4
	pos_cmd.points.append(pos_cmd_point)
		
	header = Header()
	
	while not rospy.is_shutdown():
		# update the header
		header.stamp = rospy.Time.now()
		pos_cmd.header = header
		# publish the message
		pos_pub.publish(pos_cmd)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
