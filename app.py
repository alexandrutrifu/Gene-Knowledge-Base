# app.py
from flask import Flask
from flask_scss import Scss

import dataframes
from data_interaction import retrieve_dataframes
from routes import main_bp  # Import your blueprint

app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets')

# Register the blueprint with your app
app.register_blueprint(main_bp)

# Load dataframes
dataframes.df_values, dataframes.df_limma = retrieve_dataframes()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)