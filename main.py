import PySimpleGUI as sg
from video_listing import VideoListing

if __name__ == '__main__':

    menubar_def = [
        ['File', ['Command1', 'Command2']],
        ['Options', ['Command3']]
    ]

    queued_video_entries = []

    video_entry_def = [sg.Image('test_thumbnail.png', size=(128, 72)), sg.Column(
        [[sg.Text('Video Title', font=12, pad=(5, 0))], [sg.Text('Channel', pad=(5, 0))],
         [sg.Text('10:01', pad=(5, 0))]])]
    video_entry_def1 = [sg.Image('test_thumbnail.png', size=(128, 72)), sg.Column(
        [[sg.Text('Video Title1', font=12, pad=(5, 0))], [sg.Text('ChannelName', pad=(5, 0))],
         [sg.Text('4:02', pad=(5, 0))]])]

    # queued_video_entry.append(video_entry_def)
    # queued_video_entry.append(video_entry_def1)

    queue_tab_layout = [
        [sg.Text('Search:'), sg.In(key='-QUEUE_SEARCH_INPUT-', enable_events=True)],
        [sg.Frame('', [

            # [sg.Listbox(queued_video_entries, key='-QUEUED_VIDEOS-', size=(25, 25), pad=(0, 0))]], pad=(5, 0)),
            [sg.Listbox(queued_video_entries, size=(30, 30), key='-QUEUE_LISTBOX-'),
             sg.Column([
                 [sg.Frame('', [[sg.Image('', key='-THUMBNAIL_IMAGE', size=(640, 360), pad=(0, 0))]], pad=(5, 5))],
                 [sg.Button(button_text='Download'), sg.Button(button_text='Delete')]
             ], element_justification='c')]

        ], pad=(5, 0))],
        [sg.Text('Youtube URL:', pad=((5, 0), 3)),
         sg.Input(key='-URL_INPUT-', size=(35, 1), pad=(0, 3), do_not_clear=False),
         sg.Button(button_text='Add', key='-YT_URL_ADD-', bind_return_key=True, pad=((5, 20), 0)),
         sg.Text('Save to:', pad=((5, 0), 3)), sg.Input(size=(35, 1), key='-FOLDER-', pad=(0, 3)),
         sg.FolderBrowse('Browse')],
        [sg.Text('', size=(35, 1), key='-RESPONSE_TO_URL_INPUT-'),
         sg.Checkbox(text='test', pad=((5,300),3)), sg.Button(button_text='Download All', key='-DOWNLOAD_ALL-')],
        [sg.Button(button_text='test1'), sg.Button(button_text='test2'), sg.Button(button_text='test3')] # remove tests
    ]

    downloaded_video_entries = []

    downloaded_tab_layout = [
        [sg.Text('Search:'), sg.In(key='-DOWNLOAD_SEARCH_INPUT-', enable_events=True)],
        [sg.Frame('', [
            [sg.Listbox(downloaded_video_entries, size=(30, 30), key='-DOWNLOAD_LISTBOX-'),
             sg.Column([
                 [sg.Frame('', [[sg.Image('test_thumbnail.png', key='-THUMBNAIL_IMAGE', size=(640, 360), pad=(0, 0))]], pad=(5, 5))],
                 [sg.Button(button_text='Play'), sg.Button(button_text='Delete')]
             ], element_justification='c')]

        ], pad=(5, 0))],
    ]

    tab_group_layout = [[
        sg.Tab('Queue', queue_tab_layout, key='-QUEUE_TAB-'),
        sg.Tab('Downloaded', downloaded_tab_layout, key='-DOWNLOADED_TAB-')
    ]]

    main_layout = [
        [sg.MenubarCustom(menubar_def, tearoff=False)],
        [sg.TabGroup(tab_group_layout)]
    ]

    window = sg.Window('Title', main_layout, size=(800, 800))

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == '-YT_URL_ADD-' and values['-URL_INPUT-'] != '':
            url_input = values['-URL_INPUT-']
            base_youtube_url = 'www.youtube.com/watch?v='
            if base_youtube_url in url_input:
                #url valid, youtube api to get info
                # video_entry = VideoListing(url_input)
                queued_video_entries.append(VideoListing(url_input))
                window['-RESPONSE_TO_URL_INPUT-'].update('Added video to queue')
                print(queued_video_entries)

                window['-QUEUE_LISTBOX-'].update(queued_video_entries)

            else:
                window['-RESPONSE_TO_URL_INPUT-'].update('Please provide a valid youtube video URL!')

        #tests. remove
        if event == 'test1':
            window['-URL_INPUT-'].update('https://www.youtube.com/watch?v=UAdwUWhfZmM')
        if event == 'test2':
            window['-URL_INPUT-'].update('https://www.youtube.com/watch?v=SP1XDSBU4qk')
        if event == 'test3':
            window['-URL_INPUT-'].update('https://www.youtube.com/watch?v=AXcSyPETFBw')


        if values['-QUEUE_SEARCH_INPUT-'] != '':
            search_query = values['-QUEUE_SEARCH_INPUT-'].lower()
            # search_query = search_query.lower()
            search_response = [entry for entry in queued_video_entries if search_query in entry.lower()]
            window['-QUEUE_LISTBOX-'].update(search_response)
        else:
            window['-QUEUE_LISTBOX-'].update(queued_video_entries)

            #window[]

    window.close()

    #already in running while loop
    def is_valid_url(url):
        base_youtube_url = 'www.youtube.com/watch?v='
        return base_youtube_url in url