def fix(rightSpd, leftSpd, dev, y, w):
    """
    return devised rightSpd and leftSpd to fix the deviation
    """
    if dev > 10:
        devlev = (dev/abs(dev))*(dev//30)
    else:
        devlev = 0
    
    Spd = (rightSpd + leftSpd)/2
    if y == 1 and w == 1:
        # both line found, dev is the deviation
        if devlev == 0:
            rightSpd = Spd
            leftSped = Spd
        elif devlev > 0:
            rightSpd = max(0,rightSpd-devlev*5)
            leftSpd = min(100,leftSpd+devlev*5)
        else:
            rightSpd = min(100,rightSpd+develv*5)
            leftSped = max(0,leftSped-devlev*5)
    elif y == 1 and w <= 0:
        if devlev == 0:
            rightSpd = Spd
            leftSped = Spd
        elif devlev > 0:
            rightSpd = max(0,rightSpd-devlev*5)
            leftSpd = min(100,leftSpd+devlev*5)
        else:
            rightSpd = min(100,rightSpd+develv*5)
            leftSped = max(0,leftSped-devlev*5)
    else:
        # stop
        rightSpd = 0
        leftSpd = 0

    return rightSpd, leftSpd
        
