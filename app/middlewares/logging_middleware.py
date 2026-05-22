import time
from flask import request, g, current_app


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()

        def custom_start_response(status, headers, exc_info=None):
            status_code = int(status.split(' ')[0])
            g.response_status = status_code
            cost_ms = int((time.time() - start_time) * 1000)
            g.request_cost = cost_ms

            log_msg = (
                f'[{request.method}] [{request.path}] '
                f'[{g.response_status}] [{cost_ms}ms] [{request.remote_addr}]'
            )

            if status_code >= 500:
                current_app.logger.error(log_msg)
            elif status_code >= 400:
                current_app.logger.warning(log_msg)
            else:
                current_app.logger.info(log_msg)

            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
