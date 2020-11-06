import logging
import sys

from settings import (PROJECT_ROOT,
                      LOG_LEVEL, LOG_FORMAT, LOG_WRITE_MODE,
                      LOG_PATH, COLOR_SEQ, COLORS, RESET_SEQ, BOLD_SEQ, )


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(LOG_FORMAT))
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(LOG_PATH, mode=LOG_WRITE_MODE)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler


def get_logger(logger_name, level: str = None):
    if not level:
        level = LOG_LEVEL
    logger = logging.getLogger(logger_name)
    logger.addHandler(get_console_handler())
    # logger.addHandler(get_file_handler())
    logger.propagate = False
    level = level.lower()
    possible_levels = dict(debug=logging.DEBUG, info=logging.INFO,
                           warning=logging.WARNING, error=logging.ERROR)
    if level not in possible_levels:
        _lvlmsgpart = " or ".join([f"'{key}'" for key in possible_levels])
        raise ValueError(f"""Log level should be {_lvlmsgpart}, not {level}""")
    logger.setLevel(possible_levels[level])
    return logger
