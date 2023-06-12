import logging

from core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
if settings.debug:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
