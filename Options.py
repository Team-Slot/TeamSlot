# Deals with choosing options to present from available
class Options:
    def __init__(self, idealSlots, otherSlots):
        self.idealSlots = idealSlots
        self.otherSlots = otherSlots
        self.lastOptions = []

    def getOptions(self, noOptions=3):
        if (len(self.idealSlots) >= noOptions):
            # Return ideal options if there's enough
            lastOptions = self.idealSlots[:noOptions]
            idealSlots = self.idealSlots[noOptions:]

            return lastOptions
        else:
            # If idealSlots don't cover the number we need, mix ideal and other
            noOthersUsed = noOptions - len(self.idealSlots)

            lastOptions = self.idealSlots + self.otherSlots[:noOthersUsed]
            idealSlots = []
            otherSlots = self.otherSlots[noOthersUsed:]

            return lastOptions

    def getLastOptions(self):
        return set(self.lastOptions)
