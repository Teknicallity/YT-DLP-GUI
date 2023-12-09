# Simple YT-DLP GUI

### Description:
This project is a GUI application built using PySimpleGUI that allows users to download YouTube videos using the yt-dlp library. The application features two tabs - "Queue" for managing the download queue and "Downloaded" for viewing and playing downloaded videos.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Limitations](#limitations)
- [Screenshots](#screenshots)

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
- Queue Management: Add, download, and delete videos from the download queue.
- Download All: Download all videos in the queue with a single click.
- Play and Delete: Play a video with the system's default video player or delete video file.
- Thumbnail Display: Thumbnails of selected videos are displayed.
- Search Functionality: Search through the queue and downloaded videos.

## Limitations
- No current database functionality, meaning no session-to-session saved videos. Video files remain on the disk

## Screenshots
### Queue Tab
![Main Queue Tab](/assets/screenshots/queue_tab.png)

*Caption: The primary tab, which functions as a queue for added videos before download*

### Download Tab
![Download Tab](/assets/screenshots/download_tab.png)

*Caption: The downloaded videos tab where you can play or delete a downloaded video*
