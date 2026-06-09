import json
import os
from dotenv import load_dotenv
load_dotenv()
APP_NAME=os.getenv("APP_NAME")
VERSION=os.getenv("VERSION")
def load_tasks(file_path="data/tasks.json"):
    try:
        with open(file_path,"r")as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def save_tasks(tasks,file_path='data/tasks.json'):
    with open(file_path,'w')as file:
        json.dump(tasks,file,indent=4)

def load_study_history(filepath='data/study_history.json'):
    if not os.path.exists(filepath):
        return []
    with open(filepath,'r') as file:
        return json.load(file)
def save_study_session(duration):
    history=load_study_history()
    history.append({
        "duration":duration
    })
    with open("data/study_history.json",'w') as file:
        json.dump(history,file,indent=4)
notes_file="data/notes.json"
def load_notes():
    if not os.path.exists(notes_file):
        return[]
    with open(notes_file,'r') as file:
        return json.load(file)
def save_note(notes):
   with open(notes_file,'w') as file:
       json.dump(notes,file,indent=4) 
def load_assignment():
    if not os.path.exists("data/assignment.json"):
        return[]
    with open("data/assignment.json",'r') as file:
        return json.load(file)
def save_assignment(assignments):
    with open("data/assignment.json",'w') as file:
        json.dump(assignments,file,indent=4)
def total_study_sessions():
    history=load_study_history()
    return len(history)
def total_study_time():
    history=load_study_history()
    total_time=sum(session['duration'] for session in history)
    return total_time
def total_notes_count():
    history=load_notes()
    return len(history)
def total_assignments_count():
    history=load_assignment()
    return len(history)
def pending_assignments():
    history=load_assignment()
    count=0
    for assign in history:
        if assign["completed"]==False:
            count+=1
    return count
def completed_assignments():
    history=load_assignment()
    count=0
    for assign in history:
        if assign["completed"]==True:
            count+=1
    return count
def load_users():
    file="data/users.json"
    if not os.path.exists(file):
        print("no file exists")
    else: 
       with open(file,'r') as file:
          return json.load(file) 

def save_users(user,file_path='data/users.json'):
    if not os.path.exists(file_path):
        print("file not found")
    else:
      with open(file_path,'w') as file:
        json.dump(user,file,indent=4)

    





