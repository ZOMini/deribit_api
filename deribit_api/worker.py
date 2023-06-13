from apscheduler.schedulers.background import (
    BackgroundScheduler,
    BlockingScheduler
)
from pytz import utc  # type: ignore[import]

from core.config import settings
from core.logger import logger
from services.worker_service import worker_run

logger.name = 'worker'
scheduler = BlockingScheduler(timezone=utc)  # Или BackgroundScheduler
scheduler._logger = logger
scheduler.add_job(worker_run,
                  'interval',
                  seconds=settings.scheduler_interval)
scheduler.start()
