import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


logging_format = logging.Formatter("%(asctime)s:%(module)s:%(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.DEBUG)
streamhandler.setFormatter(logging_format)

logger.addHandler(streamhandler)
