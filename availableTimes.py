import datetime

# Splits available times into blocks of the right length
def _splitBlocks(availableBlocks, meetingLength):
    allBlocks = availableBlocks.copy()
    slots = set()

    while allBlocks:
        block = allBlocks.pop()

        start = block[0]
        end = block[1]
        duration = end - start
        
        if (duration >= meetingLength):
            slots.add((start, start + meetingLength))

            if (duration > meetingLength):
                allBlocks.append((start + meetingLength, end))


    return list(slots)

# Select ideal options
def getSlots(availableBlocks, meetingLength, idealHours):
    slots = _splitBlocks(availableBlocks, meetingLength)
    idealSlots = set()
    otherSlots = set()

    while slots:
        slot = slots.pop()

        startHour = slot[0].hour
        endHour = slot[1].hour

        if (startHour >= idealHours[0] and endHour <= idealHours[1]):
            idealSlots.add(slot)
        else:
            otherSlots.add(slot)

    return (list(idealSlots), list(otherSlots))
