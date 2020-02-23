# Deals with choosing options to present from available
class Options:
    def __init__(self, idealSlots, otherSlots):
        self.idealSlots = idealSlots
        self.otherSlots = otherSlots
        self.lastOptions = []

    def getOptions(noOptions=3):
        if (len(idealSlots) >= noOptions):
            # Return ideal options if there's enough
            lastOptions = idealSlots[:noOptions]
            idealSlots = idealSlots[noOptions:]

            return lastOptions
        else:
            # If idealSlots don't cover the number we need, mix ideal and other
            noOthersUsed = noOptions - len(idealSlots)

            lastOptions = idealSlots + otherSlots[:noOthersUsed]
            idealSlots = []
            otherSlots = otherSlots[noOthersUsed:]

            return lastOptions

    def getLastOptions():
        return set(self.lastOptions)
