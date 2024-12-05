import os

class Config(object):
    # Statement for enabling the development environment
    DEBUG = True

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
        