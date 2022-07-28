import argparse
from PIL import Image
import replicate
import requests
from dotenv import load_dotenv
import random
import os
from newsapi import NewsApiClient

load_dotenv()

# [START cloudrun_helloworld_service]
# [START run_helloworld_service]
import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]
