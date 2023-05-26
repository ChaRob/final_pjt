from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events
from .views import update_database, update_boxoffice
import datetime


def start():
    scheduler=BackgroundScheduler()
    register_events(scheduler)
    @scheduler.scheduled_job('cron', hour=datetime.datetime.now().time().hour+1,
                              minute=datetime.datetime.now().time().minute + (datetime.datetime.now().time().second+2)//60,
                              second=(datetime.datetime.now().time().second+2)%60, name = 'update_database')
    def auto_check():
        update_database()
        update_boxoffice()
    scheduler.start()