from colorama import Fore,init
init(autoreset=True)
def start_assistant():
    print(Fore.CYAN ,"============STUDENT ASSISTANT============") 
    name=input("Enter your NAME :")
    print(Fore.GREEN +f"Welcome {name}!")
    while(True):
        print("\nChoose any option ")
        print("1 Study timer")
        print("2 Notes")
        print("3 Exit")
        choice=int(input("Enter choice"))
        if choice==1:
            print(Fore.YELLOW+"study timer feature coming soon....")
        elif choice==2:
            print(Fore.YELLOW+"notes analyzer feature coming soon....")
        elif choice==3:
            print(Fore.BLUE+"Exiting student assistant...")
            break
        else:
            print(Fore.RED+"INVALID CHOICE ")