from flask import Flask
from config import Config
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return "Hello there!"

# Register all routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
