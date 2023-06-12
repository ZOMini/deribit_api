from apscheduler.schedulers.background import (
    BackgroundScheduler,
    BlockingScheduler
)
from pytz import utc

from core.config import settings
from core.logger import logger
from db.pg import migrate
from services.worker_service import WorkerService

logger.name = 'worker'
# Если запускать только воркер, без ручек, то миграции ниже.
# migrate()
worker_sevice = WorkerService()
scheduler = BlockingScheduler(timezone=utc) #  Или BackgroundScheduler
scheduler._logger = logger
scheduler.add_job(worker_sevice.run_works,
                  'interval',
                  seconds=settings.scheduler_interval)
scheduler.start()
