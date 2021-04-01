import datetime


DAYS = [
    "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"
]

def isLeapYear(yearNum):
    return (yearNum % 400 == 0) or ((yearNum % 100 != 0) and (yearNum % 4 == 0))

def getMonthLength(monthNum, yearNum=None):
    leapYear = False

    if(yearNum):
        leapYear = isLeapYear(yearNum)

    monthLengths = (
        31,
        29 if leapYear else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31
    )

    return monthLengths[monthNum - 1]

def getMonthName(monthNum):
    monthNames = (
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    )

    return monthNames[monthNum - 1]

def getDayName(dayNum):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return days[dayNum]

def getWeekRanges(date=None):
    if not date:
        date = datetime.date.today()

    weekRanges = []
    monthLength = getMonthLength(date.month, date.year)

    zeroethMonday = (date.day - date.weekday()) % 7

    """
        Something is going wrong with this case where the "zeroeth"
        Monday falls in the previous month, because today is:
            Sunday, March 28th

        meaning that the month ends,
            Tuesday, March 30th

        and thus there is
            Wednesday, April 1st
            Thursday, April 2nd
            Friday, April 3rd

        in short, this week is still falling in April. However, when
        I call this function today, I get the week ranges for March.
    """

    # If the zeroeth monday falls in the previous month
    if zeroethMonday < 1 and zeroethMonday > -1:
        # Get the number of the previous month
        prevMonthNum = 12 if date.month - 1 == 0 else date.month - 1

        # Get the length of the previous month
        prevMonthLen = monthLength(
            prevMonthNum,
            date.year if prevMonthNum != 12 else date.year - 1
        )

        #Construct the week range
        weekRange = (
            {'month': prevMonthNum, 'date': prevMonthLen + zeroethMonday},
            {'month': date.month, 'date': zeroethMonday + 4}
        )
        weekRanges.push(weekRange)

        zeroethMonday += 7

    for i in range(0, 5):
        curMonday = (i * 7) + zeroethMonday

        if curMonday <= monthLength:
            weekRange = (
                {'month': date.month, 'date': curMonday},
                {'month': date.month, 'date': curMonday + 4}
            )

            weekRanges.append(weekRange)
        elif curMonday < monthLength + 3:
            nextMonthNum = 1 if date.month == 12 else date.month + 1
            weekRange = (
               {'month': date.month, 'date': curMonday},
               {'month': nextMonthNum, 'date': curMonday + 4 - monthLength}
            )

            weekRanges.append(weekRange)

    return weekRanges

def getWeekNumber(date):
    weekRanges = getWeekRanges(date)
    day = date.day
    weekNum = -1

    print(weekRanges)

    for i in range(0, len(weekRanges)):
        weekRange = weekRanges[i]

        if (day >= weekRange[0]['date'] - 1) and (day <= weekRange[1]['date'] + 1):
            weekNum = i
        elif(weekRange[0]['month'] is not weekRange[1]['month']):
            if (day >= weekRange[0]['date'] - 1) or (day <= weekRange[1]['date'] + 1):
                weekNum = i

    return weekNum

def getMonth(date=None):
    if not date:
        date = datetime.date.today()

    return date.month

def getYear(date=None):
    if not date:
        date = datetime.date.today()

    return date.year

def getToday():
    return datetime.date.today()

# ======

def determineYear(date):
    pass




#========

#Accepts a date object and a weekday as a string,
#sets the day of that date to the corresponding weekday
def setWeekDay(day, date):
    curWeekDay = date.weekday()

    if day.lower() in DAYS:
        dayNum = DAYS.index(day.lower())

        curWeekDay = (date.weekday() + 1) % 7
        dayNum = date.day - curWeekDay + dayNum
        date = date.replace(day=dayNum)
    else:
        print("Error setting weekday: " + day)

    return date



#========

#Converts a day of the week to a string in mm-dd-yy format
#as though that day were in this week
def confirmDateFormat(string):
    tokens = string.split('_')
    offset = 0

    #expecting something like "next friday" or "last monday"
    if len(tokens) > 1:
        if tokens[0] == "next":
            offset = 7
        elif tokens[0] == "last":
            offset = -7

        string = tokens[1]

    if string.lower() in DAYS:
        date = getDateByWeekday(string)

        dayNum = date.day + offset
        date = date.replace(day=dayNum)

        string = date.strftime("%m-%d-%y")

    #To do: add a bunch of exception handling

    return string


def getDateByWeekday(string):
    dayNum = DAYS.index(string.lower())
    date = datetime.datetime.today()

    curWeekDay = (date.weekday() + 1) % 7
    dayNum = date.day - curWeekDay + dayNum
    date = date.replace(day=dayNum)

    return date

#Retuns a date object based on a string
#Valid strings are:
#   mm-dd-yy

def timestampToDate(timestamp):
    #date = datetime.datetime.strptime(string, "%m-%d-%y")
    date = datetime.datetime.fromtimestamp(timestamp / 1000.0)

    return date

def stringToDate(string):
    date = datetime.datetime.strptime(string, "%m-%d-%y")

    return date
