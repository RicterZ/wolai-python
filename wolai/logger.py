import logging

logger = logging.getLogger('wolai-sdk')
handler = logging.StreamHandler()
formatter = logging.Formatter("\r[%(asctime)s] %(filename)s: %(message)s", "%H:%M:%S")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)
