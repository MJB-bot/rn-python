import os
import logging
from logging.handlers import RotatingFileHandler
from flask import has_request_context, request, g


def setup_logger(app):
    log_dir = app.config['LOG_DIR']
    os.makedirs(log_dir, exist_ok=True)

    log_format = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    app_log_path = os.path.join(log_dir, 'app.log')
    app_file_handler = RotatingFileHandler(
        app_log_path, maxBytes=10 * 1024 * 1024, backupCount=10, encoding='utf-8'
    )
    app_file_handler.setFormatter(log_format)
    app_file_handler.setLevel(logging.INFO)

    error_log_path = os.path.join(log_dir, 'error.log')
    error_file_handler = RotatingFileHandler(
        error_log_path, maxBytes=10 * 1024 * 1024, backupCount=10, encoding='utf-8'
    )
    error_file_handler.setFormatter(log_format)
    error_file_handler.setLevel(logging.ERROR)

    app.logger.addHandler(console_handler)
    app.logger.addHandler(app_file_handler)
    app.logger.addHandler(error_file_handler)
    app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))


class RequestLogFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.method = request.method
            record.url = request.path
            record.ip = request.remote_addr
            record.status_code = getattr(g, 'response_status', '-')
            record.cost = getattr(g, 'request_cost', '-')
        else:
            record.method = '-'
            record.url = '-'
            record.ip = '-'
            record.status_code = '-'
            record.cost = '-'
        return True
