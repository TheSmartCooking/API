from flask import jsonify, current_app
from pymysql import DatabaseError
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, Forbidden, MethodNotAllowed

def handle_database_error(error):
    # Log the error
    current_app.logger.error('Database connection error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Database connection error'})
    response.status_code = 500
    return response

def handle_not_found_error(error):
    # Log the error
    current_app.logger.error('Not found error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Resource not found'})
    response.status_code = 404
    return response

def handle_bad_request_error(error):
    # Log the error
    current_app.logger.error('Bad request error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Bad request'})
    response.status_code = 400
    return response

def handle_unauthorized_error(error):
    # Log the error
    current_app.logger.error('Unauthorized error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Unauthorized'})
    response.status_code = 401
    return response

def handle_forbidden_error(error):
    # Log the error
    current_app.logger.error('Forbidden error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Forbidden'})
    response.status_code = 403
    return response

def handle_method_not_allowed_error(error):
    # Log the error
    current_app.logger.error('Method not allowed error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Method not allowed'})
    response.status_code = 405
    return response

def handle_server_error(error):
    # Log the error
    current_app.logger.error('Server error: %s', error)

    # Return a custom error message to the client
    response = jsonify({'error': 'Internal server error'})
    response.status_code = 500
    return response

def register_error_handlers(app):
    app.register_error_handler(DatabaseError, handle_database_error)
    app.register_error_handler(NotFound, handle_not_found_error)
    app.register_error_handler(BadRequest, handle_bad_request_error)
    app.register_error_handler(Unauthorized, handle_unauthorized_error)
    app.register_error_handler(Forbidden, handle_forbidden_error)
    app.register_error_handler(MethodNotAllowed, handle_method_not_allowed_error)
    app.register_error_handler(Exception, handle_server_error)
