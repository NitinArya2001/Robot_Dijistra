#!/usr/bin/python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseArray
import math
PI = math.pi
# Example
x_goals = [0,1,-1,0,0]
y_goals = [1,-1,-1,1,-1]
theta_goals = [(PI)/4, (3*(PI))/4, -(3*PI)/4, -(PI)/4, 0]


class ROSEnter:
	def task1_goals_Cb(self,msg):
			global x_goals, y_goals, theta_goals

			x_goals.clear()
			y_goals.clear()
			theta_goals.clear()
			print("in tsak1 running")
			for i in range(len(x_goals)):
					print(x_goals[i])

			for waypoint_pose in msg.poses:
				x_goals.append(waypoint_pose.position.x)
				y_goals.append(waypoint_pose.position.y)

				orientation_q = waypoint_pose.orientation
				orientation_list = [orientation_q.x, orientation_q.y,
									orientation_q.z, orientation_q.w]
				theta_goal = euler_from_quaternion(orientation_list)[2]
				theta_goals.append(theta_goal)
	def __init__(self):
		# Starts a new node
		rospy.init_node('controller')
		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.sub = rospy.Subscriber("/odom", Odometry, self.get_orientation)
		rospy.Subscriber('task1_goals', PoseArray, self.task1_goals_Cb)
		self.x = 0
		self.y = 0
		self.theta = 0
	
	def get_orientation(self, msg):
		# Update position and orientation
		self.x = msg.pose.pose.position.x
		self.y = msg.pose.pose.position.y
		rot_q = msg.pose.pose.orientation

		#print("theta: ", self.theta*(180/PI))
		_, _, self.theta = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
		if(self.theta < 0):
			self.theta += 2*PI
			
		   


		

	def move_to(self,x,y, xi, yi,i):
		#Starts a new node
		vel_msg = Twist()
		# print("vel_msg ", vel_msg)
		rate = rospy.Rate(10)

		
		goal = Point()
		goal.x = x
		goal.y = y

		print("Starting Coordinate of Robot:")
		print("X : ", self.x)
		print("Y : ", self.y)

		print("Expected final destination Coordinate:")
		print("X : ", goal.x)
		print("Y : ", goal.y)

	# calculating angle between current point and target point
		inc_x = goal.x - self.x
		inc_y = goal.y - self.y
		relative_angle = math.atan2(inc_y, inc_x)
		print(" ****** Rotating robot at a position *******")
		print()
		
		if relative_angle < 0:
			relative_angle = 2*PI + relative_angle
		print("Expected angle rotation for Robot : ",relative_angle*(180/PI))

		# speed = 40
		ang_vel =2.0
		vel_msg.angular.z = ang_vel
		current_angle = self.theta
		while(current_angle > relative_angle):
			# while(current_angle > ):
			self.pub.publish(vel_msg)
			rate.sleep()
			current_angle = self.theta
		while(current_angle < relative_angle):
			self.pub.publish(vel_msg)
			rate.sleep()
			current_angle = self.theta

		#Forcing our robot to stop
		print("Actual angle rotation of Robot : ", self.theta*180/PI)
		vel_msg.angular.z = 0
		self.pub.publish(vel_msg)

		print("Angular Velocity : ",ang_vel)
		
		# Move now in that direction
		# rate = rospy.Rate(10)
		print()
		print("Moving robot in straight Line at that Direction")
		speed = 0.6
		dis = math.sqrt(((x - xi)**2) + ((y - yi)**2))
		vel_msg.linear.x=abs(speed)
		vel_msg.linear.y=0
		vel_msg.linear.z=0
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0

		
		current_dis = 0
		print("Expected Distance covered by Robot: ", dis)
		while(current_dis < dis):
			self.pub.publish(vel_msg)
			rate.sleep()
			current_dis = math.sqrt(((self.x-xi)**2) + ((self.y-yi)**2))
	
		print("Actual Distance covered by Robot : ",current_dis)

		print()
		print("**** Robot reach at his destination ******")
		vel_msg.linear.x = 0
		self.pub.publish(vel_msg)

		print()
		print("Actual final destination Coordinate:")
		print("X : ", self.x)
		print("Y : ", self.y)
		print("Actual FINAL  angle OF ROBOT  : ",self.theta*(180/PI))

		return
	def todo(self) :
		xi = yi = 0
		ros_inter = ROSEnter()
		
		for i in range(0,5):
	
				x = x_goals[i]
				y = y_goals[i]
				if i==0:
					xi=0
					yi=0
				else:
					xi=x_goals[i-1]
					yi=y_goals[i-1]		
				ros_inter.move_to(x, y, xi, yi,i)
				
				


			
def main() :
	ros_inter = ROSEnter()
	ros_inter.todo()
	


if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	
	