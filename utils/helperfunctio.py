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

