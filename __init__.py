from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp
from dashboard.routes import dashboard_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(dashboard_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
