##  Plan the code out here :
##  make method which takes tuple list of all users tuples and send to 


class Scheduler:
    def __init__(self, idealStart, idealEnd):
        self.users = list()
        self.idealTimes = list()
        self.nonIdealTimes = list()
        self.idealStart = idealStart
        self.idealEnd = idealEnd


    def addUser(self,usr):
        self.users.append(usr)

    ##  When receiving a list of times, will classify into ideal times and non ideal times then store
    def classifyReceivedTimes(self,received):
        ## received is a list of DateTime tuples
        ## if within ideal time range, then add to idealTimes
        ## if not, add to nonIdealTimes
        for start,end in received:
            if (start >= self.idealStart and end <= self.idealEnd):
                self.idealTimes.append((start,end))
            else:
                self.nonIdealTimes.append((start,end))



    def getAllIdealTimes(self,idealTimes):
        pass

    ##  invoked when message received with times users agreed on (after being prompted)
    ##  if empty, should send another 3. If has one, should send that one as the one chosen
    ##  if more than one invoke method to select one randomly
    def processReceivedAgreedTimes(self,agreedTimes):
        if (len(agreedTimes) == 0):
            pass ## send message of 3 others 
        elif (len(agreedTimes) == 1):
            pass ## this means this one is the one we confirm straight away
        else:
            pass ## select random 3 and store rest

    ##def 


##class User:
    pass
