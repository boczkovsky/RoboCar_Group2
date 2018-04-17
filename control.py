import signal, os
import RPi.GPIO as GPIO
import time

PWMA = 17
PWMB = 23
AIN1 = 2
AIN2 = 3
BIN1 = 14
BIN2 = 15

IO_FORWARD = 16
IO_BACKWARD = 20
IO_STOP = 21
IO_TURN_LEFT = 19
IO_TURN_RIGHT = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

GPIO.setup(IO_FORWARD, GPIO.OUT)
GPIO.setup(IO_BACKWARD, GPIO.OUT)
GPIO.setup(IO_STOP, GPIO.OUT)
GPIO.setup(IO_TURN_LEFT, GPIO.OUT)
GPIO.setup(IO_TURN_RIGHT, GPIO.OUT)

leftSide = GPIO.PWM(PWMA, 50)
rightSide = GPIO.PWM(PWMB, 50)

speed = 40

def forwardCar():
    print("Setup forward")
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    spin(leftSide, speed)
    spin(rightSide, speed)
    GPIO.output(IO_FORWARD, GPIO.LOW)
    
def backwardCar():
    print("Setup backward")
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    spin(leftSide, speed)
    spin(rightSide, speed)
    GPIO.output(IO_BACKWARD, GPIO.LOW)
    
def turnLeftCar():
    print("Setup turn left")
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    spin(leftSide, speed)
    spin(rightSide, speed)
    GPIO.output(IO_TURN_LEFT, GPIO.LOW)
    
def turnRightCar():
    print("Setup turn right")
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    spin(leftSide, speed)
    spin(rightSide, speed)
    GPIO.output(IO_TURN_RIGHT, GPIO.LOW)
    
def stop(motor):
    motor.start(0)
    motor.ChangeDutyCycle(0)
    
def stopCar():
    stop(leftSide)
    stop(rightSide)
    GPIO.output(IO_STOP, GPIO.LOW)

def spin(motor, speed):
    print("Spin the motor!")
    motor.start(0)
    motor.ChangeDutyCycle(speed)

def handler(signum, frame): #stop when ctrl-c is recieved
    print("Signal handler called with signal", signum)
    print("Exiting...")
    GPIO.output(PWMA, GPIO.LOW)
    GPIO.output(PWMB, GPIO.LOW)
    GPIO.cleanup()
    exit(0)

# When recieving ctrl-C
signal.signal(signal.SIGINT, handler)

while True:
	if GPIO.input(IO_FORWARD):
		forwardCar()
		
	if GPIO.input(IO_BACKWARD):
		backwardCar()
		
	if GPIO.input(IO_STOP):
		stopCar()
		
	if GPIO.input(IO_TURN_LEFT):
		turnLeftCar()
		
	if GPIO.input(IO_TURN_RIGHT):
		turnRightCar()

	time.sleep(0.1)

