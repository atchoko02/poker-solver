import numpy as np
from datetime import datetime
# import plyer


class Table:
    """
    we wish to be able to track our poker history that being...
    * numpy table keeping track of history
        * history - location, time, values
    * input - value of earning (pos/neg)
    * combine with total
    * keep track of 

    
    table:
    1.  +10 tchoko's house 10:34 pm
    2.  -20 seb's house 12:30 am
    """

    # constructor
    def __init__ (self):
        self.table = np.array([])
    
    # add a new entry to the table
    def add_entry(self, session):
        self.table = np.append(self.table, session)
    
    def remove_entry(self, index):
        self.table = np.delete(self.table, index-1)
    
    # get total of values of sessions from the table
    def get_total(self):
        return sum(session.value for session in self.table)
    
    # output of table
    def __repr__(self):
        table_str = [f"{i + 1}. {repr(item)}" for i, item in enumerate(self.table)]
        return ("Table:\n" + "\n".join(table_str)).rstrip()
    
class Session:  

    #constructor
    def __init__(self, value):
        self.value = value
        self.time = str(datetime.now().date()) + " " + str(datetime.now().time().strftime("%I:%M %p"))
        # g = geocoder.ip('me')
        # self.location = g.

    # output of session
    def __repr__(self):
        return str(self.value) + " " + self.location + " " + self.time

test = Session(10)
print(test)
table = Table()
table.add_entry(test)
table.add_entry(Session(-20))
print(table)
print(table.get_total())
table.remove_entry(1)
print(table)


