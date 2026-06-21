from colorama import Fore,init 
from assistant import start_assistant
from assistant import auth
def main():
 while(True):
  if not auth():
    break
  if not start_assistant():
    break
 
main()

