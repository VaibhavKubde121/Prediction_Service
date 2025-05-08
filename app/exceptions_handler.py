# In main.py or a separate app/exception_handlers.py file
#
# from fastapi import Request
# from fastapi.responses import JSONResponse
# from app.exceptions import AppException
#
# async def app_exception_handler(request: Request, exc: AppException):
#     return JSONResponse(
#         status_code=400,
#         content={
#             "code": exc.code,
#             "message": exc.message,
#             "details": exc.details or "No additional details"
#         },
#     )