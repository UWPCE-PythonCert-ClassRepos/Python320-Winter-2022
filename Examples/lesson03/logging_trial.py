from loguru import logger

import trial2

logger.add("sample_log.txt")

logger.info("here's an example message")

trial2.log_something()

