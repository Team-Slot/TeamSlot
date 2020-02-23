class Scheduler:
    def __init__(self, idealStart, idealEnd):
        self.users = list()
        self.idealTimes = list()
        self.nonIdealTimes = list()
        self.sentItems = list()
        self.idealStart = idealStart
        self.idealEnd = idealEnd

    def addUser(self,usr):
        self.users.append(usr)

    def setIdealTimes(self,idealTimes):
        self.idealTimes = idealTimes

    def setNonIdealTimes(self,nit):
        self.nonIdealTimes = nit

    ##  invoked when message received with times users agreed on (after being prompted)
    ##  if empty, should send another 3. If has one, should send that one as the one chosen
    ##  if more than one invoke method to select one randomly
    def processReceivedAgreedTimes(self,agreedTimes):
        if (len(agreedTimes) == 0):
            return self.selectNextThreeItems() 
        elif (len(agreedTimes) == 1):
            return agreedTimes ## this means this one is the one we confirm straight away
        else:
            return agreedTimes[0] ## select this as the final meeting time

    ## selects 3 items to send out as best available meeting slots
    def selectNextThreeTimes(self):
        selectedThree = list()

        ##  repeat selection of next item in list as long as length is smaller than 3
        while len(selectedThree) < 3:
            ##  next item to send
            itemToSend = None

            ##  checking every pair in idealTimes first, if found item to send break loop 
            for pair in self.idealTimes:
                if pair in self.sentItems:
                    continue ## do nothing

                else:
                    itemToSend = pair
                    break

            ##  if item to send found in ideal times, add to sent items and seleted three
            #  then move to next loop iteration
            if itemToSend != None:
                selectedThree.append(itemToSend)
                sentItems.append(itemToSend)
                continue

            for pair in self.nonIdealTimes:
                if pair in self.sentItems:
                    continue ## continue to next loop iteration

                else:
                    itemToSend = pair
                    break 

            if itemToSend != None:
                selectedThree.append(itemToSend)
                sentItems.append(itemToSend)
                continue

            else:
                break

        return selectedThree
