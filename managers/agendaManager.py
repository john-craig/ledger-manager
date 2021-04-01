import handlers.logHandler as logHandler
import handlers.dateHandler as dateHandler
import handlers.ledgerHandler as ledgerHandler
import handlers.joplinHandler as noteHandler

from objects.Log import Log
from objects.Notes import Notes

def addLogTask(date, string):
    pass

def getLogTasks(date):
    pass

def addLogDeed(date, string):
    pass

def getLogDeeds(date):
    pass

def completeLogTask(date, string):
    pass

#===========

## TODO: add exception handling
def manageTask(note):
    log = getLogByNote(note)
    section = getDaySection(note, log)

    tasks = logHandler.getTasks(section)
    deeds = logHandler.getDeeds(section)

    inTasks = matchGraphsNote(tasks, note)
    inDeeds = matchGraphsNote(deeds, note)

    isComplete = bool(note['todo_completed'])

    if isComplete:
        if inTasks:
            #This means note is marked as complete in Joplin
            #but it is not a Deed in the Log yet
            logHandler.completeTask(note['title'], section)
        elif inDeeds:
            #The note is marked as complete in Joplin and
            #as complete in the Log -- the note can
            #safely be deleted
            pass
        else:
            #The note is marked as complete in Joplin but
            #it is listed as neither a Deed or a Task in
            #the Log; thus, add it as a Deed
            logHandler.addDeed(note['title'], section)

        #Technically the note should be deleted in all cases
        #here
    else:
        if inTasks:
            #This means the note is incomplete and
            #it is listed as a Task in the log,
            #thus, nothing needs to happen
            pass
        elif inDeeds:
            #This means the note is marked as incomplete
            #in Joplin but is listed under Deeds in the
            #Log. This suggests I manually added it as
            #a Deed. Thus it should be deleted from
            #Joplin.
            pass
        else:
            #This means it is marked incomplete in Joplin
            #but is not in the Deeds or the Tasks of a
            #Log. Thus, add it as a Task.
            logHandler.addTask(note['title'], section)

    saveLogByNote(log, note)





def matchGraphsNote(graphs, note):
    match = False

    for graph in graphs:
        if graph.text == note['title']:
            match = True

    return match


#===========


def getDaySection(note, log):
    date = dateHandler.stringToDate(note['todo_due'])
    day = dateHandler.getDayName(date.weekday())

    return logHandler.getSectionByDay(day, log)

def getLogByNote(note):
    date = dateHandler.stringToDate(note['todo_due'])
    path = ledgerHandler.getWeekLogByDate(date)

    print(path)

    return logHandler.getLog(path)

def saveLogByNote(log, note):
    date = dateHandler.stringToDate(note['todo_due'])
    path = ledgerHandler.getWeekLogByDate(date)

    log.save(path)


#===========

#Update the Agenda of the Log
def run():
    date = dateHandler.getToday()

    notes = Notes()
    notes.get_items()

def update():
    date = dateHandler.getToday()

    notes = Note()
    notes.get_items()

    # log = Log(date)
    # print(log.get_items(date))

#Fetch the Agenda of the current Day
def fetch():
    date = dateHandler.getToday()
    log = Log(date)

    month_items = log.get_items(scope='month')
    week_items = log.get_items(scope='week')
    day_items = log.get_items(date, 'day')

    agendaString = "Month Goals: \n"

    for item in month_items:
        agendaString = agendaString + "\t -" + item['text'] + "\n"

    agendaString += "\nWeek Objectives: \n"

    for item in week_items:
        agendaString = agendaString + "\t -" + item['text'] + "\n"

    agendaString += "\nDaily Tasks: \n"

    for item in day_items:
        agendaString = agendaString + "\t -" + item['text'] + "\n"

    return agendaString
