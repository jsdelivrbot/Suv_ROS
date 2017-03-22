#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class joy_mapper(object):
	"""docstring for joy_mapper"""
	def __init__(self,):
		
		rospy.loginfo("Iniciando")
		self.sub = rospy.Subscriber('/suv/joy', Joy, self.process, queue_size=1)
		self.pub= rospy.Publisher('/suv/mobile_base_controller/cmd_vel', Twist, queue_size=1)
		self.joy = Joy()
		self.linear_scale = rospy.get_param("~linear_scale", 2)
		self.angular_scale = rospy.get_param("~angular_scale", 2)
		rospy.spin()

	def process(self,msg):
		self.joy=msg
		twist = self.joy2twist()
		self.pub.publish(twist)

	def joy2twist(self):
		cmd=Twist()
		cmd.linear.x = self.linear_scale * 0.5 * (self.joy.axes[2] - self.joy.axes[5])
		cmd.angular.z = self.angular_scale * self.joy.axes[0]
 		return cmd

		


if __name__ == '__main__':
	rospy.init_node("joy_mapper",anonymous=False)
	node = joy_mapper()