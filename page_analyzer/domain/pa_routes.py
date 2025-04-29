from flask import Blueprint, render_template

app_route = Blueprint('app_route', __name__)


@app_route.route('/')
def index():
    return render_template('index.html')

@app_route.route('/sites')
def show_sites():
    return render_template('index.html')

@app_route.route('/data-for-url')
def show_data_for_url():
    return render_template('index.html')