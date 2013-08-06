#!/usr/bin/python

# @author Jay Rajput.
# @email jayrajput@gmail.com

# for calculation of work day.
from datetime import date, timedelta

# python logging
import logging

# http://docs.python.org/2/howto/logging.html#logging-basic-tutorial
# redirect logging to a /tmp file
# Uncomment to see the logging.
# logging.basicConfig(filename='/tmp/projectPlan.log', filemode='w', level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

# Project started on 01 Aug, '2013.
PROJ_START_DATE = date.today()

def getDurationEndDate(startDate, workInManDays):
    """
    Duration of an activity is variable depending on the leaves, holidays and
    weekend.  If I start a 2 day work activity on Friday, my duration will be 4
    days (as Saturday and Sunday are weekends), but if I start the same 2-day
    activity on Monday, the duration will be two days. This function returns
    the "duration end date" based on provided start date and work in man days,
    taking only working day in consideration.  Duration is inclusive of start
    and end date.
    """

    # Add your holidays here.
    # TODO - find if there is a better way to input the holidays.
    holidays = [
        #    YYYY, M, DD
        date(2013, 8, 9 ), # Eid-ul-fitr
        date(2013, 8, 15), # Independence day
        date(2013, 8, 20), # Raksha Bandhan
    ]

    # sanitize arguments.
    if workInManDays < 0: 
        raise ValueError("Invalid Work:{1}".format(workInManDays))

    endDate  = startDate
    nextDate = startDate
    while True:
        if workInManDays == 0: return endDate

        nextDate = nextDate + timedelta(days=1)

        # do not include weekends in calculating duration.  Return the day of
        # the week as an integer, where Monday is 0 and Sunday is 6
        if (nextDate.weekday() in (5, 6)): continue
        # do not include holidays in calculating duration.
        if (nextDate in holidays): continue

        endDate       = nextDate
        workInManDays = workInManDays - 1

class SubTask:
    def __init__(self, data):
        self.data = dict(
            name      = None,
            work      = None,
            deps      = [],
        )
        self.data.update(data)
        self.name  = self.data['name']
        self.work  = self.data['work']
        self.deps  = self.data['deps']
        self.subTasks = []

    def getWork(self):
        return self.data['work']

    def getDurationDays(self):
        duration = self.getEndDate() - self.getStartDate()
        return duration.days

    def getStartDate(self):
        if (self.name == None): return PROJ_START_DATE
        startDate = getParentTask(self.name).getStartDate()
        for dep in self.data['deps']:
            depEndDatePlusOne = dep.getEndDate() + timedelta(days = 1)
            if (depEndDatePlusOne > startDate):
                startDate = depEndDatePlusOne
        return startDate

    def getEndDate(self):
        return getDurationEndDate(self.getStartDate(), self.data['work'])

# @TODO: work is only supported as man days. Minimum work is 1 man day

# Inherit from SubTask.
class SummaryTask(SubTask):
    def __init__(self, data):
        self.data = dict(
            name      = None,
            subTasks  = [],
            deps      = [],
        )
        self.data.update(data)
        self.name     = self.data['name']
        self.subTasks = self.data['subTasks']
        self.deps     = self.data['deps']

    def getWork(self):
        """ Work is sum of work of all sub tasks """
        work = 0
        for subTask in self.data.get('subTasks'):
            work = work + subTask.getWork()
        return work

    def getEndDate(self):
        """ End date is equal to end date of last sub task """
        endDate = self.getStartDate()
        for subTask in self.data['subTasks']:
            subTaskEndDate = subTask.getEndDate()
            if (subTaskEndDate > endDate):
                endDate = subTaskEndDate
        return endDate

# Task Manager - START
# Wanted task manager to be a singleton and on doing google, suggestion was to
# just used a bunch of functions. So implemented singleton using tasks global
# variable and bunch of functions.
tasks = []  # global list of tasks.
def addTask(task):
    tasks.append(task)

def getTaskByName(name):
    for task in tasks:
        if task.name == name:
            return task
    return None

def getParentTask(subTaskName):
    for task in tasks:
        for subTask in task.subTasks:
            if subTask.name == subTaskName:
                return task
    # return an empty task indicating there is no parent.
    return SubTask(dict())

def printTasks():
    print "{name:<30} {startDate} {endDate:<10} {duration:<10} {work:<10}".format(
        name = "Name",
        startDate = "Start Date",
        endDate   = "End Date",
        duration  = "Duration",
        work      = "Work"
    )
    for task in sorted(tasks, key = lambda task: task.getStartDate()):
        if len(task.subTasks) > 0:
            print "{name:<30} {startDate} {endDate} {duration:<10} {work:<10}".format(
                name      = task.data['name'],
                startDate = task.getStartDate(),
                endDate   = task.getEndDate(),
                duration  = task.getDurationDays(),
                work      = task.getWork()
            )
            for subTask in sorted(task.subTasks, key = lambda task: task.getStartDate()):
                print "{name:<30} {startDate} {endDate} {duration:<10} {work:<10}".format(
                    name      = "    " + subTask.data['name'],
                    startDate = subTask.getStartDate(),
                    endDate   = subTask.getEndDate(),
                    duration  = subTask.getDurationDays(),
                    work      = subTask.getWork()
                )
# Task Manager - END

if __name__ == '__main__':
    subTask1     = SubTask(dict(name = "SubTask1", work = 5))
    subTask2     = SubTask(dict(name = "SubTask2", work = 25, deps = [subTask1]))
    summaryTask1 = SummaryTask(dict(name = "SummaryTask1", subTasks = [subTask1, subTask2]))
    addTask(summaryTask1)
    addTask(subTask1)
    addTask(subTask2)

    subTask3     = SubTask(dict(name = "SubTask3", work = 5, deps = [summaryTask1]))
    subTask4     = SubTask(dict(name = "SubTask4", work = 25))
    summaryTask2 = SummaryTask(
        dict(
            name = "SummaryTask2", 
            subTasks = [
                subTask3, 
                subTask4
            ],
        )
    )
    addTask(summaryTask2)
    addTask(subTask3)
    addTask(subTask4)

    printTasks()
