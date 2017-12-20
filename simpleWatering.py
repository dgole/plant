import RPi.GPIO as GPIO
import time

# pump timing info
# pump is 100-350 L/H -> 50-200 oz/min -> 0.8-3.0 oz/s -> about 1 oz/s
# 2 pints a week is 32oz/wk -> 4.6 oz/day -> 0.19 oz/hr

# pump on for 5s once every day -> about 5*7=35oz/wk
#cycleTimeDHMS = [1, 0, 0, 0]
#pumpTimeDHMS  = [0, 0, 0, 5]

# test pump in sink: should fill pint glass once every minute
# 1 pint takes about 60s
# 20s per day would be 2.333 pints per week
# 15s per day would be 1.75 pints per week
# trying 3s every 2 hours, 36s per day, first second or two not much water goes to plant, just moves up tube  
cycleTimeDHMS = [0, 2, 0, 0]
pumpTimeDHMS  = [0, 0, 0, 3]


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
time.sleep(60*6)
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
