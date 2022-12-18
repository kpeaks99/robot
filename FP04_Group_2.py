from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer

#assigns the PrimeHub to a easier name
hub = PrimeHub()
timer = Timer()
dis = DistanceSensor('D')
motor_pair = MotorPair('A', 'B')
motor = Motor('C')
bottomSensor = ColorSensor('F')
frontSensor = ColorSensor('E')
hub = PrimeHub()
grid = 10
yAxis = 0

#motor.run_for_rotations(-10, 15)
#motor.run_for_rotations(10, 15)

#dis.light_up_all()

def search():
    #reset yAxis to 0 so it can count how many grid spaces it travels
    global yAxis
    yAxis = 0
    #indicates if it must turn left or right to return to base
    trunDirection = 0
    while True:
        #moves 1 grid space
        yAxis = yAxis + 1
        motor_pair.move(grid,'cm', 0, 10)
        print('move')

        #rotates left to see an object
        #if true, breaks loop and goes to pick up object
        motor_pair.move(.5,'rotations', -100, 10)
        motor_pair.stop()
        print('left stop')
        if((dis.get_distance_cm()!=None) and (dis.get_distance_cm()<30)):
            turnDirection = -1
            break
        
        #rotates right to see an object
        #if true, breaks loop and goes to pick up object
        motor_pair.move(1,'rotations', 100, 10)
        motor_pair.stop()
        print('right stop')
        if((dis.get_distance_cm()!=None) and (dis.get_distance_cm()<30)):
            turnDirection = 1
            break
        
        #rotates left to continue straight
        motor_pair.move(.5,'rotations', -100, 10)
        motor_pair.stop()
        print('recenter')


    pickup()
    return_to_base(turnDirection)

def pickup():
    motor_pair.start(speed = 10)
    dis.wait_for_distance_closer_than(5, 'cm')
    motor_pair.stop()
    motor_pair.move(3,'cm', 0, 10)
    motor.run_for_rotations(5, 75)
    #motor_pair.move(-20,'cm', 0, 20)
    #motor.run_for_degrees(-50, 5)


def return_to_base(turnDirection):
    #reverses until it reaches the center black line
    motor_pair.start(speed = -10)
    bottomSensor.wait_until_color("black")
    motor_pair.move(5,'cm', 0, -10)

    #rotates left and moves the amount of spaces it counted
    motor_pair.move(.5,'rotations', 100*turnDirection, 10)
    return_to_center()

    #places block into designated color area
    color = frontSensor.get_color()
    if  color == 'blue':
        motor_pair.move(.5,'rotations', 100, 10)
        motor_pair.start(speed = 10)
        bottomSensor.wait_until_color("blue")
        motor_pair.stop()
        turnDirection = 1
    else:
        motor_pair.move(.5,'rotations', -100, 10) 
        motor_pair.start(speed = 10)
        bottomSensor.wait_until_color("green")
        motor_pair.stop()
        turnDirection = -1

    #drops block off
    motor_pair.move(3,'cm', 0, 10)
    motor.run_for_rotations(-5, 75)

    #reverses to go back to center line
    motor_pair.start(speed = -10)
    bottomSensor.wait_until_color("black")
    motor_pair.move(5,'cm', 0, -10)
    motor_pair.stop()

    #rotates back to collect more blocks
    motor_pair.move(.5,'rotations', 100*turnDirection, 10)
    
    
    #dis.wait_for_distance_farther_than(20, 'cm')
    #motor_pair.move(1,'rotations', -100, 10)

#returns to it's starting location
def return_to_center():
    while True:
        motor_pair.move(yAxis*grid,'cm', 0, 10)
        break
    print(yAxis*grid)

while True:
    search()
