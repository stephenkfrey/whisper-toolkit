# %% [markdown]
# # --- Input custom variables here --- 

# %%
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL9zq2zalZB1JRZsPtYeFVQAZkrDbZx3Qw" # My Learning Playlist 
TEST_URL = "https://www.youtube.com/watch?v=1AElONvi9WQ" # 1 minute video 

WHISPER_MODEL_SIZE = "tiny"

# %% [markdown]
# # --- How to use --- 
# 
# Export notebook as `transcribe_youtube.py`, then import to use the key functions
# 
# 
# 
# ### example usage 
# 
# In your Python script/notebook: 
# 
# ```
# from transcribe_youtube import get_transcription_from_youtube_url, get_transcriptions_from_youtube_playlist
# 
# PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL9zq2zalZB1JRZsPtYeFVQAZkrDbZx3Qw" # My Learning Playlist 
# TEST_URL = "https://www.youtube.com/watch?v=vaUy6zyJfwU" # 1 minute video 
# 
# # get transcription for a single video 
# single_video_transcription = get_transcription_from_youtube_url(TEST_URL)
# 
# # get transcriptions for all videos in a playlist
# playlist_transcriptions = get_transcriptions_from_youtube_playlist(PLAYLIST_URL)
# 
# ```
# 
# 
# ### return object
# Returns a dict with `title`, `url`, and `transcription`
# 
# 
# Example: 
# ```
# {'title': 'Deep Learning Maps Animal Movement',
#  'url': 'https://www.youtube.com/watch?v=vaUy6zyJfwU',
#  'transcription': ' We developed a new type of 3D deep learning approach that can take in normal color videos of behaving animals and behaving humans and then output the precise 3D locations of body landmarks so skeletal joints that you can track over time and thus provide a comprehensive description of how subjects are moving. This is a huge leap forward compared to a traditional motion capture system in which subjects need to wear highly invasive markers on the body. And then another big issue with motion captures that it requires that you have a clear line of sights to these markers and in a deep learning-based approach that we develop, we relieve this requirement.'}
#  ```

# %% [markdown]
# # --- Run Notebook --- 

# %%
# !pip install replicate
# !pip install pytube
# !pip install flask 

# %%
import pandas as pd
from pytube import YouTube, Playlist 

# %% [markdown]
# ### Load Replicate's Whisper API 

# %%
import os
from dotenv import load_dotenv
load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_KEY")
REPLICATE_MODEL_VERSION = os.getenv("REPLICATE_MODEL_VERSION")

# %%
# create a replicate client 
import replicate
client = replicate.Client(api_token=REPLICATE_API_TOKEN)
model = client.models.get("openai/whisper")
version = model.versions.get(REPLICATE_MODEL_VERSION)

# %%
def transcribe_audio(audio_url):
    output = version.predict(
        audio=audio_url,
        language="en", 
        model=WHISPER_MODEL_SIZE
    )

    return output 

# %%
def get_mp3_url_from_youtube(youtube_url):
    mp3 = YouTube(youtube_url).streams.filter(only_audio=True).first()
    return mp3.url 

# %%
# the main function 
import time 

def get_raw_transcription_from_youtube_url(youtube_url):
    start_time = time.time()
    mp3_url = get_mp3_url_from_youtube(youtube_url)
    whisperresponse = transcribe_audio(mp3_url)

    # if whiser fails then return err 
    
    # print ("Time taken to transcribe (sec): ", time.time() - start_time)
    return whisperresponse['transcription']


# %%
def get_transcription_from_youtube_url(youtube_url):
    yt_object = YouTube(youtube_url)
    title = yt_object.title
    transcription = get_raw_transcription_from_youtube_url(youtube_url)

    return {
        "title": title,
        "url": youtube_url,
        "content": transcription
    }


# %%
# TESTING 
# # create an mp3 object from the youtube video

# mp3 = YouTube(TEST_URL).streams.filter(only_audio=True).first()
# print (mp3.url)

# whisperresponse = transcribe_audio(mp3.url)
# trans = whisperresponse['transcription']
# trans

# %%
# trans = get_transcription_from_yt_url(TEST_URL)
# trans

# %% [markdown]
# # Run transcription on an entire YouTube Playlist 

# %% [markdown]
# ### playlist helpers 

# %%
def get_urls_from_youtube_playlist(playlist_url):
    """Returns a list of video urls from a youtube playlist"""
    playlist = Playlist(playlist_url)
    return playlist.video_urls

# print (get_urls_from_youtube_playlist(PLAYLIST_URL))

# %% [markdown]
# ### main function: youtube playlist -> dict of transcriptions

# %%
# get the urls from the playlist

def get_transcriptions_from_youtube_playlist(playlist_url):
    """
    Returns a list of dictionaries with the following keys:
    - title
    - url
    - content
    """

    start_time = time.time()

    # Get list of individual video URLS
    playlist_url_list = get_urls_from_youtube_playlist(PLAYLIST_URL)

    # Get playlist title 
    playlist_title = Playlist(PLAYLIST_URL).title

    # ========
    # For each video, get the transcription
    transcriptions = [] # list to be returned 

    for url in playlist_url_list:
        transcriptions.append(
            get_transcription_from_youtube_url(url)
        )

    # OPTIONAL: save to a csv file
    df = pd.DataFrame(transcriptions)
    df.to_csv(f"{playlist_title}_transcriptions.csv", index=False)

    # log the time taken, round to 2 decimal places
    print (f"\n===\nTime taken to transcribe Playlist '{playlist_title}' (sec): \n", round(time.time() - start_time, 2), "\n===")

    return transcriptions


# %% [markdown]
# # --- Run tests ---

# %%
# single_video_transcription = get_transcription_from_youtube_url(TEST_URL)
# single_video_transcription

# %%
# # save that to a csv file

# with open ("single_video_transcription.csv", "w") as f:
#     f.write(single_video_transcription['transcription'])

# %%
# playlist_transcriptions = get_transcriptions_from_youtube_playlist(PLAYLIST_URL)
# playlist_transcriptions

# %%


# %% [markdown]
# # --- with Banana.dev ---

# %%


# %%
from io import BytesIO
import base64
import banana_dev as banana

api_key = "2782cbc2-5317-49e8-a7a3-eb5fcb308c9f"
model_key = "b80a43e4-06ff-420e-9f74-1e099ee75755"

# Expects an mp3 file named test.mp3 in directory
with open(f'whisper.mp3', 'rb') as file:
    mp3bytes = BytesIO(file.read())
mp3 = base64.b64encode(mp3bytes.getvalue()).decode("ISO-8859-1")

model_payload = {"mp3BytesString": mp3}

out = banana.run(api_key, model_key, model_payload)
print(out)



