import handlers.docHandler as docHandler
import handlers.ledgerHandler as ledgerHandler
import handlers.dateHandler as dateHandler

class Log:
    HEADER_LABELS = ("Week Objectives", "Month Goals")
    BODY_LABELS = (
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    )

    def __init__(self, date):
        self.date = date
        self.path = ledgerHandler.getWeekLogByDate(self.date)
        self.document = docHandler.get_document(self.path)


    def get_items(self, date=None, scope=None):
        #Note -- there should be an exception here for when a date is requested entirely outside
        #of the date that was used to create this
        items = []
        sections = self.get_sections()

        for section in sections:
            #Only return items with the corresponding scope and date
            if scope and date:
                for entry in section['items']:
                    if entry['date'] == date and entry['scope'] == scope:
                        items.append(entry)
            #Only return items with the corresponding scope, regardless of their date
            elif scope and not date:
                for entry in section['items']:
                    if entry['scope'] == scope:
                        items.append(entry)
            #Only return items of a corresponding date, regardless of their scope
            #This will generally miss the weekly and monthly items, because their dates
            #are set for sunday
            elif not scope and date:
                for entry in section['items']:
                    if entry['date'] == date:
                        items.append(entry)
            # No qualifiers, return everything
            else:
                items = items + section['items']

        return items


    def add_item(self, item):
        pass


    # def set_items(self, items, date=None, scope=None):
    #     for item in items:
    #         section = item


    #Return all sections contained
    def get_sections(self):
        sections = []

        for label in Log.HEADER_LABELS:
            sections.append(self.get_section(label))

        for label in Log.BODY_LABELS:
            sections.append(self.get_section(label))

        return sections

    def get_section(self, label):
        section = {}
        contents = []

        if(label in Log.HEADER_LABELS):
            contents = docHandler.get_header(self.document)

        if(label in Log.BODY_LABELS):
            contents = docHandler.get_table_contents(self.document)

        section = self.__graph_to_dict__(
            docHandler.get_section(label, contents)
        )

        return section

    # Searchers

    #Returns the label of the section in which the item is found
    #returns an empty string otherwise
    def find_section(item):
        section = ""

        for label in Log.HEADER_LABELS:
            section = self.get_section(label)

            if in_section(item, section):
                if section == "":
                    section = label
                else:
                    raise Error("There was a duplicate item found in %s", self.path)

        for label in Log.BODY_LABELS:
            section = self.get_section(label)

            if in_section(item, section):
                if section == "":
                    section = label
                else:
                    raise Error("There was a duplicate item found in %s", self.path)

        return section

    # Determines if an item is in a section
    def in_section(item, section):
        found = False

        for entry in section['items']:
            found = found or entry['title'] == item['title']

        return found

    # Private methods

    def __item_to_label__(self, item):
        label = ""

        if item['scope'] == "month":
            label = Log.HEADER_LABELS[1]
        elif item['scope'] == "week":
            label = Log.HEADER_LABELS[0]
        elif item['scope'] == "day":
            day = item['date'].weekday()

            # weekday() returns the day of the week in the order: sunday, monday, tuesday, wednesday... saturday; with sunday as 0 and saturday as 6
            # I have the days stored as monday, tuesday, wednesday... saturday, sunday, with monday as 0 and sunday as 6
            # a lesser programmer would need more than one line to convert these. I am not a lesser programmer.
            label = Log.BODY_LABELS[day - 1] if day > 0 and day < 6 else Log.BODY_LABELS[5 + (1 -(day / 6))]
        else:
            raise Error("The item %s had unexpected scope %", item['title'], item['scope'])

        return label


    def __graph_to_dict__(self, graphs):
        dict = {}
        dict['label'] = graphs[0].text
        dict['items'] = []

        if(graphs[0].style.name == "Month Label"):
            listStyles = ('Incomplete Item','Complete Item')

            #For each graph in the list after the label
            for i in range(1, len(graphs)):
                graph = graphs[i]

                #If it is a list item, append it to the items array
                if(graph.style.name in listStyles):
                    #Confirm item is not an emdash
                    if(graph.text.find("—") == -1):
                        #Set completion status based on whether the style is 'Incomplete Item' or 'Complete Item'
                        dict['items'].append({
                            'title': graph.text,
                            'completed': graph.style.name == listStyles[1],
                            'date': dateHandler.setWeekDay('sunday', self.date),
                            'scope': 'month'
                        })

        graphs[0].style.name == "Week Label"
        if ():
            listStyles = ('Incomplete Item','Complete Item')

            #For each graph in the list after the label
            for i in range(1, len(graphs)):
                graph = graphs[i]

                #If it is a list item, append it to the items array
                if(graph.style.name in listStyles):
                    #Confirm item is not an emdash
                    if(graph.text.find("—") == -1):
                        #Set completion status based on whether the style is 'Incomplete Item' or 'Complete Item'
                        dict['items'].append({
                            'title': graph.text,
                            'completed': graph.style.name == listStyles[1],
                            'date': dateHandler.setWeekDay('sunday', self.date),
                            'scope': 'week'
                        })

        # We are dealing with the body contents
        if(graphs[0].style.name == "Day Label"):
            listStyles = ('List Item','List Item (Inactive)')
            tasksStart = False

            # For each graph in the list after the label
            for i in range(1, len(graphs)):
                graph = graphs[i]
                sublabel = 0

                #If it is a list item, append it to the items array
                if(graph.style.name in listStyles):
                    #Confirm item is not an emdash
                    if(graph.text.find("—") == -1):
                        #Set completion status based on whether we have gone into the tasks list or not
                        dict['items'].append({
                            'title': graph.text,
                            'completed': sublabel == 1,
                            'date': dateHandler.setWeekDay(dict['label'], self.date),
                            'scope': 'day'
                        })
                #If it is not a list item, check if it is the Tasks label to determine
                else:
                    sublabel += 1

        return dict
