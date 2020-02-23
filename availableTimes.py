import datetime

# Splits available times into blocks of the right length
def __selectAvailableBlocks(timeBlocks, meetingLength):
    allBlocks = timeBlocks.copy()
    available = set()

    while allBlocks:
        block = allBlocks.pop()

        start = block[0]
        end = block[1]
        duration = end - start
        
        if (duration >= meetingLength):
            available.add((start, start + meetingLength))

            if (duration > meetingLength):
                allBlocks.append((start + meetingLength, end))


    return list(available)

# Select ideal options
def selectIdealBlocks(timeBlocks, meetingLength, idealTimeStart, idealTimeEnd):
    blocks = selectAvailableBlocks(timeBlocks, meetingLength)
    idealBlocks = set()
    otherBlocks = set()

    days = list(range(0,6)) # 0..5 (mon-fri)

    while blocks:
        block = blocks.pop()

        startHour = block[0].hour
        endHour = block[1].hour

        if (startHour >= idealTimeStart and endHour <= idealTimeEnd):
            idealBlocks.add(block)
        else:
            otherBlocks.add(block)

    return (list(idealBlocks), list(otherBlocks))
