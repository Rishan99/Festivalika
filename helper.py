from datetime import datetime


def convert_datetime_from_database(value:str)->datetime:
    return datetime.strptime(value,"%Y-%m-%d %H:%M:%S")

    
    
def convert_datetime_to_default(value:datetime)->str:
    return value.strftime("%m/%d/%y")
        