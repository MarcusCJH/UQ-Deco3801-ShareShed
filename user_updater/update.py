from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from user_updater import userUpdate, lendingUpdate

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(userUpdate.update_user, 'cron', day_of_week='mon-sun',
                      hour=1, coalesce=True)
    scheduler.add_job(lendingUpdate.update_lending, 'cron', day_of_week='mon-sun',
                      hour=1, coalesce=True)
    scheduler.start()
