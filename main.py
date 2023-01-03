from flask import Flask
from src import setup

app = Flask(__name__)


if __name__ == '__main__':
    setup.configure()
    app.run(host='0.0.0.0', port=8000)
