# music_recommender
Welcome to NextSong! smart music recommender, using machine learning.

Team:
Michal Moryosef, Abel Asfaw, Dor Ulman, Tenzin Sherpa

### Brief Background:
The goal of this project is to study how music affects heart rate variability and see how audio features affect our heart rate speed. This has both entertainment and health benefit.
In the development of the product, NextSong used:

"CooSpo Heart Rate Monitor" to monitor heart rate.1
Pulsoid - heart rate widget for live streams used to broadcast user's live heart rate to NextSong server and feed it later to the model.2
Spotify API for all music analysis 3
"musicnn"- an open source, deep learning-based music tagger, used as NextSong tansfer model 4
1 https://www.amazon.com/gp/product/B07R8741CN/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
2 https://pulsoid.net/
3 https://developer.spotify.com/console/
4 https://github.com/jordipons/musicnn, https://towardsdatascience.com/musicnn-5d1a5883989b


### Install Locally:
Install the necessary Python packages by running:

<code> $ pip install -r requirements.txt> </code>

### Run Locally
Export the environment variables:

<code> $ export SPOTIFY_AUTHORIZATION_TOKEN=value_grabbed_from_spotify</code>

<code> $ export SPOTIFY_USER_ID=value_grabbed_from_spotify</code>

go to the colned project folder and run the entry-point script in cmd/termial:
<code> python app.py</code>

### NextSong Project Deck
put here a link

![This is an image](https://github.com/michali123/music_recommender/blob/cd1052abfbe285fc9c7fe13e9f1c2c0eb4b3601e/static/images/readme_screenshot.png)
