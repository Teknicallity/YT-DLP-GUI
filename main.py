"""
Copyright (c) 2023, Joshua Sheputa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
import os.path

import PySimpleGUI as sg
from video_listing import VideoListing
from os import getcwd

if __name__ == '__main__':

    menubar_def = [
        ['File', ['Command1', 'Command2']],
        ['Options', ['Command3']]
    ]

    queued_video_entries = []

    queue_tab_layout = [
        [sg.Text('Search:'), sg.In(key='-QUEUE_SEARCH_INPUT-', enable_events=True)],
        [sg.Frame('', [

            [sg.Listbox(queued_video_entries, size=(30, 30), key='-QUEUE_LISTBOX-',
                        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True),
             sg.Column([
                 [sg.Frame('', [
                     [sg.Image('', key='-QUEUE_THUMBNAIL_IMAGE-', size=(640, 360), expand_x=False, expand_y=False,
                               pad=(0, 0))]
                 ], pad=(5, 5), size=(640, 360))],
                 [sg.Button(button_text='Download', key='-DOWNLOAD-'),
                  sg.Button(button_text='Delete', key='-QUEUE_DELETE-')]
             ], element_justification='c')]

        ], pad=(5, 0))],
        [sg.Text('Youtube URL:', pad=((5, 0), 3)),
         sg.Input(key='-URL_INPUT-', size=(35, 1), pad=(0, 3), do_not_clear=False),
         sg.Button(button_text='Add', key='-YT_URL_ADD-', bind_return_key=True, pad=((5, 20), 0)),
         sg.Text('Save to:', pad=((5, 0), 3)), sg.Input(size=(35, 1), key='-FOLDER-', enable_events=True, pad=(0, 3)),
         sg.FolderBrowse('Browse', target='-FOLDER-', initial_folder='./videos')],
        [sg.Text('', size=(35, 1), key='-RESPONSE_TO_URL_INPUT-'), sg.Push(),
         sg.Button(button_text='Download All', key='-DOWNLOAD_ALL-')],
        [sg.Button(button_text='test1'), sg.Button(button_text='test2'), sg.Button(button_text='test3')]  # remove tests
    ]

    downloaded_video_entries = []

    downloaded_tab_layout = [
        [sg.Text('Search:'), sg.In(key='-DOWNLOAD_SEARCH_INPUT-', enable_events=True)],
        [sg.Frame('', [
            [sg.Listbox(downloaded_video_entries, size=(30, 30), key='-DOWNLOAD_LISTBOX-',
                        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True),
             sg.Column([
                 [sg.Frame('',
                           [[sg.Image('', key='-DOWNLOAD_THUMBNAIL_IMAGE-', size=(640, 360), pad=(0, 0))]],
                           pad=(5, 5), size=(640, 360))],
                 [sg.Button(button_text='Play', key='-PLAY_VIDEO-'),
                  sg.Button(button_text='Delete', key='-DOWNLOAD_DELETE-')]
             ], element_justification='c')]

        ], pad=(5, 0))],
    ]

    tab_group_layout = [[
        sg.Tab('Queue', queue_tab_layout, key='-QUEUE_TAB-'),
        sg.Tab('Downloaded', downloaded_tab_layout, key='-DOWNLOADED_TAB-')
    ]]

    main_layout = [
        # [sg.MenubarCustom(menubar_def, tearoff=False)],
        [sg.TabGroup(tab_group_layout)]
    ]

    window = sg.Window('Title', main_layout, size=(800, 800))

    is_something_queued_selected = False
    is_something_downloaded_selected = False

    download_wait_message = "Downloading\nPlease Wait"
    auto_close_time = 1.5
    download_path = ''


    def update_download_path():
        global download_path
        if values['-FOLDER-'] == '':
            cwd = getcwd()
            print("CWD", cwd)
            raw_download_path = os.path.join(cwd, 'videos')
            download_path = os.path.normpath(raw_download_path)
        else:
            download_path = values['-FOLDER-']
            print(download_path)


    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            break

        # add video from url button
        if event == '-YT_URL_ADD-' and values['-URL_INPUT-'] != '':
            url_input: str = values['-URL_INPUT-']
            base_youtube_url = 'youtube.com/watch?v='
            if base_youtube_url in url_input:
                # url valid, youtube api to get info
                # video_entry = VideoListing(url_input)
                video_id = url_input.split('v=')[1]
                queued_video_entries.append(VideoListing(video_id))
                print(queued_video_entries)
                window['-QUEUE_LISTBOX-'].update(queued_video_entries)
                window['-RESPONSE_TO_URL_INPUT-'].update('Added video to queue')

            else:
                window['-RESPONSE_TO_URL_INPUT-'].update('Please provide a valid youtube video URL!')

        # queue listbox selection
        elif event == '-QUEUE_LISTBOX-':
            selection = values['-QUEUE_LISTBOX-']  # get selection
            if selection:  # makes sure the selection is not empty
                is_something_queued_selected = True
                entry: VideoListing = selection[0]
                # print(f'this: {entry}')  # video object to string
                window['-QUEUE_THUMBNAIL_IMAGE-'].update(entry.thumbnail_data)

        # delete queued video given something exists and is selected
        elif event == '-QUEUE_DELETE-' and queued_video_entries and is_something_queued_selected:
            queued_video_entries.remove(entry)
            window['-QUEUE_THUMBNAIL_IMAGE-'].update('', size=(640, 360))

        # downloads queued video given something exists and is selected
        elif event == '-DOWNLOAD-' and queued_video_entries and is_something_queued_selected:
            update_download_path()
            downloaded_video_entries.append(entry)
            queued_video_entries.remove(entry)
            # self-closing download indicated
            sg.popup_timed(download_wait_message, auto_close_duration=auto_close_time, non_blocking=True)
            window['-QUEUE_THUMBNAIL_IMAGE-'].update('', size=(640, 360))
            entry.download_to(download_path)

        # downloads queued video given something exists
        elif event == '-DOWNLOAD_ALL-' and queued_video_entries:
            print('Starting Download All')
            update_download_path()
            temp_queued_list = queued_video_entries.copy()
            # self-closing download indicated
            sg.popup_timed(download_wait_message, auto_close_duration=auto_close_time * len(queued_video_entries),
                           non_blocking=True)
            for video in temp_queued_list:
                downloaded_video_entries.append(video)
                window['-QUEUE_THUMBNAIL_IMAGE-'].update('', size=(640, 360))
                queued_video_entries.remove(video)
                video.download_to(download_path)
            # close sg.popup

        # download listbox selection
        elif event == '-DOWNLOAD_LISTBOX-':
            selection = values['-DOWNLOAD_LISTBOX-']
            # print(selection)  # video object
            if selection:  # makes sure the selection is not empty
                is_something_downloaded_selected = True
                entry: VideoListing = selection[0]
                # print(f'this: {entry}')  # video object to string
                window['-DOWNLOAD_THUMBNAIL_IMAGE-'].update(entry.thumbnail_data)

        # play downloaded video given something exists and is selected
        elif event == '-PLAY_VIDEO-' and downloaded_video_entries and is_something_downloaded_selected:
            entry.play_video()

        # delete downloaded video given something exists and is selected
        elif event == '-DOWNLOAD_DELETE-' and downloaded_video_entries and is_something_downloaded_selected:
            entry.delete_video()
            downloaded_video_entries.remove(entry)
            window['-DOWNLOAD_THUMBNAIL_IMAGE-'].update('', size=(640, 360))


        # tests. remove
        elif event == 'test1':
            window['-URL_INPUT-'].update('https://www.youtube.com/watch?v=UAdwUWhfZmM')
        elif event == 'test2':
            window['-URL_INPUT-'].update('https://www.youtube.com/watch?v=SP1XDSBU4qk')
        elif event == 'test3':
            window['-URL_INPUT-'].update('https://www.youtube.com/watch?v=AXcSyPETFBw')

        # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Listbox_Search_Filter.py
        if values['-QUEUE_SEARCH_INPUT-'] != '':
            queued_search_query = values['-QUEUE_SEARCH_INPUT-'].lower()
            # search_query = search_query.lower()
            queued_search_response = [entry for entry in queued_video_entries if queued_search_query in entry.lower()]
            window['-QUEUE_LISTBOX-'].update(queued_search_response)
        else:
            window['-QUEUE_LISTBOX-'].update(queued_video_entries)

        if values['-DOWNLOAD_SEARCH_INPUT-'] != '':
            downloaded_search_query = values['-DOWNLOAD_SEARCH_INPUT-'].lower()
            # search_query = search_query.lower()
            downloaded_search_response = [entry for entry in downloaded_video_entries if
                                          downloaded_search_query in entry.lower()]
            window['-DOWNLOAD_LISTBOX-'].update(downloaded_search_response)
        else:
            window['-DOWNLOAD_LISTBOX-'].update(downloaded_video_entries)

    window.close()
