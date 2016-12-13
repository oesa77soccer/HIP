import RPi.GPIO as GPIO, time
import threading, sys

PinR = 21
PinG = 19
PinB = 20
threshold = 0.03
Green = 17
Red = 27
Blue = 22
Motor1A = 23
Motor1B = 24
Motor1E = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, GPIO.PUD_UP)
button = 26

def shutOff():  #shut off entire system
        GPIO.setmode(GPIO.BCM)
        stopStationMotor()
        GPIO.output(Green, False)
        GPIO.output(Blue, False)
        GPIO.output(Red, False)

def measureFilltime():
        #discharge the capacitor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PinR, GPIO.OUT)
        GPIO.setup(PinB, GPIO.OUT)
        GPIO.setup(PinG, GPIO.OUT)
        GPIO.output(PinB,False)
        GPIO.output(PinG,False)
        GPIO.output(PinR,False)
        time.sleep(0.05)
        #fill capacitor and measure time
        GPIO.setup(PinG, GPIO.IN)
        GPIO.setup(PinB, GPIO.IN)
        GPIO.setup(PinR, GPIO.IN)
        GPIO.setup(Red,GPIO.OUT)
        GPIO.setup(Green,GPIO.OUT)
        GPIO.setup(Blue,GPIO.OUT)
        time.sleep(threshold)
        
def brakeUp():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Green,GPIO.OUT)
        GPIO.output(Green, False)
        print "                                 Brake is in braking position."

def brakeDown():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Green,GPIO.OUT)
        GPIO.output(Green, True)
        print "                                 Brake is in lowered position."

def stopStationMotor():
        #station motor stops
        GPIO.setup(Motor1E,GPIO.OUT)
        GPIO.output(Motor1E,GPIO.LOW)

        
def stationMotorforward():
        #station motor moves forward
        GPIO.setup(Motor1A,GPIO.OUT)
        GPIO.setup(Motor1B,GPIO.OUT)
        GPIO.setup(Motor1E,GPIO.OUT)
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
        
def liftMotorforward():
        #lift motor moves forward
        GPIO.setup(Motor1A,GPIO.OUT)
        GPIO.setup(Motor1B,GPIO.OUT)
        GPIO.setup(Motor1E,GPIO.OUT)
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        
def stationChainEnter():
        #continue station motor until train is in place in the station
        measureFilltime()
        stationMotorforward()
        while (True):
                measureFilltime()
                if (GPIO.input(PinR) == True):
                        print "                                 Train 2 is not in station."
                else:  
                        stopStationMotor()
                        print "                                 Train 2 is in station."
                        break

def checkIfinStation():
        #check if the train is inside the station
        measureFilltime()
        if (GPIO.input(PinR) == False):
                print "                                 Train 1 is at station."
                GPIO.output(Red, True)
        else:
                print "                                 Train 1 is not at station."
                GPIO.output(Red, False)
                
def checkIfinStation2():
        #check if the 2nd train is placed inside the station
        measureFilltime()
        if (GPIO.input(PinR) == False):
                print "                                 Train 2 is at station."
                GPIO.output(Red, True)
        else:
                print "                                 Train 2 is not at station."
                GPIO.output(Red, False)

def checkIfatBrakerun():
        #checks if train 2 is located at the brake run
        measureFilltime()
        if (GPIO.input(PinG) == False):
                print "                                 Train 2 is at brake run."
                GPIO.output(Green, True)
        else:
                print "                                 Train 2 is not at brake run."
                GPIO.output(Green, False)


def stationChainExit():
        #counts the change in light as each wheel of each car intersects light
        stationchange = 0
        stationcount = 0
        measureFilltime()
        stationMotorforward()
        print stationchange, " = stationchange"
        for stationinx in range (0,2):
                print stationinx, " = stationinx"
                if (GPIO.input(PinR) == True):  
                    GPIO.output(Red, True)
                    print stationchange, " = stationchange"
                    while (stationchange == stationinx) and (stationcount < 6):
                            #while these conditions are true, the program will count the 5 wheels passing...
                            #...the light and exit out of the while loop after the train has passed
                        print stationcount, " = stationcount"   
                        measureFilltime()
                                #detects if the wheel is there, then goes into another while to check if it changes.
                        if (GPIO.input(PinR) == True):
                                GPIO.output(Red, True)
                        else:
                            if (GPIO.input(PinR) == False):
                                    GPIO.output(Red, False)
                                    while (stationchange == stationinx):
                                        measureFilltime()  
                                        if (GPIO.input(PinR) == False):
                                                GPIO.output(Red, False)
                                        else:
                                            if (GPIO.input(PinR) == True):
                                                    GPIO.output(Red, True)
                                                    stationcount = stationcount + 1
                                                    break
                    else:
                                continue
                else:
                        stationchange = stationchange + 1
                        print "bottom else"
def liftChainExit():
        #(same style of program as the station) Checks if the entire train has passed the certain point on the lift.
        liftchange = 0
        liftcount = 0
        measureFilltime()
        print liftchange, " =liftchange"
        for liftinx in range (0,3):
                print liftinx, " =liftinx"
                checkIfinStation2()
                measureFilltime()
                if (GPIO.input(PinG) == True):  
                    GPIO.output(Blue, True)
                    print liftchange, " liftchange"
                    while (liftchange == liftinx) and (liftcount < 6):
                        measureFilltime()
                        print liftcount, " =liftcount"   
                        if (GPIO.input(PinB) == True):
                                GPIO.output(Blue, False)
                        else:
                            if (GPIO.input(PinB) == False):
                                    GPIO.output(Blue, True)
                                    while (liftchange == liftinx):
                                        measureFilltime()                         
                                        if (GPIO.input(PinB) == False):
                                                GPIO.output(Blue, True)
                                        else:
                                            if (GPIO.input(PinB) == True):
                                                    GPIO.output(Blue, False)
                                                    liftcount = liftcount + 1
                                                    break
                    else:
                             continue
                else:
                        GPIO.output(Blue, False)
                        liftchange = liftchange + 1
                        print ""
                        

def brakeExit():
        #same way it checks the lift and station to see if the train has left the brake run.
        brakechange = 0
        brakecount = 0
        measureFilltime()
        print brakechange, " =brakechange"
        for brakeinx in range (0,2):
                print brakeinx, " =brakeinx"
                if (GPIO.input(PinG) == True):  
                    GPIO.output(Green, True)
                    print brakechange, " brakechange"
                    while (brakechange == brakeinx) and (brakecount < 5):
                        print brakecount, " =brakecount"   
                        measureFilltime()  
                        if (GPIO.input(PinG) == True):
                                GPIO.output(Green, True)
                        else:
                            if (GPIO.input(PinG) == False):
                                    GPIO.output(Green, False)
                                    while (brakechange == brakeinx):
                                        measureFilltime()                         
                                        if (GPIO.input(PinG) == False):
                                                GPIO.output(Green, False)
                                        else:
                                            if (GPIO.input(PinG) == True):
                                                    GPIO.output(Green, True)
                                                    brakecount = brakecount + 1
                                                    break

                else:
                        brakechange = brakechange + 1
                        print "bottom else"

#runs what a round of how the roller coaster should perform in order, checking specific points at certain times to ensure safety.
def rollercoasterProgram():
        #t = threading.Thread(target=measureFilltime, args = ())
        #t.daemon = True
        #t.start()
        measureFilltime()
        GPIO.output(Green, False)
        GPIO.output(Blue, False)
        GPIO.output(Red, False) 
        while (True):
                #breaks out of the while loop after 1 complete run, turning off when the two trains are in the ending position.
                measureFilltime()
                checkIfinStation()
                checkIfatBrakerun()
                if (GPIO.input(PinG) == False) and (GPIO.input(PinR) == False):
                        print "                                 Train 1 is leaving station."
                        stationChainExit()
                        print "                                 Train 1 is entering lift hill."
                        GPIO.output(Green, False)
                        stopStationMotor()
                        GPIO.output(Blue, True)
                        print "                                 Start lift hill motor"
                        shutOff()
                        brakeDown()
                        brakeExit()
                        GPIO.output(Green, False)
                        print "                                 Train 2 left brake run, heading to station."
                        brakeUp()
                        measureFilltime()
                        if (GPIO.input(PinR) == False):
                                stopStationMotor()
                        else:
                                stationChainEnter()        
                        liftChainExit()
                        print "                                 Train 1 left lift hill."
                        measureFilltime()
                        if (GPIO.input(PinR) == False):
                                stopStationMotor()
                        else:
                                stationChainEnter()
                        print "                                 Station chain stopped."
                        break

#runs entire program once per time the button is pressed.

while True:
   
   GPIO.setup(26, GPIO.IN, GPIO.PUD_UP)
   button_state = GPIO.input(button)
   if button_state == GPIO.LOW:
        while True:   
                rollercoasterProgram()
                shutOff()
                break
   else:
      print " "
      time.sleep(1)

GPIO.cleanup()
