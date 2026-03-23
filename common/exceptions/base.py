from rest_framework import status
from rest_framework.exceptions import APIException


class BusinessRuleViolation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The requested operation violates a business rule."
    default_code = "business_rule_violation"


class ResourceConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "The resource already exists or is in a conflicting state."
    default_code = "resource_conflict"
