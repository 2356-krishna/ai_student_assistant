from utils.helperfunctio import load_tasks,save_tasks,APP_NAME,VERSION
print(f"Welcome to {APP_NAME}")
print(f"Version: {VERSION}")
tasks=load_tasks()
while True:
    print("\n 1 View tasks")
    print("2 Add tasks")
    print("3 exit")
    choice=int(input("enter your choice : "))
    if choice==1:
        if not tasks:
            print("no tasks available")
        else:
            for i,task in enumerate(tasks,start=1):
                print(f"{i}. {task}")
    elif choice==2:
        new_task=input("Enter new task : ")
        tasks.append(new_task)
        save_tasks(tasks)
        print("tasks added succesfully ")
    elif choice==3:
        print("Exiting tasks...")
        break
    else:
        print("invalid choice")
