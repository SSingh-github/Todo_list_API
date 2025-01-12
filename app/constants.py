# Database Constants
class Database:
    URI_TEMPLATE = "mysql+pymysql://{user}:{password}@{host}/{dbname}"
    TABLE_NAME_USERS = 'users'
    TABLE_NAME_TASKS = 'tasks'
    COLUMN_ID = 'id'
    COLUMN_USERNAME = 'username'
    COLUMN_PASSWORD = 'password'

# App Configuration Constants
class AppConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Messages
class Messages:
    HELLO_WORLD = "hello world"

