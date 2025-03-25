# run.py
from flask import Flask
from flask_scss import Scss

from app import dataframes
from app.data_interaction import retrieve_dataframes
from app.routes import main_bp

app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets')

app.register_blueprint(main_bp)

# Load dataframes
dataframes.df_values, dataframes.df_limma = retrieve_dataframes()
dataframes.original_df_limma = dataframes.df_limma.copy()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)