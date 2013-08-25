projectPlan
===========

Project plan for creating schedules for software features.

I got promoted to Engineering Project Manager role and had to create project
schedules using existing GUI based software available for Project Planning
(MPP). Before using the MPP, we were doing it in excel and manually managing
various things.

Advantages of using MPP for project planning (over excel):
----------------------------------------------------------
* Automatic DURATION Calculation: Software was able to handle the duration
  automatically.  Duration field is variable depending on the leaves, holidays
  and weekend. If I start a 2 day work activity on Friday, my duration will be
  4 days (as Saturday and Sunday are weekends), but if I start the same 2-day
  activity on Monday, the duration will be two days. Manually managing this was
  error-prone and tedious.
* Automatic task LINKING: Software allows linking of tasks. For example, unit
  testing can only start when the code is completed. Hand managing dependencies
  between tasks is error-prone and tedious.

One advantage which I did not listed above is that MPP taught us lot about the
project planning. This python script projectPlan will not be helpful in
teaching you about the project plan so I have not listed this advantage with
other two.

Disadvantages of using MPP for project planning:
------------------------------------------------
* LICENSE FEE has to be paid and company did not provided MPP to everyone in
  the team.
* MPP has options to export the data in XLS, but it is not as nice as what we
  were able to do manually. Any formatting which we were able to do with XLS,
  cannot be done (or we were not aware on how it can be done) with MPP.
* MPP was NOT EXTENSIBLE. No scripting interface.

Ideas/Concepts:
--------------

This python script will have the listed advantages without the disadvantages.
Also, there are multiple open source project planning software available which
are either GUI based or command line and are much heavier than this script.
This script is different from others as it takes ASCII text (in a specified
    EBNF) and provides the output.


## License

CC0 Public Domain - http://creativecommons.org/publicdomain/zero/1.0/


## Contact me

Contact jayrajput@gmail.com for any questions.
