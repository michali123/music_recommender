# NextSong- Smart Music Recommender Using ML 

Team:
Michal Moryosef, Abel Asfaw, Dor Ulman, Tenzin Sherpa



![screenshot frontend](https://github.com/michali123/music_recommender/blob/7f202032e3563666a6b00c081ba7054d439794d7/static/images/screenshot%20frontend.png)

Welcome to NextSong! smart music recommender, using machine learning.

### Jupyter Notebook + HTML View 
Included in this repo inside Jupyter Noebook folder.
If for some reason you can not access to it please find it here:
https://drive.google.com/file/d/14vR92W6vfm4MUqNBWYZDgtj_hZXuvvLP/view?usp=sharing
https://drive.google.com/file/d/1Y5u6gnrgd5_Ts83fuJUs21UBriU5GwLN/view?usp=sharing

*In order to view visuals in HTML format you need to download Music Files folder (in Google Drive link) to the same path of your HTML.

### Demo
https://www.youtube.com/watch?v=_EVDI73n0sU
![image](https://user-images.githubusercontent.com/42022911/146870778-edec0e69-2d60-4b8d-8e07-a0f6e0d74fdd.png)

### NextSong Project Deck Sldes 
https://docs.google.com/presentation/d/1vv_OHbvcxyG1vmFbQ4ac_xXvftjzGMk01B1HucKkwiM/edit?usp=sharing

### Brief Background:
The goal of this project is to study how music affects heart rate variability and see how audio features affect our heart rate speed. This has both entertainment and health benefit.  
In the development of the product, NextSong used:
1. "CooSpo Heart Rate Monitor" to monitor heart rate.<sup>1</sup> 
2. Pulsoid - heart rate widget for live streams used to broadcast user's live heart rate to NextSong server and feed it later to the model.<sup>2</sup>
3. Spotify API for all music analysis <sup>3</sup>
4. "musicnn"- an open source, deep learning-based music tagger, used as NextSong tansfer model <sup>4</sup>

<sup>1</sup> https://www.amazon.com/gp/product/B07R8741CN/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1 <br>
<sup>2</sup> https://pulsoid.net/ <br>
<sup>3</sup> https://developer.spotify.com/console/ <br>
<sup>4</sup> https://github.com/jordipons/musicnn, https://towardsdatascience.com/musicnn-5d1a5883989b

### Technologies Used:

1. Flask
2. Bootstrap
3. Methods and Algorithms: CNN, Linear Regression, Transfer Learning
4. API's extensive usage from Spotify and Pulsoid

## Pre-Requisites To Run NextSong Locally:

#### 1. Clone project

#### Running the pretrained model:
You have to create a virtual enviorement for this, we recommend using anaconda for this.
If you dont have anaconda installed: (https://www.anaconda.com/products/individual)
open anaconda on your machine,
then run the follwing

<code> Conda create —name myenv</code> <br>
<code> Conda activate myenv</code> <br>
<code> After that run the requirements txt</code> <br>
* Make sure python is 3.7 not 3.8 


#### 2. Install the necessary Python packages

<code> $ pip install -r requirements.txt> </code>

#### 3. Own a Spotify account to get the music recommendation playlist created directly to your account.
https://www.spotify.com

#### 4. Export the environment variables

<code> $ export SPOTIFY_AUTHORIZATION_TOKEN=value_grabbed_from_spotify</code>

<code> $ export SPOTIFY_USER_ID=value_grabbed_from_spotify</code>

#### 5. Have a Pulsoid app account in order to live stream your heart rate to the website
https://pulsoid.net/

#### 6. In cloned project folder run the entry-point script in cmd/termial
<code> python app.py</code>

#### 7. Download "musicnn" transfer model from GoogleDrive link below and put in your cloned folder
(We couldn't attach it directly in this repo due to size limitations)
https://drive.google.com/drive/folders/1H9v07PqVAwPicbWGRxhDk3EQb3TY9VnF?usp=sharing

