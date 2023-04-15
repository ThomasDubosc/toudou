import os

config = dict(
    DATABASE_URL=os.getenv('TOUDOU_DATABASE_URL', ''),
    DEBUG=os.getenv('TOUDOU_DEBUG', 'False') == 'True',
    UPLOAD_FOLDER=os.getenv('TOUDOU_UPLOAD_FOLDER', '.'),
)


