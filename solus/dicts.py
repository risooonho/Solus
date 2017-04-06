import pygame
pygame.init()
#Dictionary used in character creation Level:(hp, attack, defence)
#Should be expanded to fit different combos of stats like high defence
# & low attack, high attack, low hp, etc...
CHR_LEVEL = {3: (100, 10, 10), 2: (50, 5, 5), 1: (10, 1, 1)}
PROMPTS = {'create player': 'Enter your name: ',
            'choose difficulty': 'Choose a difficulty.\n3 - Easy\n2 - '\
            'Medium\n1 - Hard\n>>>'}
CLR = {'wht': (255, 255, 255),
        'blk': (0, 0, 0)}
FNT = {'lrg': pygame.font.SysFont(None, 60),
        'med': pygame.font.SysFont(None, 30),
        'sml': pygame.font.SysFont(None, 15),
        'smlx': pygame.font.SysFont(None, 17)}

TXT = {'YES': FNT['smlx'].render('YES', 1, CLR['wht']),
        'NO': FNT['smlx'].render('NO', 1, CLR['wht']),
        'yes': FNT['sml'].render('yes', 1, CLR['blk']),
        'no': FNT['sml'].render('no', 1, CLR['blk'])}
