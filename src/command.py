import serial

SERIAL_PORT = "/dev/ttyTHS1"
BAUD_RATE = 9600

driverPin = 8
lastCommand: str = "STOP"

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
    global lastCommand
    if lastCommand == action:
        return
    if action == "STOP":
        driveMotor(1, 0)
        driveMotor(2, 0)
    elif action == "LEFT":
        print("LEFT command not implemented")
    elif action == "RIGHT":
        print("RIGHT command not implemented")
    elif action == "FORWARD":
        driveMotor(1, 10)
        driveMotor(2, 10)
    elif action == "BACKWARD":
        print("BACKWARD command not implemented")
    elif action == "MODE":
        print("MODE command not implemented")
    else:
        print("Unknown command: ", action)
    lastCommand = action
