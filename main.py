import PySimpleGUI as sg
import test_functions
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
            # [sg.Column(queued_video_entry, key='-QUEUE_VIDEO_COLUMN-', scrollable=True, vertical_scroll_only=True,
            #            size=(800, 500), background_color='#335267', pad=(0, 0))]

            # [sg.Listbox(queued_video_entries, key='-QUEUED_VIDEOS-', size=(25, 25), pad=(0, 0))]], pad=(5, 0)),
            [sg.Listbox(queued_video_entries, size=(30, 30), key='-QUEUE_LISTBOX-'),
             sg.Column([
                 [sg.Image('test_thumbnail.png', key='-THUMBNAIL_IMAGE', size=(640, 360))],
                 [sg.Button(button_text='Play'), sg.Button(button_text='Delete')]
             ], element_justification='c')]

        ], pad=(5, 0))],
        [sg.Text('Youtube URL:', pad=((5, 0), 3)),
         sg.Input(key='-SEARCHINPUT-', size=(35, 1), pad=(0, 3), do_not_clear=False),
         sg.Button(button_text='Add', key='-YT_URL_ADD-', bind_return_key=True, pad=((5, 20), 0)),
         sg.Text('Save to:', pad=((5, 0), 3)), sg.Input(size=(35, 1), key='-FOLDER-', pad=(0, 3)),
         sg.FolderBrowse('Browse')],
        [sg.Text('', size=(30, 1), key='-RESPONSE_TO_URL_INPUT-'), sg.Checkbox(text='test', pad=((5,380),3)), sg.Button(button_text='Download')]
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
        if event == '-YT_URL_ADD-' and values['-SEARCHINPUT-'] != '':
            url_input = values['-SEARCHINPUT-']
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


        if values['-QUEUE_SEARCH_INPUT-'] != '':
            search_query = values['-QUEUE_SEARCH_INPUT-']

            #window[]

    window.close()

    def is_valid_url(url):
        base_youtube_url = 'www.youtube.com/watch?v='
        return base_youtube_url in url