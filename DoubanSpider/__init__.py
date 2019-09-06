import os

# 环境检查


try:
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    import requests
    import re
    import time
    import csv
    import threading
    import sqlite3
    import logging
except:
    print('[System]正在安装支持库...')
    os.system('pip install SQLAlchemy')
    os.system('pip install sqlite')
    os.system('pip install threading')
    os.system('pip install csv')
    os.system('pip install requests')
    os.system('pip install logging')
    import requests
    import csv
    import logging
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
