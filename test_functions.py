import PySimpleGUI as sg


def add_video(lis):
    video = [sg.Image('test_thumbnail.png', size=(128, 72)), sg.Column(
        [[sg.Text('Video Title', font=12, pad=(5, 0))], [sg.Text('Channel', pad=(5, 0))],
         [sg.Text('10:01', pad=(5, 0))]])]
    lis.append(video)
    # return lis


def add_text_video(target_list):
    i=0