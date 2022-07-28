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
import datetime


cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'second-flame-357709.appspot.com'
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
    for headline in top_headlines["articles"]:
        print(headline["title"])
        titles.append(headline["title"])
        styles = ["A Soviet propoganda poster of ", "A beautiful painting by William Turner of ", "A vivid pencil sketch of ", "An abstract art representation of ", "A beautiful painting by Van Gogh ", "A generative digital artwork of" "A watercolour sketch of ", "A colourful Japanese etching of ", "A celtic artwork of", "A geometric artwork of ", "A minimalistic pointillism painting of ", "A paper collage artwork of "]        
        prompt = random.choice(styles) + random.choice(titles)  + ", " + "trending on Artstation"
        print(prompt)
        prediction_generator = replicate.models.get("nightmareai/disco-diffusion").predict(
            prompt=prompt,
            steps="150"

        )
        count+=1
        if count <=15:
            for index, url in enumerate(prediction_generator):
                print(url)
                # construct filename
                prefix = str(count).zfill(4)  # 0001, 0002, etc.
                uuid = url.split("/")[-2]
                extension = url.split(".")[-1]  # jpg, png, etc
                filename = f"{temp_dir}/{prefix}.{extension}"

                # download and save the file
                if(index == 7):
                    data = requests.get(url)
                    image_data = data.content

                    bucket = storage.bucket()
                    blob = bucket.blob(f"{date}/{prefix}.{extension}")
                    blob.upload_from_string(
                            image_data,
                            content_type=f"image/{extension}"
                        )
                    # Opt : if you want to make public access from the URL
                    blob.make_public()
                    print("your file url", blob.public_url)
          


@app.route("/")
def hello_world():
    
   


    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


if __name__ == "__main__":
    getPicture()
    # app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END run_helloworld_service]
# [END cloudrun_helloworld_service]
