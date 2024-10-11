#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pygame_textinput
import random
import time
import json
from dataclasses import dataclass
import datetime

@dataclass
class Score:
    name: str
    score: int
    date: str


def save_user(score: Score) -> None:
    with open("scores.json", "r") as file:
        try:
            file_data = json.load(file)
        except JSONDecodeError:
            file_data = {}
        file_data[score.scorename] = [{
            "name": score.name,
            "score": score.score,
            "date": score.date,
        }]
    with open("scores.json", "w") as outfile:
        json.dump(file_data, outfile, indent=4)


def register(score):
    name_input = input("Name: ")
    user_data = User(
        name=name_input,
        score=score,
        date=datetime.datetime.now(),
    )
    save_user(user=user_data)

pygame.init()
clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)

BACKGROUND = 255, 255, 255
BACKGROUND2 = 0, 0, 0

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 128)


KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]


class Game():
    def __init__(self):
        self.score = 0
        self.isKO = False
        self.score_text = font.render('', True, red)
        self.can_add_memo = True
        self.can_play = False
        self.memos = []
        self.memos_show = []
        self.guess = []
        self.x_window_size = 1920
        self.y_window_size = 1080
        self.game_window = pygame.display.set_mode((self.x_window_size, self.y_window_size))
        self.background = pygame.Surface(self.game_window.get_size())
        self.images_arrow= {pygame.K_UP: pygame.image.load("up_arrow.png").convert_alpha(), pygame.K_DOWN: pygame.image.load("down_arrow.png").convert_alpha(), pygame.K_RIGHT: pygame.image.load("right_arrow.png").convert_alpha(), pygame.K_LEFT: pygame.image.load("left_arrow.png").convert_alpha()}
        self.images_arrow_check_true= {pygame.K_UP: pygame.image.load("up_arrow_check_true.png").convert_alpha(), pygame.K_DOWN: pygame.image.load("down_arrow_check_true.png").convert_alpha(), pygame.K_RIGHT: pygame.image.load("right_arrow_check_true.png").convert_alpha(), pygame.K_LEFT: pygame.image.load("left_arrow_check_true.png").convert_alpha()}
        self.images_arrow_check_false= {pygame.K_UP: pygame.image.load("up_arrow_check_false.png").convert_alpha(), pygame.K_DOWN: pygame.image.load("down_arrow_check_false.png").convert_alpha(), pygame.K_RIGHT: pygame.image.load("right_arrow_check_false.png").convert_alpha(), pygame.K_LEFT: pygame.image.load("down_arrow_check_false.png").convert_alpha()}





def add_new_memo(game):
    game.memos.append(random.choice (KEYS))
    game.can_add_memo = False
    game.can_play = True
    game.memos_show = game.memos.copy()


def add_new_guess(key_pressed, game):
    game.guess.append(key_pressed)

    if (game.guess[-1] == game.memos[len(game.guess) - 1]):
        print("OK")
        if (len(game.guess) == len(game.memos)):
            game.can_play = False
            game.can_add_memo = True
            game.guess = []
            game.score = game.score + 1
        else:
            game.can_play = True
            game.can_add_memo = False
        show_image_input(game, key_pressed, True)
    else:
        print("KO")
        game.isKO = True
        game.can_play = False
        game.can_add_memo = False
        show_image_input(game, key_pressed, False)


def show_image_input(game, input, is_valid):

    print(is_valid)
    game.background.fill(BACKGROUND)
    game.game_window.blit(game.background, (0, 0))
    pygame.display.flip()


    # time.sleep(0.5)
    if (is_valid):
        game.game_window.blit(game.images_arrow_check_true[input], (0, 50))
    else:
        game.game_window.blit(game.images_arrow_check_false[input], (0, 50))
    pygame.display.flip()
    time.sleep(0.5)



def show_memo_image(game):
    game.background.fill(BACKGROUND)
    game.game_window.blit(game.background, (0, 0))
    pygame.display.flip()
    for m in game.memos_show:
        game.game_window.blit(game.images_arrow[m], (0, 50))
        pygame.display.flip()

        time.sleep(1)

        game.background.fill(BACKGROUND)
        game.game_window.blit(game.background, (0, 0))
        pygame.display.flip()
    game.memos_show.clear()


def create_score(name):
    pass

def main():
    game = Game()

    pygame.display.set_caption('MEMO')

    textinput = pygame_textinput.TextInputVisualizer()
    textinput.cursor_width = 12
    textinput.value = "Hello, World!"
    loop = True
    textRect = game.score_text.get_rect()
    textRect.center = (game.x_window_size // 2, game.y_window_size // 2)

    game.background.fill(BACKGROUND)
    game.game_window.blit(game.background, (0, 0))



    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False


        if (game.isKO):
            game.score_text = font.render("GAME OVER YOUR SCORE IS : " + str(game.score), True, red)
            game.game_window.blit(game.score_text, textRect)
        else:
            if (len(game.memos_show) != 0):
                show_memo_image(game)

            if (game.can_add_memo):
                add_new_memo(game)
                print(game.memos)
            if event.type == pygame.KEYDOWN and game.can_play and event.key in KEYS:
                add_new_guess(event.key, game)
                time.sleep(0.2)




        pygame.display.flip()
        clock.tick(120)#FPS

if __name__ == '__main__':
    main()