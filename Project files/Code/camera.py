####################################################################
# File name: camera.py                                             #
# Purpose  : Initialize the USB camera and takes the image using   # 
#            fswebcam utility in the Linux Debian distribution.    # 
#  		     It Encodes the image into string using openCV python  # 
#            libraries .                                           #
# Return   : Returns a string equivalent of the image              #
# Author   : Surjith Bhagavath Singh, Manohar Karthikeyan		   #
#		     OpenCV library has been used   				       #
####################################################################

#Importing the openCV and system libraries
import cv2
import os

####################################################################
# Class name: VideoCamera							               #
# Purpose   : Contains get_frame function                          #
#											                       # 
####################################################################

class VideoCamera(object):

####################################################################
# Function name: get_frame                                         #
# Purpose      : Initializing the USB camera and taking a picture  # 
#                using fswebcam and storing it as “image.png”      #                
# Return       : Returns the string format of the image for        #  
#                streaming purpose.                                #
#											                       # 
####################################################################

    def get_frame(self):
		cmd ='fswebcam image.png'
		#Entering the command from linux terminal
		os.system(cmd)
		#Reading the image from the local directory
		image=cv2.imread('image.png')
		#encoding the image to jpeg format
	    ret, jpeg = cv2.imencode('.jpg', image)
        #Converting the image in jpeg format to string
		return jpeg.tostring()

