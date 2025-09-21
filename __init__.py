from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp
from dashboard.routes import dashboard_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(dashboard_bp, url_prefix='/api')

# Check for valid database URL
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL or "@" not in DATABASE_URL or "://" not in DATABASE_URL:
    raise RuntimeError("Invalid or missing DATABASE_URL environment variable. Please set it to a valid connection string.")

if __name__ == '__main__':
    app.run(debug=True)
