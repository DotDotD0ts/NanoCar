import serial
import globalVar

SERIAL_PORT = "/dev/ttyTHS1"
BAUD_RATE = 9600

driverPin = 8
lastCommand: str = "STOP"
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
    global lastCommand, speedA, speedB
    if action == lastCommand:
        return
    if action == "STOP":
        speedA = 0
        speedB = 0
    elif action == "LEFT":
        speedA = 0
        speedB = globalVar.speed
    elif action == "RIGHT":
        speedA = globalVar.speed
        speedB = 0
    elif action == "FORWARD":
        speedA = globalVar.speed
        speedB = globalVar.speed
    elif action == "BACKWARD":
        speedA = -globalVar.speed
        speedB = -globalVar.speed
#    elif action == "SLEFT":
#        speedB -= globalVar.speed
#    elif action == "SRIGHT":
#        speedA -= globalVar.speed
#    elif action == "SFORWARD":
#        speedA -= globalVar.speed
#        speedB -= globalVar.speed
#    elif action == "SBACKWARD":
#        speedA += globalVar.speed
#        speedB += globalVar.speed
    elif action == "MODE":
        globalVar.automode = not globalVar.automode
    elif action.startswith("SPEED"):
        globalVar.speed = int(action.lstrip("SPEED"))
    else:
        print("Unknown command: ", action)
    driveMotor(1, speedA)
    driveMotor(2, speedB)
    lastCommand = action
