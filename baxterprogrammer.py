#!/usr/bin/env python

import argparse

import rospy
import ast

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION

waypoints = []
current_point = 0
movement_incr = 0.1






def main():
    
    """RSDK Joint Position Example: Keyboard Control

    Use your dev machine's keyboard to control joint positions.

    Each key corresponds to increasing or decreasing the angle
    of a joint on one of Baxter's arms. Each arm is represented
    by one side of the keyboard and inner/outer key pairings
    on each row for each joint.
    """
    epilog = """See help inside the example with the '?' key for key bindings. """
    
    
    
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__,
                                     epilog=epilog)
    parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node("rsdk_joint_position_keyboard")
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled

    def clean_shutdown():
        print("\nExiting example...")
        if not init_state:
            print("Disabling robot...")
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    print("Enabling robot... ")
    rs.enable()

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
    lj = left.joint_names()
    rj = right.joint_names()  


    map_keyboard()
    

    print("Done.")



def map_keyboard():
    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
    lj = left.joint_names()
    rj = right.joint_names() 
    
    global movement_incr

    def set_j(limb, joint_name, direction):
        current_position = limb.joint_angle(joint_name)
        if direction == 1:
	  delta = movement_incr
	else:
	  delta = 0- movement_incr
        
        joint_command = {joint_name: current_position + delta}
        
        limb.set_joint_positions(joint_command)

    bindings = {
    #   key: (function, args, description)
        'Q': (set_j, [left, lj[0], 1], "left_s0 increase"),
        'q': (set_j, [left, lj[0], -1], "left_s0 decrease"),
        'W': (set_j, [left, lj[1], 1], "left_s1 increase"),
        'w': (set_j, [left, lj[1], -1], "left_s1 decrease"),
        'E': (set_j, [left, lj[2], 1], "left_e0 increase"),
        'e': (set_j, [left, lj[2], -1], "left_e0 decrease"),
        'R': (set_j, [left, lj[3], 1], "left_e1 increase"),
        'r': (set_j, [left, lj[3], -1], "left_e1 decrease"),
        'T': (set_j, [left, lj[4], 1], "left_w0 increase"),
        't': (set_j, [left, lj[4], -1], "left_w0 decrease"),
        'Y': (set_j, [left, lj[5], 1], "left_w1 increase"),
        'y': (set_j, [left, lj[5], -1], "left_w1 decrease"),
        'U': (set_j, [left, lj[6], 1], "left_w2 increase"),
        'u': (set_j, [left, lj[6], -1], "left_w2 decrease"),
        '[': (grip_left.close, [], "left: gripper close"),
        '{': (grip_left.open, [], "left: gripper open"),
        'p': (grip_left.calibrate, [], "left: gripper calibrate"),

        'A': (set_j, [right, rj[0], 1], "right_s0 increase"),
        'a': (set_j, [right, rj[0], -1], "right_s0 decrease"),
        's': (set_j, [right, rj[1], 1], "right_s1 increase"),
        'S': (set_j, [right, rj[1], -1], "right_s1 decrease"),
        'd': (set_j, [right, rj[2], 1], "right_e0 increase"),
        'D': (set_j, [right, rj[2], -1], "right_e0 decrease"),
        'f': (set_j, [right, rj[3], 1], "right_e1 increase"),
        'F': (set_j, [right, rj[3], -1], "right_e1 decrease"),
        'g': (set_j, [right, rj[4], 1], "right_w0 increase"),
        'G': (set_j, [right, rj[4], -1], "right_w0 decrease"),
        'h': (set_j, [right, rj[5], 1], "right_w1 increase"),
        'H': (set_j, [right, rj[5], -1], "right_w1 decrease"),
        'J': (set_j, [right, rj[6], 1], "right_w2 increase"),
        'j': (set_j, [right, rj[6], -1], "right_w2 decrease"),
        ';': (grip_right.close, [], "right: gripper close"),
        ':': (grip_right.open, [], "right: gripper open"),
        'l': (grip_right.calibrate, [], "right: gripper calibrate"),
    }
    done = False
    print("Controlling joints. Press ? for help, Esc to quit.")
    
    while not done and not rospy.is_shutdown():
        c = baxter_external_devices.getch()
        if c:
            print("INCHAR:%s", c) 
            
            #catch Esc or ctrl-c
            if c in ['\x1b', '\x03']:
                done = True
                rospy.signal_shutdown("Example finished.")
                
                
            elif c in bindings:
                print ("joint command")
                cmd = bindings[c]
                #expand binding to something like "set_j(right, 's0', 0.1)"
                cmd[0](*cmd[1])
                print("command: %s" % (cmd[2],))
                
            elif c == 'z':
                print ("Current location (RIGHT)")
                #for key, val in right.endpoint_pose.items():
                    #   print("  %s: %s" % (key, val[1]))
                
                current_angles = right.joint_angles()
                for key, val in current_angles.items():
                    print("  %s: %s" % (key, val))
                
                print ("Current location (LEFT)")
                # for key, val in left.endpoint_pose.items():
                #    print("  %s: %s" % (key, val[1]))
                
                current_angles = left.joint_angles()
                for key, val in current_angles.items():
                    print("  %s: %s" % (key, val))

            elif c == ' ':
                saveWaypoint(right.joint_angles().items(),left.joint_angles().items())

            elif c == 'x':
                execWaypoint()
            
            elif c == 'v':
                openWaypoints()

            elif c == 'b':
                printWaypoints()

            elif c == 'n':
                writeWaypoints()

            elif c == ',':
                prevWaypoint()
            
            elif c == '.':
                nextWaypoint()
            
            elif c == 'm':
		lastWaypoint()

            elif c == '(':
                left.move_to_neutral()

            elif c == ')':
                right.move_to_neutral()
	    
	    elif c == '|':
		global waypoints
		waypoints=[]
	    
	    elif c == '=':
		print ("movement increment is:"),
		print (movement_incr)
		
	    elif c == '+':
		if movement_incr < .4:
		  movement_incr *= 2
		print ("movement increment is:"),
		print (movement_incr)
		
	    elif c == '-':
		movement_incr /= 2
		print ("movement increment is:"),
		print (movement_incr)

            else:
                print ("key bindings: ")
                print ("  Esc: Quit")
                print ("  ?: Help")
                print ("  z: Position")
                print ("  <SPACE>: Save Waypoints")
                print ("  b: Print Waypoints")
                print ("  .: Forward")
                print ("  ,: Backward")
                print ("  m: Latest")
                print ("  x: Execute Waypoints")
                print ("  v: Import Waypoints")
                print ("  n: Write Waypoints to File")
                print ("  (: Left to Neutral")
                print ("  ): Right to Neutral")
                print ("  |: Right to Neutral")
                
                for key, val in sorted(bindings.items(),
                                        key=lambda x: x[1][2]):
                    print("  %s: %s" % (key, val[2]))



    


def nextWaypoint():
    global current_point
    if current_point + 1 > waypoints.count:
        print ("END OF WAYPOINTS")
    else:
        current_point += 1

def prevWaypoint():
    global current_point
    if current_point - 1 < 0:
        print ("START OF WAYPOINTS")
    else:
        current_point -= 1

def lastWaypoint():
    global current_point
    current_point = waypoints.count
    #print ("AT LAST WAYPOINTS")


def saveWaypoint(right,left):
    waypoint={'right':right, 'left':left}
    waypoints.append(str(waypoint))
    print ("waypoint saved")
    
def writeWaypoints():
    routine = raw_input("Enter routine name: ")
    
    
    path = '/home/ruser/pizza/'+routine+'.dat'
    
    f = open(path, 'w')
    # f = open('test/02238wx.dat', 'w')
    f.seek(0)
    for step in waypoints:
        print(step)
        f.write(str(step))
        f.write("\n")
    
    print ("ITER DONE")
        
    f.truncate()
    f.close()
    print ("WRITE DONE")
    print (path)


def openWaypoints():
    global waypoints, current_point
    waypoints=[]
    current_point=0
    
    routine = raw_input("Enter routine name: ")
    path = '/home/ruser/pizza/'+routine+'.dat'
    
    
    try:
        with open(path, 'r') as file:
            for line in file:
                waypoints.append(line)
                print("******")
                print(line)
        print ("opened sucessfully")
    except:
        print ("error parsing states file")




def execWaypoint():
    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
    lj = left.joint_names()
    rj = right.joint_names() 
    
    right.set_command_timeout(5)
    left.set_command_timeout(5)


    wpointstring = waypoints[current_point]
    #print (wpoint)
    print ("!!!")
    wpoint = ast.literal_eval(wpointstring)
    print (wpoint)
    #for item in wpoint:
    #    print (">"),
    #    print (item)
            
    if 'right' in wpoint:
        pointdict={}
        print (wpoint['right'])
        for item in wpoint['right']:
            print (">"),
            print (item[1])
            pointdict[item[0]]=item[1]
        right.set_joint_positions(pointdict)
    
    if 'left' in wpoint:
        pointdict={}
        print (wpoint['left'])
        for item in wpoint['left']:
            print (">"),
            print (item[1])
            pointdict[item[0]]=item[1]
        left.set_joint_positions(pointdict)

    #if right exists
        #break out angle
    #if left exists
        #break out angle
    
    global current_point
    current_point += 1
    
    

def printWaypoints():
    for i, step in enumerate(waypoints):
        if i == current_point:
            print ("-->"),
        else:
            print ("   "),
        print (i),
        print (" :"),
        if 'right' in step:
            print (" Right "),
        if 'left' in step:
            print (" Left ")
        #print (step)
        



#def writePOS():
#def waypoint();
#def xmitPOS();









if __name__ == '__main__':
    main()
