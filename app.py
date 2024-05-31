from flask import Flask
from config import Config
from routes import register_routes
from error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

# Register error handlers
register_error_handlers(app)

@app.route('/')
def home():
    return "Hello there!"

# Register all routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
