from flask import Flask
from config import Config
from db import get_db_connection
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

# Register all routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
