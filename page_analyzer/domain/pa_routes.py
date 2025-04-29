from flask import Blueprint, render_template

app_route = Blueprint('app_route', __name__)


@app_route.route('/test')
def index():
    # return '<h1>Page Analyzer</h1>'
    return render_template('index.html')
