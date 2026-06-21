import time
import os
import hashlib
import csv
from colorama import Fore,init
from utils.helperfunctio import load_study_history,save_study_session,load_notes,save_note
from utils.helperfunctio import load_assignment,save_assignment
from utils.helperfunctio import total_study_sessions,total_study_time,total_notes_count,total_assignments_count,pending_assignments,completed_assignments
from utils.helperfunctio import load_users,save_users,save_goals,load_goals,save_pomodoro,load_pomodoro,load_streaks,save_streak
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
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
    minutes=int(input(Fore.CYAN+"Enter how many minutes you want to study : "))
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
        writer.writerow(['duration'])
        for session in history:
            writer.writerow([session['duration']])
    print(f"{Fore.GREEN} Study history exported successfully to exports/study_history.csv")
def export_menu():
    global current_user
    while(True):
        print(f"\n{Fore.BLUE}===== EXPORT MENU =====")
        print(f"{Fore.MAGENTA}1. export notes")
        print(f"{Fore.MAGENTA}2. export assignment")
        print(f"{Fore.MAGENTA}3. export study history")
        print(f"{Fore.RED}4. Back")
        choice = input(Fore.CYAN+"Enter choice: ")
        if choice == "1":
            export_notes(current_user)
        elif choice == '2':
            assignment_export(current_user)
        elif choice == '3':
            export_study_history(current_user)
        elif choice == "4":
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
    return f"{load[0]['goals']} minutes"
def pomodoro(current_username):
    study_minutes=int(input(Fore.CYAN+"Enter how many minutes you want to study or default 25 : ") or 25)
    break_time=int(input(Fore.CYAN+"Enter how many minutes of break you want  or default 5 : ")or 5)
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
    

def dashboard():
    global current_user
    print(f"\n{Fore.BLUE}===== DASHBOARD =====")
    print(f"{Fore.YELLOW}Total Study Sessions: {Fore.WHITE}{total_study_sessions(current_user)}")
    print(f"{Fore.YELLOW}Total Study Time: {Fore.WHITE}{total_study_time(current_user)} minutes")
    
    print(f"{Fore.YELLOW}Daily goal: {Fore.WHITE}{view_goal(current_user)} ")
    progress(current_user)
    print(f"{Fore.YELLOW}Current Streak: {Fore.WHITE} {view_streak(current_user)} days")
    
    

    print(f"{Fore.YELLOW}Total Notes: {Fore.WHITE}{total_notes_count(current_user)}")
    print(f"{Fore.YELLOW}Total Assignments: {Fore.WHITE}{total_assignments_count(current_user)}")
    # if pending_assignments()<1:
    #     print(f"{Fore.GREEN}Great job! You have no pending assignments.")
    # elif pending_assignments()==total_assignments_count():
    #     print(f"{Fore.RED}You have a lot of pending assignments. Try to complete them soon!")
    print(f"{Fore.YELLOW}Pending Assignments: {Fore.WHITE}{pending_assignments(current_user)}")
    print(f"{Fore.GREEN}Completed Assignments: {Fore.WHITE}{completed_assignments(current_user)}")
    print(f"{Fore.RED}Overdue Assignments: {Fore.WHITE}{overdue_count(current_user)}")

    completion_rate= (completed_assignments(current_user) / total_assignments_count(current_user) * 100) if total_assignments_count(current_user) > 0 else 0
    print(f"{Fore.CYAN}Assignment Completion Rate: {Fore.WHITE}{completion_rate}%")
    if completion_rate>=80:
        print(Fore.GREEN+"Excellent work! Your assignment completion rate is high.")

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
    result=[n for n in data if keyword in n]
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
   
def search_menu():
  global current_user

  while(True):
    print(f"\n{Fore.BLUE}===== SEARCH MENU =====")
    print(f"{Fore.MAGENTA} 1. Seacrh notes")
    print(f"{Fore.MAGENTA} 2. Search assignments")
    print(f"{Fore.MAGENTA} 3. VIEW PENDING ASSIGNMENTS")
    print(f"{Fore.MAGENTA} 4. VIEW COMPLETED ASSIGNMENTS")
    print(f"{Fore.RED} 5. Back")
    choice=input(Fore.CYAN+"Enter your choice: ")
    if choice=="1":
        search_notes(current_user)
    elif choice=='2':
        search_assignments(current_user)
    elif choice=='3':
        pending1_assignments(current_user)
    elif choice=='4':
        completed1_assignmments(current_user)
    elif choice=="5":
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
            print(f"\n {Fore.GREEN} Welcome : {username}")
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
  while(True):
    print(Fore.BLUE+"====== Settings ======")
    print(Fore.MAGENTA+"1. Change username ")
    print(Fore.MAGENTA+"2. Change Password ")
    print(Fore.MAGENTA+"3. Delete account")
    print(Fore.MAGENTA+"4. View account details")
    print(Fore.MAGENTA+"5. exit")
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
        break
    else:
        print(Fore.RED+"Invaid choice")


def productivity_score(current_username):
    load=load_assignment(current_username)
    streak=load_streaks(current_username)
    completed=sum(1 for a in load if a['completed'])
    score=completed*10+streak[0]['streaks']*5
    print(f"\n🎖️ Productivity score: {score}")

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
            productivity_score(current_user)
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

def analytics_menu():
   global current_user
   while(True):
    print(Fore.BLUE+"====== Analytics ======")
    print(Fore.MAGENTA+"1. Study graph")
    print(Fore.MAGENTA+"2. Assignment chart")
    print(Fore.MAGENTA+"3. Back")
    choice=input(Fore.CYAN+"Enter your choice: ")
    if choice=='1':
        study_graph(current_user)
    elif choice=='2':
       assignment_chart(current_user)
    elif choice=='3':
        break
    else:
        print(Fore.RED+"Invalid choice")


  
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
        print(f"{Fore.MAGENTA}5. Dashboard")
        print(f"{Fore.MAGENTA}6. Alerts")
        print(f"{Fore.MAGENTA}7. Export Data")
        print(f"{Fore.MAGENTA}8. Settings")
        print(f"{Fore.MAGENTA}9. Search")
        print(f"{Fore.MAGENTA}10. Productivity features")
        print(f"{Fore.MAGENTA}11. Insights")
        print(f"{Fore.MAGENTA}12. Analytics")
        print(f"{Fore.MAGENTA}13. View achievements")
        print(f"{Fore.MAGENTA}14. View Profile")
        print(f"{Fore.MAGENTA}15. Logout")
        print(f"{Fore.RED}16. Exit")
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
            dashboard()
        elif choice=='6':
            alerts_menu()
        elif choice=='7':
            export_menu()
        elif choice=='8':
            result=setting_menu()
            if result=="logout":
                return                
        elif choice=='9':
            search_menu()
        elif choice=='10':
            productivity_menu()
        elif choice=='11' :
            insights_menu()
        elif choice=='12':
            analytics_menu()
        elif choice=='13':
            achievements()
        elif choice=='14':
            profile()
            
        elif choice=='15':
            logout()
            break
        elif choice=='16':
            print(Fore.BLUE+"Exiting student assistant...")
            return False
        else:
            print(Fore.RED+"INVALID CHOICE ")
