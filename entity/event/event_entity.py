
import sqlite3
from datetime import datetime

from utility.helper import convert_datetime_from_database


class EventEntity:
    def __init__(self, id, title, address, description, startDate, endDate, price, createdDate):
        self.id = id
        self.title = title
        self.address = address
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.price = price
        self.createdDate = createdDate
        
    def event_status_text(self)->str:
        has_event_started=False
        has_event_ended=False
        start_date=convert_datetime_from_database(self.startDate)
        end_date=convert_datetime_from_database(self.endDate)
        temp=datetime.now()
        current_datetime= datetime(temp.year,temp.month,temp.day)
        if(current_datetime>=start_date):
            has_event_started=True
        if(current_datetime>end_date):
            has_event_ended=True
        if(not has_event_started):
            status_text = f"Event starts in {(start_date - current_datetime).days} days"
        elif(has_event_started and not has_event_ended):
            if(current_datetime==end_date):
                status_text = f"Event Ends Today" 
            else:
                status_text = f"Event Ends in {(end_date - current_datetime).days+1} days"       
        else:
            status_text = f"Event Ended {(current_datetime - end_date).days} days ago"    
        return status_text      

# Class Method, access by Entity.fromMap(), can access and modify class state, where static method cannot
    @classmethod
    def fromMap(self, data:sqlite3.Row):
        map=dict(data)
        return self(map.get('id'), map.get('title'),map.get('address'),map.get('description'),map.get('startDate'),map.get('endDate'),map.get('price'),map.get('createdDate'))
    