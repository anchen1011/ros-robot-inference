#!/usr/bin/env python

import sys
import rospy
from robot_inference.srv import *
import array

reverse_table = {0:"stay", 4:"right", 3:"left", 1:"up", 2:"down"}
table = {"stay":0, "right":4, "left":3, "up":1, "down":2}
def translate(i):
    if i in table:
        return table[i]
    return i
def restore(i):
    return reverse_table[i]
def demonstrate(inference):
    lst = list(eval(str(inference)))
    sequence = []
    for i in range(0,len(lst)-2,3):
        action = restore(lst[i+2])
        sequence.append((lst[i],lst[i+1],action))
    for i in sequence:
        print(i)
def load_observations(filename):
    # loads a list of observations saved by save_observations()
    f = open(filename, 'r')
    print ("Filename: "+filename)
    observations = []
    for line in f.readlines():
        line = line.strip()
        if line == 'missing':
            observations.append(None)
        else:
            parts  = line.split()
            x      = int(parts[0])
            y      = int(parts[1])
            observations.append( (x, y) )

    f.close()
    result = []
    for state in observations:
        for entry in state:
            result.append(translate(entry))
    return result

def robot_inference_client(x):
    rospy.wait_for_service('inference')
    try:
        infer = rospy.ServiceProxy('inference', Inference)
        resp1 = infer(x)
        return resp1.inference
    except rospy.ServiceException, e:
        print ("Service call failed: %s"%e)

def usage():
    return "infer robot behavior from observations"

if __name__ == "__main__":
    print ("file name of observations (put in the same folder)")
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
	x = load_observations(filename)
    else:
        print (usage())
        sys.exit(1)
    print ("Requesting")
    print ("Infered behavior:")
    inf = robot_inference_client(x)
    demonstrate(inf)
