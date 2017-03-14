import RPi.GPIO as GPIO, time, math

Servo = 12
PinR = 21
PinG = 19
PinB = 20
thresholdR = 0.06 #station
thresholdG = 0.06 #brake
thresholdB = 0.06 #lifthill
Green = 22
Red = 27
Blue = 17
Motor1A = 23
Motor1B = 24
Motor1E = 25
button = 26
Motor2A = 5
Motor2B = 6
Motor2E = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(Servo,GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(Red,GPIO.OUT)
GPIO.setup(Green,GPIO.OUT)
GPIO.setup(Blue,GPIO.OUT)
GPIO.setup(PinG, GPIO.IN)
GPIO.setup(PinB, GPIO.IN)
GPIO.setup(PinR, GPIO.IN)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
pwm = GPIO.PWM(Servo,50)
        
def shutOff():  #shut off entire system
        stopStationMotor()
        stopliftMotor()
        GPIO.output(Green, False)
        GPIO.output(Blue, False)
        GPIO.output(Red, False)
        
def clean(): 
  GPIO.cleanup()


def measureFilltimeB():
        #discharge the capacitor
        GPIO.setup(PinB, GPIO.OUT)
        GPIO.output(PinB,False)
        time.sleep(0.01)
        #fill capacitor and measure time
        GPIO.setup(PinB, GPIO.IN)
        time.sleep(thresholdB)
def measureFilltimeG():
        #discharge the capacitor
        GPIO.setup(PinG, GPIO.OUT)
        GPIO.output(PinG,False)
        time.sleep(0.01)
        #fill capacitor and measure time
        GPIO.setup(PinG, GPIO.IN)
        time.sleep(thresholdG)
def measureFilltimeR():
        #discharge the capacitor
        GPIO.setup(PinR, GPIO.OUT)
        GPIO.output(PinR,False)
        time.sleep(0.01)
        #fill capacitor and measure time
        GPIO.setup(PinR, GPIO.IN)
        time.sleep(thresholdR)
        
def brakeUp():
        pwm.start(5)
        time.sleep(.13)
        pwm.start(0)
        #GPIO.output(Green, False)
        print "                                 Brake is in braking position."

def brakeDown():
        pwm.start(11)
        time.sleep(.15)
        pwm.start(0)
        print "                                 Brake is in lowered position."

def stopStationMotor():
        #station motor stops
        GPIO.output(Motor1E,GPIO.LOW)

def stopliftMotor():
        #lift motor stops
        GPIO.output(Motor2E,GPIO.LOW)
        
def stationMotorforward():
        #station motor moves forward
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
        
def liftMotorforward():
        #lift motor moves forward
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        
def stationChainEnter():
        #continue station motor until train is in place in the station
        measureFilltimeR()
        stationMotorforward()
        while (True):
                measureFilltimeR()
                if (GPIO.input(PinR) == True):
                        print "                                 Train 2 is not in station."
                else:  
                        stopStationMotor()
                        print "                                 Train 2 is in station."
                        break

def checkIfinStation():
        #check if the train is inside the station
        measureFilltimeR()
        if (GPIO.input(PinR) == False):
                        print "                                 Train 1 is at station."
                        #GPIO.output(Red, True)                
        else:
                        print "                                 Train 1 is not at station."
                        #GPIO.output(Red, False)
                
def checkIfinStation2():
        #check if the 2nd train is placed inside the station
        measureFilltimeR()
        if (GPIO.input(PinR) == False):
                print "                                 Train 2 is at station."
                #GPIO.output(Red, True)
        else:
                print "                                 Train 2 is not at station."
                #GPIO.output(Red, False)

def checkIfatBrakerun():
        #checks if train 2 is located at the brake run
        measureFilltimeG()
        if (GPIO.input(PinG) == False):
                print "                                 Train 2 is at brake run."
                #GPIO.output(Green, True)
        else:
                print "                                 Train 2 is not at brake run."
                #GPIO.output(Green, False)


def stationChainExit():
        #counts the change in light as each wheel of each car intersects light
        stationchange = 0
        stationcount = 0
##        measureFilltimeR()
        stationMotorforward()
        print stationchange, " = stationchange"
        for stationinx in range (0,2):
                print stationinx, " = stationinx"
                while (GPIO.input(PinR) == False) and (stationcount == 0):
                        print "Train 1 is still at station"
                        #time.sleep(thresholdR)
                        time.sleep(0.025)                       
                if (GPIO.input(PinR) == True):  
                    #GPIO.output(Red, True)
                    print stationchange, " = stationchange"
                    while (stationchange == stationinx) and (stationcount < 4):
                            #while these conditions are true, the program will count the 5 wheels passing...
                            #...the light and exit out of the while loop after the train has passed
                        print stationcount, " = stationcount"   
                        measureFilltimeR()
                                #detects if the wheel is there, then goes into another while to check if it changes.
                        if (GPIO.input(PinR) == True):
                                GPIO.output(Red, True)
                        else:
                                while (stationchange == stationinx):
                                    measureFilltimeR()
                                    #GPIO.output(Red, False)
                                    if (GPIO.input(PinR) == False):
                                        GPIO.output(Red, True)     
                                    else:
                                                GPIO.output(Red, True)
                                                stationcount = stationcount + 1
                                                break
                else:
                        stationchange = stationchange + 1
                        print "bottom else"

def liftChainExit():
        #(same style of program as the station) Checks if the entire train has passed the certain point on the lift.
        liftchange = 0
        liftcount = 0
        measureFilltimeB()
        print liftchange, " =liftchange"
        for liftinx in range (0,2):
                print liftinx, " =liftinx"
                checkIfinStation2()
                measureFilltimeB()
                if (GPIO.input(PinG) == True):  
                    #GPIO.output(Blue, True)
                    print liftchange, " liftchange"
                    while (liftchange == liftinx) and (liftcount < 2):
                        measureFilltimeB()
                        print liftcount, " =liftcount"   
                        if (GPIO.input(PinB) == True):
                                GPIO.output(Blue, True)
                        else:
                            #GPIO.output(Blue, True)
                            while (liftchange == liftinx):
                                measureFilltimeB()                         
                                if (GPIO.input(PinB) == False):
                                        GPIO.output(Blue, True)
                                else:
                                    #GPIO.output(Blue, False)
                                    liftcount = liftcount + 1
                                    break
                else:
                        #GPIO.output(Blue, False)
                        liftchange = liftchange + 1
                        print ""
        stopliftMotor()

def brakeExit():
        #same way it checks the lift and station to see if the train has left the brake run.
        brakechange = 0
        brakecount = 0
        measureFilltimeG()
        print brakechange, " =brakechange"
        for brakeinx in range (0,2):
                print brakeinx, " =brakeinx"
                while (GPIO.input(PinG) == False) and (brakecount == 0):
                        print "Train 2 is still at brake run"
                        time.sleep(thresholdG)
                if (GPIO.input(PinG) == True):  
                    #GPIO.output(Green, True)
                    print brakechange, " brakechange"
                    while (brakechange == brakeinx) and (brakecount < 3):
                        print brakecount, " =brakecount"   
                        measureFilltimeG()  
                        if (GPIO.input(PinG) == True):
                                GPIO.output(Green, True)
                        else:
                            #GPIO.output(Green, False)
                            while (brakechange == brakeinx):
                                measureFilltimeG()                         
                                if (GPIO.input(PinG) == False):
                                        GPIO.output(Green, True)
                                else:
                                    #GPIO.output(Green, True)
                                    brakecount = brakecount + 1
                                    break

                else:
                        brakechange = brakechange + 1
                        print "bottom else"

#runs what a round of how the roller coaster should perform in order, checking specific points at certain times to ensure safety.
def rollercoasterProgram():
        GPIO.output(Green, True)
        GPIO.output(Red, True)                           #breaks out of the while loop after 1 complete run, turning off when the two trains are in the ending position.
        for numberOfRuns in range (1):
                while(True):
                        checkIfinStation()
                        checkIfatBrakerun()
                        if (GPIO.input(PinG) == False) and (GPIO.input(PinR) == False):
                                print "                                 Train 1 is leaving station."
                                stationChainExit()
                                print "                                 Train 1 is entering lift hill."
                                #GPIO.output(Green, False)
                                stopStationMotor()
                                liftMotorforward()
                                GPIO.output(Blue, True)
                                print "                                 Start lift hill motor"
                                #shutOff()
                                brakeDown()
                                brakeExit()
                                #GPIO.output(Green, False)
                                print "                                 Train 2 left brake run, heading to station."
                                brakeUp()
                                measureFilltimeR()
                                if (GPIO.input(PinR) == False):
                                        stopStationMotor()
                                else:
                                        stationChainEnter()        
                                liftChainExit()
                                print "                                 Train 1 left lift hill."
                                measureFilltimeR()
                                if (GPIO.input(PinR) == False):
                                        stopStationMotor()
                                else:
                                        stationChainEnter()
                                print "                                 Station chain stopped."
                                
                                break

def getTime(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,False)
    time.sleep(0.2)

    GPIO.setup(pin, GPIO.IN)
    startTime = time.time()
    while (GPIO.input(pin) == False):
        pass
    threshold = time.time() - startTime;
    print ("Time:", pin, threshold);
    return threshold;

def initializeThresholds():
    GPIO.output(Red,True)
    GPIO.output(Blue,True)
    GPIO.output(Green,True)

    maxTime = 0.0;
    for i in range(5):
        currentTime = getTime(PinR)
        if (currentTime > maxTime):
            maxTime = currentTime;
    thresholdR =  math.ceil(100 * maxTime) / 100;
    print ("Threshold R set to ", thresholdR);

    maxTime = 0.0
    for i in range(5):
        currentTime = getTime(PinG)
        if (currentTime > maxTime):
            maxTime = currentTime;
    thresholdG =  math.ceil(100 * maxTime) / 100;
    print ("Threshold G set to ", thresholdG);    

    maxTime = 0.0
    for i in range(5):
        currentTime = getTime(PinB)
        if (currentTime > maxTime):
            maxTime = currentTime;
    thresholdB =  math.ceil(100 * maxTime) / 100;
    print ("Threshold B set to ", thresholdB);    

                        

#runs entire program once per time the button is pressed.

initializeThresholds()

while True:
   shutOff()
   GPIO.setup(26, GPIO.IN, GPIO.PUD_UP)
   button_state = GPIO.input(button)
   if button_state == GPIO.LOW:
        rollercoasterProgram()
        shutOff()
        break
   else:
      print " "
      time.sleep(1)

GPIO.cleanup()
