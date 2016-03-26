####################################################################
# File name: main.py								               #
# Purpose  : This is the main python code, which is calling        # 
#		     functions and classes from other files. This code     #                 
#            initializes the flask webserver and hosts the webpage # 
# Return   : Returns a string with latitude, longitude co=ordinates#
# Author   : Surjith Bhagavath Singh, Manohar Karthikeyan		   #
#		  Open source Adafruit libraries for GPIO and PWM has      # 
#            been used                                             #
####################################################################


from flask import Flask, render_template, Response
from camera import VideoCamera
from gps import main
import Adafruit_BBIO.PWM as PWM
import time
import Adafruit_BBIO.GPIO as GPIO
import os

#Graphic LCD Pin declaration
RST = "P8_3"
D_C = "P8_5"
CS  = "P8_7"
DIN = "P8_9"
CLK = "P8_11"

#Graphic LCD variables
CONTROL_DATA = 1        #Data Selection
CONTROL_CMD  = 0        #command Selection
LCD_X = 84              #length of LCD
LCD_Y = 48              #width of LCD

#This table contains the hex values that represent pixels
#for a font that is 5 pixels wide and 8 pixels high
ASCII = ([[0x00, 0x00, 0x00, 0x00, 0x00] # 20
  ,[0x00, 0x00, 0x5f, 0x00, 0x00] # 21 !
  ,[0x00, 0x07, 0x00, 0x07, 0x00] # 22 "
  ,[0x14, 0x7f, 0x14, 0x7f, 0x14] # 23 #
  ,[0x24, 0x2a, 0x7f, 0x2a, 0x12] # 24 $
  ,[0x23, 0x13, 0x08, 0x64, 0x62] # 25 %
  ,[0x36, 0x49, 0x55, 0x22, 0x50] # 26 &
  ,[0x00, 0x05, 0x03, 0x00, 0x00] # 27 ' 
  ,[0x00, 0x1c, 0x22, 0x41, 0x00] # 28 (
  ,[0x00, 0x41, 0x22, 0x1c, 0x00] # 29 )
  ,[0x14, 0x08, 0x3e, 0x08, 0x14] # 2a *
  ,[0x08, 0x08, 0x3e, 0x08, 0x08] # 2b +
  ,[0x00, 0x50, 0x30, 0x00, 0x00] # 2c ,
  ,[0x08, 0x08, 0x08, 0x08, 0x08] # 2d -
  ,[0x00, 0x60, 0x60, 0x00, 0x00] # 2e .
  ,[0x20, 0x10, 0x08, 0x04, 0x02] # 2f /
  ,[0x3e, 0x51, 0x49, 0x45, 0x3e] # 30 0
  ,[0x00, 0x42, 0x7f, 0x40, 0x00] # 31 1
  ,[0x42, 0x61, 0x51, 0x49, 0x46] # 32 2
  ,[0x21, 0x41, 0x45, 0x4b, 0x31] # 33 3
  ,[0x18, 0x14, 0x12, 0x7f, 0x10] # 34 4
  ,[0x27, 0x45, 0x45, 0x45, 0x39] # 35 5
  ,[0x3c, 0x4a, 0x49, 0x49, 0x30] # 36 6
  ,[0x01, 0x71, 0x09, 0x05, 0x03] # 37 7
  ,[0x36, 0x49, 0x49, 0x49, 0x36] # 38 8
  ,[0x06, 0x49, 0x49, 0x29, 0x1e] # 39 9
  ,[0x00, 0x36, 0x36, 0x00, 0x00] # 3a :
  ,[0x00, 0x56, 0x36, 0x00, 0x00] # 3b ;
  ,[0x08, 0x14, 0x22, 0x41, 0x00] # 3c <
  ,[0x14, 0x14, 0x14, 0x14, 0x14] # 3d =
  ,[0x00, 0x41, 0x22, 0x14, 0x08] # 3e >
  ,[0x02, 0x01, 0x51, 0x09, 0x06] # 3f ? 
  ,[0x32, 0x49, 0x79, 0x41, 0x3e] # 40 @
  ,[0x7e, 0x11, 0x11, 0x11, 0x7e] # 41 A
  ,[0x7f, 0x49, 0x49, 0x49, 0x36] # 42 B
  ,[0x3e, 0x41, 0x41, 0x41, 0x22] # 43 C
  ,[0x7f, 0x41, 0x41, 0x22, 0x1c] # 44 D
  ,[0x7f, 0x49, 0x49, 0x49, 0x41] # 45 E
  ,[0x7f, 0x09, 0x09, 0x09, 0x01] # 46 F
  ,[0x3e, 0x41, 0x49, 0x49, 0x7a] # 47 G
  ,[0x7f, 0x08, 0x08, 0x08, 0x7f] # 48 H
  ,[0x00, 0x41, 0x7f, 0x41, 0x00] # 49 I
  ,[0x20, 0x40, 0x41, 0x3f, 0x01] # 4a J
  ,[0x7f, 0x08, 0x14, 0x22, 0x41] # 4b K
  ,[0x7f, 0x40, 0x40, 0x40, 0x40] # 4c L
  ,[0x7f, 0x02, 0x0c, 0x02, 0x7f] # 4d M
  ,[0x7f, 0x04, 0x08, 0x10, 0x7f] # 4e N
  ,[0x3e, 0x41, 0x41, 0x41, 0x3e] # 4f O
  ,[0x7f, 0x09, 0x09, 0x09, 0x06] # 50 P
  ,[0x3e, 0x41, 0x51, 0x21, 0x5e] # 51 Q
  ,[0x7f, 0x09, 0x19, 0x29, 0x46] # 52 R
  ,[0x46, 0x49, 0x49, 0x49, 0x31] # 53 S
  ,[0x01, 0x01, 0x7f, 0x01, 0x01] # 54 T
  ,[0x3f, 0x40, 0x40, 0x40, 0x3f] # 55 U
  ,[0x1f, 0x20, 0x40, 0x20, 0x1f] # 56 V
  ,[0x3f, 0x40, 0x38, 0x40, 0x3f] # 57 W  
  ,[0x63, 0x14, 0x08, 0x14, 0x63] # 58 X
  ,[0x07, 0x08, 0x70, 0x08, 0x07] # 59 Y
  ,[0x61, 0x51, 0x49, 0x45, 0x43] # 5a Z
  ,[0x00, 0x7f, 0x41, 0x41, 0x00] # 5b [
  ,[0x02, 0x04, 0x08, 0x10, 0x20] # 5c \
  ,[0x00, 0x41, 0x41, 0x7f, 0x00] # 5d ]
  ,[0x04, 0x02, 0x01, 0x02, 0x04] # 5e ^
  ,[0x40, 0x40, 0x40, 0x40, 0x40] # 5f _
  ,[0x00, 0x01, 0x02, 0x04, 0x00] # 60 `
  ,[0x20, 0x54, 0x54, 0x54, 0x78] # 61 a
  ,[0x7f, 0x48, 0x44, 0x44, 0x38] # 62 b
  ,[0x38, 0x44, 0x44, 0x44, 0x20] # 63 c
  ,[0x38, 0x44, 0x44, 0x48, 0x7f] # 64 d
  ,[0x38, 0x54, 0x54, 0x54, 0x18] # 65 e
  ,[0x08, 0x7e, 0x09, 0x01, 0x02] # 66 f
  ,[0x0c, 0x52, 0x52, 0x52, 0x3e] # 67 g
  ,[0x7f, 0x08, 0x04, 0x04, 0x78] # 68 h
  ,[0x00, 0x44, 0x7d, 0x40, 0x00] # 69 i
  ,[0x20, 0x40, 0x44, 0x3d, 0x00] # 6a j
  ,[0x7f, 0x10, 0x28, 0x44, 0x00] # 6b k
  ,[0x00, 0x41, 0x7f, 0x40, 0x00] # 6c l
  ,[0x7c, 0x04, 0x18, 0x04, 0x78] # 6d m
  ,[0x7c, 0x08, 0x04, 0x04, 0x78] # 6e n
  ,[0x38, 0x44, 0x44, 0x44, 0x38] # 6f o
  ,[0x7c, 0x14, 0x14, 0x14, 0x08] # 70 p
  ,[0x08, 0x14, 0x14, 0x18, 0x7c] # 71 q
  ,[0x7c, 0x08, 0x04, 0x04, 0x08] # 72 r
  ,[0x48, 0x54, 0x54, 0x54, 0x20] # 73 s
  ,[0x04, 0x3f, 0x44, 0x40, 0x20] # 74 t
  ,[0x3c, 0x40, 0x40, 0x20, 0x7c] # 75 u
  ,[0x1c, 0x20, 0x40, 0x20, 0x1c] # 76 v
  ,[0x3c, 0x40, 0x30, 0x40, 0x3c] # 77 w
  ,[0x44, 0x28, 0x10, 0x28, 0x44] # 78 x
  ,[0x0c, 0x50, 0x50, 0x50, 0x3c] # 79 y
  ,[0x44, 0x64, 0x54, 0x4c, 0x44] # 7a z
  ,[0x00, 0x08, 0x36, 0x41, 0x00] # 7b [
  ,[0x00, 0x00, 0x7f, 0x00, 0x00] # 7c |
  ,[0x00, 0x41, 0x36, 0x08, 0x00] # 7d ]
  ,[0x10, 0x08, 0x08, 0x10, 0x08] # 7e ~
  ,[0x78, 0x46, 0x41, 0x46, 0x78]])


#Grapic LCD Pin cofiguration
GPIO.setup(RST,GPIO.OUT)
GPIO.setup(D_C,GPIO.OUT)
GPIO.setup(CS,GPIO.OUT)
GPIO.setup(DIN,GPIO.OUT)
GPIO.setup(CLK,GPIO.OUT)

####################################################################
#Function name: lcd_init                                           # 
#Purpose      : Initializing the parameters to configure the       # 
#               Graphic LCD (Using extended command list, setting  # 
#               entry mode, powerdown control temperature          # 
#               coefficient, bias system, setting the contrast and # 
#               display mode)                                      #             
####################################################################
def lcd_init():
	print "init"
	GPIO.output(RST, GPIO.LOW)
    GPIO.output(RST, GPIO.LOW)
    spi_write(0x21, CONTROL_CMD)    #Use Extended commands
    spi_write(0xB0, CONTROL_CMD)    #Setting the contrast
	spi_write(0x04, CONTROL_CMD)    #Temparature coefficient
    spi_write(0x14, CONTROL_CMD)    #Bias system
    spi_write(0x20, CONTROL_CMD)    #Display mode
    spi_write(0x0C, CONTROL_CMD)    #Normal Display mode
		
		
####################################################################
#Function name: spi_write                                          # 
#Purpose      : The function writes data to display RAM or command #                
#               instruction depending on the CONTROL variable      #             
####################################################################

def spi_write(DATA,CONTROL):
	#The Graphic LCD is selected by giving a low signal to CS
	GPIO.output(CS, GPIO.LOW) 
    #Check if the CONTROL variable is Data or Command
	if CONTROL: 			  
    	GPIO.output(D_C, GPIO.HIGH)
    else:
      	GPIO.output(D_C, GPIO.LOW)
    temp_data = DATA
	#for loop for writing 8 bits
    for x in range (1,9):
    	#wait for 0.01seconds
		time.sleep(0.01) 
     	#computation to send one bit at a time starting from MSB
        send_bit  = temp_data & 0x080  #data is AND with 0x80
        if send_bit == 0x80: 
           	GPIO.output(DIN, GPIO.HIGH)
        elif send_bit == 0x00:
			GPIO.output(DIN, GPIO.LOW)
        # Clock is made HIGH,data sampled at positive clock edge.
		GPIO.output(CLK, GPIO.HIGH)                
		time.sleep(0.01)
		#Clock is made low	
		GPIO.output(CLK, GPIO.LOW) 
        #the data is left shifted
		temp_data = DATA << x         
	# LCD is disabled.
	GPIO.output(CS, GPIO.HIGH) 


####################################################################
#Function name: goto_xy                                            # 
#Purpose      : The function enables to go to the required location# 
#               in the LCD                                         #             
####################################################################

def goto_xy(x,y):
	#loading column #for setting the X address, DB7 is set to 1
	spi_write(0x80|x,CONTROL_CMD)   
	#loading row for setting Y address,DB7=1 DB6,DB5,DB4 = 0     
	spi_write(0x40|y,CONTROL_CMD)   


####################################################################
#Function name: lcd_clear                                          # 
#Purpose      : clears the LCD display by wroing 0 in all addresses#                                                      
####################################################################

def lcd_clear():
	#go to the first address of the LCD
	goto_xy(0,0) 
    #writes zeros in all the address
    #the address gets incremented automatically if data is written
    for z in range (0,(LCD_X*LCD_Y/8)): 
    	spi_write(0x00,CONTROL_DATA)
   	#go back to start of address
	goto_xy(0,0) 
	
####################################################################
#Function name: lcd_char                                           # 
#Purpose      : writes a character to display by calling the       # 
#               spi_write function                                 #                                                      
####################################################################

def lcd_char(char_data):
	#the data is until the 5 pixels wide character is done
	for p in range (0,5): 
    	#Manipulating ASCII character in ASCII Array
		spi_write(ASCII[ord(char_data)-0x20][p],CONTROL_DATA) 

####################################################################
#Function name: lcd_string                                         # 
#Purpose      : writes a string to display by calling the          # 
#               lcd_char function                                  #                                                      
####################################################################

def lcd_string(char_data):
	i=0
    #lcd_char function is called until the end of the string
    while (char_data[i]!='\0')
    	lcd_char(char_data[0])
       	i=i+1

#Stepper motor Pin configuration
GPIO.setup("P8_13", GPIO.OUT)	
GPIO.setup("P8_14", GPIO.OUT)
GPIO.setup("P8_15", GPIO.OUT)
GPIO.setup("P8_16", GPIO.OUT)

#initializing the LCD
lcd_init() 
lcd_clear()
input_str = "Program has started"
#go the address 1,1 in the lcd
goto_xy(1,1) 
#display the string in the LCD
lcd_string(input_str) 

#Initializing the flask server
app = Flask(__name__)
#Defining default page ‘/’
@app.route('/')
####################################################################
#Function name: index                                              # 
#Purpose      : renders the index page                             #                                                      
####################################################################

def index():
	#rendering index page
	return render_template('index.html')

####################################################################
#Function name: alarm                                              # 
#Purpose      : Blows the Buzzer and LCD with warning string       #                                                      
####################################################################

def alarm():
	#Enabling PWM for Buzzer and LCD_Backlight
	PWM.start("P9_14", 50, 1000, 1)
	#Clearing the LCD
	lcd_clear()
	#Setting the cursor to 0,0
	goto_xy(0,0) 
  	input_str = "Theft Detected!"
   	#display the string in the LCD
	lcd_string(input_str) 
    goto_xy(0,1)
    input_str = "Contact Surjith"
    #display the string in the LCD
	lcd_string(input_str) 
    goto_xy(0,2)
    input_str = "@ 720-238-3307"
    #display the string in the LCD	
	lcd_string(input_str) 
    
	#Blinking the backlight and turning on and off the buzzer
   	for x in range(0, 3):
       	PWM.stop("P9_14")
       	PWM.start("P9_16", 50,2000,0)
       	time.sleep(0.5)
       	PWM.start("P9_14",50,2000,0)
       	PWM.stop("P9_16")
    PWM.stop("P9_16")


####################################################################
#Function name: lock                                               # 
#Purpose      : rotates the stepper motor by giving the sequence   #                                                      
####################################################################

def lock():
	# 512 sequence of 1000,0100,0010,0001 has to be given for 360 # degree rotation
	for x in range(0,512):
    	GPIO.output("P8_13", GPIO.HIGH)
    	GPIO.output("P8_14", GPIO.LOW)
     	GPIO.output("P8_15", GPIO.LOW)
     	GPIO.output("P8_16", GPIO.LOW)
     	time.sleep(0.001)
     	GPIO.output("P8_13", GPIO.LOW)
     	GPIO.output("P8_14", GPIO.HIGH)
     	GPIO.output("P8_15", GPIO.LOW)
     	GPIO.output("P8_16", GPIO.LOW)
     	time.sleep(0.001)
     	GPIO.output("P8_13", GPIO.LOW)
     	GPIO.output("P8_14", GPIO.LOW)
     	GPIO.output("P8_15", GPIO.HIGH)
     	GPIO.output("P8_16", GPIO.LOW)
     	time.sleep(0.001)
     	GPIO.output("P8_13", GPIO.LOW)
     	GPIO.output("P8_14", GPIO.LOW)
     	GPIO.output("P8_15", GPIO.LOW)
     	GPIO.output("P8_16", GPIO.HIGH)
     	time.sleep(0.001)

####################################################################
#Function name: gen(camera)                                        # 
#Purpose      : gets the data from camera.py and stores the data in# 
#               frame                                              #                                                      
####################################################################

def gen(camera):
while True:
    	frame = camera.get_frame()
       	yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#defining route for locate GPS
@app.route('/locate')
####################################################################
#Function name: ggps                                               # 
#Purpose      : gets the data from gps.py and stores the data in   # 
#               string and returns the string to webpage           #                                                      
####################################################################
def ggps():
   	string = main()    
    return '<h3 align="center">'+string+'</h3>'

#defining route for alarm
@app.route('/alarm')
####################################################################
#Function name: notify alarm                                       # 
#Purpose      : executes alarm function and notifies the user      #                                                      
####################################################################

def notify_alarm():
alarm()
   	return '<h1 align="center"> ALARM Notified!</h1>'

#defining route for engine lock
@app.route('/lock')


####################################################################
#Function name: lock_stepper                                       # 
#Purpose      : executes lock function and notifies the user       #                                                      
####################################################################
def lock_stepper():
    lock()
    return '<h1 align="center"> Engine and Doors have been locked </h1>'

#defining route for video feed
@app.route('/video_feed')
####################################################################
#Function name: video_feed                                         # 
#Purpose      : gets the reponse from camera and streams the data  # 
#               in webpage                                         #                                                      
####################################################################
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

