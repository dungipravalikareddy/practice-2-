from typing import List, Any

import pygame
from pygame import mixer
pygame.init()

height = 800
width = 1400
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
red = (251, 21, 21)
blue = (115, 87, 249)
green = (8, 245, 92)
sky_blue = (89, 236, 250)
yellow = (240, 250, 89)
gold = (212, 175, 55)
neon_blue = (0,255,255)
dark_grey = (50,50,50)
colours = [red, blue, green, sky_blue, yellow, white]
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("beat cracker")
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font =pygame.font.Font('freesansbold.ttf', 24)
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes: list[Any] = []
run = True
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True
hi_hat = mixer.Sound('sounds\\hi hat.WAV')
crash = mixer.Sound('sounds\\crash.wav')
kick = mixer.Sound('sounds\\kick.WAV')
snare = mixer.Sound('sounds\\snare.WAV')
tom = mixer.Sound('sounds\\tom.WAV')
clap = mixer.Sound('sounds\\clap.wav')
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat, actives):

    left_box = pygame.draw.rect(screen, grey, [0, 0, 250, height-200], 5)
    bottom_box = pygame.draw.rect(screen, grey, [0, height-200, width, 200], 5)
    colour = [grey, white, grey]
    colour1 = [grey, red, grey]
    colour2 = [grey, blue, grey]
    colour3 = [grey, green, grey]
    colour4 = [grey,sky_blue,grey]
    colour5 = [grey,yellow,grey]
    boxes = []
    hi_hat = label_font.render("HI_HAT", True, colour1[actives[0]])
    screen.blit(hi_hat, (30, 30))
    snare_text = label_font.render("SNARE", True, colour2[actives[1]])
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render("BASS_DRUM", True, colour3[actives[2]])
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render("CRASH", True, colour4[actives[3]])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render("CLAP", True, colour[actives[4]])
    screen.blit(clap_text, (30, 430))
    floor_tom = label_font.render("FLOOR_TOM", True, colour5[actives[5]])
    screen.blit(floor_tom, (30, 530))
    for i in range(instruments):
        pygame.draw.line(screen, grey, (0, (i*100)+100), (245, (i*100)+100))
    for i in range(beats):
            for j in range(instruments):
                if clicks[j][i] == -1:
                    colour = grey
                else:
                    if actives[j] == 1:
                      colour = green
                    else:
                        colour = dark_grey
                rect = pygame.draw.rect(screen, colour,
                                            [i * ((width - 245) // beats) + 250, (j * 100)+5, ((width - 245) // beats) - 10,
                                             ((height - 245) // instruments) - 10 ], 0, 3)
                pygame.draw.rect(screen, gold,
                                        [i * ((width - 245) // beats) + 245, (j * 100), ((width - 245) // beats),
                                         ((height - 245) // instruments)], 5, 5)
                rect = pygame.draw.rect(screen, black,
                                        [i * ((width - 245) // beats) + 245, (j * 100), ((width - 245) // beats),
                                         ((height - 200) // instruments)], 2,3 )

                boxes.append((rect, (i, j)))
            active = pygame.draw.rect(screen, neon_blue,[beat * ((width - 245)//beats) + 245, 0, ((width-245)//beats), instruments*100], 5, 3)
    return boxes


while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen,grey,[50,height-150, 245, 100],0 ,5)
    play_text = label_font.render('play/pause',True, white)
    screen.blit(play_text,(70,height-130))
    if playing:
        play_text2 = medium_font.render("playing",True, dark_grey)
    else:
        play_text2 = medium_font.render("Paused",True, dark_grey)
    screen.blit(play_text2, (70, height-100))
    # bpm stuff
    bpm_react = pygame.draw.rect(screen,grey,[300, height-150, 200,100],2,2)
    bpm_text = medium_font.render("beatsperminute",True, sky_blue)
    screen.blit(bpm_text,(308,height-130))
    bpm_text2 = label_font.render(f'{bpm}',True, gold)
    screen.blit(bpm_text2,(370, height-100))
    bpm_add_rect = pygame.draw.rect(screen,grey, [510, height-150,48,48],0,5)
    bpm_sub_rect = pygame.draw.rect(screen,grey, [510, height-100,48,48],0,5)
    add_text = medium_font.render("+5",True,neon_blue)
    sub_text = medium_font.render('-5', True, red)
    screen.blit(add_text, (520, height-140))
    screen.blit(sub_text, (520, height-98))
    #beats stuff
    beats_react = pygame.draw.rect(screen, grey, [600, height - 150, 200, 100], 2, 2)
    beats_text = medium_font.render("BEATS IN LOOP", True, sky_blue)
    screen.blit(beats_text, (608, height - 130))
    beats_text2 = label_font.render(f'{beats}', True, gold)
    screen.blit(beats_text2, (670, height - 100))
    beats_add_rect = pygame.draw.rect(screen, grey, [810, height - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, grey, [810, height - 100, 48, 48], 0, 5)
    add_text = medium_font.render("+1", True, neon_blue)
    sub_text = medium_font.render('-1', True, red)
    screen.blit(add_text, (820, height - 140))
    screen.blit(sub_text, (820, height - 98))
    #instrument stuff
    instruments_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i*100), (245 ,100))
        instruments_rects.append(rect)

    #save and load stuff
    save_circle = pygame.draw.circle(screen , grey, [920, height-100], 50, 50)
    save_text = label_font.render("Save ", True, green)
    save_text2 = label_font.render("beat", True, green)
    screen.blit(save_text, (885, height-130))
    screen.blit(save_text2,(885, height-100))
    load_circle = pygame.draw.circle(screen , grey, [1030, height-100], 50 ,50)
    load_text = label_font.render('Load', True, yellow)
    load_text2 = label_font.render("beat",True, yellow)
    screen.blit(load_text,(995, height-130))
    screen.blit(load_text2,(995,height-100))


    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    cords = boxes[i][1]
                    clicked[cords[1]][cords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            for i in range(len(instruments_rects)):
                if instruments_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1





    beat_length = 3600//bpm
    if playing:
        if active_length<beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True


    pygame.display.flip()

pygame.quit()
