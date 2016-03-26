####################################################################
# File name: gps.py								                   #
# Purpose  : Initialize the GPS module, Functionality to configure # 
#  		     GPS module and extract the information obtained from  # 
# 		     GPS module to human readable form. 			       #
# Return   : Returns a string with latitude, longitude co=ordinates#
# Author   : Surjith Bhagavath Singh, Manohar Karthikeyan          #
#		     Open source Adafruit library for UART has been used   # 
####################################################################



#importing the libraries for Beagle Bone Black
import serial
import Adafruit_BBIO.UART as UART
from time import sleep
UART.setup("UART1")

#Configuring UART1 for 9600 Baudrate
ser=serial.Serial('/dev/ttyO1',9600)


####################################################################
# Class name: GPS								                   #
# Purpose   : Contains initialization function, Read function      #
####################################################################

class GPS:

####################################################################
# Function name: __init__								           #
# Purpose      : Initializing the parameters to configure the GPS  #
#    			 module(Baudrate, rate of measurement, rate of     #
#			     report using PMTK statements                      #
####################################################################

    	def __init__(self):
     		#Initialization
               
			#This set is used to set the rate the GPS reports
			UPDATE_1_sec=  "$PMTK220,1000*1F\r\n"	
               
			#setting the GPS to take measurements @ 1 sec rate    
            MEAS_1_sec = "$PMTK300,1000,0,0,0,0*1C\r\n"
                
			#Set the Baud Rate of GPS as 57600
			BAUD_57600 = "$PMTK251,57600*2C\r\n"    

			#Commands for which NMEA Sentences are sent
			ser.write(BAUD_57600)
			sleep(1)
			ser.baudrate=57600
				
			#Send GPRMC AND GPGGA Sentences
			ser.write(UPDATE_1_sec)

			GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"
			sleep(1)
			ser.write(MEAS_200_msec)
			sleep(1)
			ser.write(GPRMC_GPGGA)
			sleep(1)
			ser.flushInput()
			ser.flushInput()
			print "GPS Initialized"

####################################################################
# Function name: read								               #
# Purpose      : Reads the data from UART and parse the information#
#                from GPRMC and GPGGA sentences and stores it in   # 
#                separate array variables                          #
#											                       # 
####################################################################

def read(self):
      	ser.flushInput()
        ser.flushInput()
                
		#Reading NMEA sentences from GPS module
		while ser.inWaiting()==0:
           	pass
            self.NMEA1=ser.readline()
        while ser.inWaiting()==0:
        	pass
            self.NMEA2=ser.readline()
				
		#Splitting the NMEA sentence 
        NMEA1_array=self.NMEA1.split(',')
        NMEA2_array=self.NMEA2.split(',')
                
		#Parsing the data Longitude,Latitude, Hemisphere, Altitude
 		
		if NMEA1_array[0]=='$GPRMC':
 			self.timeUTC=NMEA1_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:-4]
           	self.latDeg=NMEA1_array[3][:-7]
           	self.latMin=NMEA1_array[3][-7:]
           	self.latHem=NMEA1_array[4]
           	self.lonDeg=NMEA1_array[5][:-7]
           	self.lonMin=NMEA1_array[5][-7:]
           	self.lonHem=NMEA1_array[6]
           	self.knots=NMEA1_array[7]
      	
		if NMEA1_array[0]=='$GPGGA':
           	self.fix=NMEA1_array[6]
           	self.altitude=NMEA1_array[9]
           	self.sats=NMEA1_array[7]
         	
		if NMEA2_array[0]=='$GPRMC':
           	self.timeUTC=NMEA2_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:-4]
           	self.latDeg=NMEA2_array[3][:-7]
           	self.latMin=NMEA2_array[3][-7:]
           	self.latHem=NMEA2_array[4]
           	self.lonDeg=NMEA2_array[5][:-7]
           	self.lonMin=NMEA2_array[5][-7:]
           	self.lonHem=NMEA2_array[6]
           	self.knots=NMEA2_array[7]

        if NMEA2_array[0]=='$GPGGA':
           	self.fix=NMEA2_array[6]
           	self.altitude=NMEA2_array[9]
           	self.sats=NMEA2_array[7]


####################################################################
# Function name: main  							                   #
# Purpose      : Calls the initialization function, read function  # 
#                and parse the information into human readable     # 
#                string format.                                    #
#											                       # 
####################################################################
						
def main():
	
	#assigning class
	myGPS=GPS()
	
	#infinite loop
	while(1):
        	
		#Calling GPS read function
		myGPS.read()
			
		#Printing the NMEA sentences for Debugging purposes
        	print myGPS.NMEA1
        	print myGPS.NMEA2
        	
		#Checks for GPS Fix
		if myGPS.fix!=0:
        	print 'Universal Time: ',myGPS.timeUTC
        	print 'You are Tracking: ',myGPS.sats,' satellites'
        	print 'My Latitude: ',myGPS.latDeg, 'Degrees ', myGPS.latMin,' minutes ', myGPS.latHem
        	print 'My Longitude: ',myGPS.lonDeg, 'Degrees ', myGPS.lonMin,' minutes ', myGPS.lonHem
        	print 'My Speed: ', myGPS.knots
        	print 'My Altitude: ',myGPS.altitude
			
			#Compiling a string to display in the web UI
			string = "Time :"+ str(myGPS.timeUTC) + " You are Tracking: "+ str(myGPS.sats) +" satellites"+" at Latitude: "+str(myGPS.latDeg)+ " Degrees "+str(myGPS.latMin)+" minutes "+ str(myGPS.latHem)+" Hemisphere"+" Longitude: "+str(myGPS.lonDeg)+ " Degrees "+str(myGPS.lonMin)+" minutes "+ str(myGPS.lonHem)+" Hemisphere"+"  Speed of the car "+str(myGPS.knots)+" Altitude: "+str(myGPS.altitude)
			
			#Returning the string
			return string


