def float_validator(value:str):
    if(len(value)==0):
        return True
    if(len(value)>=1 and value.replace('.',"",1).isdigit()  and len(value)<=6):
        return True
    return False

def empty_validator(value:str):
    return len(value.strip())==0