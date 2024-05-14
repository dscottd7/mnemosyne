from flask import Flask
from api.routes.api import api_route
from api.routes.views import views_route
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'static/files'

app.register_blueprint(api_route)
app.register_blueprint(views_route)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
