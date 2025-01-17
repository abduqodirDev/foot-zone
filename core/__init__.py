import os


environment = os.getenv("DJANGO_ENV")


if environment == 'production':
    import pymysql

    pymysql.install_as_MySQLdb()
