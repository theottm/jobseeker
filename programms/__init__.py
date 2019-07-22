from flask import Flask

flask_app = Flask(__name__)

from programms import routes

if __name__ == '__main__':
    flask_app.run(debug=False)
