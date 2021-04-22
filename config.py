import os


class Config:
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_HTTP_PORT = os.getenv('RABBITMQ_HTTP_PORT', '16672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'rmquser')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'qpassword')
    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_HOST_ACTION = os.getenv('DB_HOST_ACTION', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '6432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USESSL = os.getenv('DB_USESSL', '')
    DB_ACTION_CERTIFICATES = os.getenv('DB_ACTION_CERTIFICATES',
                                       (" sslmode=verify-ca sslrootcert=/home/monitoring/.postgresql-action/root.crt "
                                        "sslcert=/home/monitoring/.postgresql-action/postgresql.crt "
                                        "sslkey=/home/monitoring/.postgresql-action/postgresql.key"))
    EXCEPTIONMANAGER_HOST = os.getenv('EXCEPTIONMANAGER_HOST', 'localhost')
    EXCEPTIONMANAGER_PORT = os.getenv('EXCEPTIONMANAGER_PORT', '8666')
    EXCEPTIONMANAGER_URL = f'http://{EXCEPTIONMANAGER_HOST}:{EXCEPTIONMANAGER_PORT}'
    BAD_MESSAGE_MINIMUM_SEEN_COUNT = os.getenv('BAD_MESSAGE_MINIMUM_SEEN_COUNT', '4')
