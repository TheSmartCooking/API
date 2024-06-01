from datetime import timedelta
from flask import Flask
from config import Config
from routes import register_routes
from error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

@app.route('/')
def home():
    return "Hello there!"

# Register routes and error handlers
register_routes(app)
register_error_handlers(app)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=29565)
