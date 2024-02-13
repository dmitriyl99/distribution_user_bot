from app.core.models.models import Distribution

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


_scheduler = BackgroundScheduler(
    jobstores={
        'default': MemoryJobStore()
    }
)


def _once_template():
    pass


def _interval_template():
    pass


def add_template(template: Distribution):
    if not template.interval_measure:
        _scheduler.add_job(_once_template, trigger=DateTrigger(run_date=datetime.now() + timedelta(minutes=2)))
        return
    additional_counts = template.interval_number * template.interval_count
    trigger = None
    if template.interval_measure == 'hour':
        trigger = IntervalTrigger(hours=template.interval_number, end_date=datetime.now() + timedelta(hours=additional_counts))
    elif template.interval_measure == 'day':
        trigger = IntervalTrigger(days=template.interval_number, end_date=datetime.now() + relativedelta(days=additional_counts))
    elif template.interval_measure == 'week':
        trigger = IntervalTrigger(weeks=template.interval_number, end_date=datetime.now() + relativedelta(weeks=additional_counts))
    if trigger:
        _scheduler.add_job(_interval_template, trigger=trigger)

