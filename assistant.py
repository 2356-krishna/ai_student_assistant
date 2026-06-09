import time
import csv
from colorama import Fore,init
from utils.helperfunctio import load_study_history,save_study_session,load_notes,save_note
from utils.helperfunctio import load_assignment,save_assignment
from utils.helperfunctio import total_study_sessions,total_study_time,total_notes_count,total_assignments_count,pending_assignments,completed_assignments
from utils.helperfunctio import load_users,save_users
init(autoreset=True)
def study_timer():
    minutes=int(input(Fore.CYAN+"Enter how many minutes you want to study : "))
    print(f"study session started for {minutes} minutes")
    time.sleep(minutes*60)
    print("congratulations !")
    print(f"you have completed your study session {minutes} minutes")
    save_study_session(minutes)
def view_study_history():
    history=load_study_history()
    if not history:
        print("\n no study session found")
        return
    print(f"\n{Fore.BLUE}===== STUDY HISTORY =====")
    for i, session in enumerate(history,start=1):
        print(f"{i}. {session["duration"]} minutes")


def export_notes():
            notes=load_notes()
            with open("exports/notes.csv",'w',newline='') as file:
                writer=csv.writer(file)
                writer.writerow(['note'])
                for note in notes:
                    writer.writerow([note])
            print(f"{Fore.GREEN} Notes exported successfully to exports/notes.csv")
def assignment_export():
    assignments=load_assignment()
    with open("exports/assignment.csv",'w') as file:
        writer=csv.writer(file)
        writer.writerow(['Title','Due_Date','Completed'])
        for assignment in assignments:
            writer.writerow([assignment['title'],assignment['due_date'],assignment['completed']])
    print(f"{Fore.GREEN} Assignment exported successfully to exports/assignment.csv")
def export_study_history():
    history=load_study_history()
    with open("exports/study_history.csv",'w',newline='')as file:
        writer=csv.writer(file)
        writer.writerow(['duration'])
        for session in history:
            writer.writerow([session['duration']])
    print(f"{Fore.GREEN} Study history exported successfully to exports/study_history.csv")
def export_menu():
    while(True):
        print(f"\n{Fore.BLUE}===== EXPORT MENU =====")
        print(f"{Fore.MAGENTA}1. export notes")
        print(f"{Fore.MAGENTA}2. export assignment")
        print(f"{Fore.MAGENTA}3. export study history")
        print(f"{Fore.RED}4. Back")
        choice = int(input(Fore.CYAN+"Enter choice: "))
        if choice == 1:
            export_notes()
        elif choice == 2:
            assignment_export()
        elif choice == 3:
            export_study_history()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")

def add_assignment():
    assignments=load_assignment()
    title=input(Fore.CYAN+"enter asssignment title")
    due_date=input(Fore.CYAN+"enter due date of assignment (YYYY-MM-DD)")
    
    assignments.append({
        "title":title,
        "due_date":due_date,
        "completed":False
    })
    save_assignment(assignments)
def view_assignment():
    assignments=load_assignment()
    if not assignments:
        print("no assignment found")
        return
    print(f"\n{Fore.BLUE}===== ASSIGNMENTS =====")
    for i,assignment in enumerate(assignments,start=1):
        status="completed✅" if assignment["completed"] else "pending❌"
        print(f"{i}. {assignment['title']} | DUE:{assignment['due_date']} | STATUS:{status}")
def mark_complete():
    assignments=load_assignment()
    if not assignments:
        print("no assignment found")
        return
    view_assignment()
    try: 
        num=int(input(Fore.CYAN+"Enter number which assignment you want to mark as completed"))
        if num>=1 and num<=len(assignments):
            assignments[num-1]["completed"]=True
            save_assignment(assignments)
        else:
            print("invalid number")
    except ValueError:
        print("invalid number") 
def delete_Assignment():
    assignments=load_assignment()
    if not assignments:
        print("no assignments found")
        return
    view_assignment()
    try:
        num=int(input(Fore.CYAN+"Enter number which assignment you want to delete : "))
        if num>=1 and num<=len(assignments):
            assignments.pop(num-1)
            save_assignment(assignments)
            print("assignment deleted")
        else:
            print("invalid number")
    except ValueError:
        print("invalid number")
def assignment_menu():
    while(True):
        print(f"\n{Fore.BLUE}===== ASSIGNMENT MENU =====")
        print(f"{Fore.MAGENTA}1. Add Assignment")
        print(f"{Fore.MAGENTA}2. View Assignment")
        print(f"{Fore.MAGENTA}3. Mark assignment as completed")
        print(f"{Fore.MAGENTA}4. Delete Assignment")
        print(f"{Fore.RED}5. Back")

        choice = input(Fore.CYAN+"Enter choice: ")

        if choice == "1":
            add_assignment()

        elif choice == "2":
            view_assignment()

        elif choice == "3":
            mark_complete()

        elif choice == "4":
            delete_Assignment()

        elif choice == "5":
            break

        else:
            print("Invalid choice.")
def add_note():
    note=load_notes()
    new_note=input(Fore.CYAN+"enter new note you want to add")
    note.append(new_note)
    save_note(note)
def view_notes():
    note=load_notes()
    if not note:
        print("no note found")
        return
    print(f"\n{Fore.BLUE}===== NOTES =====")
    for i,notes in enumerate(note,start=1):
        print(f"{i}. {notes}")
def delete_note():
    note=load_notes()
    if not note:
       print("no notes to be deleted")
       return 
    try:
      view_notes()
      num=int(input(Fore.CYAN+"\nEnter number which note you want to delete"))
      
      if num>=1 and num<=len(note):
        deleted=note.pop(num-1)
        save_note(note)
        print(f"deleted {deleted}")
      else:
        print("invalid note number")
    except ValueError:
        print("invalid number ")
def notes_menu():
    while(True):
        print(f"\n{Fore.BLUE}===== NOTES MENU =====")
        print(f"{Fore.MAGENTA}1. Add Note")
        print(f"{Fore.MAGENTA}2. View Notes")
        print(f"{Fore.MAGENTA}3. Delete Note")
        print(f"{Fore.RED}4. Back")

        choice = input(Fore.CYAN+"Enter choice: ")

        if choice == "1":
            add_note()

        elif choice == "2":
            view_notes()

        elif choice == "3":
            delete_note()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")

def dashboard():
    print(f"\n{Fore.BLUE}===== DASHBOARD =====")
    print(f"{Fore.YELLOW}Total Study Sessions: {total_study_sessions()}")
    print(f"{Fore.YELLOW}Total Study Time: {total_study_time()} minutes")
    print(f"{Fore.YELLOW}Total Notes: {total_notes_count()}")
    print(f"{Fore.YELLOW}Total Assignments: {total_assignments_count()}")
    # if pending_assignments()<1:
    #     print(f"{Fore.GREEN}Great job! You have no pending assignments.")
    # elif pending_assignments()==total_assignments_count():
    #     print(f"{Fore.RED}You have a lot of pending assignments. Try to complete them soon!")
    print(f"{Fore.RED}Pending Assignments: {pending_assignments()}")
    print(f"{Fore.GREEN}Completed Assignments: {completed_assignments()}")
    completion_rate= (completed_assignments() / total_assignments_count() * 100) if total_assignments_count() > 0 else 0
    print(f"{Fore.CYAN}Assignment Completion Rate: {completion_rate}%")
    if completion_rate>=80:
        print(Fore.GREEN+"Excellent work! Your assignment completion rate is high.")

def search_notes():
    note=load_notes()
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
def search_assignments():
    data=load_assignment()
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
def pending_assignments():
    assign=load_assignment()
    for a in assign:
        if not a['completed']:
            print(f"{Fore.RED}Pending Assignment: {a['title']} | DUE: {a['due_date']}")
def completed_assignmments():
    assign=load_assignment()
    for a in assign:
        if a['completed']:
            print(f"{Fore.GREEN}Completed Assignment: {a['title']} | DUE: {a['due_date']}")
    print(Fore.CYAN ,"============STUDENT ASSISTANT============") 
    name=input(Fore.CYAN+"Enter your NAME :")
    print(Fore.GREEN +f"Welcome {name}!")
def search_menu():
  while(True):
    print(f"\n{Fore.BLUE}===== SEARCH MENU =====")
    print(f"{Fore.MAGENTA} 1. Seacrh notes")
    print(f"{Fore.MAGENTA} 2. Search assignments")
    print(f"{Fore.MAGENTA} 3. VIEW PENDING ASSIGNMENTS")
    print(f"{Fore.MAGENTA} 4. VIEW COMPLETED ASSIGNMENTS")
    print(f"{Fore.RED} 5. Back")
    choice=int(input(Fore.CYAN+"Enter your choice: "))
    if choice==1:
        search_notes()
    elif choice==2:
        search_assignments()
    elif choice==3:
        pending_assignments()
    elif choice==4:
        completed_assignmments()
    elif choice==5:
        print(f"{Fore.BLUE} returning to main menu...")
        break
    else:
        print(f"{Fore.RED}invalid choice")



def register():
  load=load_users()
  username=input(f"{Fore.MAGENTA} Enter username: ")
  password=input(f"{Fore.MAGENTA} Enter password: ")
  
  for user in load:
      if user['username']==username:
        print(f"{Fore.RED} User Already Exists!")
        return
  load.append({
      'username':username,
      'password':password})    
  save_users(load)
  print(Fore.GREEN+"Registration Successfully!")


def login():
    load=load_users()
    username=input(f"{Fore.MAGENTA} Enter username: ")
    password=input(f"{Fore.MAGENTA} Enter password: ")
    for user in load:
        if user['username']==username and user['password']==password:
            print("login successfully") 
            return True
    print(Fore.RED+"Invalid crendtials")    
    return False   
def auth():
  while(True):
    print(f"{Fore.BLUE}======= Login system =======")
    print(f"{Fore.MAGENTA}1. Register")
    print(f"{Fore.MAGENTA}2. Login")
    print(f"{Fore.MAGENTA}3. Exit")
    choice=int(input(f"{Fore.CYAN} Enter your choice : "))
    if choice==1:
        register()
    elif choice==2:
        if login():
            return True
    elif choice==3:
        return False
    else:
        print(Fore.RED+"Invalid choice")


    


  
def start_assistant():
   user=input(f"{Fore.CYAN} Enter Your Name: ")
   print(f"{Fore.GREEN} ====== Welcome {user} ====== ")
   
   while(True):    
        print(f"\n{Fore.BLUE}Choose any option ")
        print(f"{Fore.MAGENTA}1. Study timer")
        print(f"{Fore.MAGENTA}2. Notes")
        print(f"{Fore.MAGENTA}3. View study history")
        print(f"{Fore.MAGENTA}4. Assignments")
        print(f"{Fore.MAGENTA}5. Dashboard")
        print(f"{Fore.MAGENTA}6. Export Data")
        print(f"{Fore.MAGENTA}7. Search")
        print(f"{Fore.RED}8. Exit")
        choice=int(input(Fore.CYAN+"Enter choice"))
        if choice==1:
            study_timer()
        elif choice==2:
            notes_menu()
        elif choice==3:
            view_study_history()
        elif choice==4:
            assignment_menu()
        elif choice==5:
            dashboard()
        elif choice==6:
            export_menu()
        elif choice==7:
            search_menu()
        elif choice==8:
            print(Fore.BLUE+"Exiting student assistant...")
            break
        else:
            print(Fore.RED+"INVALID CHOICE ")
