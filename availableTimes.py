import datetime

# Splits available times into blocks of the right length
def selectAvailableBlocks(timeBlocks, meetingLength):
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


    return available
