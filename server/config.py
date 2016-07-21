import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Use PostgreSQL if credentials are available
sql_username = os.environ.get('STFD_DB_USER', None)
sql_dbname = os.environ.get('STFD_DB_NAME', None)
sql_password = os.environ.get('STFD_DB_PASS', None)
sql_url = os.environ.get('STFD_DB_URL', None)

SECRET_KEY = os.environ.get('SECRET_KEY', 'tempsecret')

if os.environ.get('STFD_MODE', None) == 'PRODUCTION':
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(
        sql_username,
        sql_password,
        sql_url,
        sql_dbname
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 3600
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'data.db')
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False