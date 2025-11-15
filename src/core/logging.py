import logging
logging.basicConfig(level=logging.INFO)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
logger = logging.getLogger()
logger.addHandler(stdout_handler)
