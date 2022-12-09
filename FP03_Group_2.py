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
yAxis = 0
blueDrop = []
greenDrop = []
corners = []

#motor.run_for_rotations(-10, 15)
#motor.run_for_rotations(10, 15)

#dis.light_up_all()

#Robot locates corner points of the grid
def calibrate():
    
    #log origin
    bottomSensor.wait_until_color('black')
    corners.append([0,0])
    blueDrop.append([0,0])
    motor_pair.start(0,10)
    bottomSensor.wait_until_color('white')
    timer.reset()

    bottomSensor.wait_until_color('black')
    motor_pair.stop()
    corners.append([timer.now(),0])
    greenDrop.append([timer.now(),0])
    motor_pair.move(1.15,'rotations', -100, 10)

    motor_pair.move((corners[1][0])*.75,'seconds', 0, 10)
    motor_pair.stop()
    motor_pair.move(.575,'rotations', 100, 10)
    
#Robot moves and searches for block to pick up
def search():
    res = dis.get_distance_cm()
    print(res)
    """while dis.get_distance_cm==None:
        print(res)
        motor_pair.move(2,'seconds', 0, 10)
        if dis.get_distance_cm==None:
            motor_pair.move(.575,'rotations', 100, 10)
            if dis.get_distance_cm==None:
                motor_pair.move(1.15,'rotations', -100, 10)
                if dis.get_distance_cm==None:
                    motor_pair.move(.575,'rotations', 100, 10)
                else:
                    break
            else:
                break
        else:
            break
        y += 2"""
    motor_pair.start(0,10)
    timer.reset()
    dis.wait_for_distance_closer_than(5, 'cm')
    motor_pair.stop()
    y= timer.now()
    res = dis.get_distance_cm()
    print(res)

    pickup()
    return_to_base()

#Raises the pallet jack to lift up the block
def pickup():
    motor_pair.move(3,'cm', 0, 10)
    motor.run_for_rotations(7, 75)
    #motor_pair.move(-20,'cm', 0, 20)
    #motor.run_for_degrees(-50, 5)

#Retraces it's steps to bring the bring the block to designated location
def return_to_base():
    motor_pair.move(1.15,'rotations', -100, 10)
    motor_pair.move(y,'seconds', 0, 10)
    if frontSensor == 'blue':
        motor_pair.move(.575,'rotations', 100, 10)
    else:
       motor_pair.move(.575,'rotations', -100, 10) 
    bottomSensor.wait_until_color("black")
    motor_pair.stop()
    motor.run_for_rotations(-7, 75) #values are adjusted to fit Paul's configuration, not the official version
    motor_pair.move((corners[1][0])*.75,'seconds', 0, -10)
    #dis.wait_for_distance_farther_than(20, 'cm')
    #motor_pair.move(1,'rotations', -100, 10)

calibrate()
search()
