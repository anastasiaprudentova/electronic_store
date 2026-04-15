import logging
import time

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """Логирование всех HTTP запросов"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        if not request.path.startswith("/static/") and not request.path.startswith(
            "/admin/"
        ):
            logger.info(
                f"{request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.2f}s - "
                f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
            )

        return response
