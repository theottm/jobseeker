from configparser import ConfigParser
import os

project_root = os.path.abspath("..")

# Load the configuration file
config = ConfigParser()
config.read(os.path.join(project_root, "config.ini"))
user = config["general"]["user"]
