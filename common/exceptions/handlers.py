from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data.get("detail") if isinstance(response.data, dict) else None
    response.data = {
        "success": False,
        "message": detail or "Request could not be processed.",
        "errors": response.data,
    }
    return response
