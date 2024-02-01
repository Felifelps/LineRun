import os

from Source.GameBase.board import Board
from Source.GameBase.relation import Relation
from Source.GameBase.score import Score

from Source.GUI.position import Position
from Source.GUI.color import Color
from Source.GUI.Label import Label
from Source.GUI.Font import Font
from Source.GUI.Button import Button

import pygame
pygame.init()

class app:
    mixer = True
    def __init__(self):
        self.data_image_path = os.getcwd() + ("\\Source" if "Source" not in os.getcwd() else "") + "\\Data\\Images"
        self.data_sound_path = os.getcwd() + ("\\Source" if "Source" not in os.getcwd() else "") + "\\Data\\Sounds"
        self.best_score = Score.get_best_score()
        self.screen = pygame.display.set_mode(Position.relative_game_screen_size)
        pygame.display.set_icon(pygame.image.load(self.data_image_path + "\\Ico.png"))
        pygame.display.set_caption("LineRun")
        try:
            pygame.mixer.music.load(self.data_sound_path + "\\Cyberpunk Moonlight Sonata.mp3")
        except Exception as e:
            self.mixer = False
        self.main_menu()
    #---------------------------------------------------------------------------------------------------------------------------------
    def main_menu(self):
        #Music
        if self.mixer:
            pygame.mixer.music.play(-1)

        #Background and title
        background = pygame.image.load(os.path.join(self.data_image_path + "\\background.png"))
        title = pygame.image.load(os.path.join(self.data_image_path + "\\title.png"))
        title_rect = title.get_rect()
        title_rect.y = 70

        #title y floating
        title_y_speed = 1

        def title_moving(title_y_speed, miny=70, maxy=85):
            if title_rect.y == miny:
                title_y_speed = 1
            elif title_rect.y == maxy:
                title_y_speed = -1

            title_rect.y += title_y_speed
            return title_y_speed

        #Global vars
        running = 1

        #Widgets
        best_score = Label("Melhor pontuação: " + str(self.best_score),
                    Color.main_purple, 
                    [Position.relx(275), Position.rely(770)],
                    "Corbel",
                    30
                    )
        best_score.centerX(Position.relx(300))

        play = Button(self.screen, 
                    os.path.join(self.data_image_path + "\\button_background.png"), 
                    [Position.relx(88), Position.rely(567), Position.relw(420), Position.relh(200)], 
                    self.game_screen, 
                    hover_path=os.path.join(self.data_image_path + "\\button_hover_background.png"),
                    text="Jogar",
                    font_family="Impact",
                    font_size=100,
                    font_color=Color.ligther_purple
                    )

        #Mainloop
        while running:
            click = False
            ##Drawing
            self.screen.blit(background, self.screen.get_rect())
            self.screen.blit(title, [27, title_rect.y])
            
            ##Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = event

            ##Updates

            #title y
            title_y_speed = title_moving(title_y_speed)
              
            #play button
            play.update(click)

            #bestscore
            best_score.text = "Melhor pontuação: " + str(self.best_score)
            best_score.update(self.screen)

            #screen
            pygame.display.flip()

    #---------------------------------------------------------------------------------------------------------------------------------
    def game_screen(self):
        #Background 
        background = pygame.image.load(os.path.join(self.data_image_path + "\\game_background.png"))

        #Global vars
        self.current_level = 1
        self.board = Board(self.current_level)
        
        #Time
        clock = pygame.time.Clock()
        tick = 0
        seconds = 0

        #Checking for gameover
        def check_status(status):
            if status == -1:
               self.gameover(self.current_level, seconds)
               return 0
            elif status == 2:
                if self.current_level < list(Relation.map_relation)[-1]:
                    self.current_level += 1
                    self.board = Board(self.current_level)
                elif self.current_level > list(Relation.map_relation)[-1]:
                    return self.victory(Score.calculate_score(self.current_level, seconds))

            return 1
                
        #Widgets
        level = Label("Nível " + str(self.current_level),
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(150)],
                      "Impact",
                      100
                      )
        level.centerX(Position.relx(300))
        
        pause = Button(self.screen, 
                       os.path.join(self.data_image_path + "\\pause.png"), 
                       [Position.relx(20), Position.rely(20), Position.relw(75), Position.relh(75)], 
                       self.pause
                       )

        time = Label("Tempo: " + str(seconds),
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(780)],
                      "Corbel",
                      40
                      )
        time.centerX(Position.relx(150))

        score = Label("Pontuação" + str(Score.calculate_score(self.current_level, seconds)),
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(780)],
                      "Corbel",
                      40
                      )
        score.centerX(Position.relx(450))
        
        running = 1
        while running:
            click = False

            #Time
            clock.tick(120)
            tick += 1
            if tick == 60:
                tick = 0
                seconds += 1

            self.screen.blit(background, self.screen.get_rect())

            #Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = event
            #Updates
            if check_status(self.board.update(self.screen, click)) == 0:
                running = 0

            level.text = "Nível " + str(self.current_level)
            level.update(self.screen)

            time.text = "Tempo: " + str(seconds)
            time.update(self.screen)

            score.text = "Pontuação: " + str(Score.calculate_score(self.current_level, seconds))
            score.update(self.screen)

            if pause.update(click) == 0:
                running = 0
            pygame.display.flip()

    #---------------------------------------------------------------------------------------------------------------------------------
    def gameover(self, max_level, time):
        #Music
        if self.mixer:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.data_sound_path + "\\Alone.mp3")
            pygame.mixer.music.play(-1)

        #Score
        game_score = Score.calculate_score(max_level, time)

        def return_0():
            return 0

        #Background
        background = pygame.image.load(os.path.join(self.data_image_path + "\\gameover.png"))
        title = pygame.image.load(os.path.join(self.data_image_path + "\\gameover_title.png"))
        title_rect = title.get_rect()
        title_rect.y = 70

        #title y floating
        title_y_speed = 1

        def title_moving(title_y_speed, miny=70, maxy=85):
            if title_rect.y == miny:
                title_y_speed = 1
            elif title_rect.y == maxy:
                title_y_speed = -1

            title_rect.y += title_y_speed
            return title_y_speed

        #Widgets
        menu = Button(self.screen, 
                      os.path.join(self.data_image_path + "\\button_background.png"), 
                      [Position.relx(88), Position.rely(567), Position.relw(420), Position.relh(200)], 
                      return_0, 
                      hover_path=os.path.join(self.data_image_path + "\\button_hover_background.png"),
                      text="Menu",
                      font_family="Impact",
                      font_size=80,
                      font_color=Color.ligther_purple
                      )
        
        score = Label("Sua pontuação: " + str(game_score),
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(770)],
                      "Corbel",
                      30
                      )
        score.centerX(Position.relx(300))

        running = 1
        while running != 0:
            click = False

            self.screen.blit(background, self.screen.get_rect())
            self.screen.blit(title, [5, title_rect.y])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = event

            title_y_speed = title_moving(title_y_speed)
            running = menu.update(click) 
            score.update(self.screen)
            pygame.display.flip()

        if game_score > self.best_score:
            Score.save_score(game_score)
            self.best_score = game_score
        
        #Music 
        if self.mixer:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.data_sound_path + "\\Cyberpunk Moonlight Sonata.mp3")
            pygame.mixer.music.play(-1)
    #---------------------------------------------------------------------------------------------------------------------------------
    def pause(self):
        #Background
        background = pygame.image.load(os.path.join(self.data_image_path + "\\pause_background.png"))
        title = pygame.image.load(os.path.join(self.data_image_path + "\\pause_title.png"))
        title_rect = title.get_rect()
        title_rect.y = -10

        #title y floating
        title_y_speed = 1

        def title_moving(title_y_speed, miny=-10, maxy=5):
            if title_rect.y == miny:
                title_y_speed = 1
            elif title_rect.y == maxy:
                title_y_speed = -1

            title_rect.y += title_y_speed
            return title_y_speed

        def back_to_screen(screen):
            #0 = menu, 1 = game
            return screen

        back_to_game = Button(self.screen,
                      os.path.join(self.data_image_path + "\\button_background.png"),
                      [Position.relx(88), Position.rely(430), Position.relw(420), Position.relh(200)],
                      lambda: back_to_screen(1),
                      centerx=300,
                      hover_path=os.path.join(self.data_image_path + "\\button_hover_background.png"),
                      text="Voltar ao jogo", 
                      font_color=Color.ligther_purple, 
                      font_family="Impact", 
                      font_size=50
                      )

        back_to_menu = Button(self.screen,
                      os.path.join(self.data_image_path + "\\button_background.png"),
                      [Position.relx(88), Position.rely(650), Position.relw(420), Position.relh(200)],
                      lambda: back_to_screen(0),
                      centerx=300,
                      hover_path=os.path.join(self.data_image_path + "\\button_hover_background.png"),
                      text="Voltar ao menu", 
                      font_color=Color.ligther_purple, 
                      font_family="Impact", 
                      font_size=50
                      )

        running = 1
        while running:
            click = False

            self.screen.blit(background, self.screen.get_rect())
            self.screen.blit(title, [5, title_rect.y])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = event

            #Updates
            title_y_speed = title_moving(title_y_speed)
            btg = back_to_game.update(click)
            btm = back_to_menu.update(click)

            if btg == 1:
                return btg
            elif btm == 0:
                return btm

            pygame.display.flip()
    #---------------------------------------------------------------------------------------------------------------------------------
    def victory(self, game_score):
        #Music
        if self.mixer:
            pygame.mixer.music.load(self.data_sound_path + "\\Viktor Kraus - Victory!.mp3")
            pygame.mixer.music.play(-1)

        #Background
        background = pygame.image.load(os.path.join(self.data_image_path + "\\gameover.png"))
        title = pygame.image.load(os.path.join(self.data_image_path + "\\victory.png"))
        title_rect = title.get_rect()
        title_rect.y = -10

        def return_0():
            return 0

        #title y floating
        title_y_speed = 1

        def title_moving(title_y_speed, miny=-10, maxy=5):
            if title_rect.y == miny:
                title_y_speed = 1
            elif title_rect.y == maxy:
                title_y_speed = -1

            title_rect.y += title_y_speed
            return title_y_speed

        #Widgets
        menu = Button(self.screen, 
                      os.path.join(self.data_image_path + "\\button_background.png"), 
                      [Position.relx(88), Position.rely(580), Position.relw(420), Position.relh(200)], 
                      return_0, 
                      hover_path=os.path.join(self.data_image_path + "\\button_hover_background.png"),
                      text="Menu",
                      font_family="Impact",
                      font_size=80,
                      font_color=Color.ligther_purple
                      )

        message = [Label("Você conseguiu",
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(380)],
                      "Impact",
                      40
                      ),
                    Label(f"passar do nível {list(Relation.map_relation)[-1]}.",
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(430)],
                      "Impact",
                      40
                      ),
                    Label("Parabéns!",
                      Color.especial_red, 
                      [Position.relx(275), Position.rely(480)],
                      "Impact",
                      60
                      ), 
                  ]

        for label in message:
            label.centerX(Position.relx(300))
        
        score = Label("Sua pontuação: " + str(game_score),
                      Color.main_purple, 
                      [Position.relx(275), Position.rely(800)],
                      "Corbel",
                      30
                      )
        score.centerX(Position.relx(300))

        running = 1
        while running != 0:
            click = False

            self.screen.blit(background, self.screen.get_rect())
            self.screen.blit(title, [5, title_rect.y])
            pygame.draw.rect(self.screen, Color.black, [124, 370, 346, 180])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = event

            title_y_speed = title_moving(title_y_speed)
            for label in message:
                label.update(self.screen)
            running = menu.update(click) 
            score.update(self.screen)
            pygame.display.flip()

        #Music
        if self.mixer:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.data_sound_path + "\\Cyberpunk Moonlight Sonata.mp3")
            pygame.mixer.music.play(-1)


