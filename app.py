from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from db_app import Users1
from db_app import db
from db_app import app

refreshTokenURL = os.environ['REFRESH_TOKEN_URL']
client_id = os.environ['CLIENT_BASE64_ENCODED']
redirect_uri = os.environ['REDIRECT_URL']
spotify_api_url = os.environ['SPOTIFY_API_URL']
spotify_current_playing_url = os.environ['SPOTIFY_CURRENT_PLAYING_URL']
spotify_recently_played_url = os.environ['SPOTIFY_RECENTLY_PLAYED_URL']

@app.route('/', methods=['POST']) 
def login():
    content = request.get_json()
    code = content["code"]
    latitude = content["latitude"]
    longitude = content["longitude"]
    import requests

    # Get access_token and refresh_token using authorization_code
    headers = {
        'Authorization': 'Basic '+ client_id,
    }
    data = {
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': redirect_uri
    }
    response = requests.post(spotify_api_url, headers=headers, data=data)
    token_json = response.json()
    token = token_json["access_token"]
    refresh_token = token_json["refresh_token"]

    # Get user profile details using access_token

    headers = {
        'Authorization': 'Bearer '+ token,
    }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_data_json = response.json()
    user_id = user_data_json["id"]

    # Remove user if already present in Databse
    user = Users1.query.filter_by(userid=user_id).first()
    if user is not None:
        Users1.query.filter_by(userid=user_id).delete()
        db.session.commit()
    new_user = Users1(userid = user_id, refreshtoken = refresh_token, latitude = latitude, longitude = longitude, city = "Tokyo")
    db.session.add(new_user)
    db.session.commit()

    # Get refresh token for all users and use them to get new token
    users = Users1.query.all()
    user_names = []
    song_names = []
    song_urls = []
    album_urls = []
    for user in users:
        
        # Refresh access token
        user_refresh_token = user.refreshtoken

        headers = {
            'Authorization': 'Basic ' + client_id,
        }

        data = {
          'grant_type': 'refresh_token',
          'refresh_token': user_refresh_token 
        }

        # Get personal info
        response = requests.post(spotify_api_url, headers=headers, data=data)
        if (response.status_code == 200):
            refreshed_token_json = response.json()
            new_access_token = refreshed_token_json["access_token"]
            # print(new_access_token)
            headers = {
                'Authorization': 'Bearer '+ new_access_token,
            }
            response = requests.get('https://api.spotify.com/v1/me', headers=headers)
            personal_info_json = response.json()
            user_name = personal_info_json["display_name"]
            
            # Get current playing 
            headers = {
                'Authorization': 'Bearer ' + new_access_token,
            }
            response = requests.get(spotify_current_playing_url, headers=headers)
            song_name = ""
            song_url = ""
            album_url = ""
            # Get current playing
            if (response.status_code == 200):
                current_playing_json = response.json()
                print(current_playing_json)
                song_name = current_playing_json["item"]["name"]
                song_url = current_playing_json["item"]["uri"]
                album_url = current_playing_json["item"]["album"]["images"][-1]["url"]
            # Get recetly played
            else:
                headers = {
                    'Authorization': 'Bearer ' + new_access_token,
                }

                response = requests.get(spotify_recently_played_url, headers=headers)
                if (response.status_code == 200):
                    recently_played_json = response.json()
                    # print(recently_played_json)
                    song_name = recently_played_json["items"][0]["track"]["name"]
                    song_url = recently_played_json["items"][0]["track"]["uri"]
                    album_url = recently_played_json["items"][0]["track"]["album"]["images"][-2]["url"]
            user_names.append(user_name)
            song_names.append(song_name)
            song_urls.append(song_url)
            album_urls.append(album_url)        
    # print(user_names)
    # print(song_names)
    # print(song_urls)
    return_json = {"users" : user_names, "song_names" : song_names, "song_urls" : song_urls, "album_urls" : album_urls}
    return return_json
