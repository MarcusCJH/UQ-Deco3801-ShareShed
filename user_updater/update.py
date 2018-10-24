from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from user_updater import userUpdate

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(userUpdate.update_user, 'cron', day_of_week='mon-sun',
                      hour=1, coalesce=True)
    scheduler.start()
