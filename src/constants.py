from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

WHATSNEW_PATH = 'whatsnew/'
WHATSNEW_SECTION_ID = 'what-s-new-in-python'
WHATSNEW_DIV_CLASS = 'toctree-wrapper'
WHATSNEW_LI_CLASS = 'toctree-l1'

PEP_URL = 'https://peps.python.org/'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
PEP_TABLE_CLASS = 'pep-zero-table docutils align-default'
PEP_TR_CLASS = 'row-odd'
PEP_A_CLASS = 'pep reference internal'
