from flask import Flask

app = Flask(__name__, instance_relative_config=True, static_url_path='', static_folder='static')

from app import views

# Load the config file
app.config.from_object('config')