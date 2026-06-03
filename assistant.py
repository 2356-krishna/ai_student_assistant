import time
from colorama import Fore,init
from utils.helperfunctio import load_study_history,save_study_session,load_notes,save_note
from utils.helperfunctio import load_assignment,save_assignment
init(autoreset=True)
def study_timer():
    minutes=int(input("Enter how many minutes you want to study : "))
    print(f"study session started for {minutes} minutes")
    time.sleep(minutes)
    print("congratulations !")
    print(f"you have completed your study session {minutes} minutes")
    save_study_session(minutes)
def view_study_history():
    history=load_study_history()
    if not history:
        print("\n no study session found")
        return
    print("\n study history")
    for i, session in enumerate(history,start=1):
        print(f"{i}. {session["duration"]} minutes")
def add_note():
    note=load_notes()
    new_note=input("enter new note you want to add")
    note.append(new_note)
    save_note(note)
def view_notes():
    note=load_notes()
    if not note:
        print("no note found")
        return
    print("\n===== NOTES =====")
    for i,notes in enumerate(note,start=1):
        print(f"{i}. {notes}")
def delete_note():
    note=load_notes()
    if not note:
       print("no notes to be deleted")
       return 
    try:
      view_notes()
      num=int(input("\nEnter number which note you want to delete"))
      
      if num>=1 and num<=len(note):
        deleted=note.pop(num-1)
        save_note(note)
        print(f"deleted {deleted}")
      else:
        print("invalid note number")
    except ValueError:
        print("invalid number ")
def add_assignment():
    assignments=load_assignment()
    title=input("enter asssignment title")
    due_date=input("enter due date of assignment (YYYY-MM-DD)")
    
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
    print("\n===== ASSIGNMENTS =====")
    for i,assignment in enumerate(assignments,start=1):
        status="completed" if assignment["completed"] else "pending"
        print(f"{i}. {assignment['title']} | DUE:{assignment['due_date']} | STATUS:{status}")
def mark_complete():
    assignments=load_assignment()
    if not assignments:
        print("no assignment found")
        return
    view_assignment()
    try: 
        num=int(input("Enter number which assignment you want to mark as completed"))
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
        num=int(input("Enter number which assignment you want to delete : "))
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
        print("\n===== ASSIGNMENT MENU =====")
        print("1. Add Assignment")
        print("2. View Assignment")
        print("3. Mark assignment as completed")
        print("4. Delete Assignment")
        print("5. Back")

        choice = input("Enter choice: ")

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
def notes_menu():
    while(True):
        print("\n===== NOTES MENU =====")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Delete Note")
        print("4. Back")

        choice = input("Enter choice: ")

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

def start_assistant():
    print(Fore.CYAN ,"============STUDENT ASSISTANT============") 
    name=input("Enter your NAME :")
    print(Fore.GREEN +f"Welcome {name}!")
    while(True):
        print("\nChoose any option ")
        print("1 Study timer")
        print("2 Notes")
        print("3 view study history ")
        print("4 Assignments")
        print("5 Exit")
        choice=int(input("Enter choice"))
        if choice==1:
            study_timer()
        elif choice==2:
            notes_menu()
        elif choice==3:
            view_study_history()
        elif choice==4:
            assignment_menu()
        elif choice==5:
            print(Fore.BLUE+"Exiting student assistant...")
            break
        else:
            print(Fore.RED+"INVALID CHOICE ")