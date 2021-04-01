import handlers.joplinHandler as joplinHandler
import handlers.dateHandler as dateHandler

class Notes:
    def __init__(self):
        joplinHandler.synchonize()


    def get_items(self):
        items = self.__note_to_dict__(
            joplinHandler.get_notebook_entries("Tasks")
        )

        joplinHandler.synchonize()
        print(items)



#        print(notes)

    def __note_to_dict__(self, notes):
        items = []

        for note in notes:
            # Make sure each of the notes we recieved was a todo, and has some sort of tag
            if note['is_todo'] == '1' and len(note['tags']) > 0:
                item = {
                    'title': note['title'],
                    'completed': note['todo_completed'] == '1',
                    #'date': dateHandler.setWeekDay('sunday', self.date),
                    'scope': 'day'
                }

                date = dateHandler.confirmDateFormat(note['tags'][0])

                if date is not note['tags'][0]:
                    joplinHandler.set_notebook_entry_tags("Tasks", item['title'], [date])
                elif date == "":
                    pass #Parsing failed

                item['date'] = dateHandler.stringToDate(date)

                items.append(item)

        return items
