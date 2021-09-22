from PyInquirer.prompt import prompt
from simral.driver.DppaSimralDriver import DppaSimralDriver
from simral.config.Config import Config
from simral.sipd.Backup import findAllSkpd, findSubSkpd

import sqlite3

conn = sqlite3.connect("sipd_backup.db")