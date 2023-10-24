import PySimpleGUI as sg


def add_video(lis):
    lis.append(video)


video = [sg.Image('test_thumbnail.png', size=(128, 72)), sg.Column(
    [[sg.Text('Video Title', font=12, pad=(5, 0))], [sg.Text('Channel', pad=(5, 0))],
     [sg.Text('10:01', pad=(5, 0))]])]
