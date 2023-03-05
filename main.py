from random import shuffle
import pygame
from pygame import time, display, draw, event, font, image, rect, surface, init, quit


SCREEN_SIZE = (1280, 960)

## COLORS
# general
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
# MENU
COLOR_WHITE = (255, 255, 255)
COLOR_MENU_BG = (255, 0, 0)
COLOR_MENU_BUTTON = (0, 0, 0)
COLOR_MENU_BUTTON_OUTLINE = (4, 181, 217)
COLOR_MENU_BUTTON_OUTLINE_HOVER = (229, 15, 4)
COLOR_MENU_TEXT = (255, 255, 255)
# UNIT
COLOR_UNIT_TEXT = (255, 255, 255)
COLOR_UNIT_EXIT = (0, 0, 0)
COLOR_UNIT_BUTTON_OUTLINE = (4, 181, 217)
COLOR_UNIT_BUTTON_OUTLINE_HOVER = (0, 255, 0)
COLOR_UNIT_BUTTON = (0, 0, 0)

#QUESTION PAGE
COLOR_QUESTION_BACKGROUND = (255,255,255)
COLOR_QUESTION_TEXT = (0, 0, 0)
COLOR_QUESTION_OPTION_OUTLINE = (0, 0, 0)
COLOR_QUESTION_OPTION_OUTLINE_HOVER = (0, 0, 255)
COLOR_QUESTION_OPTION_OUTLINE_SELCTED = (0, 255, 0)
COLOR_QUESTION_OPTION_OUTLINE_WRONG = (255, 0, 0)

COLOR_LESSON_OPTION_TEXT = (0, 0, 0)
COLOR_LESSON_OPTION_OUTLINE = (0, 0, 0)
COLOR_LESSON_OPTION_OUTLINE_HOVER = (0, 0, 255)

COLOR_INSTRUCTION_TEXT = (0, 0, 0)
COLOR_INSTRUCTION_OUTLINE = (0, 0, 0)
COLOR_INSTRUCTION_OUTLINE_HOVER = (0, 0, 255)

## DIMENSIONS
# constants for dimensions MENU
MENU_BUTTON_LEFT_X = 300
MENU_BUTTON_TOP_MARGIN = 100
MENU_BUTTON_BUTTOM_MARGIN = 60
MENU_BUTTON_WIDTH = 680
MENU_BUTTON_HEIGHT = 200
MENU_BUTTON_HEIGHT_MARGIN = 50
MENU_BUTTON_OUTLINE_THICKNESS = 10

# constants for dimensions UNITS EXIT
UNIT_BUTTON_LEFT_X = 140
UNIT_BUTTON_TOP_Y = 80
UNIT_BUTTON_WIDTH = 400
UNIT_BUTTON_HEIGHT = 200
UNIT_BUTTON_OUTLINE_THICKNESS = 5
UNIT_BUTTON_HEIGHT_SPACE = 100
UNIT_BUTTON_WIDTH_SPACE = 100
UNIT_BUTTON_WIDTH_SPACE_S = 50
UNIT_BUTTON_WIDTH_MARGIN = 150
UNIT_BUTTON_HEIGHT_MARGIN = 100

# constants fro dimensions QUESTION
QUESTION_PROMPT_LEFT_X = 140
QUESTION_PROMPT_TOP_Y = 130
QUESTION_PROMPT_WIDTH = 650
QUESTION_PROMPT_HEIGHT = 700
QUESTION_OPTION_LEFT_X = 800
QUESTION_OPTION_LETTER_WIDTH = 50
QUESTION_OPTION_WIDTH = 250
QUESTION_OPTION_HEIGHT = 100
QUESTION_OPTION_TOP_Y = 130
QUESTION_OPTION_OUTLINE_THICKNESS = 3
QUESTION_BUTTON_OUTLINE_THICKNESS = 5
QUESTION_OPTION_MARGIN = 50
QUESTION_LAST_NEXT_WIDTH = 100
QUESTION_LAST_NEXT_HEIGHT = 50

LESSON_BUTTON_LEFT_X = 1000
LESSON_BUTTON_TOP_Y = 800
LESSON_BUTTON_WIDTH = 200
LESSON_BUTTON_HEIGHT = 100
LESSON_BUTTON_OUTLINE_THICKNESS = 5

INSTRUCTION_IMAGE_TOP_Y = 200
INSTRUCTION_BUTTON_TOP_Y = 700
INSTRUCTION_BUTTON_WIDTH = 400
INSTRUCTION_BUTTON_HEIGHT = 100
INSTRUCTION_BUTTON_OUTLINE_THICKNESS = 5

PAGE_EXIT = 0
PAGE_MENU = 1
PAGE_QUESTION = 2
PAGE_LESSON = 3
PAGE_HISTORY = 4
PAGE_INSTRUCTION = 5
PAGE_QUESTION_QUESTION = 6
PAGE_LESSON_LESSON = 7
PAGE_RESULT = 8

ANSWERS = (
    (3, 1, 1, 3, 0, 2),
    (3, 3, 0, 2, 2, 0),
    (0, 0, 0, 1, 0, 1),
)

#IF CLICKED
clicked_option = []
current_question = 0

selected_lesson = 0
lesson_page = 0

page = PAGE_MENU

running = True

init()

screen = display.set_mode(SCREEN_SIZE)
timer = time.Clock()

mouse_x, mouse_y = -1, -1
mouse_clicked = False

# images
image_bg = image.load("Images/bg_resized.png")

class class_question():
    def __init__(self, ans):
        self.q = surface.Surface((0, 0))
        self.opt = []
        self.ans = ans

class class_surface:
    def __init__(self, obj):
        self.obj = obj
        self.w, self.h = obj.get_size()


questions = []
questions_shuffled = []
for i in range(3):  # chagne this to 5 maybe
    questions.append([])
    for j in range(6):
        questions[-1].append(class_question(ANSWERS[i][j]))
        questions[-1][-1].q = class_surface(image.load("Images/Questions/u%dq%d.png" % (i+1, j+1)))
        for k in range(4):
            questions[-1][-1].opt.append(class_surface(image.load("Images/Questions/u%dq%d_%d.png" % (i+1, j+1, k+1))))

# fonts
font_menu_button = font.Font("Fonts/ARIBLK.TTF", 48)
font_unit_button = font.Font("Fonts/ARIBLK.TTF", 56)
font_question_option = font.Font("Fonts/ARIBLK.TTF", 36)
font_question_last_next = font.Font("Fonts/ARIBLK.TTF", 24)
font_lesson = font.Font("Fonts/ARIBLK.TTF", 36)
font_instruction = font.Font("Fonts/ARIBLK.TTF", 40)

instruction_return_page = 0
instruction_question = class_surface(image.load("Images/instruction_question.png"))
instruction_lesson = class_surface(image.load("Images/instruction_lesson.png"))
image_instruction = class_surface(surface.Surface((0, 0)))

TEXT_MENU_BUTTON = (
    "Questions",
    "Lessons",
    "Results",
)
text_menu = {}
for text in TEXT_MENU_BUTTON:
    text_menu[text] = class_surface(font_menu_button.render(text, True, COLOR_MENU_TEXT))

# rendered font for unit
TEXT_UNIT_BUTTON = (
    "Exit",
    "Instruction",
    "Unit 1",
    "Unit 2",
    "Unit 3",
    "Unit 4",
    "Unit 5",
)

text_unit = {}
for text in TEXT_UNIT_BUTTON:
    text_unit[text] = class_surface(font_unit_button.render(text, True, COLOR_UNIT_TEXT))

TEXT_QUESTION_OPTION = (
    "A",
    "B",
    "C",
    "D",
    "Submit",
    "Back",
)
TEXT_QUESTION_LAST_NEXT = (
    "Last",
    "Next",
)

text_question = {}
for text in TEXT_QUESTION_OPTION:
    text_question[text] = class_surface(font_question_option.render(text, True, COLOR_QUESTION_TEXT))
for text in TEXT_QUESTION_LAST_NEXT:
    text_question[text] = class_surface(font_question_last_next.render(text, True, COLOR_QUESTION_TEXT))

TEXT_LESSON = (
    "Back",
    "Next",
)
text_lesson = {}
for text in TEXT_LESSON:
    text_lesson[text] = class_surface(font_lesson.render(text, True, COLOR_LESSON_OPTION_TEXT))

image_lesson = []
for i in range(3):  # change to 5
    image_lesson.append([])
    for j in range(2):
        image_lesson[-1].append(class_surface(image.load("Images/Lessons/%d_%d.png" % (i+1, j+1))))

TEXT_INSTRUCTION = (
    "Continue",
)
text_instruction = {}
for text in TEXT_INSTRUCTION:
    text_instruction[text] = class_surface(font_instruction.render(text, True, COLOR_INSTRUCTION_TEXT))

# rendered font for lesson
def draw_menu() -> int:
    screen.blit(image_bg, (0, 0))

    unit_rect = draw.rect(screen, COLOR_MENU_BUTTON, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT))

    if unit_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_MENU_BUTTON_OUTLINE_HOVER, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT), MENU_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            return PAGE_QUESTION
    else:
        draw.rect(screen, COLOR_MENU_BUTTON_OUTLINE, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT), MENU_BUTTON_OUTLINE_THICKNESS)

    lesson_rect = draw.rect(screen, COLOR_MENU_BUTTON, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT+MENU_BUTTON_HEIGHT_MARGIN, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT))

    screen.blit(text_menu["Questions"].obj, (MENU_BUTTON_LEFT_X+MENU_BUTTON_WIDTH//2-text_menu["Questions"].w//2, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT//2-text_menu["Questions"].h//2))

    if lesson_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_MENU_BUTTON_OUTLINE_HOVER, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT+MENU_BUTTON_HEIGHT_MARGIN, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT), MENU_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            return PAGE_LESSON
    else:
        draw.rect(screen, COLOR_MENU_BUTTON_OUTLINE, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT+MENU_BUTTON_HEIGHT_MARGIN, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT), MENU_BUTTON_OUTLINE_THICKNESS)

    result_rect = draw.rect(screen, COLOR_MENU_BUTTON, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT*2+MENU_BUTTON_HEIGHT_MARGIN*2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT))

    screen.blit(text_menu["Lessons"].obj, (MENU_BUTTON_LEFT_X+MENU_BUTTON_WIDTH//2-text_menu["Lessons"].w//2, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT+MENU_BUTTON_HEIGHT_MARGIN+MENU_BUTTON_HEIGHT//2-text_menu["Lessons"].h//2))

    if result_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_MENU_BUTTON_OUTLINE_HOVER, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT*2+MENU_BUTTON_HEIGHT_MARGIN*2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT), MENU_BUTTON_OUTLINE_THICKNESS)
        # prevent users going into history page
        # if mouse_clicked:
        #     return PAGE_HISTORY
    else:
        draw.rect(screen, COLOR_MENU_BUTTON_OUTLINE, (MENU_BUTTON_LEFT_X, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT*2+MENU_BUTTON_HEIGHT_MARGIN*2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT), MENU_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_menu["Results"].obj, (MENU_BUTTON_LEFT_X+MENU_BUTTON_WIDTH//2-text_menu["Results"].w//2, MENU_BUTTON_TOP_MARGIN+MENU_BUTTON_HEIGHT*2+MENU_BUTTON_HEIGHT_MARGIN*2+MENU_BUTTON_HEIGHT//2-text_menu["Results"].h//2))

    return PAGE_MENU

def draw_question():
    global image_instruction, instruction_return_page

    # Exit Button
    screen.blit(image_bg, (0, 0))
    exit_rect = draw.rect(screen,COLOR_UNIT_EXIT,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if exit_rect.collidepoint(mouse_x, mouse_y):
        #Exit Highlight
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            return PAGE_MENU
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Exit"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH//2-text_unit["Exit"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT//2-text_unit["Exit"].h//2))

    #Standerd Button
    instruction_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if instruction_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            image_instruction = instruction_question
            instruction_return_page = PAGE_QUESTION
            return PAGE_INSTRUCTION
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Instruction"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH//2-text_unit["Instruction"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN+UNIT_BUTTON_HEIGHT//2-text_unit["Instruction"].h//2))

    unit1_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if unit1_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            question_init(0)
            return PAGE_QUESTION_QUESTION
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
    
    screen.blit(text_unit["Unit 1"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN+UNIT_BUTTON_WIDTH//2-text_unit["Unit 1"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN+UNIT_BUTTON_HEIGHT//2-text_unit["Unit 1"].h//2))

    unit2_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if unit2_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            question_init(1)
            return PAGE_QUESTION_QUESTION
    else:
         draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Unit 2"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH//2-text_unit["Unit 2"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2+UNIT_BUTTON_HEIGHT//2-text_unit["Unit 2"].h//2))

    unit3_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if unit3_rect.collidepoint(mouse_x, mouse_y):
         draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
         if mouse_clicked:
            question_init(2)
            return PAGE_QUESTION_QUESTION
    else:
         draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Unit 3"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN+UNIT_BUTTON_WIDTH//2-text_unit["Unit 3"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2+UNIT_BUTTON_HEIGHT//2-text_unit["Unit 3"].h//2))

    return PAGE_QUESTION

def get_result():
    global text_result
    count = 0
    for i in range(3):
        if clicked_option[i] == questions_shuffled[i].ans:
            count += 1
    text_result = class_surface(font_question_option.render("Score: %d/3" % (count), True, COLOR_QUESTION_TEXT))

def draw_question_question():
    global clicked_option, current_question
    screen.fill(COLOR_QUESTION_BACKGROUND)

    #QUESTION PROMPT
    screen.blit(questions_shuffled[current_question].q.obj,(QUESTION_PROMPT_LEFT_X+QUESTION_PROMPT_WIDTH//2-questions_shuffled[current_question].q.w//2,QUESTION_PROMPT_TOP_Y+QUESTION_PROMPT_HEIGHT//2-questions_shuffled[current_question].q.h//2))

    screen.blit(questions_shuffled[current_question].opt[0].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[0].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[0].h//2))

    screen.blit(questions_shuffled[current_question].opt[1].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[1].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[1].h//2))

    screen.blit(questions_shuffled[current_question].opt[2].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[2].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[2].h//2))

    screen.blit(questions_shuffled[current_question].opt[3].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[3].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[3].h//2))

    screen.blit(text_question["A"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["A"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT//2-text_question["A"].h//2))

    screen.blit(text_question["B"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["B"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_HEIGHT//2-text_question["B"].h//2))

    screen.blit(text_question["C"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["C"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2+QUESTION_OPTION_HEIGHT//2-text_question["C"].h//2))

    screen.blit(text_question["D"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["D"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3+QUESTION_OPTION_HEIGHT//2-text_question["D"].h//2))

    rect_a = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    rect_b = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    rect_c = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    rect_d = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    if rect_a.collidepoint(mouse_x,mouse_y):
        draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_HOVER,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)
        if mouse_clicked:
            clicked_option[current_question] = 0
    elif rect_b.collidepoint(mouse_x,mouse_y):
        draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_HOVER,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)
        if mouse_clicked:
            clicked_option[current_question] = 1
    elif rect_c.collidepoint(mouse_x,mouse_y):
        draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_HOVER,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)
        if mouse_clicked:
            clicked_option[current_question] = 2
    elif rect_d.collidepoint(mouse_x,mouse_y):
        draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_HOVER,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)
        if mouse_clicked:
            clicked_option[current_question] = 3

    if clicked_option[current_question] >= 0:
        draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_SELCTED,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*clicked_option[current_question],QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    submit_rect = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_MARGIN,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_BUTTON_OUTLINE_THICKNESS)

    last_rect = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2,QUESTION_LAST_NEXT_WIDTH,QUESTION_LAST_NEXT_HEIGHT),QUESTION_BUTTON_OUTLINE_THICKNESS)

    next_rect = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH+QUESTION_OPTION_MARGIN,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2,QUESTION_LAST_NEXT_WIDTH,QUESTION_LAST_NEXT_HEIGHT),QUESTION_BUTTON_OUTLINE_THICKNESS)

    if submit_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_QUESTION_OPTION_OUTLINE_HOVER, (QUESTION_OPTION_LEFT_X, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_MARGIN, QUESTION_OPTION_WIDTH, QUESTION_OPTION_HEIGHT), QUESTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            get_result()
            return PAGE_RESULT
    elif last_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_QUESTION_OPTION_OUTLINE_HOVER, (QUESTION_OPTION_LEFT_X, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2, QUESTION_LAST_NEXT_WIDTH, QUESTION_LAST_NEXT_HEIGHT), QUESTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            current_question -= 1
            current_question %= 3
    elif next_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_QUESTION_OPTION_OUTLINE_HOVER, (QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH+QUESTION_OPTION_MARGIN, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2, QUESTION_LAST_NEXT_WIDTH, QUESTION_LAST_NEXT_HEIGHT), QUESTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            current_question += 1
            current_question %= 3

    screen.blit(text_question["Submit"].obj, (QUESTION_OPTION_LEFT_X+QUESTION_OPTION_WIDTH//2-text_question["Submit"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_MARGIN+QUESTION_OPTION_HEIGHT//2-text_question["Submit"].h//2))

    screen.blit(text_question["Last"].obj, (QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH//2-text_question["Last"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2+QUESTION_LAST_NEXT_HEIGHT//2-text_question["Last"].h//2))

    screen.blit(text_question["Next"].obj, (QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH+QUESTION_OPTION_MARGIN+QUESTION_LAST_NEXT_WIDTH//2-text_question["Next"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2+QUESTION_LAST_NEXT_HEIGHT//2-text_question["Next"].h//2))
    
    return PAGE_QUESTION_QUESTION

def draw_lesson():
    global selected_lesson, lesson_page, image_instruction, instruction_return_page

    # Exit Button
    screen.blit(image_bg, (0, 0))
    exit_rect = draw.rect(screen,COLOR_UNIT_EXIT,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if exit_rect.collidepoint(mouse_x, mouse_y):
        #Exit Highlight
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            return PAGE_MENU
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Exit"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH//2-text_unit["Exit"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT//2-text_unit["Exit"].h//2))

    #Standerd Button
    instruction_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if instruction_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            image_instruction = instruction_lesson
            instruction_return_page = PAGE_LESSON
            return PAGE_INSTRUCTION
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Instruction"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH//2-text_unit["Instruction"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN+UNIT_BUTTON_HEIGHT//2-text_unit["Instruction"].h//2))

    unit1_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if unit1_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            selected_lesson = 0
            lesson_page = 0
            return PAGE_LESSON_LESSON
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
    
    screen.blit(text_unit["Unit 1"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN+UNIT_BUTTON_WIDTH//2-text_unit["Unit 1"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT+UNIT_BUTTON_HEIGHT_MARGIN+UNIT_BUTTON_HEIGHT//2-text_unit["Unit 1"].h//2))

    unit2_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if unit2_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            selected_lesson = 1
            lesson_page = 0
            return PAGE_LESSON_LESSON
    else:
         draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Unit 2"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH//2-text_unit["Unit 2"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2+UNIT_BUTTON_HEIGHT//2-text_unit["Unit 2"].h//2))

    unit3_rect = draw.rect(screen,COLOR_UNIT_BUTTON,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT))

    if unit3_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            selected_lesson = 2
            lesson_page = 0
            return PAGE_LESSON_LESSON
    else:
        draw.rect(screen,COLOR_UNIT_BUTTON_OUTLINE_HOVER,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2,UNIT_BUTTON_WIDTH,UNIT_BUTTON_HEIGHT),UNIT_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_unit["Unit 3"].obj,(UNIT_BUTTON_LEFT_X+UNIT_BUTTON_WIDTH+UNIT_BUTTON_WIDTH_MARGIN+UNIT_BUTTON_WIDTH//2-text_unit["Unit 3"].w//2,UNIT_BUTTON_TOP_Y+UNIT_BUTTON_HEIGHT*2+UNIT_BUTTON_HEIGHT_MARGIN*2+UNIT_BUTTON_HEIGHT//2-text_unit["Unit 3"].h//2))

    return PAGE_LESSON

def draw_lesson_lesson():
    global lesson_page

    screen.fill(COLOR_WHITE)

    screen.blit(image_lesson[selected_lesson][lesson_page].obj, (640-image_lesson[selected_lesson][lesson_page].w//2, 480-image_lesson[selected_lesson][lesson_page].h//2))

    button = draw.rect(screen, COLOR_LESSON_OPTION_OUTLINE, (LESSON_BUTTON_LEFT_X, LESSON_BUTTON_TOP_Y, LESSON_BUTTON_WIDTH, LESSON_BUTTON_HEIGHT), LESSON_BUTTON_OUTLINE_THICKNESS)

    if lesson_page == 0:
        screen.blit(text_lesson["Next"].obj, (LESSON_BUTTON_LEFT_X+LESSON_BUTTON_WIDTH//2-text_lesson["Next"].w//2, LESSON_BUTTON_TOP_Y+LESSON_BUTTON_HEIGHT//2-text_lesson["Next"].h//2))
        if button.collidepoint(mouse_x, mouse_y):
            draw.rect(screen, COLOR_LESSON_OPTION_OUTLINE_HOVER, (LESSON_BUTTON_LEFT_X, LESSON_BUTTON_TOP_Y, LESSON_BUTTON_WIDTH, LESSON_BUTTON_HEIGHT), LESSON_BUTTON_OUTLINE_THICKNESS)
            if mouse_clicked:
                lesson_page += 1
    else:
        screen.blit(text_lesson["Back"].obj, (LESSON_BUTTON_LEFT_X+LESSON_BUTTON_WIDTH//2-text_lesson["Back"].w//2, LESSON_BUTTON_TOP_Y+LESSON_BUTTON_HEIGHT//2-text_lesson["Back"].h//2))
        if button.collidepoint(mouse_x, mouse_y):
            draw.rect(screen, COLOR_LESSON_OPTION_OUTLINE_HOVER, (LESSON_BUTTON_LEFT_X, LESSON_BUTTON_TOP_Y, LESSON_BUTTON_WIDTH, LESSON_BUTTON_HEIGHT), LESSON_BUTTON_OUTLINE_THICKNESS)
            if mouse_clicked:
                return PAGE_LESSON

    return PAGE_LESSON_LESSON

def question_init(unit):
    global questions_shuffled, current_question, clicked_option

    current_question = 0

    clicked_option = [-1] * 3
    
    del questions_shuffled

    questions_shuffled = []

    for i in range(6):  # change to 6
        questions_shuffled.append(questions[unit][i])

    shuffle(questions_shuffled)

    del questions_shuffled[4:-1]

def draw_instruction():
    screen.fill(COLOR_WHITE)

    screen.blit(image_instruction.obj, (640-image_instruction.w//2, INSTRUCTION_IMAGE_TOP_Y))

    button = draw.rect(screen, COLOR_INSTRUCTION_OUTLINE, (640-INSTRUCTION_BUTTON_WIDTH//2, INSTRUCTION_BUTTON_TOP_Y, INSTRUCTION_BUTTON_WIDTH, INSTRUCTION_BUTTON_HEIGHT), INSTRUCTION_BUTTON_OUTLINE_THICKNESS)

    screen.blit(text_instruction["Continue"].obj, (640-text_instruction["Continue"].w//2, INSTRUCTION_BUTTON_TOP_Y+INSTRUCTION_BUTTON_HEIGHT//2-text_instruction["Continue"].h//2))

    if button.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_INSTRUCTION_OUTLINE_HOVER, (640-INSTRUCTION_BUTTON_WIDTH//2, INSTRUCTION_BUTTON_TOP_Y, INSTRUCTION_BUTTON_WIDTH, INSTRUCTION_BUTTON_HEIGHT), INSTRUCTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            return instruction_return_page

    return PAGE_INSTRUCTION

def draw_result():
    global clicked_option, current_question
    screen.fill(COLOR_QUESTION_BACKGROUND)

    #QUESTION PROMPT
    screen.blit(questions_shuffled[current_question].q.obj,(QUESTION_PROMPT_LEFT_X+QUESTION_PROMPT_WIDTH//2-questions_shuffled[current_question].q.w//2,QUESTION_PROMPT_TOP_Y+QUESTION_PROMPT_HEIGHT//2-questions_shuffled[current_question].q.h//2))

    screen.blit(questions_shuffled[current_question].opt[0].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[0].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[0].h//2))

    screen.blit(questions_shuffled[current_question].opt[1].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[1].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[1].h//2))

    screen.blit(questions_shuffled[current_question].opt[2].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[2].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[2].h//2))

    screen.blit(questions_shuffled[current_question].opt[3].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH+(QUESTION_OPTION_WIDTH-QUESTION_OPTION_LETTER_WIDTH)//2-questions_shuffled[current_question].opt[3].w//2,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3+QUESTION_OPTION_HEIGHT//2-questions_shuffled[current_question].opt[3].h//2))

    screen.blit(text_question["A"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["A"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT//2-text_question["A"].h//2))

    screen.blit(text_question["B"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["B"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_HEIGHT//2-text_question["B"].h//2))

    screen.blit(text_question["C"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["C"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2+QUESTION_OPTION_HEIGHT//2-text_question["C"].h//2))

    screen.blit(text_question["D"].obj,(QUESTION_OPTION_LEFT_X+QUESTION_OPTION_LETTER_WIDTH//2-text_question["D"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3+QUESTION_OPTION_HEIGHT//2-text_question["D"].h//2))

    draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*2,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*3,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    if clicked_option[current_question] >= 0:
        if clicked_option[current_question] == questions_shuffled[current_question].ans:
            draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_SELCTED,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*clicked_option[current_question],QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)
        else:
            draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE_WRONG,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*clicked_option[current_question],QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_OPTION_OUTLINE_THICKNESS)

    back_rect = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_MARGIN,QUESTION_OPTION_WIDTH,QUESTION_OPTION_HEIGHT),QUESTION_BUTTON_OUTLINE_THICKNESS)

    last_rect = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2,QUESTION_LAST_NEXT_WIDTH,QUESTION_LAST_NEXT_HEIGHT),QUESTION_BUTTON_OUTLINE_THICKNESS)

    next_rect = draw.rect(screen,COLOR_QUESTION_OPTION_OUTLINE,(QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH+QUESTION_OPTION_MARGIN,QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2,QUESTION_LAST_NEXT_WIDTH,QUESTION_LAST_NEXT_HEIGHT),QUESTION_BUTTON_OUTLINE_THICKNESS)

    if back_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_QUESTION_OPTION_OUTLINE_HOVER, (QUESTION_OPTION_LEFT_X, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_MARGIN, QUESTION_OPTION_WIDTH, QUESTION_OPTION_HEIGHT), QUESTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            return PAGE_QUESTION
    elif last_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_QUESTION_OPTION_OUTLINE_HOVER, (QUESTION_OPTION_LEFT_X, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2, QUESTION_LAST_NEXT_WIDTH, QUESTION_LAST_NEXT_HEIGHT), QUESTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            current_question -= 1
            current_question %= 3  # change to 3
    elif next_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen, COLOR_QUESTION_OPTION_OUTLINE_HOVER, (QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH+QUESTION_OPTION_MARGIN, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2, QUESTION_LAST_NEXT_WIDTH, QUESTION_LAST_NEXT_HEIGHT), QUESTION_BUTTON_OUTLINE_THICKNESS)
        if mouse_clicked:
            current_question += 1
            current_question %= 3  # change to 3

    screen.blit(text_question["Back"].obj, (QUESTION_OPTION_LEFT_X+QUESTION_OPTION_WIDTH//2-text_question["Back"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_MARGIN+QUESTION_OPTION_HEIGHT//2-text_question["Back"].h//2))

    screen.blit(text_question["Last"].obj, (QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH//2-text_question["Last"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2+QUESTION_LAST_NEXT_HEIGHT//2-text_question["Last"].h//2))

    screen.blit(text_question["Next"].obj, (QUESTION_OPTION_LEFT_X+QUESTION_LAST_NEXT_WIDTH+QUESTION_OPTION_MARGIN+QUESTION_LAST_NEXT_WIDTH//2-text_question["Next"].w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*4+QUESTION_OPTION_HEIGHT+QUESTION_OPTION_MARGIN*2+QUESTION_LAST_NEXT_HEIGHT//2-text_question["Next"].h//2))

    screen.blit(text_result.obj, (QUESTION_OPTION_LEFT_X+QUESTION_OPTION_WIDTH//2-text_result.w//2, QUESTION_OPTION_TOP_Y+QUESTION_OPTION_HEIGHT*5+QUESTION_LAST_NEXT_HEIGHT+QUESTION_OPTION_MARGIN*3))

    return PAGE_RESULT

while True:
    # get all events
    mouse_clicked = False

    for e in event.get():
        if e.type == pygame.QUIT:
            running = False
            break
        elif e.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = e.pos
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
    if not running:
        break
    
    if page == PAGE_MENU:
        page = draw_menu()
    elif page == PAGE_QUESTION:
        page = draw_question()
    elif page == PAGE_QUESTION_QUESTION:
        page = draw_question_question()
    elif page == PAGE_RESULT:
        page = draw_result()
    elif page == PAGE_LESSON:
        page = draw_lesson()
    elif page == PAGE_LESSON_LESSON:
        page = draw_lesson_lesson()
    elif page == PAGE_INSTRUCTION:
        page = draw_instruction()
    else:
        break

    display.flip()
    timer.tick(60)
    
quit()