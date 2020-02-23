# TeamSlot

TeamSlot is a project from the University of Southampton's CampusHack 2020. It aims to make organising meetings simpler, organising group meetings according to everybody's availability. TeamSlot is comprised of ScheduleCore, a public API to schedule meetings with first and third party applications to implement this. Initially, this has been developed with a first party Slack bot.

## Aims

TeamSlot aims to organise meetings for you to save time cross checking schedules. It does this by importing everybody's calendars to schedule meeting slots as requested, confirming options with each member, confirming the final slot with the team leader and then alerting the group (e.g. via a channel in the case of Slack) with the final slot.

TeamSlot can potentially be used on various platforms, with a public API for anybody to use and extend. To begin with, we developed a Slack chat bot to implement TeamSlot's ScheduleCore into a user friendly interface.

## Features

- handles iCal calendar URLs to store user schedules
- user URLs can be updated
- takes requests to arrange a meeting slot
- returns extra options if the first load aren't good options

## Classes

- ScheduleCore.py - the main class from which our Slack bot and third parties can use ScheduleCore
- User.py - the user class
- Messages.py - the messages class
- Database.py - the database class for interfacing with our SQLite database, which holds our User URLs
- parseCals.py - takes iCal URLs, parses the calendars and extracts blocks of availability
- availableTimes.py - take blocks of availability and split by desired meeting length into potential slots, taking heuristics for a good time into account
- Options.py - the class for choosing options to present to the API user from the available slots calculated, sending ideal slots according to heuristics first

## Using the API

To use the API, developers need to first instantiate our ScheduleCore class and pass user data with the provided functions. After this, developers will need to call the `processRequest` function to handle an initial request to schedule a meeting. This will handle the scheduling and after calculating available slots, return some initial options that can be presented to the end user(s). From here, developers can implement their applications to allow for further options with our `getMoreOptions` function, which will return any remaining options calculated. We developed this function to first return ideal slots (according to our heuristics), filling in with the remaining options once these run out.

Once the user has seen the slot options, they can reply to say which they won't be available for - this allows for situations where a user doesn't have all their commitments in their calendar. Following this, ScheduleCore will decide on a final slot and return this to the developer.

### API functions

- initialiser
- addUser(userid, calURL) - takes a userid with a iCal URL and enters this to the database on the backend
- updateUser(userid, newCalURL) - takes a userid with a new iCal URL and updates this on the database on the backend
- processRequest(users, dateRange, workingHours, meetingLength, idealHours = (9,17)) - takes a few parameters to calculate possible slots and supply the initial options from these:
  - users: a list of userids to represent the list of group members intended to attend said meeting
  - dateRange: a touple of datetimes to represent the dates to book the meeting between e.g. 23/02/2020 until 28/02/2020
  - workingHours: a touple of datetime.time to represent the times that the team are willing to work between, the times of the day that the meeting must not be booked outside of
- getMoreOptions(): returns remaining options, used if none of the options supplied work for everybody
- getFinalSlot(): taking a list (potentially empty) of slots that don't work for everybody in the team, this function then calculates the slots that do work for everybody and determines a slot for the meeting, returning this as the final slot
