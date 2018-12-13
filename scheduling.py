# -*- coding: utf-8 -*-

# 2018-2019 Programação 1 (LTI)
# Grupo 38
# 49187 Sofia Torres
# 49269 Mário Gil Oliveira


from operator import itemgetter
import timeOperations
import copy


def attributional(clients,experts):
    """
    Runs the attribution function for each of the clients
    in the clients list
    Requires: clients as list
    Requires: experts as list
    Ensures: a list in the following format
    (client name, expert name)
    """
    tup = []
    for i in clients:
        exp = attribution(i,experts)
        if len(exp[0]) > 1:
            tup = tup + [(i[0],exp[0][0],exp[1],exp[2]),]
        else:
            tup = tup + [(i[0],exp[0][0]),]

    return (tup,experts)


def attribution (client, experts):
    """
    Matches a client request with a list of experts and updates the list of experts
    Requires: client as a list with the attributes as stated in the project
    Requires: experts a list in which each item is a list of attributes of a specific expert,
    as stated in the project
    Ensures: a list with the attributes of the expert that best matches the request,
    according to the project.
    An empty list means a match isn't possible
    """

    
    expertshour = copy.deepcopy(experts)
    
    for i in expertshour:
        i[5] = timeOperations.travelTime(i[5],i[6])[0]
        i[6] = timeOperations.travelTime(i[5],i[6])[1]

    compatibleExperts = []
    for i in expertshour:
        if client[6] in i[2] and i[3] >= client[5] and \
           i[4] <= client[4] and i[1] == client[1]:
            compatibleExperts.append(i)

    compatibleExperts = sorted(compatibleExperts, key=itemgetter(5, 6, 4, 7, 0))
    # sorts the compatibleExperts list by date, then by time, then by pay, then by name
    # compatibleExperts[0] >> WINNER

    
    if len(compatibleExperts) == 0:
        return (["declined",],experts)

            
    # search for the selected expert index
    indi = expertshour.index(compatibleExperts[0])
    # update just the selected expert to the new hour
    experts[indi] = copy.deepcopy(compatibleExperts[0])

    # tuple with (date, time) of the client and expert to compare them
    compareCli = (client[2],client[3])
    compareExp = (compatibleExperts[0][5],compatibleExperts[0][6])
    listaCliExp = (compareCli,compareExp)
    # finds the latest time of availability between the client and the expert
    TimeSchedule = sorted(listaCliExp, key=lambda element: (element[0], element[1]))[1]


    # updates the available time and date
    newTime = timeOperations.timeCalculate(TimeSchedule[0],TimeSchedule[1],client[7])
    experts[indi][5] = newTime[0] #date
    experts[indi][6] = newTime[1] #time

    # updates the total earned amount
    experts[indi][7] = experts[indi][7] + (experts[indi][4]*client[7])/60

    
    #returns the  expert, schedule date, schedule time and the updated experts list
    return (compatibleExperts[0],TimeSchedule[0],TimeSchedule[1],experts)


def sortScheduleOutput(schedule):
    """
    Takes an unsorted schedule list and sorts it according to the project criteria,
    in the order that will be outputted to the file.
    Requires: schedule as list (generated by the functions in this module)
    Ensures: a list with the same information, but in the correct output order
    specified in the project
    """
    declined = []

    # placing the declined in the new list first
    for i in schedule:
        if len(i) == 2:
            declined.append(i)
            schedule.remove(i)

    # sorts declined in alphabetical order
    declined = sorted(declined, key=itemgetter(0))

    # sorts the scheduled appointments
    schedule = sorted(schedule, key=itemgetter(2,3,0))

    # merging the two lists, making sure the declined requests go first
    sortedSchedule = declined + schedule
    return sortedSchedule


def sortExpertsOutput(experts):
    """
    Takes an unsorted experts list and sorts it according to the project criteria,
    in the order that will be outputted to the file.
    Requires: experts as list
    Ensures: an experts list sorted by their availability
    """

     #sorting by date, then time
     output = sorted(experts, key=lambda element: (element[5], element[6]))
     return output
