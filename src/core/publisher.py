import rospy
from geometry_msgs.msg import PoseStamped
from .core import Core
import cv2
from enum import Enum


class BlockType(Enum):
    ORANGE = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4


def publish(location: Core):
    # use the PoseStamped, and (x, y, z, 0, 0, type (BlockType)) to represent the blocks
    rospy.init_node("cv_data", anonymous=True)
    pub_blocks = rospy.Publisher("blocks", PoseStamped, queue_size=10)
    pub_location = rospy.Publisher("location", PoseStamped, queue_size=10)
    rate = rospy.Rate(10)  # 5\unit{\Hz}
    while not rospy.is_shutdown():
        location = location.get_location()
        pose_location = PoseStamped()
        pose_location.header.stamp = rospy.Time.now()
        pose_location.pose.position.x = location.x
        pose_location.pose.position.y = location.y
        pose_location.pose.position.z = location.z
        pose_location.pose.orientation.x = location.roll
        pose_location.pose.orientation.y = location.pitch
        pose_location.pose.orientation.z = location.yaw
        pub_location.publish(pose_location)

        blocks = location.get_blocks()
        for block in blocks:
            pose = PoseStamped()
            pose.header.stamp = rospy.Time.now()
            pose.pose.position.x = block[1][0]
            pose.pose.position.y = block[1][1]
            pose.pose.position.z = block[1][2]
            pose.pose.orientation.x = 0
            pose.pose.orientation.y = 0
            pose.pose.orientation.z = block[0].value
            pub_blocks.publish(pose)
        rate.sleep()


def main():
    core = Core(cv2.VideoCapture(0))
    publish(core)
