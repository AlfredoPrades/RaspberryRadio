import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pI = 0
playLists = [  "News" ,"Chillout" ,"Trance","DI_resto" ]


playing = 0
haltCount = 0


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
inp =       [ 0 ,0 ,0 ,0 ,0 ,0 ]
prev_input =[ 0 ,0 ,0 ,0 ,0 ,0 ]

for i in range(0,len(inputPins)):
  GPIO.setup(inputPins[i],GPIO.IN)


print ("radior")
while True:
  for i in range(0,len(inputPins)):
    #take a reading
    inp[i] = GPIO.input(inputPins[i])
    #if the last reading was low and this one high, print
    if ( (not prev_input[i]) and ( inp[i] )  ):
      print(inputPins[i])
      (outButton[inputPins[i]][1])()	  

    prev_input[i] = inp[i]
  time.sleep(0.10)


