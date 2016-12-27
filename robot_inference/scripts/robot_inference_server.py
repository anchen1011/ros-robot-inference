#!/usr/bin/env python

from robot_inference.srv import *
import rospy
import inference
import array

def handle(req):
    lst = list(eval(str(req.observation)))
    return InferenceResponse(inference.wrapped_infer(lst))

def robot_inference_server():
    rospy.init_node('robot_inference_server')
    s = rospy.Service('inference', Inference, handle)
    print ("Ready to infer robot behavior.")
    rospy.spin()

if __name__ == "__main__":
    robot_inference_server()
