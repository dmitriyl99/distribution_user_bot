from app.core.models.models import Distribution

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from app.scheduler.template import template


_scheduler = BackgroundScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
    }
)


def start():
    _scheduler.start()


def stop():
    _scheduler.shutdown()


def add_template(distribution: Distribution):
    print(f"adding template: {distribution.name}")
    existing_job = _scheduler.get_job(f'distribution:{distribution.id}')
    if existing_job:
        return
    if not distribution.interval_measure:
        _scheduler.add_job(
            template,
            trigger=DateTrigger(run_date=datetime.now() + timedelta(seconds=10)),
            args=[distribution.id],
            id=f'distribution:{distribution.id}'
        )
        return
    additional_counts = distribution.interval_number * distribution.interval_count
    trigger = None
    if distribution.interval_measure == 'hour':
        trigger = IntervalTrigger(hours=distribution.interval_number, end_date=datetime.now() + timedelta(hours=additional_counts))
    elif distribution.interval_measure == 'day':
        trigger = IntervalTrigger(days=distribution.interval_number, end_date=datetime.now() + relativedelta(days=additional_counts))
    elif distribution.interval_measure == 'week':
        trigger = IntervalTrigger(weeks=distribution.interval_number, end_date=datetime.now() + relativedelta(weeks=additional_counts))
    if trigger:
        print(f"Add job distribution:{distribution.id}")
        _scheduler.add_job(template, trigger=trigger, id=f'distribution:{distribution.id}', args=[distribution.id])


