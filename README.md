# Simple YT-DLP GUI

### Description:
This project is a GUI application built using PySimpleGUI that allows users to download YouTube videos using the yt-dlp library. The application features two tabs - "Queue" for managing the download queue and "Downloaded" for viewing and playing downloaded videos.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation
1. Make sure you have Python 3
2. In the console, "pip install PySimpleGUI yt-dlp Pillow cloudscraper"
3. Change the api key in config.ini with your own from [YouTube API v3](https://developers.google.com/youtube/v3)
4. Run main.py

## Usage
Open the application and navigate between the "Queue" and "Downloaded" tabs.
To add a video to the queue, enter a valid YouTube video URL in the input field and click the "Add" button.
Manage the queue using the listbox and the provided buttons (Download, Delete).
Download all videos in the queue by clicking the "Download All" button.
Play or delete downloaded videos in the "Downloaded" tab.

## Features
Queue Management: Add, download, and delete videos from the download queue.
Download All: Download all videos in the queue with a single click.
Play and Delete: Play and delete downloaded videos.
Thumbnail Display: Thumbnails of selected videos are displayed.
Search Functionality: Search through the queue and downloaded videos.