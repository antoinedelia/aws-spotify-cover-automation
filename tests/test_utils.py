import json

from src.utils import format_response, handle_exception


def test_format_response_success():
    """
    Test format_response for a typical successful response (e.g., 200 OK).
    """
    message = "Operation successful"
    status_code = 200
    data = {"id": 123, "name": "Test Item"}

    expected_body_dict = {"message": message, "body": data}

    response = format_response(message, status_code, data)

    assert response["statusCode"] == status_code
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    assert isinstance(response["body"], str)
    assert json.loads(response["body"]) == expected_body_dict


def test_format_response_client_error_no_data():
    """
    Test format_response for a client error (e.g., 404 Not Found) with no data.
    """
    message = "Resource not found"
    status_code = 404

    expected_body_dict = {"message": message, "body": None}

    response = format_response(message, status_code=status_code)

    assert response["statusCode"] == status_code
    assert response["headers"]["Content-Type"] == "application/json"
    assert json.loads(response["body"]) == expected_body_dict


def test_format_response_server_error_with_exception_message():
    """
    Test format_response when message is an exception object.
    """
    error_message = "Something went terribly wrong"
    exception_obj = ValueError(error_message)
    status_code = 500

    expected_body_dict = {"message": error_message, "body": None}

    response = format_response(exception_obj, status_code=status_code)

    assert response["statusCode"] == status_code
    assert json.loads(response["body"]) == expected_body_dict


def test_handle_exception_returns_500_error_response():
    """
    Test handle_exception to ensure it formats an exception into a 500 error response.
    """
    error_message = "A test exception occurred"
    exception_obj = RuntimeError(error_message)

    response = handle_exception(exception_obj)

    assert response["statusCode"] == 500
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    assert isinstance(response["body"], str)
    actual_body_dict = json.loads(response["body"])
    assert actual_body_dict["message"] == error_message
    assert actual_body_dict["body"] is None
