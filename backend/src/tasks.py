from src import celery, app
from datetime import datetime
from celery.schedules import crontab

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

# celery.Task = ContextTask

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(5000, just_say_hello.s(), name="Runs every 5 seconds.")

@celery.task()
def just_say_hello():
    print("Inside Task")
    print(f"Hello, Manmay.")
    # return name