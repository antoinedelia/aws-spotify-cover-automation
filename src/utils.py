from loguru import logger
import json


def format_response(message: str, status_code: int = 500, data=None):
    logger.info(f"Status code: {status_code}")
    logger.info(f"Message: {message}")
    logger.info(f"Data: {data}")

    if status_code >= 400:
        logger.error(message)
    else:
        logger.info(message)

    body = {
        "message": str(message),
        "body": data
    }

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(body)
    }


def handle_exception(exception: Exception):
    logger.error(exception)
    return format_response(exception, status_code=500)
