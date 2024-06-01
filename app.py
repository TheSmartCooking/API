from flask import Flask
from config import Config
from routes import register_routes
from error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return "Hello there!"

# Register routes and error handlers
register_routes(app)
register_error_handlers(app)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='localhost', port=29565)
