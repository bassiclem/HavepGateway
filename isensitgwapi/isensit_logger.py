import logging
import os.path


def initialize_logger(output_dir):

    """
    Logging for ISesnit Gateway API
    @param output_dir:
    @type output_dir:
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(format=FORMAT)
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "all.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

initialize_logger("./")
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}

logging.debug("debug message")
logging.debug("debug2  message")
logging.info("info message")
logging.warning("Protocol problem: %s", "connection reset", extra=d)
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

