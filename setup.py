from setuptools import setup

APP = ['main.py']
DATA_FILES = ['src/data/db/sales.db']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'packages': ['tkinter', 'sqlite3']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
