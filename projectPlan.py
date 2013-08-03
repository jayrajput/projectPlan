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

def getDurationEndDate(startDate, workInManDays):
    """
    Duration field is variable depending on the leaves, holidays and weekend.
    If I start a 2 day work activity on Friday, my duration will be 4 days (as
        Saturday and Sunday are weekends), but if I start the same 2-day
    activity on Monday, the duration will be two days. This function returns
    the "duration end date" based on provided start date and work in man days,
    taking only working day in consideration.  Duration is inclusive of start
    and end date.
    """

    holidays = [
        date(2013, 8, 9 ), # ID
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

if __name__ == '__main__':
    print "Inside main";
    print getDurationEndDate(date.today(), 2)
    print getDurationEndDate(date.today(), 30)

