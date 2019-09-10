import os

# 环境检查


try:
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    import random
    import re
    import time
    import csv
    import requests
    import time
    import sqlite3
    import logging
except:
    print('[System]正在安装支持库...')
    os.system(r'pip install -r .\DoubanSpider\requirements.txt')
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    import random
    import re
    import time
    import csv
    import requests
    import time
    import sqlite3
    import logging

finally:
    print('[System]运行库加载完毕！')
