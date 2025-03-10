from flask import Blueprint, render_template
from process_db import generate_plot

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	script, div = generate_plot()

	return render_template('home.html', script=script, div=div)