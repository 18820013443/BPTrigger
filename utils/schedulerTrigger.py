from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def TriggerFunc():
    # print('哇，开始扫描数据库了')
    pass


def ScanDatabase():
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(seconds=1)
    scheduler.add_job(TriggerFunc, trigger)
    scheduler.start()


ScanDatabase()
