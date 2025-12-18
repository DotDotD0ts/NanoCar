lastCommand: str = "STOP"

def execCommand(action: str):
    global lastCommand
    if lastCommand == action:
        return
    if action == "STOP":
        print("STOP command not implemented")
    elif action == "LEFT":
        print("LEFT command not implemented")
    elif action == "RIGHT":
        print("RIGHT command not implemented")
    elif action == "FORWARD":
        print("FORWARD command not implemented")
    elif action == "BACKWARD":
        print("BACKWARD command not implemented")
    elif action == "MODE":
        print("MODE command not implemented")
    else:
        print("Unknown command: ", action)
    lastCommand = action
