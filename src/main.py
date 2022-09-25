from os.path import exists
from os import mkdir as dir
from config import *
from .fltk import *
from lang import *
import PySimpleGUI as sg
from random import choice
from pathlib import Path
from timeit import default_timer as timer


# Main class representing Image
class Image:
    def __init__(self):

        self.path = None    # Path to image, pathlib.Path value
        self.name = None    # Name of the image, str value
        self.format = None  # Image format, str value, one of P1, P2, P3, P4, P5, P6
        self.width = None   # Image width, int value
        self.height = None  # Image height, int value
        self.depth = None   # Color depth, int value or None
        self.data = None    # Image data value, bytes or list of int values

    def open(self, path: Path):

        '''
        :param path: pathlib.Path file
        :return: None
        '''

        self.path = path
        self.name = self.path.name[:-4]
        self.data = list()

        data = open(self.path, 'rb').read()

        if data.isascii():  # File is ASCII, clean from comments

            data_, data = data.decode('ascii').splitlines(), list()

            for line in data_:
                line = line.split('#')[0]
                if line:
                    data.append(line)

            self.format = data[0]
            self.width, self.height = [int(value) for value in data[1].split()]
            if self.format not in ('P1', 'P4'):
                self.depth = int(data[2])
                data.pop(0)
            data.pop(0)
            data.pop(0)

            data = ' '.join(data).strip().split()

        else:   # File is Binary
            data_ = list()
            start, stop = 0, 0
            for num, value in enumerate(data):
                if value == 10 or value == 13 or value == 32:
                    stop = num
                    line = data[start: stop]
                    start = num + 1
                    if line:
                        data_.append(line)
                    if data_:
                        val = line.decode('ascii')
                        if (not self.format) and (val in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')):
                            self.format = val
                        elif self.format and (not self.width) and check_for_convert(val):
                            self.width = int(val)
                        elif self.width and (not self.height) and check_for_convert(val):
                            self.height = int(val)
                            if self.format in ('P1', 'P4'):
                                break
                        elif self.height and (not self.depth) and (
                                self.format not in ('P1', 'P4')) and check_for_convert(val):
                            self.depth = int(val)
                            break

            data_.append(data[start:])
            data, data_ = data_[-1], None

            data = self.decode(data)

        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x

                if self.format in ('P1', 'P4'):
                    r = g = b = abs(int(data[index])-1) * 255
                elif self.format in ('P2', 'P5'):
                    r = g = b = round(int(data[index]) * 255 / self.depth)
                elif self.format in ('P3', 'P6'):
                    r, g, b = [round(int(value) * 255 / self.depth) for value in data[3 * index : 3 * index + 3]]
                self.data.append(rgb2hex((r, g, b)))

    def decode(self, data):

        '''
        :param data: list
        :return: data: list
        '''

        data_ = list()

        if self.format == 'P4':
            if self.width % 8:
                cur = (self.width // 8 + 1) * 8
            else:
                cur = self.width
            for num, value in enumerate(data):
                bit = list()
                val = value
                for i in range(8):
                    if (num * 8 + i) % cur < self.width:
                        if not value % 2:
                            bit.append(0)
                        else:
                            bit.append(1)
                        value = value // 2
                for tup in bit[::-1]:
                    data_.append(tup)

        elif self.format == 'P5' or self.format == 'P6':

            depth = self.depth
            bits = 1
            while depth > 255:
                depth /= 255
                bits += 1

            for num, value in enumerate(data):
                if num % bits == 0:
                    value_ = 0
                    for bit in range(bits):
                        value_ = value_ * 255 + data[num + bit]
                    data_.append(value_)

        return data_

    def display(self, window: sg.Window):

        '''
        :param window: sg.Window
        :return: None
        '''

        cree_fenetre(self.width, self.height)
        time = timer()
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x

                point(
                    x=x,
                    y=y,
                    couleur=self.data[index],
                )
            if not OPTIMIZE and not bool(y % round(self.height / 100)):
                mise_a_jour()

        time = timer() - time
        window['-STATUS-'].update(IMAGE_DISPLAYED.format(time=round(time, 2)))
        attend_ev()

        ferme_fenetre()

    def resize(self, width: int, height: int):

        '''
        :param width: int
        :param height: int
        :return: None
        '''

        data = list()
        scale_x = self.width / width
        scale_y = self.height / height
        for y in range(height):
            for x in range(width):
                index = int(y * self.width * scale_y) + int(x * scale_x)
                data.append(self.data[index])

        self.data = data
        self.width = width
        self.height = height

    def convert(self, format: str):

        '''
        :param format: str
        :return: None
        '''

        self.format = format

        if self.format in ('P2', 'P5'):
            for index, value in enumerate(self.data):
                r, g, b = hex2rgb(value)
                avg = round((r + g + b) / 3)
                hex = rgb2hex((avg, avg, avg))
                self.data[index] = hex

        elif self.depth and self.format in ('P1', 'P4'):

            for index, value in enumerate(self.data):
                r, g, b = hex2rgb(value)
                avg = round((r + g + b) / 3)
                bol = int(avg / 128) * 255
                hex = rgb2hex((bol, bol, bol))
                self.data[index] = hex

            self.depth = None

        self.format = format

    def rename(self, name: str):

        '''
        :param name: str
        :return: None
        '''

        self.name = name

    def encode(self, data: list):

        '''
        :param data: list
        :return: data: list
        '''

        data_ = b''

        if self.format == 'P4':
            for line in data:
                it = 0
                for num, value in enumerate(line):
                    if not num % 8 and num != 0:

                        data_ += int(it).to_bytes(1, byteorder='big')
                        it = 0

                    it = it * 2 + int(value)
                if num % 8:
                    while num < 8:
                        it *= 2
                    data_ += int(it).to_bytes(1, byteorder='big')

        else:

            depth = self.depth
            bits = 1
            while depth > 255:
                depth /= 255
                bits += 1

            for line in data:
                for value in line:
                    data_ += int(value).to_bytes(bits, byteorder='little')

        data = data_
        return data

    def save(self):

        '''
        :return: None
        '''

        path = Path(f'{IMAGE_SAVE_DIR}/{self.path}')

        data = list()
        for y in range(self.height):
            line = list()
            for x in range(self.width):
                index = y * self.width + x

                if self.format in ('P1', 'P4'):
                    if hex2rgb(self.data[index])[0]:
                        line.append('0')
                    else:
                        line.append('1')

                elif self.format in ('P2', 'P5'):
                    val = f'{round(hex2rgb(self.data[index])[0] * self.depth / 255)}'
                    line.append(val)

                elif self.format in ('P3', 'P6'):
                    r, g, b = hex2rgb(self.data[index])
                    line.append(str(round(r * self.depth / 255)))
                    line.append(str(round(g * self.depth / 255)))
                    line.append(str(round(b * self.depth / 255)))

            data.append(line)

        with open(path, 'w', encoding='ascii') as file:
            if self.depth:
                file.write(f'{self.format}\n{self.width} {self.height}\n{self.depth}\n')
            else:
                file.write(f'{self.format}\n{self.width} {self.height}\n')

        if self.format in ('P4', 'P5', 'P6'):   # Check if file is Binary

            data = self.encode(data)

            with open(path, 'ab') as file:
                file.write(data)

        else:
            with open(path, 'a', encoding='ascii') as file:
                data_, data = data, list()
                for line in data_:
                    line_ = ' '.join(line).strip()
                    data.append(line_)

                for line in data:
                    print(line)
                    file.write(f'{line}\n')

def main(theme='DefaultNoMoreNagging'):

    sg.theme(theme)

    image = None

    layout = [
        [
            sg.Input(
                key='-BROWSE-',
                visible=False,
                enable_events=True
            ),
            sg.FileBrowse(
                target='-BROWSE-',
                key='-BROWSE-FILE-',
                file_types=(('PNM images', ('*.pnm', '*.pbm', '*.pgm', '*.ppm')),)
            )
        ],
        [
            sg.Text(
                text=STATUS,
                size=10
            ),
            sg.Text(
                text=WELCOME,
                key='-STATUS-'
            )
        ],
        [
            sg.Text(
                text=NAME,
                size=10
            ),
            sg.InputText(
                key='-RENAME-VALUE-',
                visible=False
            ),
            sg.OK(
                key='-RENAME-OK-',
                visible=False
            ),
            sg.Text(
                key='-NAME-'
            )
        ],
        [
            sg.Text(
                text=FORMAT,
                size=10
            ),
            sg.Listbox(
                values=('P1', 'P2', 'P3', 'P4', 'P5', 'P6'),
                default_values=['P1'],
                key='-CONVERT-VALUE-',
                size=(2, 3),
                visible=False
            ),
            sg.OK(
                key='-CONVERT-OK-',
                visible=False
            ),
            sg.Text(
                key='-FORMAT-'
            )
        ],
        [
            sg.Text(
                text=WIDTH,
                size=10
            ),
            sg.InputText(
                key='-WIDTH-VALUE-',
                visible=False
            ),
            sg.OK(
                key='-WIDTH-OK-',
                visible=False
            ),
            sg.Text(
                key='-WIDTH-'
            )
        ],
        [
            sg.Text(
                text=HEIGHT,
                size=10
            ),
            sg.InputText(
                key='-HEIGHT-VALUE-',
                visible=False
            ),
            sg.OK(
                key='-HEIGHT-OK-',
                visible=False
            ),
            sg.Text(
                key='-HEIGHT-'
            )
        ],
        [
            sg.Text(
                text=DEPTH,
                size=10
            ),
            sg.Text(
                key='-DEPTH-'
            )
        ],
        [
            sg.Button(
                button_text=DISPLAY,
                key='-DISPLAY-',
                disabled=True
            ),
            sg.Button(
                button_text=RENAME,
                key='-RENAME-',
                disabled=True
            ),
            sg.Button(
                button_text=RESIZE,
                key='-RESIZE-',
                disabled=True
            ),
            sg.Button(
                button_text=CONVERT,
                key='-CONVERT-',
                disabled=True
            ),
            sg.Button(
                button_text=SAVE,
                key='-SAVE-',
                disabled=True
            )
        ],
        [
            sg.Text(
                text=CURRENT_THEME
            ),
            sg.Text(
                key='-CURRENT-THEME-'
            ),
            sg.Button(
                button_text=SWITCH_THEME,
                key='-THEME-'
            ),
            sg.Button(
                button_text=EXIT,
                key='-EXIT-'
            )
        ],
    ]

    window = sg.Window(PNM_VIEWER, layout=layout, icon='icon.ico', font=('Comic Sans', 12), resizable=True)

    while True:

        event, values = window.read()
        print(event, values)

        if event == '-BROWSE-':

            window['-STATUS-'].update(IMAGE_OPENING)

            image = Image()

            try:
                time = timer()
                image.open(path=Path(values['-BROWSE-']))

                window['-NAME-'].update(image.name)
                window['-FORMAT-'].update(image.format)
                window['-WIDTH-'].update(image.width)
                window['-HEIGHT-'].update(image.height)
                window['-DEPTH-'].update(image.depth)
                enable_buttons(window)

                time = round(timer() - time, 2)
                window['-STATUS-'].update(IMAGE_OPENED.format(time=time))

            except ValueError:
                window['-STATUS-'].update(FORMAT_UNKNOWN)
                window['-NAME-'].update()
                window['-FORMAT-'].update()
                window['-WIDTH-'].update()
                window['-HEIGHT-'].update()
                window['-DEPTH-'].update()
                disable_buttons(window)

        if event == '-DISPLAY-':
            window['-STATUS-'].update(IMAGE_DISPLAYING)
            disable_buttons(window)

            image.display(window)

            enable_buttons(window)

        if event == '-RENAME-':
            disable_buttons(window)
            window['-NAME-'].update(visible=False)
            window['-RENAME-VALUE-'].update(image.name, visible=True)
            window['-RENAME-OK-'].update(visible=True)

        if event == '-RENAME-OK-':
            time = timer()

            window['-STATUS-'].update(IMAGE_RENAMING)

            image.rename(values['-RENAME-VALUE-'])

            window['-NAME-'].update(image.name, visible=True)
            window['-RENAME-VALUE-'].update(visible=False)
            window['-RENAME-OK-'].update(visible=False)
            enable_buttons(window)

            time = round(timer() - time, 2)
            window['-STATUS-'].update(IMAGE_RENAMED.format(time=time))

        if event == '-RESIZE-':

            disable_buttons(window)
            window['-WIDTH-'].update(visible=False)
            window['-HEIGHT-'].update(visible=False)
            window['-WIDTH-VALUE-'].update(image.width, visible=True)
            window['-HEIGHT-VALUE-'].update(image.height, visible=True)
            window['-WIDTH-OK-'].update(visible=True)
            window['-HEIGHT-OK-'].update(visible=True)

        if event == '-WIDTH-OK-' or event == '-HEIGHT-OK-':
            time = timer()

            width, height = values['-WIDTH-VALUE-'], values['-HEIGHT-VALUE-']
            if not (check_for_convert(width) and check_for_convert(height)):
                window['-STATUS-'].update(RESIZE_FAILED)
                continue
            else:
                width, height = int(width), int(height)

            window['-STATUS-'].update(IMAGE_RESIZING)

            image.resize(width, height)

            window['-WIDTH-'].update(f'{image.width}', visible=True)
            window['-HEIGHT-'].update(f'{image.height}', visible=True)
            window['-WIDTH-VALUE-'].update(image.width, visible=False)
            window['-HEIGHT-VALUE-'].update(image.height, visible=False)
            window['-WIDTH-OK-'].update(visible=False)
            window['-HEIGHT-OK-'].update(visible=False)
            enable_buttons(window)

            time = round(timer() - time, 2)
            window['-STATUS-'].update(IMAGE_RESIZED.format(time=time))

        if event == '-CONVERT-':
            disable_buttons(window)
            window['-FORMAT-'].update(visible=False)
            window['-CONVERT-VALUE-'].update(visible=True)
            window['-CONVERT-OK-'].update(visible=True)

        if event == '-CONVERT-OK-':

            window['-STATUS-'].update(IMAGE_CONVERTING)
            time = timer()

            image.convert(values['-CONVERT-VALUE-'][0])
            window['-FORMAT-'].update(image.format, visible=True)
            window['-CONVERT-VALUE-'].update(visible=False)
            window['-CONVERT-OK-'].update(visible=False)
            enable_buttons(window)

            time = round(timer() - time, 2)
            window['-STATUS-'].update(IMAGE_CONVERTED.format(time=time))

        if event == '-SAVE-':

            if not exists(IMAGE_SAVE_DIR):
                dir(IMAGE_SAVE_DIR)

            if SAVE_PNM:
                image.path = f'{image.name}.pnm'
            elif image.format in ('P1', 'P4'):
                image.path = f'{image.name}.pbm'
            elif image.format in ('P2', 'P5'):
                image.path = f'{image.name}.pgm'
            elif image.format in ('P3', 'P6'):
                image.path = f'{image.name}.ppm'

            if not check_for_save(image.path):
                if sg.popup_yes_no(FILE_EXISTS) == 'Yes':

                    window['-STATUS-'].update(IMAGE_SAVING)
                    disable_buttons(window)

                    time = timer()

                    image.save()

                    enable_buttons(window)
                    time = round(timer() - time, 2)
                    window['-STATUS-'].update(IMAGE_SAVED.format(time=time))

            else:
                window['-STATUS-'].update(IMAGE_SAVING)
                disable_buttons(window)

                time = timer()

                image.save()

                enable_buttons(window)
                time = round(timer() - time, 2)
                window['-STATUS-'].update(IMAGE_SAVED.format(time=time))

        if event == '-THEME-':
            change_theme(window)

        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break

    window.close()


def enable_buttons(window: sg.Window):
    window['-DISPLAY-'].update(disabled=False)
    window['-RENAME-'].update(disabled=False)
    window['-RESIZE-'].update(disabled=False)
    window['-CONVERT-'].update(disabled=False)
    window['-SAVE-'].update(disabled=False)
    window['-BROWSE-FILE-'].update(disabled=False)


def disable_buttons(window: sg.Window):
    window['-DISPLAY-'].update(disabled=True)
    window['-RENAME-'].update(disabled=True)
    window['-RESIZE-'].update(disabled=True)
    window['-CONVERT-'].update(disabled=True)
    window['-SAVE-'].update(disabled=True)
    window['-BROWSE-FILE-'].update(disabled=True)


def change_theme(window: sg.Window):
    theme = choice(sg.theme_list())
    window.close()
    main(theme)


def warning(text: str):
    return sg.popup_error(text)


def check_for_save(path: Path):
    if exists(Path(f'{IMAGE_SAVE_DIR}/{path}')):
        return False
    else:
        return True


def check_for_convert(value: str):
    try:
        value = int(value)
        return True
    except ValueError:
        return False


def rgb2hex(rgb: tuple):
    color = max(rgb)
    bits = 0
    hex = '#'
    while color > 0:
        color = color // 16
        bits += 1
    for color in rgb:
        hx = '%02x' % color
        while len(hx) < bits:
            hx = f'0{hx}'
        hex += hx
    return hex


def hex2rgb(hex: str):
    hex = hex.lstrip('#')
    bits = len(hex) // 3
    rgb = tuple()
    for num in range(3):
        v = hex[num * bits:(num + 1) * bits]
        clr = int(v, 16)
        rgb += ((clr),)
    return rgb
