import PySimpleGUI as sg
import test_functions

if __name__ == '__main__':

    menubar_def = [
        ['File', ['Command1', 'Command2']],
        ['Options', ['Command3']]
    ]

    queued_video_entry = []

    video_entry_def = [sg.Image('test_thumbnail.png', size=(128, 72)), sg.Column(
        [[sg.Text('Video Title', font=12, pad=(5, 0))], [sg.Text('Channel', pad=(5, 0))],
         [sg.Text('10:01', pad=(5, 0))]])]
    video_entry_def1 = [sg.Image('test_thumbnail.png', size=(128, 72)), sg.Column(
        [[sg.Text('Video Title1', font=12, pad=(5, 0))], [sg.Text('ChannelName', pad=(5, 0))],
         [sg.Text('4:02', pad=(5, 0))]])]


    queue_tab_layout = [
        [sg.Text('Search:'), sg.In(key='-QUEUE_SEARCH_INPUT-', enable_events=True)],
        [sg.Frame('', [[sg.Column(queued_video_entry, key='-QUEUE_VIDEO_COLUMN-', scrollable=True, vertical_scroll_only=True,
                                  element_justification='C', size=(800, 500), background_color='#335267', pad=(0, 0))]],
                  pad=(5, 0))],
        # [sg.Column([[sg.Frame('', [video_entry_def])]], scrollable=True, vertical_scroll_only=True, element_justification='center', size=(800, 500))],
        [sg.Text('Youtube URL:', pad=((5, 0), 3)), sg.Input(key='-SEARCHINPUT-', size=(35, 1), pad=(0, 3)),
         sg.Button(button_text='Add', key='-YT_URL_ADD-', bind_return_key=True, pad=((5, 20), 0)),
         sg.Text('Save to:', pad=((5, 0), 3)), sg.Input(size=(35, 1), key='-FOLDER-', pad=(0, 3)),
         sg.FolderBrowse('Browse')],
        [sg.Checkbox(text='test')]
    ]

    downloaded_video_entry = []

    downloaded_tab_layout = [
        [sg.Text('Search:'), sg.In(key='-DOWNLOAD_SEARCH_INPUT-', enable_events=True)],
        [sg.Frame('', [[sg.Column(downloaded_video_entry, scrollable=True, vertical_scroll_only=True,
                                  element_justification='C', size=(800, 500), background_color='#335267', pad=(0, 0))]],
                  pad=(5, 0))],
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
        if event ==  '-YT_URL_ADD-':
            # test_functions.add_video(queued_video_entry)
            # queued_video_entry.append(video_entry_def)
            # print(queued_video_entry)
            # window.refresh()
            window['-QUEUE_VIDEO_COLUMN-'].update(visible=False)
            queued_video_entry.append(video_entry_def)
            window['-QUEUE_VIDEO_COLUMN-'].update(visible=True)



    window.close()
