# app.py
from flask import Flask
from flask_scss import Scss
from routes import main_bp  # Import your blueprint

app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets')

# Register the blueprint with your app
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)