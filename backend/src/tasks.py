from src import celery
from datetime import datetime

@celery.task()
def just_say_hello(name):
    print("Inside Task")
    print(f"Hello, {name}.")
    return name