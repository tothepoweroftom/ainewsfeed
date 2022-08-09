import argparse
from PIL import Image
import replicate
import requests
from dotenv import load_dotenv
import random
import os
from newsapi import NewsApiClient

# Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

import datetime


cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'second-flame-357709.appspot.com', 
    'databaseURL': 'https://second-flame-357709-default-rtdb.europe-west1.firebasedatabase.app/',
     'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

load_dotenv()

# [START cloudrun_helloworld_service]
# [START run_helloworld_service]
import os

from flask import Flask


NEWS_API = os.getenv("NEWS_API")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
newsapi = NewsApiClient(api_key=NEWS_API)


app = Flask(__name__)
if not os.path.exists('images'):
    os.makedirs('images')
temp_dir = "./images"


def getPicture():
    date = datetime.date.today().strftime("%B %d, %Y")
    top_headlines = newsapi.get_top_headlines(
        sources="bbc-news",
        language="en",
    )
    titles = []
    count = 0
    headline = random.choice(top_headlines["articles"])
    print(headline["title"])
    titles.append(headline["title"])
    
    styles = ["A Soviet propoganda poster of ",  "A beautiful painting of ", "A vivid pencil sketch of ", "An abstract art representation of ", "A beautiful painting of ", "A generative digital artwork of " "A watercolour sketch of ", "A colourful Japanese etching of ", "A celtic artwork of ", "A geometric artwork of ", "A minimalistic pointillism painting of ", "A paper collage artwork of "]        
    artists = ["Hiroshi Yoshida", "Max Ernst", "Paul Signac", "Salvador Dali", "James Gurney", "M.C. Escher", "Thomas Kinkade", "Ivan Aivazovsky", "Italo Calvino", "Norman Rockwell", "Albert Bierstadt", "Giorgio de Chirico", "Rene Magritte", "Ross Tran", "Marc Simonetti", "John Harris", "Hilma af Klint", "George Inness", "Pablo Picasso", "William Blake", "Wassily Kandinsky", "Peter Mohrbacher", "Greg Rutkowski", "Paul Signac", "Steven Belledin", "Studio Ghibli"]
    prompt = random.choice(styles) + random.choice(titles)  + " by " + random.choice(artists) +  ", " + "trending on Artstation"
    print(prompt)
    prediction_generator = replicate.models.get("nightmareai/disco-diffusion").predict(
        prompt=prompt,
        steps="100",
    )
    print(prediction_generator)
 
    for index, url in enumerate(prediction_generator):
        print(url)
        # construct filename
        uuid = url.split("/")[-2]
        extension = url.split(".")[-1]  # jpg, png, etc
        filename = f"{temp_dir}/{uuid}.{extension}"

        # download and save the file
        if(index == 6):  
            print("Getting image from url ---")
            data = requests.get(url)
            image_data = data.content

            bucket = storage.bucket()
            blob = bucket.blob(f"{date}/{uuid}.{extension}")
            print("Uploading to Google Storage")
            blob.upload_from_string(
                    image_data,
                    content_type=f"image/{extension}"
            )

            # Opt : if you want to make public access from the URL
            blob.make_public()
            print("your file url", blob.public_url)
            ref = db.reference('artworks/'+ f"{date}/{uuid}")
            ref.set({'imageURL':blob.public_url, 'headline': headline["title"], 'prompt': prompt})
            return
          
          


@app.route("/")
def hello_world():
    getPicture()
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]
