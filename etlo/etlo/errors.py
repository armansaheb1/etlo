'''from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, MethodNotAllowed, NotFound, NotAcceptable, PermissionDenied, bad_request, ValidationError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):

    if isinstance(exc, NotAuthenticated):
        return Response({"status": False, 'data': {'message': "Authentication credentials were not provided."}}, status=status.HTTP_401_UNAUTHORIZED)
    if isinstance(exc, MethodNotAllowed):
        return Response({"status": False, 'data': {'message': "Method Not Allowed"}}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if isinstance(exc, NotFound):
        return Response({"status": False, 'data': {'message': "Not Found"}}, status=status.HTTP_404_NOT_FOUND)
    if isinstance(exc, NotAcceptable):
        return Response({"status": False, 'data': {'message': "Not Acceptable"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if isinstance(exc, PermissionDenied):
        return Response({"status": False, 'data': {'message': "FORBIDDEN"}}, status=status.HTTP_403_FORBIDDEN)
    if isinstance(exc, ValidationError):
        errors = ''
        for item in exc.detail:
            for itemm in exc.detail[item]:
                errors = errors + item + ' : ' + itemm + '\\n'
        return Response({'status': False, 'data': errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if exc.status_code == 403:
        return Response({"status": False, 'data': {'message': "Token not provided or in a wrong format."}}, status=status.HTTP_403_FORBIDDEN)
    if exc.status_code == 401:
        return Response({"status": False, 'data': {'message': "Token not provided or in a wrong format."}}, status=status.HTTP_403_FORBIDDEN)
    if exc.status_code == 400:
        return Response({"status": False, 'data': {'message': str(exc).replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace(", code='blank')", '').replace('ErrorDetail(', '').replace('string=', '').replace('', '')}}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"status": False, 'data': {'message': "Server Error"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # else
    # default case
    return exception_handler(exc, context)
'''
