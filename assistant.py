import time
import os
import hashlib
import csv
from colorama import Fore,init
from utils.helperfunctio import load_study_history,save_study_session,load_notes,save_note
from utils.helperfunctio import load_assignment,save_assignment
from utils.helperfunctio import total_study_sessions,total_study_time,total_notes_count,total_assignments_count,pending_assignments,completed_assignments
from utils.helperfunctio import load_users,save_users,save_goals,load_goals,save_pomodoro,load_pomodoro,load_streaks,save_streak,load_tasks,save_tasks
from utils.helperfunctio import high_priority_tasks,low_priority_tasks,medium_priority_tasks,total_tasks,completed_tasks,pending_tasks,highprior_andnotcompleted,nothighandnotcompleted
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    PageBreak
)
from openpyxl import Workbook
import zipfile
from utils.helperfunctio import load_Settings,save_settings
init(autoreset=True)
current_user='krishna'
def pasrse_date(date_string):
    return datetime.strptime(date_string,"%d/%m/%Y")



def update_streaks(current_username):
     load=load_streaks(current_username)
     print(load)
     today=datetime.now().date()
     strintime=today.strftime('%d/%m/%Y')
     yesterday=today-timedelta(days=1)
     yesterdaystrin=yesterday.strftime("%d/%m/%Y")
     if load[0]['yesterday']==yesterdaystrin or load[0]['yesterday']=="":
         load[0]['streaks']+=1
         load[0]['yesterday']=strintime
         save_streak(current_username,load)
def view_streak(current_username):
    load=load_streaks(current_username)
    return load[0]['streaks']
def get_badges(current_username):
    badges=[]
    history=load_study_history(current_username)
    session=len(history)
    if session>=5:
        badges.append("🥉Beginner Level💫")
    if session>=25:
        badges.append("🥈Consistent student✅")
    if session>=100:
        badges.append("🥇Master study ✅💪")
    return badges
def view_badges(current_username):
    badge=get_badges(current_username)
    print(Fore.BLUE+"======== Achievements🏅 ========")
    if not badge:
        print(Fore.RED+"Badges not earned yet")

    for badges in badge:
        print(badges)

def weekly_report(current_username):
    history=load_study_history(current_username)
    sessions=0
    min=0
    today=datetime.now().date()
    daybefweek=today-timedelta(days=7)
    strdaybef=daybefweek.strftime("%d/%m/%Y")
    for his in history:
       if his['date']>strdaybef:
        min+=his['duration']
        sessions+=1
    print(Fore.BLUE+"====== Weekly report ======")
    print(f"{Fore.YELLOW}Total sessions :{sessions}")
    print(f"Study time: {min}mins")
def achievements():
    global current_user
    while(True):
        print(Fore.MAGENTA+"1. View badges")
        print(Fore.MAGENTA+"2. Weekly report")
        print(Fore.MAGENTA+"3. Back")
        choice=input(Fore.CYAN+"Enter your choice")
        if choice=='1':
            view_badges(current_user)
        elif choice=='2':
            weekly_report(current_user)
        elif choice=="3":
            break
        else:
            print(f"{Fore.RED}Invalid choice")
def study_timer(current_username):
    load=load_Settings(current_username)
    minutes=int(input(Fore.CYAN+"Enter how many minutes you want to study or press enter to default for default_study_time : "))
    if minutes=="":
        minutes=load[0]['default_study_timer']
    print(f"{Fore.CYAN}study session started for {minutes} minutes")
    time.sleep(minutes)
    print(Fore.GREEN+"congratulations !")
    print(Fore.GREEN+f"you have completed your study session {minutes} minutes")
    history=load_study_history(current_username)
    today=datetime.now().date()
    strtime=today.strftime("%d/%m/%Y")
    streak=False
    for his in history:
        # print("running")
        if not his['date']==strtime:
            streak=True
            # print("running")
             
    if streak==True:
      update_streaks(current_username)
    #   print("running")

    history.append({
        "duration":minutes,
        "date":strtime
    })
    
    
    
    save_study_session(history,current_username)
    
def view_study_history(current_username):
    history=load_study_history(current_username)
    if not history:
        print("\n no study session found")
        return
    print(f"\n{Fore.BLUE}===== STUDY HISTORY =====")
    for i, session in enumerate(history,start=1):
        print(f"{i}. {session["duration"]} minutes")




def add_assignment(current_username):
    assignments=load_assignment(current_username)
    title=input(Fore.CYAN+"enter asssignment title")
    due_date=input(Fore.CYAN+"enter due date of assignment (YYYY-MM-DD)")
    
    assignments.append({
        "title":title,
        "due_date":due_date,
        "completed":False
    })
    save_assignment(assignments,current_username)
def view_assignment(current_username):
    assignments=load_assignment(current_username)
    if not assignments:
        print("no assignment found")
        return
    print(f"\n{Fore.BLUE}===== ASSIGNMENTS =====")
    for i,assignment in enumerate(assignments,start=1):
        status="completed✅" if assignment["completed"] else "pending❌"
        print(f"{i}. {assignment['title']} | DUE:{assignment['due_date']} | STATUS:{status}")
def mark_complete(current_username):
    assignments=load_assignment(current_username)
    if not assignments:
        print("no assignment found")
        return
    view_assignment(current_username)
    try: 
        num=int(input(Fore.CYAN+"Enter number which assignment you want to mark as completed"))
        if num>=1 and num<=len(assignments):
            assignments[num-1]["completed"]=True
            save_assignment(assignments,current_username)
        else:
            print("invalid number")
    except ValueError:
        print("invalid number") 
def delete_Assignment(current_username):
    assignments=load_assignment(current_username)
    if not assignments:
        print("no assignments found")
        return
    view_assignment(current_username)
    try:
        num=int(input(Fore.CYAN+"Enter number which assignment you want to delete : "))
        if num>=1 and num<=len(assignments):
            assignments.pop(num-1)
            save_assignment(assignments,current_username)
            print("assignment deleted")
        else:
            print("invalid number")
    except ValueError:
        print("invalid number")
def assignment_menu():
    global current_user
    while(True):
        print(f"\n{Fore.BLUE}===== ASSIGNMENT MENU =====")
        print(f"{Fore.MAGENTA}1. Add Assignment")
        print(f"{Fore.MAGENTA}2. View Assignment")
        print(f"{Fore.MAGENTA}3. Mark assignment as completed")
        print(f"{Fore.MAGENTA}4. Delete Assignment")
        print(f"{Fore.RED}5. Back")

        choice = input(Fore.CYAN+"Enter choice: ")

        if choice == "1":
            add_assignment(current_user)

        elif choice == "2":
            view_assignment(current_user)

        elif choice == "3":
            mark_complete(current_user)

        elif choice == "4":
            delete_Assignment(current_user)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")
def add_note(current_username):
    note=load_notes(current_username)
    new_note=input(Fore.CYAN+"enter new note you want to add")
    note.append(new_note)
    save_note(note,current_username)
def view_notes(current_username):
    note=load_notes(current_username)
    if not note:
        print("no note found")
        return
    print(f"\n{Fore.BLUE}===== NOTES =====")
    for i,notes in enumerate(note,start=1):
        print(f"{i}. {notes}")
def delete_note(current_username):
    note=load_notes(current_username)
    if not note:
       print("no notes to be deleted")
       return 
    try:
      view_notes(current_username)
      num=int(input(Fore.CYAN+"\nEnter number which note you want to delete"))
      
      if num>=1 and num<=len(note):
        deleted=note.pop(num-1)
        save_note(note,current_username)
        print(f"deleted {deleted}")
      else:
        print("invalid note number")
    except ValueError:
        print("invalid number ")
def notes_menu():
    global current_user
    while(True):
        print(f"\n{Fore.BLUE}===== NOTES MENU =====")
        print(f"{Fore.MAGENTA}1. Add Note")
        print(f"{Fore.MAGENTA}2. View Notes")
        print(f"{Fore.MAGENTA}3. Delete Note")
        print(f"{Fore.RED}4. Back")

        choice = input(Fore.CYAN+"Enter choice: ")

        if choice == "1":
            add_note(current_user)

        elif choice == "2":
            view_notes(current_user)

        elif choice == "3":
            delete_note(current_user)

        elif choice == "4":
            break

        else:
            print("Invalid choice.")
def export_notes(current_username):
            notes=load_notes(current_username)
            with open(f"exports/{current_username}/notes.csv",'w',newline='') as file:
                writer=csv.writer(file)
                writer.writerow(['note'])
                for note in notes:
                    writer.writerow([note])
            print(f"{Fore.GREEN} Notes exported successfully to exports/notes.csv")
def assignment_export(current_username):
    assignments=load_assignment(current_username)
    with open(f"exports/{current_username}/assignment.csv",'w') as file:
        writer=csv.writer(file)
        writer.writerow(['Title','Due_Date','Completed'])
        for assignment in assignments:
            writer.writerow([assignment['title'],assignment['due_date'],assignment['completed']])
    print(f"{Fore.GREEN} Assignment exported successfully to exports/{current_username}assignment.csv")
def export_study_history(current_username):
    history=load_study_history(current_username)
    with open(f"exports/{current_username}/study_history.csv",'w',newline='')as file:
        writer=csv.writer(file)
        writer.writerow(['date','duration'])
        for session in history:
            writer.writerow([session['date'],session['duration']])
    print(f"{Fore.GREEN} Study history exported successfully to exports/study_history.csv")
def export_tasks(current_username):
    load=load_tasks(current_username)
    file=f"exports/{current_username}/tasks.csv"
    with open(file,'w',newline='')as fi:
       writer=csv.writer(fi)
       writer.writerow(['Title','Priority','Deadline','Completed'])
       for task in load:
           writer.writerow([task['Title'],task['Priority'],task['Deadline'],task['Completed']])
    print(f"{Fore.GREEN} Tasks exported successfully to exports/{current_username}/study_history.csv")

        
        
def export_menu():
    global current_user
    while(True):
        print(f"\n{Fore.BLUE}===== EXPORT MENU =====")
        print(f"{Fore.MAGENTA}1. export notes")
        print(f"{Fore.MAGENTA}2. export assignment")
        print(f"{Fore.MAGENTA}3. export study history")
        print(f"{Fore.MAGENTA}4. export Tasks")
        print(f"{Fore.RED}5. Back")
        choice = input(Fore.CYAN+"Enter choice: ")
        if choice == "1":
            export_notes(current_user)
        elif choice == '2':
            assignment_export(current_user)
        elif choice == '3':
            export_study_history(current_user)
        elif choice=='4':
            export_tasks(current_user)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
def overdue_count(current_username):
    load=load_assignment(current_username)
    today=datetime.now().date()
    overdues_count=0
    for assign in load:
        if pasrse_date(assign['due_date']).date() < today:
            overdues_count+=1
    return overdues_count

def set_goals(current_username):
    load=[]
    goal=int(input(f"{Fore.CYAN}Enter daily study goal: "))
    today=datetime.now().date()
    load.append({"goals":goal})
    save_goals(load,current_username)
    print(Fore.GREEN+"Goal Saved")
def view_goal(current_username):
    load=load_goals(current_username)
    if not load:
        return Fore.RED+"please add goal in productivity features"
    return int(load[0]['goals'])
def pomodoro(current_username):
    setting=load_Settings(current_username)
    study_minutes=int(input(Fore.CYAN+"Enter how many minutes you want to study or press enter for default  : ") or setting[0]['pomodoro'])
    break_time=int(input(Fore.CYAN+"Enter how many minutes of break you want  or default 5 : ")or load[0]['break_time'])
    total_seconds=study_minutes
    while(total_seconds):
        minutes=total_seconds//60
        sec=total_seconds% 60
        print(f"{Fore.YELLOW}{minutes:02d}:{sec:02d}")
        time.sleep(1)
        total_seconds-=1
    print(Fore.LIGHTBLUE_EX+"\n\nWell done study session completed!")
    history=load_study_history(current_username)
    today=datetime.now().date()
    strtime=today.strftime("%d/%m/%Y")
    streak=False
    for his in history:
        # print("running")
        if not his['date']==strtime:
            # print("running")
            streak=True
    if streak==True:
    #   print("running")
      update_streaks(current_username)
    
    history.append({
        "duration":study_minutes,
        "date":strtime
    })
    save_study_session(history,current_username)
    load=load_pomodoro(current_username)
    load[0]['pomodoro']+=1
    print(load)
   
    
    save_pomodoro(load,current_username)
    print(f"\n{Fore.GREEN} Take a break for {break_time} minutes")
    break_seco=break_time
    while break_seco:
        mins=break_seco//60
        secs=break_seco%60
        print(f"{Fore.YELLOW}{mins:02d}:{secs:02d}")
        time.sleep(1)
        break_seco-=1

    print(f"{Fore.RED} Break over!")
    continu=input(Fore.CYAN+"Do you want to continue or exit pomodoro timer Yes or No: ")
    if continu.lower()=='yes':
        pomodoro(current_username)
    else:return
# pomodoro(current_user)

def view_progress(current_username):
    load=load_study_history(current_username)
    today=datetime.now().date()
    strintime=today.strftime("%d/%m/%Y")
    study_min=0
    goal=load_goals(current_username)
    goa=goal[0]['goals']
    print(type(goa))
    for duration in load:
        # print(duration['date'])
        if duration['date']==strintime:
            study_min+=duration['duration']
            # print(type(study_min))
    percentage=(study_min / goa)*100
    print(f"{Fore.YELLOW}Goal:{goa}mins")
    print(f"{Fore.YELLOW}completed :{study_min}mins")
    print(f"{Fore.YELLOW}Progress: {percentage:.1f}%")
    if percentage>=100:
        print(f"{Fore.GREEN}Goal achieved!")
def progress(current_username):
    load=load_study_history(current_username)
    today=datetime.now().date()
    strintime=today.strftime("%d/%m/%Y")
    study_min=0
    goal=load_goals(current_username)
    if not goal:
         return Fore.RED+"please add goal in productivity features"
    goa=goal[0]['goals']
    # print(type(goa))
    for duration in load:
        # print(duration['date'])
        if duration['date']==strintime:
            study_min+=duration['duration']
            # print(type(study_min))
    percentage=(study_min / goa)*100
    # print(f"{Fore.YELLOW}Goal:{goa}mins")
    print(f"{Fore.YELLOW}completed :{Fore.WHITE}{study_min}mins")
    print(f"{Fore.YELLOW}Progress: {Fore.WHITE}{percentage:.1f}%")
    return
    


def productivity_menu():
    global current_user
    
    while(True):
        print(Fore.BLUE+"======  Productivity Menu  ======")
        print(f"{Fore.MAGENTA}1. Set goal")
        print(f"{Fore.MAGENTA}2. Start pomodoro")
        print(f"{Fore.MAGENTA}3. View Progress")
        print(f"{Fore.MAGENTA}4. Exit") 
        choice=input(Fore.CYAN+"enter your choice : ")
        if choice=='1':
            set_goals(current_user)
        elif choice=='2':

            pomodoro(current_user)
        elif choice=='3':
            view_progress(current_user)
        elif choice=="4":
            break
        else:
            print(Fore.RED+"Invalid choice")
    
def progress_bar(percentage):
    filled = int(percentage // 10)
    empty = 10 - filled

    return "█" * filled + "░" * empty


def search_notes(current_username):
    note=load_notes(current_username)
    if not note:
        print("no notes found")
        return
    keyword=input(Fore.CYAN+"enter keyword to search in notes")
    result=[n for n in note if keyword.lower() in n.lower()]
    if result:
        print(f"{Fore.GREEN} FOUND {len(result)} notes containing this {keyword}")
        for i,notes in enumerate(result,start=1):
            print(f"{i}. {notes}")
    else:
        print(Fore.RED+"no keyword match to notes")
def search_assignments(current_username):
    data=load_assignment(current_username)
    keyword=input(Fore.CYAN+"enter title of assignment to search in assignments")
    result=[n for n in data if keyword.lower() in n['title'].lower()]
    if result:
        print(f"{Fore.GREEN} found {len(keyword)} matches in assignment")
        for i,assi in enumerate(result,start=1):
            print(f"""{i}. Title : {assi['title']}
                           DUE: {assi['due_date']}
                           Status: {assi['status']}   """)
    else:
        print(f"{Fore.RED}No keyword match the assignment title")
def pending1_assignments(current_username):
    assign=load_assignment(current_username)
    for a in assign:
        if not a['completed']:
            print(f"{Fore.RED}Pending Assignment: {a['title']} | DUE: {a['due_date']}")
def completed1_assignmments(current_username):
    assign=load_assignment(current_username)
    for a in assign:
        if a['completed']:
            print(f"{Fore.GREEN}Completed Assignment: {a['title']} | DUE: {a['due_date']}")
def search_tasks(current_username):
    load=load_tasks(current_username)
    keyword=input("Enter task title to search in tasks: ")
    result=[n for n in load if keyword.lower()in n['Title'].lower()]
    if result:
        print(f"{Fore.MAGENTA}==== Matching keywords ====")
        for k in result:
            print(f"""Title: {k['Title']}
Priority: {k['Priority']}
Deadline: {k['Deadline']}
Completed: {k['Completed']}""")
   
def search_menu():
  global current_user

  while(True):
    print(f"\n{Fore.BLUE}===== SEARCH MENU =====")
    print(f"{Fore.MAGENTA} 1. Seacrh notes")
    print(f"{Fore.MAGENTA} 2. Search assignments")
    print(f"{Fore.MAGENTA} 3. Search Tasks")
    print(f"{Fore.MAGENTA} 4. VIEW PENDING ASSIGNMENTS")
    print(f"{Fore.MAGENTA} 5. VIEW COMPLETED ASSIGNMENTS")
    print(f"{Fore.RED} 6. Back")
    choice=input(Fore.CYAN+"Enter your choice: ")
    if choice=="1":
        search_notes(current_user)
    elif choice=='2':
        search_assignments(current_user)
    elif choice=='3':
        search_tasks(current_user)
    elif choice=='4':
        pending1_assignments(current_user)
    elif choice=='5':
        completed1_assignmments(current_user)
    elif choice=="6":
        print(f"{Fore.BLUE} returning to main menu...")
        break
    else:
        print(f"{Fore.RED}invalid choice")

def overdue_assignment(current_username):
    print(Fore.BLUE+"====== Overdue assignments ======")
    load=load_assignment(current_username)
    today=datetime.now().date()
    found=False
    i=1
    for assign in load:
        if pasrse_date(assign['due_date']).date()<today and not assign['completed']:
            print("\n")
            print(f"{Fore.RED}{i}. title :{assign['title']}")
            print(f"{Fore.RED}     assignment is due on {assign['due_date']}")
            found=True
            i+=1

    if found==False:
     print(Fore.GREEN+"No assignments overdue")
    

def due_assignments(current_username):
    load=load_assignment(current_username)
    today=datetime.now().date()
    found=False
    print(f"{Fore.BLUE} ====== DUE ASSIGNMENTS ====== ")
    i=1
    for assign in load:       
        if pasrse_date(assign['due_date']).date()> today and not assign['completed']:
            print("\n")
            print(f"{Fore.YELLOW}{i}. Title : {assign['title']}")
            print(f"{Fore.YELLOW}     Due date: {assign['due_date']}")
            found=True
            i+=1
    if not found:
        print(Fore.GREEN+"No assignments due")
def upcoming_assignments(currren_username):
    print(Fore.YELLOW+" ====== Upcomming assignments in 3 days ======")
    i=1
    load=load_assignment(currren_username)
    today=datetime.now().date()
    next_days=today + timedelta(days=3)
    found=False
    for assign in load:
        if today<pasrse_date(assign['due_date']).date()<next_days:
            print("\n")
            print(Fore.LIGHTBLUE_EX+f"{i}. Title : {assign['title']}")
            print(Fore.LIGHTBLUE_EX+f"     Due_date {assign['due_date']}")
            found=True
            i=+1

    if not found:
        print(Fore.GREEN+"No upcoming assignment in 3 Days")
        print("\n")

def alerts_menu():
   global current_user
   while(True):
    print(Fore.MAGENTA+"1. Check overdue assignments")
    print(Fore.MAGENTA+"2. Check Due assignments")
    print(Fore.MAGENTA+"3. Check Upcoming assignments")
    print(Fore.MAGENTA+"4. Exit")
    Choice=input(Fore.CYAN+"Enter your choice : ")
    if Choice=='1':
        overdue_assignment(current_user)
    elif Choice=='2':
        due_assignments(current_user)
    elif Choice=='3':
        upcoming_assignments(current_user)
    elif Choice=='4':
        print(Fore.GREEN+"Exiting alerts")
        break
    else:
        print(Fore.RED+"invalid choice ")


def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()
def create_user_files(username):
    os.mkdir(
        f"data/{username}"
    )

    files=['assignment.json','notes.json','tasks.json','study_history.json','study_goals.json','pomodoro.json','streak.json','badges.json']
    expor=['assignment.csv','notes.csv','studyhistory.csv','tasks.csv']
    for file in files:
        with open(f'data/{username}/{file}','w')as fi:
            if file=='pomodoro.json':
                fi.write('[{"pomodoro":0}]')
            elif file=='streak.json':
                fi.write('[{"streaks":0,"yesterday":""}]')
            else:
              fi.write("[]")
    os.mkdir(f"exports/{username}")


def register():
  load=load_users()
  username=input(f"{Fore.MAGENTA} Enter username: ")
  password=hashpass(input(f"{Fore.MAGENTA} Enter password: "))
  
  for user in load:
      if user['username']==username:
        print(f"{Fore.RED} User Already Exists!")
        return
  load.append({
      'username':username,
      'password':password})    
  save_users(load)
  print(Fore.GREEN+"Registration Successfully!")
  create_user_files(username)




  


def login():
    load=load_users()
    username=input(f"{Fore.MAGENTA} Enter username: ")
    password=hashpass(input(f"{Fore.MAGENTA} Enter password: "))
    for user in load:
        if user['username']==username and user['password']==password:
            global current_user
            current_user=username
            print(Fore.GREEN+"login successfully") 
            setting=load_Settings(current_user)
            print(f"\n{Fore.YELLOW}Welcome : {setting[0]['display_name']}")
            return True
    print(Fore.RED+"Invalid crendtials")    
    return False   
def profile():
    global current_user
    
    print(Fore.BLUE+"\n ======== PROFILE  ========")
    print(f"username :  {current_user}")
def logout():
    global current_user
    current_user=None
    print(f"{Fore.GREEN} Successfully logout")
def change_password():
    global current_user
    load=load_users()
    for user in load:
        if user['username']==current_user:
            new_password=input(Fore.CYAN+"Enter new password : ")
            user['password']=new_password
            save_users(load)
            print(f"{Fore.GREEN} Password changed successfully")

def change_username():
    load=load_users()
    global current_user
    new_username=input(Fore.CYAN+"Enter new  ")
    for name in load:
            if name['username']==new_username:
                print("username already exists")
                return
    for user in load:
       if  user['username']==current_user:
           user['username']=new_username
           save_users(load)
           current_user=new_username
           print(f"{Fore.GREEN} Username changed successfully")
def delete_account():
    global current_user
    load=load_users()
    confirm=input("Type DELETE to confirm deletion of account")
    if confirm.lower()!='delete':
        print(Fore.GREEN+"deletion cancelled")
        return
    load=[user for user in load if user['username']!=current_user]
    save_users(load)
    print(Fore.YELLOW+"Account Deleted Succesfully")
    current_user=None
    return True
def account_details():

    global current_user

    print(Fore.BLUE+"\n===== ACCOUNT =====")
    
    print(
        f"{Fore.GREEN}Username: {current_user}"
    )
def setting_menu():
  global current_user
  while(True):
    load=load_Settings(current_user)
    print(Fore.BLUE+"====== Settings ======")
    print(Fore.MAGENTA+"1. Change username ")
    print(Fore.MAGENTA+"2. Change Password ")
    print(Fore.MAGENTA+"3. Delete account")
    print(Fore.MAGENTA+"4. View account details")
    print(Fore.MAGENTA+"5. Change dispaly name")
    print(Fore.MAGENTA+"6. change default study")
    print(Fore.MAGENTA+"7. change default pomodoro timer")
    print(Fore.MAGENTA+"8. change default break time in pomodoro")
    print(Fore.MAGENTA+"9. change notifications settings")

    print(Fore.MAGENTA+"10. exit")
    choice=input(Fore.CYAN+"Enter your choice")
    if choice=='1':
        change_username()
    elif choice=='2':
        change_password()
    elif choice=='3':
        if delete_account():
            return "logout"
    elif choice=='4':
        account_details()
    elif choice=='5':
        load[0]['display_name']=input("Enter display name : ")
    elif choice=='6':
        load[0]['default_study_timer']=input("Enter study time you want to set as default : ")
    elif choice=='7':
        load[0]['pomodoro']=input("Enter pomodoro timer you want to set as default : ")
    elif choice=='8':
        load[0]['break_time']=input("Enter break time you want to set as default : ")
    elif choice=='9':
       while(True):
        notification=input("Do you want notifications in dashboard yes or no ")
        if notification.lower()=='yes':
           load[0]['show_notifications']=True
           print(Fore.GREEN+"Notification settings changed sucessfully")

        elif notification.lower=='no':
           load[0]['show_notifications']=False
           print(Fore.GREEN+"Notification settings changed sucessfully")

        else:
            print("Invalid choice")
            
        
    elif choice=='10':
        break
    else:
        print(Fore.RED+"Invaid choice")


def add_tasks(current_username):
    load=load_tasks(current_username)
    title=input("Enter title of the task: ")
    priority=input(Fore.CYAN+"Enter priority of the task high,low ,medium:")
    completed=False
    deadline=input(Fore.CYAN+'Enter deadline of the task (%d/%m/%y): ')
    load.append({
        "Title":title,
        "Priority":priority,
        "Completed":completed,
        "Deadline":deadline
    })
    save_tasks(load,current_username)
def view_tasks(current_username):
    load=load_tasks(current_username)
    for i,tasks in enumerate(load,start=1):
        status="completed✅" if tasks['Completed'] else "Pending"
        print(Fore.YELLOW+f"{i}. Title:{tasks['Title']} \n Priority:{tasks['Priority']} \n {tasks['Deadline']} \n Status:{status}")
def delete_tasks(current_username):
    view_tasks(current_username)
    load=load_tasks(current_username)
    try:
       choice=int(input(Fore.CYAN+"Enter which task you want to delete " ))
       if choice>=1 and choice<=len(load):
         load.pop(choice-1)
         save_tasks(load,current_username)
         print(Fore.GREEN+"tasks deleted sucessfully")
       else:
        print(Fore.RED+"invalid choice")
    except ValueError:
      print(ValueError)
def mark(current_username):
    load=load_tasks(current_username)
    if not load:
        print("no tasks found")
    view_tasks(current_username)
    try: 
        choice=int(input(Fore.CYAN+"Enter no which task you to mark as completed : "))
        if choice>=1 and choice<=len(load):
          load[choice-1]['Completed']=True
          save_tasks(load,current_username)
        else:
          print("invalid choice")
    except ValueError:
        print("invalid choice")
def filter_task(current_username):
    load=load_tasks(current_username)
    if not load:
        return
    high=[]
    low=[]
    medium=[]
    pending=[]
    completed=[]
    for task in load:
        if task['Priority'].lower()=='high':
            high.append(task)
        elif task['Priority'].lower()=='medium':
            medium.append(task)
        elif task['Priority']=='low':
            low.append(task)
        if task['Completed']:
            completed.append(task)
        else:
            pending.append(task)
    while(True):
      print("======  Filter menu  ======")
      print(Fore.MAGENTA+"1. Filter tasks basis on high priority")
      print(Fore.MAGENTA+"2. Filter tasks basis on medium priority")
      print(Fore.MAGENTA+"3. Filter tasks basis on low priority")
      print(Fore.MAGENTA+"4. Filter tasks basis on completed priority")
      print(Fore.MAGENTA+"5. Filter tasks basis on pending priority")
      print(Fore.MAGENTA+"6. exit the filter feature")
      choice=input(Fore.CYAN+"Please enter how you want filter to task : ")
      if choice=='1' or choice.lower()=='high':
         print("===== High priority tasks =====")
         if not high:
              print(Fore.RED+"No high priority tasks")
         else:
          for i,tasks in enumerate(high,start=1):
              status="completed✅" if tasks['Completed'] else "Pending"
              print(Fore.YELLOW+f"{i}. Title:{tasks['Title']} \n Priority:{tasks['Priority']} \n {tasks['Deadline']} \n Status:{status}")
      elif choice=='2' or choice.lower()=='medium':
         print("===== Medium priority tasks =====")
         if not medium:
              print(Fore.RED+"No Medium priority tasks")
         else:
          for i,tasks in enumerate(medium,start=1):
              status="completed✅" if tasks['Completed'] else "Pending"
              print(Fore.YELLOW+f"{i}. Title:{tasks['Title']} \n Priority:{tasks['Priority']} \n {tasks['Deadline']} \n Status:{status}")
      elif choice=='3' or choice.lower()=='low':
         print("===== Low priority tasks =====")
         if not low:
          print(Fore.RED+"NO low priority tasks")
         else:

          for i,tasks in enumerate(low,start=1):
              status="completed✅" if tasks['Completed'] else "Pending"
              print(Fore.YELLOW+f"{i}. Title:{tasks['Title']} \n Priority:{tasks['Priority']} \n {tasks['Deadline']} \n Status:{status}")
      elif choice=='4' or choice.lower()=='pending':
         print("===== Completed tasks =====")
         if not completed:
              print(Fore.RED+"No Completed tasks")
         else:
          for i,tasks in enumerate(completed,start=1):
              status="completed✅" if tasks['Completed'] else "Pending"
              print(Fore.YELLOW+f"{i}. Title:{tasks['Title']} \n Priority:{tasks['Priority']} \n {tasks['Deadline']} \n Status:{status}")
      elif choice=='5' or choice.lower()=='pending':
        print("===== Pending tasks =====")
        if not pending:
              print(Fore.RED+"No Pending tasks")
        else:
          for i,tasks in enumerate(pending,start=1):
              status="completed✅" if tasks['Completed'] else "Pending"
              print(Fore.YELLOW+f"{i}. Title:{tasks['Title']} \n Priority:{tasks['Priority']} \n {tasks['Deadline']} \n Status:{status}")
      elif choice=='6'or choice=='back':
          break
      else:
          print("invalid value")
          
def tasks(current_username):
    while(True):
       print(Fore.BLUE+"=======  Tasks menu  =======")
       print(Fore.MAGENTA+"1. Add tasks")
       print(Fore.MAGENTA+"2. Delete tasks")
       print(Fore.MAGENTA+"3. View tasks")
       print(Fore.MAGENTA+"4. Mark tasks complete")
       print(Fore.MAGENTA+"5. Filter tasks")
       print(Fore.MAGENTA+"6. Back")
       choice=input("Enter your choice: ")
       if choice=='1':
           add_tasks(current_username)
       elif choice=='2':
           delete_tasks(current_username)
       elif choice=='3':
           view_tasks(current_username)
       elif choice=='4':
           mark(current_username)
       elif choice=='5':
           filter_task(current_username)
       elif choice=='6':
           break
       else:
           print(Fore.RED+"Invalid choice")






    


def productivity_score(current_username):
    load=load_assignment(current_username)
    streak=load_streaks(current_username)
    completed=sum(1 for a in load if a['completed'])
    score=completed*10+streak[0]['streaks']*5
    return  score

def recommendation(current_username):
    load_assignmen=load_assignment(current_username)
    load_study=load_study_history(current_username)
    today=datetime.now().date()
    daybef=(today-timedelta(days=4)).strftime("%d/%m/%Y")
    minutes=0
    for stud in load_study:
        if stud['date']>daybef:
            minutes+=stud['duration']
    pomo=load_pomodoro(current_username)
    goals=load_goals(current_username)
    pending=sum(1 for a  in load_assignmen if not a['completed'])
    print(f"======== Recommendations 💫 ========")
    if minutes<300:
        print(Fore.YELLOW+"📊 Increase study time this week")
    if pending>5:
        print(Fore.RED+"⚠️  You have many pening assignments")
    if not goals:
        print(Fore.YELLOW+"You have no study goals please add goals ")
    if  not pomo:
        print(Fore.YELLOW+"You have no pomodoro sessins, please do to increase your study time")
    elif pomo[0]['pomodoro']<5:
        print(Fore.YELLOW+"You have less pomodoro sessins, please do to increase your study time")
def notification(current_username):
    load=load_assignment(current_username)
    pending=sum(1 for a in load if a['completed'])
    print(Fore.BLUE+"======== Notifications ========")
    print(f"{Fore.RED} You have {highprior_andnotcompleted(current_username)} High Priority pending tasks ")
    print(f"other pending tasks are : {nothighandnotcompleted(current_username)}")

    print(f"{Fore.RED} You have {pending} pending assignmemnts")
    Streak=load_streaks(current_username)
    print(f"{Fore.YELLOW} Current streak {Streak[0]['streaks']}")

    
            
def weekly_summary(current_username):
    load_assignmen=load_assignment(current_username)
    load_study=load_study_history(current_username)
    today=datetime.now().date()
    daybef=(today-timedelta(days=7)).strftime("%d/%m/%Y")
    min=0
    completed=0
    pending=0
    session=0
    for his in load_study:
        if his['date']>daybef:
            min+=his['duration']
            session+=1

    for assign in load_assignmen:
        if assign['completed']:
                completed+=1
        else:
                pending+=1
    print(Fore.BLUE+"====== Weekly summary ======")
    print(Fore.YELLOW+f"Total week study sessions :  {session}")
    print(Fore.YELLOW+f"Total week study minutes :  {min}")
    print(f"{Fore.GREEN} Completed assignments : {completed}")
    print(f"{Fore.RED} Pending assignments : {pending}") 
def insights_menu():
    global current_user
    while(True):
        print(Fore.MAGENTA+"1. Productivity score")    
        print(Fore.MAGENTA+"2. Recommendations")        
        print(Fore.MAGENTA+"3. Notifications")        
        print(Fore.MAGENTA+"4. Weekly summary")        
        print(Fore.MAGENTA+"5. Back")        
        choice=input("Enter your choice : ")
        if choice=='1':
            print(f"{Fore.YELLOW}productivity_score: {productivity_score(current_user)}")
        elif choice=='2':
            recommendation(current_user)
        elif choice=='3':
            notification(current_user)
        elif choice=='4':
            weekly_summary(current_user)
        elif choice=='5':
            break
        else:
            print(Fore.RED+"Invalid choice")

def pdf_Report(current_username):
    file_path=f"data/{current_username}/productivity_Report.pdf"
    pdf=SimpleDocTemplate(file_path)
    styles=getSampleStyleSheet()
    content=[]
   
    title1=Paragraph(
        """<b>
        =====
        Ai Student Assistant report
        =====</b>""",
        styles["Title"]
    )
    content.append(title1)
    content.append(Spacer(1,12))
    content.append(Paragraph(f"<b>Generated on : </b>{(datetime.now().date()).strftime("%d/%m/%Y")}",styles['BodyText']))
    content.append(Spacer(1,10))
    content.append(Paragraph(f"<b>username: </b>{current_username} ",styles['BodyText']))
    content.append(Spacer(1,10))
    title2=Paragraph(
        """<b>
        ===========
              STUDY STATISTICS
        ===========</b>""",
        styles["Title"]
    )
    content.append(title2)
    content.append(Spacer(1,12))
    history=load_study_history(current_username)
    assignments=load_assignment(current_username)
    Streak=load_streaks(current_username)
    study_time=sum(session['duration'] for session in history)
    completed=sum(1 for a in assignments if a['completed'])
    pending=len(assignments)-completed
    Streaks=Streak[0]['streaks']

    pdf_text=[
       

       f"<b>Total Study Time: </b>{study_time}mins",

       f"<b> Total Study Sessions: </b>{len(history)}"
  
       f"<b>Current Streak: </b>{Streaks}",
       
    ]
    for con in pdf_text:
      content.append(Paragraph(con,styles['BodyText']))
      content.append(Spacer(1,10))
    choice=input(Fore.MAGENTA+"Do you want graph and charts in pdf Yes or No: ")
    if choice.lower()=='yes':
        study_graph(current_username)
        assignment_chart(current_username)
        content.append(Image(f"data/{current_username}/study_graph.png",
                         width=400,
                         height=250))
        content.append(PageBreak())
    title3=Paragraph(
        f"""<b>




       ========
        ASSIGNMENT SUMMARY
       ========</b>""",
        styles["Title"]
    )
    content.append(title3)
    content.append(Spacer(1,12))
    Assign_text=[
       
      f"<b>Completed Assignments: </b>{completed}",
       
       f"<b>Pending Assignments:</b>{pending}",
       
    ]
    content.append(Paragraph(Assign_text[0],styles['BodyText']))
    content.append(Spacer(1,10))
    content.append(Paragraph(Assign_text[1],styles['BodyText']))
    content.append(Spacer(1,10))
    if choice.lower()=='yes':
       content.append(Image(f"data/{current_username}/assignment_chart.png",
                         width=350,
                         height=250))
    title6=Paragraph( f"""<b>




       ========
        TASKS SUMMARY
       ========</b>""",styles['Title'])
    content.append(title6)
    content.append(Spacer(1,10))
    task_text=[f"Total tasks: {total_tasks(current_username)}",f"Completed Task : {completed_tasks(current_username)}",f"Pending Task: {pending_tasks(current_username)}",f"High Priority tasks: {high_priority_tasks(current_username)}"]
    for text in task_text:
        content.append(Paragraph(text,styles['BodyText']))
        content.append(Spacer(1,10))
    title4=Paragraph(
        """<b>
       -------------
                  PRODUCTIVITY SCORE
       ------------</b>""",
        styles["Title"]
    )
    content.append(title4)
    content.append(Spacer(1,12))
    score=productivity_score(current_username)
    content.append(Paragraph(f"Productivity Score: {score}",styles['BodyText']))
    content.append(Spacer(1,10))
    title5=Paragraph(
        """<b>
       -------------
               ACHIEVEMENTS 
       -------------
       </b>""",
        styles["Title"]
    )
    content.append(title5)
    content.append(Spacer(1,12))
    loa=get_badges(current_username)
    
    for badge in loa:
        content.append(Paragraph(f"{badge}"))
        content.append(Spacer(1,10))
    title1=Paragraph(
        """<b>
       ==================================
        Generated by Ai Student Assistant
       ==================================</b>""",
        styles["Title"]
    )
    content.append(title1)
    content.append(Spacer(1,12))
    
    pdf.build(content)
    print(Fore.GREEN+"Pdf Report Generated")
    print(f"Saved at : {file_path}")
    
    
def import_tasks(current_username):
    load=[]
    with open(f"exports/{current_username}/tasks.csv",'r') as file:
        read=csv.DictReader(file)
        for row in read:
            load.append(row)
    save_tasks(load,current_username)
    print(Fore.GREEN+"Tasks imported sucessfully")

def import_notes(current_username):
    load=[]
    with open(f"export/{current_username}/notes.csv") as file:
        read=csv.DictReader(file)
        for note in read:
            load.append(note)
    save_note(load,current_username)
    print(Fore.GREEN+"Notes imported sucessfully")

def import_assignments(current_username):
    load=[]
    with open(f"exports/{current_username}/assignment.csv") as f:
        read=csv.DictReader(f)
        for assign in read:
            load.append(assign)
    save_assignment(load,current_username)
    print(Fore.GREEN+"assignment imported sucessfully")

def import_study(current_username):
    load=[]
    with open(f"exports/{current_username}/study_history.csv") as f:
        read=csv.DictReader(f)
        for study in read:
            load.append(study)
    save_study_session(load,current_username)
    print(Fore.GREEN+"Study imported sucessfully")
def import_menu():
    global current_user
    while(True):
        print(Fore.MAGENTA+"1. Import tasks")
        print(Fore.MAGENTA+"2. Import notes")
        print(Fore.MAGENTA+"3. Import assignment")
        print(Fore.MAGENTA+"4. Import study sessions")
        print(Fore.MAGENTA+"5. Back")
        choice=input(Fore.CYAN+"Enter your choice")
        if choice=='1':
            import_tasks(current_user)
        elif choice=='2':
            import_notes(current_user)
        elif choice=='3':
            import_assignments(current_user)
        elif choice=='4':
            import_study(current_user)
        elif choice=='5':
            break
        else:
            print(Fore.RED+"Invalid choice")

        
    

        


        

            

def auth():
  while(True):
    print(f"{Fore.BLUE}======= Login system =======")
    print(f"{Fore.MAGENTA}1. Register")
    print(f"{Fore.MAGENTA}2. Login")
    print(f"{Fore.MAGENTA}3. Exit")
    choice=input(f"{Fore.CYAN} Enter your choice : ")
    if choice=='1':
        register()
    elif choice=='2':
        if login():
            global current_user
            load=load_Settings(current_user)
            if load[0]['show_notifications']:
                notification(current_user)
            return True
    elif choice=='3':
        return False
    else:
        print(Fore.RED+"Invalid choice")
def study_graph(current_username):
    
    load_study=load_study_history(current_username)
    size=len(load_study)
    sessions=list(range(1,size+1))
    minutes=[]
    for his in load_study:
        minutes.append(his['duration'])
    plt.figure(figsize=(8,5))
    plt.plot(sessions,minutes,marker='o')
    plt.title("study session")
    plt.ylabel("minutes")
    plt.xlabel("sessions")
    plt.grid(True)
    plt.savefig(f"data/{current_username}/study_graph.png")
    print(f"Study graph  uploaded in data/{current_username}/study_graph.png")
# study_graph()
def assignment_chart(current_username):
    
    assignments=load_assignment(current_username)
    completed=sum(1 for x in assignments if x['completed']==True)
    # print(completed)
    pending=len(assignments)-completed
    # print(pending)
    labels=['completed','pending']
    values=[completed,pending]
    plt.figure(figsize=(6,6))
    plt.pie(values,labels=labels,autopct="%1.1f%%")
    plt.title("assignment chart")
    # plt.show()
    plt.savefig(f"data/{current_username}/assignment_chart.png")
    print(f"Assignment chart uploaded in data/{current_username}/assignment_chart.png")



def excel(current_username):
    wb=Workbook()
    sheet=wb.active
    sheet.title="Study history"
    sheet.append([
        "Date",
        "Duration"
    ]) 
    total_time=0
    history=load_study_history(current_username)
    for his in history:
        total_time+=his['duration']
        sheet.append([
            his['date'],
            his['duration']
        ])
    assignment_sheet=wb.create_sheet("Assignments")
    assignment_sheet.append([
            "Title",
            "Due_date",
            "Completed"
        ])
    assign=load_assignment(current_username)
    for ass in assign:
            assignment_sheet.append(
[ass['title'],
 ass['due_date'],
 ass['completed']]
            )
    tasks=wb.create_sheet("Tasks")
    tasks.append(["Title","Priority","completed","Deadline"])
    load_task=load_tasks(current_username)
    for tas in load_task:
        tasks.append([tas['Title'],tas['Priority'],tas['Completed'],tas['Deadline']])
    analytics=wb.create_sheet("Analytics")
    analytics.append([
            "Metric","Value"
        ])
    analytics.append(["study_sessons",len(history)])
    analytics.append([
    "Study Time",
    total_time
])
    streak=load_streaks(current_username)

    analytics.append([
    "Current Streak",
    streak[0]['streaks']
])
    score=productivity_score(current_username)
    analytics.append([
    "Productivity Score",
     score
])
    file_path = (
    f"data/{current_user}/"
    "productivity_report.xlsx"
)

    wb.save(file_path)
    print(Fore.GREEN+"Excel report Generated ✅")
def reports_menu():
   global current_user
   while(True):
    print(Fore.BLUE+"====== Reports ======")
    print(Fore.MAGENTA+"1. Generate Study graph")
    print(Fore.MAGENTA+"2. Generate Assignment chart")
    print(Fore.MAGENTA+"3. Generate Pdf Report")
    print(Fore.MAGENTA+"4. Generate Excel Report")
    print(Fore.MAGENTA+"5. Back")
    choice=input(Fore.CYAN+"Enter your choice: ")
    if choice=='1':
        study_graph(current_user)
    elif choice=='2':
       assignment_chart(current_user)
    elif choice=='3':
        pdf_Report(current_user)
    elif choice=='4':
        excel(current_user)
    elif choice=='5':
        break
    else:
        print(Fore.RED+"Invalid choice")
    

def create_backup(current_username):
    source_folder=f"data/{current_username}"
    backupfolder=f"backups/{current_username}_backup.zip"
    with zipfile.ZipFile(backupfolder,'w',zipfile.ZIP_DEFLATED) as zipf:
        for root,dirs,files in os.walk(source_folder):
          for file in files:
            path=os.path.join(root,file)
            arcname=os.path.relpath(path,source_folder)
            zipf.write(path,arcname)
    print(Fore.GREEN+"backup created succesfully")
def restore_backup(current_username):
    target_file=f"data/{current_username}"
    backup_file=f"backups/{current_username}_backup.zip"
    if not os.path.exists(backup_file):
        print(f"{Fore.RED}backup_file not existed")
        return
    with zipfile.ZipFile(backup_file,'r') as zipf:
        zipf.extractall(target_file)
    print(Fore.GREEN+"backup restored")
def backup_menu():
    global current_user
    print(Fore.BLUE+"======== BACKUP SYSTEM ========")
    while(True):
        print(Fore.MAGENTA+"1. Create backup")
        print(Fore.MAGENTA+"2. Restore backup")
        print(Fore.MAGENTA+"3. back")
        choice=input(Fore.CYAN+"Enter your choice : ")
        if choice=="1":
            create_backup(current_user)
        elif choice=="2":
            restore_backup(current_user)
        elif choice=="3":
            break
        else:
            print(Fore.RED+"Invalid choice")
import random
def motivational_quotes():
    quotes = [
    "Discipline beats motivation.",
    "Small progress is still progress.",
    "Success starts with consistency.",
    "Study today, succeed tomorrow.",
    "Every expert was once a beginner.",
    "Stay focused and never give up.",
    "Dream big, work hard.",
    "One chapter at a time.",
    "Learning never goes to waste.",
    "Keep showing up every day.",
    "Hard work always pays off.",
    "Your future is created today.",
    "Progress, not perfection.",
    "Success is earned, not given.",
    "Believe in your potential.",
    "Keep moving forward.",
    "Make today count.",
    "Consistency creates excellence.",
    "Small efforts lead to big results.",
    "Don't stop until you're proud.",
    "Knowledge is your greatest investment.",
    "Learn something new every day.",
    "Stay hungry for knowledge.",
    "Focus on improvement.",
    "Be stronger than your excuses.",
    "Push yourself beyond limits.",
    "You are capable of amazing things.",
    "The best investment is in yourself.",
    "Action beats intention.",
    "Success loves preparation.",
    "Every day is a new opportunity.",
    "Your habits shape your future.",
    "Study with purpose.",
    "A little progress every day adds up.",
    "Be patient with your growth.",
    "Work in silence, let success speak.",
    "Stay disciplined even when it's hard.",
    "You don't have to be perfect, just consistent.",
    "Keep learning, keep growing.",
    "Failure is a lesson, not the end.",
    "Great things take time.",
    "Never stop believing in yourself.",
    "Every minute of study counts.",
    "Start now, not later.",
    "One task at a time.",
    "Focus on what matters.",
    "Turn dreams into goals.",
    "Goals require action.",
    "Learn, practice, improve.",
    "Success is built daily.",
    "Your future self will thank you.",
    "The pain of discipline is temporary.",
    "Keep your eyes on the goal.",
    "Stay positive and productive.",
    "Confidence comes from preparation.",
    "Discipline creates freedom.",
    "Never underestimate small efforts.",
    "Keep building your future.",
    "Success begins with self-belief.",
    "Today's effort is tomorrow's success.",
    "Stay committed to your goals.",
    "The journey is worth it.",
    "Learn from yesterday, improve today.",
    "Consistency is your superpower.",
    "You are stronger than your doubts.",
    "Every accomplishment starts with a decision.",
    "Focus creates results.",
    "Work hard, stay humble.",
    "Keep your momentum alive.",
    "Nothing changes unless you do.",
    "You can do difficult things.",
    "Success comes to those who prepare.",
    "Do something today your future self will appreciate.",
    "Build habits that build success.",
    "Great achievements begin with small steps.",
    "Never quit on your dreams.",
    "Stay curious, keep learning.",
    "Every challenge makes you stronger.",
    "Success is a series of small wins.",
    "Your effort matters.",
    "Every page you read brings you closer to success.",
    "Learn with passion.",
    "Believe, achieve, repeat.",
    "Keep improving every single day.",
    "Your only competition is yesterday's you.",
    "Knowledge opens every door.",
    "One more hour of effort can change everything.",
    "Winners never stop learning.",
    "The harder you work, the luckier you become.",
    "Stay dedicated to your purpose.",
    "Make discipline your lifestyle.",
    "Success begins outside your comfort zone.",
    "The secret to success is consistency.",
    "Invest in your mind every day.",
    "Every study session brings you closer to your goals.",
    "Your dreams deserve your effort.",
    "The best project you'll ever work on is yourself.",
    "Stay focused, stay determined.",
    "Growth happens one day at a time.",
    "Keep chasing excellence.",
    "Believe in the process.",
    "Your journey has just begun."
]
    return random.choice(quotes)

def dashboard():
    global current_user
    load=load_Settings(current_user)
    dat=datetime.now().date()
    today=datetime.now().date()
    print(f"""\n{Fore.BLUE}╔════════════════════════════════════════════════════════════════════╗
║                   🎓 AI STUDENT ASSISTANT                         ║
║                     Productivity Dashboard                        ║
╚════════════════════════════════════════════════════════════════════╝""")
    ti=datetime.now().time().strftime("%H:%M")
    if ti>'12:00':
        greet="👋 Good Afternoon"
    elif ti>'17:00':
        greet="🌙 Good Evening"
    elif ti<'12:00':
        greet="☕ Good Morning"
    print(f"{Fore.YELLOW}{greet}, {Fore.WHITE}{load[0]['display_name']}!")
    print(f"{Fore.YELLOW}📅 Date : {Fore.WHITE}{dat.strftime('%A, %B %d, %Y')}    {Fore.YELLOW}🕒 Time: {Fore.WHITE}{ti}\n")
    print(f"═══════════════════════════════════════════════════════════════════════\n")
    print(f"📊 STUDY PROGRESS")
    print(f"{Fore.YELLOW}Today's goal: {Fore.WHITE}{view_goal(current_user)} Minutes ")
    load_stud=load_study_history(current_user)
    today_study_time=0
    for study in load_stud:
        if study['date']==today.strftime("%d/%m/%Y"):
            today_study_time+=study['duration']
    print(f"{Fore.YELLOW}Studied today: {Fore.WHITE}{today_study_time}")
    percent=(today_study_time / int(view_goal(current_user))) * 100 if view_goal(current_user) != Fore.RED+"please add goal in productivity features" else 0
    print(f"{Fore.YELLOW}Progress: {Fore.WHITE}{progress_bar(percent)} {percent:.1f}%\n")
    print(f"{Fore.YELLOW}Total Study Sessions: {Fore.WHITE}{total_study_sessions(current_user)}")
    print(f"{Fore.YELLOW}Total Study Time: {Fore.WHITE}{total_study_time(current_user)} minutes\n")
    
    

  
    # if pending_assignments()<1:
    #     print(f"{Fore.GREEN}Great job! You have no pending assignments.")
    # elif pending_assignments()==total_assignments_count():
    #     print(f"{Fore.RED}You have a lot of pending assignments. Try to complete them soon!")
    print(f"═══════════════════════════════════════════════════════════════════════\n")
    print(f"📋 ASSIGNMENT TRACKING")
    print(f"{Fore.YELLOW}Pending Assignments: {Fore.WHITE}{pending_assignments(current_user)}")
    print(f"{Fore.GREEN}Completed Assignments: {Fore.WHITE}{completed_assignments(current_user)}")
    print(f"{Fore.RED}Overdue Assignments: {Fore.WHITE}{overdue_count(current_user)}")

    completion_rate= (completed_assignments(current_user) / total_assignments_count(current_user) * 100) if total_assignments_count(current_user) > 0 else 0
    print(f"{Fore.CYAN}Assignment Completion Rate: {Fore.WHITE}{completion_rate}%")
    if completion_rate>=80:
        print(Fore.GREEN+"Excellent work! Your assignment completion rate is high.")
    print(f"═══════════════════════════════════════════════════════════════════════\n")
    print(f"📝 TASK MANAGEMENT")
    print(f"{Fore.YELLOW}Total Tasks: {Fore.WHITE}{total_tasks(current_user)} ")
    print(f"{Fore.YELLOW}Completed Tasks: {Fore.WHITE}{completed_tasks(current_user)} ")
    print(f"{Fore.YELLOW}Pending Tasks: {Fore.WHITE}{pending_tasks(current_user)} ")
    print(f"{Fore.YELLOW}High priority tasks: {Fore.WHITE}{high_priority_tasks(current_user)} 🔴 ")
    print(f"{Fore.YELLOW}Medium priority tasks: {Fore.WHITE}{medium_priority_tasks(current_user)} 🟡 ")
    print(f"{Fore.YELLOW}low priority tasks: {Fore.WHITE}{low_priority_tasks(current_user)} 🟢 ")
    task_completion_rate=(completed_tasks(current_user)/total_tasks(current_user))*100
    if task_completion_rate<=40:
        print(Fore.RED+"You have lots of pending assignments")
    elif task_completion_rate>40 and task_completion_rate<=69:
        print(Fore.YELLOW+"You're making progress")
    elif task_completion_rate>69 and task_completion_rate<=85:
        print(Fore.BLUE+"Great consistency 💫")
    elif task_completion_rate>=85 and task_completion_rate<=100:
        print(Fore.GREEN+"Excellent!, you're completing almost every task✅")
    print(f"═══════════════════════════════════════════════════════════════════════\n")
    print(f"📈 PRODUCTIVITY SCORE")
    print(f"{Fore.YELLOW}Current Streak: {Fore.WHITE} {view_streak(current_user)} days")
    print(f"{Fore.YELLOW}Badges Earned: {Fore.WHITE}{', '.join(get_badges(current_user)) if get_badges(current_user) else 'No badges earned yet'}")
    print(f"{Fore.YELLOW}Pomodoro sessions completed: {Fore.WHITE}{load_pomodoro(current_user)[0]['pomodoro']}")
    print(f"{Fore.YELLOW}Productivity score: {Fore.WHITE}{productivity_score(current_user)}")
    print(f"═══════════════════════════════════════════════════════════════════════\n")
    print(f"💡  RECOMMENDATIONS")
    recommendation(current_user)

    print(f"═══════════════════════════════════════════════════════════════════════\n")
    print(f"🌟 MOTIVATIONAL QUOTE")
    print(f"{Fore.WHITE}'{Fore.YELLOW}{motivational_quotes()}{Fore.WHITE}'")

dashboard()



def start_assistant():
   global current_user

   print(f"{Fore.YELLOW}=========== Student Assistant ==========")
   print(f"{Fore.GREEN} ====== Welcome {current_user} ====== ")
   
   while(True):    
        print(f"\n{Fore.BLUE}Choose any option ")
        print(f"{Fore.MAGENTA}1. Study timer")
        print(f"{Fore.MAGENTA}2. Notes")
        print(f"{Fore.MAGENTA}3. View study history")
        print(f"{Fore.MAGENTA}4. Assignments")
        print(f"{Fore.MAGENTA}5. Tasks")
        print(f"{Fore.MAGENTA}6. Dashboard")
        print(f"{Fore.MAGENTA}7. Alerts")
        print(f"{Fore.MAGENTA}8. Export Data")
        print(f"{Fore.MAGENTA}9. Import Data")

        print(f"{Fore.MAGENTA}10. Settings")
        print(f"{Fore.MAGENTA}11. Search")
        print(f"{Fore.MAGENTA}12. Productivity features")
        print(f"{Fore.MAGENTA}13. Insights")
        print(f"{Fore.MAGENTA}14. Reports")
        print(f"{Fore.MAGENTA}15. View achievements")
        print(f"{Fore.MAGENTA}16. View Profile")
        print(f"{Fore.MAGENTA}17. Backup System")
        print(f"{Fore.MAGENTA}18. Logout")
        print(f"{Fore.RED}19. Exit")
        choice=input(Fore.CYAN+"Enter choice")
        if choice=='1':
            study_timer(current_user)
        elif choice=='2':
            notes_menu()
        elif choice=='3':
            view_study_history(current_user)
        elif choice=='4':
            assignment_menu()
        elif choice=='5':
            tasks(current_user)
        elif choice=='6':
            dashboard()
        elif choice=='7':
            alerts_menu()
        elif choice=='8':
            export_menu()
        elif choice=='10':
            result=setting_menu()
            if result=="logout":
                return                
        elif choice=='11':
            search_menu()
        elif choice=='12':
            productivity_menu()
        elif choice=='13' :
            insights_menu()
        elif choice=='14':
            reports_menu()
        elif choice=='15':
            achievements()
        elif choice=='16':
            profile()
        elif choice=='17':
            backup_menu()
            break
        elif choice=='18':
           logout()
        elif choice=='19':
            print(Fore.BLUE+"Exiting student assistant...")
            return False
        else:
            print(Fore.RED+"INVALID CHOICE ")
