import RPi.GPIO as GPIO 
import time

# pump timing info
# trying 3s every 2 hours, 36s per day, first second or two not much water goes to plant, just moves up tube  
cycleTimeDHMS = [0, 4, 0, 0]
pumpTimeDHMS  = [0, 0, 0, 5]


###################################################################################
# probably don't change much below here
###################################################################################
# GPIO setup
pumpPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pumpPin, GPIO.OUT)
# time math
cycleTimeSeconds = (24.0 * 60.0 * 60.0 * cycleTimeDHMS[0]
                          + 60.0 * 60.0 * cycleTimeDHMS[1]
                                 + 60.0 * cycleTimeDHMS[2]
                                        + cycleTimeDHMS[3])
pumpTimeSeconds  = (24.0 * 60.0 * 60.0 * pumpTimeDHMS[0]
                          + 60.0 * 60.0 * pumpTimeDHMS[1]
                                 + 60.0 * pumpTimeDHMS[2]
                                        + pumpTimeDHMS[3])
waitTimeSeconds   = cycleTimeSeconds - pumpTimeSeconds
# main loop
n=0
while True:
    try:
        # turn on
        print('pump turned on at ' + time.ctime())
        GPIO.output(pumpPin, GPIO.HIGH)
        # wait for pumpTime while pump is on
        time.sleep(pumpTimeSeconds)
        # turn off
        print('pump turned off at ' + time.ctime())
        n=n+1; print(n)
        GPIO.output(pumpPin, GPIO.LOW)
        # wait for waitTime while pump is off
        time.sleep(waitTimeSeconds)
    except KeyboardInterrupt:
        GPIO.cleanup()
