import pymysql 
pymysql.install_as_MySQLdb()
pymysql.version_info = (1, 4, 13, "final", 0)
from .celery import app as celery_app

__all__ = ('celery_app',)