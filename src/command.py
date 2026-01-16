import serial
import globalVar

SERIAL_PORT = "/dev/ttyTHS1"
BAUD_RATE = 9600

driverPin = 8
lastCommand: str = "STOP"
accel = 10
speedA = 0
speedB = 0

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def driveMotor(id: int, power: int):
    """
    Power is defined between -100 and 100
    0 is stop, -100 is max reverse, 100 is max forward
    """
    speed = max(min(power, 100), -100)
    commandByte = 0
    if id == 1:
        commandByte = int(64 + (speed * 63 / 100))
    elif id == 2:
        commandByte = int(192 + (speed * 63 / 100))
    try: 
        ser.write(bytes([commandByte]))
    except Exception as e:
        print("Erreur communication moteur: ", e)

def execCommand(action: str):
    global lastCommand, speedA, speedB, accel
    if action == lastCommand:
        return
    if action == "STOP":
        speedA = 0
        speedB = 0
    elif action == "LEFT":
        speedB += accel
    elif action == "RIGHT":
        speedA += accel
    elif action == "FORWARD":
        speedA += accel
        speedB += accel
    elif action == "BACKWARD":
        speedA -= accel
        speedB -= accel
    elif action == "SLEFT":
        speedB -= accel
    elif action == "SRIGHT":
        speedA -= accel
    elif action == "SFORWARD":
        speedA -= accel
        speedB -= accel
    elif action == "SBACKWARD":
        speedA += accel
        speedB += accel
    elif action == "MODE":
        globalVar.automode = not globalVar.automode
    elif action.startswith("SPEED"):
        accel = int(action.lstrip("SPEED"))
    else:
        print("Unknown command: ", action)
    driveMotor(1, speedA)
    driveMotor(2, speedB)
    lastCommand = action
