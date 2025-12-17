def execCommand(action: str):
    match action:
        case "STOP":
            print("STOP command not implemented")
        case "LEFT":
            print("LEFT command not implemented")
        case "RIGHT":
            print("RIGHT command not implemented")
        case "FORWARD":
            print("FORWARD command not implemented")
        case "BACKWARD":
            print("BACKWARD command not implemented")
        case "MODE":
            print("MODE command not implemented")
        case _:
            print("Unknown command: ", action)
