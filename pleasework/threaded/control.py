def fix(rightSpd, leftSpd, dev, theta, type):
    """
    return devised rightSpd and leftSpd to fix the deviation
    """
    if type == "b":
        # both line found, dev is the deviation
        if dev > 10:
            # should go left
            rightSpd = 80
            leftSpd = 20
        elif dev < -10:
            # should go right
            rightSpd = 20
            leftSpd = 80
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50

    elif type == "y":
        # only found yellow line, dev is y_offset
        if dev > 10:
            # should go right
            rightSpd = 0
            leftSpd = 80
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50

    elif type == "w":
        # only found white line, dev is w_offset
        if dev < 650:
            # should go left
            rightSpd = 80
            leftSpd = 0
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50

    else:
        # stop
        rightSpd = 0
        leftSpd = 0

    return rightSpd, leftSpd
        
