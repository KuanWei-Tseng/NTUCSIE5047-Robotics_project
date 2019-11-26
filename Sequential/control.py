def fix(rightSpd, leftSpd, dev, y, w):
    """
    return devised rightSpd and leftSpd to fix the deviation
    """
    if y == 1 and w == 1:
        # both line found, dev is the deviation
        if dev > 10:
            # should go left
            rightSpd = 70
            leftSpd = 10
        elif dev < -10:
            # should go right
            rightSpd = 10
            leftSpd = 70
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50

    elif y == 1 and w <= 0:
        # only found yellow line, dev is y offset
        if dev > 10:
            # should go right
            rightSpd = 10
            leftSpd = 70
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50
    else:
        # stop
        rightSpd = 0
        leftSpd = 0

    return rightSpd, leftSpd
        
