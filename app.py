from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes import register_routes
from error_handlers import register_error_handlers
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Set JWT configuration from environment variables
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize JWTManager with the Flask app
jwt = JWTManager(app)

@app.route('/')
def home():
    return "Hello there!"

# Register routes and error handlers
register_routes(app)
register_error_handlers(app)

if __name__ == '__main__':
    # Run the app with specified host and port from environment variables
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
