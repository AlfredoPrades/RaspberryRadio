import os
import time
import RPi.GPIO as GPIO
import subprocess


#Obtain the list of playlists present at the moment and create a python list 
proc = subprocess.Popen(["mpc", "ls"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
playLists = out.split();
#playLists = [  "News" ,"Chillout" ,"Trance","DI_resto" ]


GPIO.setmode(GPIO.BCM)
#current playlist index
pI = 0
#flag indicating if we are playing at the moment
playing = 0
#counter to halt the system if needed 
haltCount = 0

#action for prev button: previous track, reset halt counter
def prevt ( ):
  print "prevt"
  os.system("mpc prev")
  global haltCount 
  haltCount = 0

def nextt ( ):
  print "next"
  os.system("mpc next")
  global haltCount
  haltCount = 0


def plist ( ):
  print "plist"
  global pI
  pI = pI -1;
  if ( pI < 0 ) :
    pI = len(playLists)-1

  os.system("mpc clear")
  os.system("mpc load " + playLists[pI] )
  os.system("mpc play")
  global playing
  playing = 1
  global haltCount
  haltCount = 0



def nlist ( ):
  print "nlist"
  global pI
  pI = pI + 1 
  if ( pI >= len(playLists) ) :
    pI = 0

  os.system("mpc clear")
  os.system("mpc load " + playLists[pI] )
  os.system("mpc play")
  global playing 
  playing = 1
  global haltCount
  haltCount = 0


def play_stop ( ):
  global playing
  if ( not playing ):
     os.system("mpc play")
     playing = 1
     print "play"
  else:
     os.system("mpc stop")
     playing = 0
     print "stop"
  global haltCount
  haltCount = 0


def down ( ):
  print "down"
  os.system("mpc stop")
  global haltCount
  haltCount = haltCount + 1
  if ( haltCount == 7 ):
     os.system("halt")
  

outButton = { 22 : ('prevt',prevt), 
               4 : ('nextt',nextt),
	      24 : ('plist',plist),
	      23 : ('nlist',nlist),
	      17 : ('play_stop',play_stop),
	      18 : ('down',down )	} 
	
inputPins= outButton.keys()
inp = 0
prev_input =[ 0 ,0 ,0 ,0 ,0 ,0 ]


#Setting up all the pins we are gone read
for i in range(0,len(inputPins)):
  GPIO.setup(inputPins[i],GPIO.IN)

print ("Raspberry Radio Control ")
while True:
  for i in range(0,len(inputPins)):
    #take a reading for this pin
    inp = GPIO.input(inputPins[i])
    #if the last reading was low and this one high, call the function
    if ( ( not prev_input[i] ) and ( inp )  ):
      print( inputPins[i] )
      (outButton[inputPins[i]][1])()	  

	#save current status to compare in the next iteration of the while  
    prev_input[i] = inp
	
  #don't fry the cpu	
  time.sleep(0.10)


