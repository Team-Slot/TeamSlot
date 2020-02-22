import datetime

# Splits available times into blocks of the right length
def selectAvailableBlocks(timeBlocks, meetingLength):
    allBlocks = set() # timeBlocks but in set
    available = set()

    while allBlocks:
        for block in allBlocks:
            start = block[0]
            end = block[1]
            duration = end - start
            allBlocks.remove(start, end)
            
            if (duration >= meetingLength):
                available.add((start, start + meetingLength))

                if (duration > meetingLength):
                    allBlocks.add(start - meetingLength, end)


    return available
