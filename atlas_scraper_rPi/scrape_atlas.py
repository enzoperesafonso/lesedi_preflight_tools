#!/usr/bin/env python3
""" 
@Author Enzo Peres Afonso 

A quick script to pull ATLAS allsky camera images from http://dashboard.fallingstar.com/dash/sth.html
and note the reported cloud cover. Ran as a crontab job on a raspberry Pi everyday at 16:00 (UCT+2) to obtain a small
dataset of allsky images at the time of Lesedi's Preflight. Images are saved into directories based on the percentage cloud 
cover reported at the time of scraping. Files are saved with the current local civil time and the reported cloud cover in parenthesis
"""

import requests
import datetime
import os
import atlas_scraper_rPi.check_reported_weather as check_reported_weather

ATLAS_STH_ALLSKY_URL = "https://www.fallingstar.com/weather/sth/latest_clr400.jpg"

current_date_and_time = datetime.datetime.now()


def download_allsky_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            reported_cloud_cover = check_reported_weather.get_predicted_cloud_cover()

            if reported_cloud_cover > 10:
                os.makedirs("cloudy", exist_ok=True)
                save_path = os.path.join(
                    "cloudy",
                    "{} ({}).jpg".format(current_date_and_time, reported_cloud_cover),
                )
            else:
                os.makedirs("clear", exist_ok=True)
                save_path = os.path.join(
                    "clear",
                    "{} ({}).jpg".format(current_date_and_time, reported_cloud_cover),
                )

            with open(save_path, "wb") as f:
                f.write(response.content)
            print("{} Image downloaded successfully".format(current_date_and_time))
        else:
            print("Failed to download image: Status code", response.status_code)
    except Exception as e:
        print("Error occurred while downloading image:", str(e))


download_allsky_image(ATLAS_STH_ALLSKY_URL)
