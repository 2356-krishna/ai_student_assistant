import json
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
APP_NAME=os.getenv("APP_NAME")
VERSION=os.getenv("VERSION")
def load_tasks(current_user):
    file_path=f'data/{current_user}/tasks.json'
    try:
        with open(file_path,"r")as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def save_tasks(tasks,current_user):
    file_path=f'data/{current_user}/tasks.json'
    with open(file_path,'w')as file:
        json.dump(tasks,file,indent=4)

def load_study_history(current_user):
    filepath=f'data/{current_user}/study_history.json'
    if not os.path.exists(filepath):
        return []
    with open(filepath,'r') as file:
        return json.load(file)
def save_study_session(duration,current_username):
   

    with open(f"data/{current_username}/study_history.json",'w') as file:
        json.dump(duration,file,indent=4)

def load_notes(current_username):
    if not os.path.exists(f"data/{current_username}/notes.json"):
        return[]
    with open(f"data/{current_username}/notes.json",'r') as file:
        return json.load(file)
def save_note(notes,current_username):
   with open(f"data/{current_username}/notes.json",'w') as file:
       json.dump(notes,file,indent=4) 
def load_assignment(current_username):
    if not os.path.exists(f"data/{current_username}/assignment.json"):
        return[]
    with open(f"data/{current_username}/assignment.json",'r') as file:
        return json.load(file)
def save_assignment(assignments,current_username):
    with open(f"data/{current_username}/assignment.json",'w') as file:
        json.dump(assignments,file,indent=4)
def total_study_sessions(current_username):
    history=load_study_history(current_username)
    return len(history)
def total_study_time(current_username):
    history=load_study_history(current_username)
    total_time=sum(session['duration'] for session in history)
    return total_time
def total_notes_count(current_username):
    history=load_notes(current_username)
    return len(history)
def total_assignments_count(current_username):
    history=load_assignment(current_username)
    return len(history)
def pending_assignments(current_username):
    history=load_assignment(current_username)
    count=0
    for assign in history:
        if assign["completed"]==False:
            count+=1
    return count
def completed_assignments(current_username):
    history=load_assignment(current_username)
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
def load_goals(current_username):
    if not os.path.exists(f"data/{current_username}/study_goals.json"):
        print("no file exists")
    else: 
       with open(f"data/{current_username}/study_goals.json",'r') as file:
           return json.load(file)
def save_goals(goals,current_username):
    if not os.path.exists(f"data/{current_username}/study_goals.json"):
        print("no file exists")
    else: 
      with open(f'data/{current_username}/study_goals.json','w') as file:
        json.dump(goals,file,indent=4)
def load_pomodoro(current_username):
    if not os.path.exists(f"data/{current_username}/pomodoro.json"):
        print("file not exists")
    else:
      with open(f"data/{current_username}/pomodoro.json",'r') as file:
          return json.load(file)
def save_pomodoro(pomo,current_username):
    if not os.path.exists(f"data/{current_username}/pomodoro.json"):
        print("file not exists")
    else:
        with open(f"data/{current_username}/pomodoro.json",'w') as file:
           json.dump(pomo,file,indent=4)
def save_streak(current_username,streaks):
    if not os.path.exists(f"data/{current_username}/streak.json"):
        print("file not exists")
    else:
        with open(f"data/{current_username}/streak.json",'w') as file:
            json.dump(streaks,file,indent=4)
def load_streaks(current_username):
    if not os.path.exists(f"data/{current_username}/streak.json"):
        print("file not exists")
    else:
        with open(f"data/{current_username}/streak.json",'r') as file:
            return json.load(file)

def load_Settings(current_username):
    path=f"data/{current_username}/settings.json"
    if not os.path.exists(path):
        settings=[{
            'display_name':current_username,
            'default_study_timer':30,
            'pomodoro':25,
            'break_time':5,
            'show_notifications':True
        }]
        with open(path,'w') as file:
            json.dump(settings,file,indent=4)
        return settings
    with open(path,'r') as f:
        return json.load(f)
def save_settings(current_username,settings):
    path=f"data/{current_username}/settings.json"
    with open(path,'w'):
        json.dump(settings,path,indent=4)

def total_tasks(current_username):
    load=load_tasks(current_username)
    return len(load)
def completed_tasks(current_username):
    load=load_tasks(current_username)
    total=0
    for task in load:
        if task['Completed']:
            total+=1
    return total 
def pending_tasks(current_username):
    total=0
    load=load_tasks(current_username)
    for task in load:
        if not task['Completed']:
            total+=1
    return total
def high_priority_tasks(current_username):
    total=0
    load=load_tasks(current_username)
    for task in load:
        if task["Priority"]=='high':
            total+=1
    return total
    
def low_priority_tasks(current_username):
    total=0
    load=load_tasks(current_username)
    for task in load:
        if task['Priority'].lower()=='low':
            total+=1
    return total
    
def medium_priority_tasks(current_username):
    total=0
    load=load_tasks(current_username)
    for task in load:
        if task['Priority'].lower()=='medium':
            total+=1
    return total
def highprior_andnotcompleted(current_username):
    load=load_tasks(current_username)
    count=0
    for task in load:
        if not task['Completed'] and task['Priority'].lower()=='high':
            count+=1
    return count
def nothighandnotcompleted(current_username):
    load=load_tasks(current_username)
    count=0
    for task in load:
        if not task['Completed'] and task["Priority"].lower()=='high':
            count+=1
    count=pending_tasks(current_username)-count
    return count

def load_activity(current_username):
    try:
        with open(f'data/{current_username}/activity.json','r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(FileNotFoundError)
def save_activity(activity,current_username):
    try: 
        with open(f"data/{current_username}/activity.json",'w') as file:
            json.dump(activity,file,indent=4)
    except FileNotFoundError:
        print(FileNotFoundError)









    
    





