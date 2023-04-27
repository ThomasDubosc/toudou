import os
import logging

config = dict(
    DATABASE_URL=os.getenv('TOUDOU_DATABASE_URL', ''),
    DEBUG=os.getenv('TOUDOU_DEBUG', 'False') == 'True',
    UPLOAD_FOLDER=os.getenv('TOUDOU_UPLOAD_FOLDER', '.'),
)


logging.basicConfig(
    level=int(os.getenv('TOUDOU_LOGGING_LEVEL', '20')),
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('toudou.log'),
        logging.StreamHandler()
    ]
)



