#!C:\Users\Puckooos\PycharmProjects\translator_website\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'py-translator==2.1.8','console_scripts','constants.py'
__requires__ = 'py-translator==2.1.8'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('py-translator==2.1.8', 'console_scripts', 'constants.py')()
    )
