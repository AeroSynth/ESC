from collections import namedtuple
import json
import matplotlib
import matplotlib.backends.backend_agg as agg
import numpy as np
import pylab
import pygame
import pygame.font
import os

SELECTED = (246, 153, 0, )
HIGHLIGHT = (104,175, 50, )

BG =  (255, 255, 255,)
BUTTON_BG = (255, 255, 255,)
BUTTON_TEXT = (0, 0, 0, )
BUTTON_EDGE = (0, 0, 0, )

LABEL_BG = HIGHLIGHT
LABEL_TEXT = (255, 255, 255, )

PLAY = HIGHLIGHT
RECORD = (255, 0, 0, )

Button = namedtuple('Button', ['pos', 'size', 'cb', 'surface', 'selected_surface'])
Label = namedtuple('Label', ['pos', 'size', 'surface'])

FONT='rasa'

class layout(object):
    def __init__(self, config):
        matplotlib.use("Agg")

        self.fig = pylab.figure(figsize=[16, 4],
                                dpi=100,
                                facecolor='none',
                                edgecolor='none',
                   )
        self.ax = self.fig.gca()

        pygame.init()
        pygame.mixer.init()
        window = pygame.display.set_mode()
        self.screen = pygame.display.get_surface()
        self._buttons = []
        self._phrase_buttons = []
        self._language_buttons = []
        self.sound = None
        self.language_choice = None
        self.phrase_choice = None
        self.labels = []

        self._cc = json.load(open(config))

    def plot_file(self, fname):
        self.sound = pygame.mixer.Sound(file=fname)
        data = np.frombuffer(self.sound.get_raw(), np.int16)
        # TODO: reshape on hello_en.get_num_channels() > 1

        self.ax.clear()
        self.ax.plot(data, 'k')
        self.ax.axis('off')

    def run(self):
        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.sound.play()
                    elif event.key == pygame.K_q:
                        crashed = True
                    elif event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
                        self.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for bt in self._buttons:
                        if np.all(np.array(pos) >= bt.pos) and \
                           np.all(np.array(pos) <= bt.pos + bt.size):
                            bt.cb()


    def add_button(self, pos, size, label, cb, pt=48):
        bt = Button(pos, size, cb, pygame.Surface(size), pygame.Surface(size))
        bt.surface.fill(BG)
        bt.selected_surface.fill(SELECTED)

        sysfont = pygame.font.get_default_font()
        font = pygame.font.SysFont(FONT, pt)
        txt = font.render(label, True, BUTTON_TEXT)

        pygame.draw.rect(bt.surface, BUTTON_EDGE, np.concatenate(([0,0],size)), 1)
        bt.surface.blit(txt, [(size[0] - txt.get_width())/2, (size[1] - txt.get_height())/2])

        pygame.draw.rect(bt.selected_surface, BUTTON_EDGE, np.concatenate(([0,0],size)), 1)
        bt.selected_surface.blit(txt, [(size[0] - txt.get_width())/2, (size[1] - txt.get_height())/2])

        self._buttons.append(bt)

        return bt

    def add_phrase_button(self, *args, **kwargs):
        self._phrase_buttons.append(self.add_button(*args, **kwargs))

    def add_language_button(self, *args, **kwargs):
        self._language_buttons.append(self.add_button(*args, **kwargs))


    def update(self):
        self.screen.fill(BG)
        if self.sound:
            canvas = agg.FigureCanvasAgg(self.fig)
            canvas.draw()
            raw_data = canvas.buffer_rgba()
            size = canvas.get_width_height()
            surf = pygame.image.frombuffer(raw_data, size, "RGBA")
            self.screen.blit(surf, [100,100])

        for bt in self._buttons:
            self.screen.blit(bt.surface, bt.pos)

        if self.phrase_choice is not None:
            bt = self._phrase_buttons[self.phrase_choice]
            self.screen.blit(bt.selected_surface, bt.pos)

        if self.language_choice is not None:
            bt = self._language_buttons[self.language_choice]
            self.screen.blit(bt.selected_surface, bt.pos)


        for l in self.labels:
            self.screen.blit(l.surface, l.pos)

        pygame.display.update()
        pygame.display.flip()

    def phrase_select(self, n: int):
        self.phrase_choice = n
        if n is not None and self.language_choice is not None:

            ll = self._cc['languages'][self.get_languages()[self.language_choice]]
            file_list = [ os.path.join('data', ll['dir'], x['file']) for x in ll['phrases'] ]

            if n < len(file_list):
                self.plot_file(file_list[n])
            else:
                print("error load_sound {}".format(n))

        self.update()

    def language_select(self, n: int):
        self.language_choice = n
        self.phrase_select(self.phrase_choice)
        self.update()

    def play(self):
        if self.sound:
            self.sound.play()

    def add_label(self, pos, number, dim = 50):
        size = np.array([dim, dim])
        l = Label(pos, size, pygame.Surface(size))
        sysfont = pygame.font.get_default_font()
        font = pygame.font.SysFont(FONT, 48)
        txt = font.render(number, True, LABEL_TEXT)
        l.surface.fill(BG)
        pygame.draw.circle(l.surface, LABEL_BG, [dim/2,dim/2], dim/2)
        l.surface.blit(txt, [(dim - txt.get_width())/2, (dim - txt.get_height())/2])

        self.labels.append(l)

    def get_languages(self):
        return list(self._cc['languages'].keys())

def main():

    gui = layout('config.json')

    gui.add_label(np.array([0,0]), '1')
    for i,language in enumerate(gui.get_languages()):
        pos = np.array([100 + (i%3) * 250, 10 + (i//3) * 75 ])
        gui.add_language_button(pos, np.array([200, 50]),
                                language,
                                lambda i=i: gui.language_select(i))
    gui.add_label(np.array([0, 150]), '2')
    for i in range(6):
        gui.add_phrase_button(np.array([50, 200 + i * 75]), np.array([200, 50]),
                              'Phrase {}'.format(i + 1),
                              lambda i=i: gui.phrase_select(i))


    gui.add_label(np.array([300, 500]), '3')
    bt = gui.add_button(np.array([600, 500]), np.array([150, 50]), 'Replay  ', gui.play, pt=30)
    pygame.draw.polygon(bt.surface, PLAY, np.array((120,10)) + np.array([(0,0), (25,15), (0,30)]))

    gui.add_label(np.array([300, 1000]), '4')

    gui.update()
    gui.run()

if __name__ == '__main__':
    main()
