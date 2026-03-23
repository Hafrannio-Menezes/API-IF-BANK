from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data.get("detail") if isinstance(response.data, dict) else None
    response.data = {
        "success": False,
        "message": str(detail) if detail else "Nao foi possivel processar a requisicao.",
        "errors": response.data,
    }
    return response
