from pathlib import Path

# Program settings/defaults

DEFAULT_WRLD_SZ_X = 10
DEFAULT_WRLD_SZ_Y = 10
_REGION_IMAGE_WIDTH = 300
_REGION_IMAGE_HEIGHT = 225

#  Directories/paths
PROJECT_ROOT = Path(__file__).parent.resolve()
LOG_PATH = PROJECT_ROOT / 'logfile.log'

RESOURCES_DIR = PROJECT_ROOT / 'resources'



# Overig log file spul
LOG_FORMAT = '%(asctime)s — %(name)s — %(levelname)s — %(message)s'
LOG_WRITE_MODE = 'w'  # 'w' for overwriting log file each run, 'a' for appending log file. For debugging; usually 'w'.
LOG_LEVEL = 'debug'

# LOG_FORMAT = '%(name)s — %(levelname)s — %(message)s'
# Kleurtjes voor log
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'ERROR': RED
}
