import pytz  # type: ignore[import]
from apscheduler.schedulers.background import BlockingScheduler

from core.config import settings
from core.logger import logger
from services.worker_service import worker_run

logger.name = 'worker'
scheduler = BlockingScheduler(timezone=pytz.utc)  # Или BackgroundScheduler
scheduler._logger = logger
scheduler.add_job(worker_run,
                  'interval',
                  seconds=settings.scheduler_interval)
scheduler.start()
