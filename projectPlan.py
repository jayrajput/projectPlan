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
PROJ_START_DATE = date(2013, 8, 1)

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

    def getWork(self):
        return self.data['work']

    def getDurationDays(self):
        duration = self.getEndDate() - self.getStartDate()
        return duration.days

    def getStartDate(self):
        startDate = PROJ_START_DATE
        for dep in self.data['deps']:
            depEndDatePlusOne = dep.getEndDate() + timedelta(days = 1)
            if (depEndDatePlusOne > startDate):
                startDate = depEndDatePlusOne
        return startDate

    def getEndDate(self):
        return getDurationEndDate(self.getStartDate(), self.data['work'])

    def __str__(self):
        return "{name:<30} {startDate} {endDate} {duration:<10} {work:<10}".format(
            name      = self.data['name'],
            startDate = self.getStartDate(),
            endDate   = self.getEndDate(),
            duration  = self.getDurationDays(),
            work      = self.getWork()
        )

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

if __name__ == '__main__':
    tasks = []

    subTask1     = SubTask(dict(name = "SubTask1", work = 5))
    subTask2     = SubTask(dict(name = "SubTask2", work = 25, deps = [subTask1]))
    summaryTask1 = SummaryTask(dict(name = "SummaryTask1", subTasks = [subTask1, subTask2]))
    tasks.append(summaryTask1)
    tasks.append(subTask1)
    tasks.append(subTask2)

    subTask3     = SubTask(dict(name = "SubTask3", work = 5))
    subTask4     = SubTask(dict(name = "SubTask4", work = 25, deps = [subTask3]))
    summaryTask2 = SummaryTask(
        dict(
            name = "SummaryTask2", 
            subTasks = [
                subTask3, 
                subTask4
            ],
            deps = [summaryTask1]
        )
    )
    tasks.append(summaryTask2)
    tasks.append(subTask3)
    tasks.append(subTask4)

    for i in tasks:
        print(i)
