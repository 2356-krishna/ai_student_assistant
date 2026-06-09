from colorama import Fore,init 
from assistant import start_assistant
from assistant import auth
if auth():
    print(f"{Fore.YELLOW}=========== Student Assistant ==========")
    start_assistant()


