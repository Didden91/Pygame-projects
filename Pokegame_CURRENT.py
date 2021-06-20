#Imports
import pygame, sys
from pygame.locals import *
import random, time
import pygame_menu
import sqlite3
import os


#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SPEED = 5
SCORE = 0
playerhp = 100
enemyhp = 100
moveused = 0
enemymoveused = ''
rollresult = 0
enemyroll = 0
enemychoice = 0
playerscore = 0
enemyscore = 0
natdexnum = 0
enemynatdexnum = 0
type1 = ''
type2 = ''
damage = 0
enemydamage = 0



conn = sqlite3.connect('pokeDB.sqlite')
cur = conn.cursor()

#############################################
#BATTLEGAME DEFINITIONS

def accroll(accuracy):

    accroll = random.randint(1, 100)
    if accroll <= accuracy:
        rollresult = 1
        return rollresult
    else:
        rollresult = 0
        return rollresult


## returns a random pokemon and what types it has
def callapoke():
    global natdexnum
    #pokemon ID number:
    pnum = random.randint(1, 649)
    type1 = ''
    type2 = ''
    alolan = False

    #get poke from DB:
    pokeinfo = cur.execute('SELECT Pokémon, Type, Type2, NationalDex, LocalDex FROM Pokedex WHERE id = ?' , (pnum, ))
    for i in pokeinfo:
        poke = i[0]
        natdexnum = i[3]
    if i[4] == None:
        alolan = True
    if i[2] == None:
        type1 = i[1]
        type2 = None
    else:
        type1 = i[1]
        type2 = i[2]


    return poke, type1, type2, alolan, natdexnum

def callanenemypoke():
    global enemynatdexnum
    #pokemon ID number:
    pnum = random.randint(1, 649)
    type1 = ''
    type2 = ''
    alolan = False

    #get poke from DB:
    pokeinfo = cur.execute('SELECT Pokémon, Type, Type2, NationalDex, LocalDex FROM Pokedex WHERE id = ?' , (pnum, ))
    for i in pokeinfo:
        poke = i[0]
        enemynatdexnum = i[3]
    if i[4] == None:
        alolan = True
    if i[2] == None:
        type1 = i[1]
        type2 = None
    else:
        type1 = i[1]
        type2 = i[2]


    return poke, type1, type2, alolan, enemynatdexnum

def getpokemoves(type1, type2 = 'None'):
    #Gets 4 random pokemon moves from the DB of only the entered types
    #If there's only 1 type, return 4 moves of that type

    move1correct = 0
    move2correct = 0
    move3correct = 0
    move4correct = 0
    while move1correct == 0:
        m1 = random.randint(1, 826)
        moveone = cur.execute('SELECT Name, Type, PP, Power, Accuracy, Category FROM Pokemoves WHERE id = ?' , (m1, ))
        for i in moveone:
            if i[1] == type1 or i[1] == type2:
                move1correct = 1
                move1 = i
    while move2correct == 0:
        m2 = random.randint(1, 826)
        movetwo = cur.execute('SELECT Name, Type, PP, Power, Accuracy, Category FROM Pokemoves WHERE id = ?' , (m2, ))
        for i in movetwo:
            if i[1] == type1 or i[1] == type2:
                move2correct = 1
                move2 = i
                if move2 == move1:
                    move2correct = 0
    while move3correct == 0:
        m3 = random.randint(1, 826)
        movethree = cur.execute('SELECT Name, Type, PP, Power, Accuracy, Category FROM Pokemoves WHERE id = ?' , (m3, ))
        for i in movethree:
            if i[1] == type1 or i[1] == type2:
                move3correct = 1
                move3 = i
                if move3 == move1 or move3 == move2:
                    move3correct = 0

    while move4correct == 0:
        m4 = random.randint(1, 826)
        movefour = cur.execute('SELECT Name, Type, PP, Power, Accuracy, Category FROM Pokemoves WHERE id = ?' , (m4, ))
        for i in movefour:
            if i[1] == type1 or i[1] == type2:
                move4correct = 1
                move4 = i
                if move4 == move1 or move4 == move2 or move4 == move3:
                    move4correct = 0


    return move1,move2,move3,move4

def getpokestats(name):
    pokemon = ''
    hp = 0
    attack = 0
    defense = 0
    spattack = 0
    spdefense = 0
    speed = 0
    total = 0
    average = 0
    specialform = None

    pokestats = cur.execute('SELECT Pokémon, HP, Attack, Defense, SpAttack, SpDefense, Speed, Total, Average, SpecialForm FROM Pokestats WHERE Pokémon = ?' , (name, ))
    for i in pokestats:
        pokemon = i[0]
        hp = i[1]
        attack = i[2]
        defense = i[3]
        spattack = i[4]
        spdefense = i[5]
        speed = i[6]
        total = i[7]
        average = i[8]
        specialform = i[9]

    return pokemon, hp, attack, defense, spattack, spdefense, speed, total, average, specialform

def playerattack(move, enemyhp):
    ## Takes in a move number and prints the results of the move
    print("Your %s used %s!" % (playerpoke[0],move[0]))
    time.sleep(0.4)
    isCrit = False
    playermissed = False
    sillystring = ':' * move[3]
    print('o==[]%s>' % sillystring)
    time.sleep(1)
    rollresult = accroll(move[4])
    if rollresult == 1:
        #RUN DAMAGE CALCS
        # this length == 4 means there are two types
        if len(enemypoke) == 4:
            damage, crit, effectiveness = playerdamagecalc(move[5],move[3],move[1], playerAttack, playerSpattack, enemyDefense, enemySpdefense, enemypoke[1], enemypoke[2] )
        # otherwise one type
        else:
            damage, crit, effectiveness = playerdamagecalc(move[5],move[3],move[1], playerAttack, playerSpattack, enemyDefense, enemySpdefense, enemypoke[1])

        if crit == 1.5:
            print("A CRITICAL HIT!")
            isCrit = True
        print("Your %s\'s attack dealt %d damage!" % (playerpoke[0],damage))

        enemyhp = enemyhp - damage
        
        if enemyhp < 0:
            enemyhp = 0
    else:
        print("Your %s\'s attack was a MISS! You dealt NO damage!" % playerpoke[0])
        playermissed = True
        effectiveness = 1
        damage = 0
    
    enemy.sprite.get_damage(damage)
    enemy.update()
        
    return enemyhp, isCrit, effectiveness, damage, playermissed

def enemyattack(move, playerhp):
    ## Takes in a move number and prints the results of the move
    movename = move[0]
    enemymissed = False
    EnemyisCrit = False
    print("The enemy %s used %s!" % (enemypoke[0],move[0]))
    time.sleep(0.4)
    sillystring = ':' * move[3]
    print('o==[]%s>' % sillystring)
    time.sleep(1)
    rollresult = accroll(move[4])
    if rollresult == 1:
        #RUN DAMAGE CALC
        # this length == 4 means there are two types
        if len(enemypoke) == 4:
            enemydamage, crit, effectiveness = enemydamagecalc(move[5],move[3],move[1], enemyAttack, enemySpattack, playerDefense, playerSpdefense, playerpoke[1], playerpoke[2] )
        # otherwise one type
        else:
            enemydamage, crit, effectiveness = enemydamagecalc(move[5],move[3],move[1], enemyAttack, enemySpattack, playerDefense, playerSpdefense, playerpoke[1])
        if crit == 1.5:
            print("A CRITICAL HIT!")
            EnemyisCrit = True
        print("Enemy %s\'s attack  dealt %d damage!" % (enemypoke[0], enemydamage))
        playerhp = playerhp - enemydamage
        if playerhp < 0:
            playerhp = 0
    else:
        print("%s\'s attack was a MISS! It dealt NO damage!" % enemypoke[0])
        enemymissed = True
        effectiveness = 1
        enemydamage = 0
        
    player.sprite.get_damage(enemydamage)
    player.update()
    
    return playerhp, EnemyisCrit, effectiveness, enemydamage, movename, enemymissed

def howeffective(movetype, enemytype1, enemytype2 = 'None'):

    effectiveness = 0
    # NORMAL
    if movetype == 'Normal':
        # is it effective AT ALL?
        if enemytype1 == 'Ghost' or enemytype2 == 'Ghost':
            effectiveness = 0
            print('doesnt affect')
        # is it SUPER effective?

        # is it NOT VERY effective?
        elif enemytype1 in ['Rock', 'Steel'] or enemytype2 in ['Rock', 'Steel']:
            effectiveness = 0.5
            print('not very')
        # none of the above means normal damage
        else:
            effectiveness = 1
            print('normal damage')

    # FIGHTING

    if movetype == 'Fighting':
        if enemytype1 == 'Ghost' or enemytype2 == 'Ghost':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 in ['Normal', 'Rock', 'Steel', 'Ice', 'Dark'] or enemytype2 in ['Normal', 'Rock', 'Steel', 'Ice', 'Dark']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Flying', 'Poison', 'Bug', 'Psychic', 'Fairy'] or enemytype2 in ['Flying', 'Poison', 'Bug', 'Psychic', 'Fairy']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # FLYING

    if movetype == 'Flying':
        if enemytype1 in ['Fighting', 'Bug', 'Grass'] or enemytype2 in ['Fighting', 'Bug', 'Grass']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Rock', 'Steel', 'Electric'] or enemytype2 in ['Rock', 'Steel', 'Electric']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # POISON

    if movetype == 'Poison':
        if enemytype1 == 'Steel' or enemytype2 == 'Steel':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 in ['Grass', 'Fairy'] or enemytype2 in ['Grass', 'Fairy']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Poison', 'Ground', 'Rock', 'Ghost'] or enemytype2 in ['Poison', 'Ground', 'Rock', 'Ghost']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # GROUND

    if movetype == 'Ground':
        if enemytype1 == 'Flying' or enemytype2 == 'Flying':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 in ['Poison', 'Rock', 'Steel', 'Fire', 'Electric'] or enemytype2 in ['Poison', 'Rock', 'Steel', 'Fire', 'Electric']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Bug', 'Grass'] or enemytype2 in ['Bug', 'Grass']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # ROCK

    if movetype == 'Rock':
        if enemytype1 in ['Flying', 'Bug', 'Fire', 'Ice'] or enemytype2 in ['Flying', 'Bug', 'Fire', 'Ice']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Fighting', 'Ground', 'Steel'] or enemytype2 in ['Fighting', 'Ground', 'Steel']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # BUG
    if movetype == 'Bug':
        if enemytype1 in ['Grass', 'Psychic', 'Dark'] or enemytype2 in ['Grass', 'Psychic', 'Dark']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Fighting', 'Flying', 'Poison', 'Ghost', 'Steel', 'Fire', 'Fairy'] or enemytype2 in ['Fighting', 'Flying', 'Poison', 'Ghost', 'Steel', 'Fire', 'Fairy']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # GHOST

    if movetype == 'Ghost':
        if enemytype1 == 'Normal' or enemytype2 == 'Normal':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 in ['Ghost', 'Psychic'] or enemytype2 in ['Ghost', 'Psychic']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 == 'Dark' or enemytype2 == 'Dark':
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # STEEL

    if movetype == 'Steel':
        if enemytype1 in ['Rock', 'Ice', 'Fairy'] or enemytype2 in ['Rock', 'Ice', 'Fairy']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Steel', 'Fire', 'Water', 'Electric'] or enemytype2 in ['Steel', 'Fire', 'Water', 'Electric']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # FIRE

    if movetype == 'Fire':
        if enemytype1 in ['Bug', 'Steel', 'Grass', 'Ice'] or enemytype2 in ['Bug', 'Steel', 'Grass', 'Ice']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Rock', 'Fire', 'Water', 'Dragon'] or enemytype2 in ['Rock', 'Fire', 'Water', 'Dragon']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # WATER

    if movetype == 'Water':
        if enemytype1 in ['Ground', 'Rock', 'Fire'] or enemytype2 in ['Ground', 'Rock', 'Fire']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Water', 'Grass', 'Dragon'] or enemytype2 in ['Water', 'Grass', 'Dragon']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # GRASS
    if movetype == 'Grass':
        if enemytype1 in ['Ground', 'Rock', 'Water'] or enemytype2 in ['Ground', 'Rock', 'Water']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Flying', 'Poison', 'Bug', 'Steel', 'Fire', 'Grass', 'Dragon'] or enemytype2 in ['Flying', 'Poison', 'Bug', 'Steel', 'Fire', 'Grass', 'Dragon']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # ELECTRIC

    if movetype == 'Electric':
        if enemytype1 == 'Ground' or enemytype2 == 'Ground':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 in ['Flying', 'Water'] or enemytype2 in ['Flying', 'Water']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Grass', 'Electric', 'Dragon'] or enemytype2 in ['Grass', 'Electric', 'Dragon']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # PSYCHIC

    if movetype == 'Psychic':
        if enemytype1 == 'Dark' or enemytype2 == 'Dark':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 in ['Fighting', 'Poison'] or enemytype2 in ['Fighting', 'Poison']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Steel', 'Psychic'] or enemytype2 in ['Steel', 'Psychic']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # ICE

    if movetype == 'Ice':
        if enemytype1 in ['Flying', 'Ground', 'Grass', 'Dragon'] or enemytype2 in ['Flying', 'Ground', 'Grass', 'Dragon']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Steel', 'Fire', 'Water', 'Ice'] or enemytype2 in ['Steel', 'Fire', 'Water', 'Ice']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # DRAGON

    if movetype == 'Dragon':
        if enemytype1 == 'Fairy' or enemytype2 == 'Fairy':
            effectiveness = 0
            print('doesnt affect')
        elif enemytype1 == 'Dragon' or enemytype2 == 'Dragon':
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 == 'Steel' or enemytype2 == 'Steel':
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # DARK
    if movetype == 'Dark':
        if enemytype1 in ['Ghost', 'Psychic'] or enemytype2 in ['Ghost', 'Psychic']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Fighting', 'Dark', 'Fairy'] or enemytype2 in ['Fighting', 'Dark', 'Fairy']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    # FAIRY

    if movetype == 'Fairy':
        if enemytype1 in ['Fighting', 'Dragon', 'Dark'] or enemytype2 in ['Fighting', 'Dragon', 'Dark']:
            effectiveness = 2
            print('VERY effective')
        elif enemytype1 in ['Poison', 'Steel', 'Fire'] or enemytype2 in ['Poison', 'Steel', 'Fire']:
            effectiveness = 0.5
            print('not very')
        else:
            effectiveness = 1
            print('normal damage')

    return effectiveness

def playerdamagecalc(movecategory, movepower, movetype, userattack, userspattack, opponentdefense, opponentspdefense, enemytype1, enemytype2 = 'None'):
    damagerange = random.uniform(0.85, 1.00)
    crit = random.randint(1, 16)
    if crit == 16:
        crit = 1.5
    else:
        crit = 1.0
    if enemytype2 == None:
        effectiveness = howeffective(movetype, enemytype1)  
    else:
        effectiveness = howeffective(movetype, enemytype1, enemytype2)  


    if movecategory == 'Physical':
        print('used a PHYSICAL move')
        #The 50 is the level, for now all pokes are level 50
        #damage pre modifiers:
        damage = ((2 * 50 / 5 + 2) * movepower * userattack / opponentdefense / 50 + 2)
        #now apply modifiers
        damage = damage * crit * damagerange * effectiveness

    elif movecategory == 'Special':
        print('used a SPECIAL move')
        damage = ((2 * 50 / 5 + 2) * movepower * userspattack / opponentspdefense / 50 + 2)
        damage = damage * crit * damagerange * effectiveness
    else:
        print('used a STATUS move')
        damage = 0
    return damage, crit, effectiveness


def enemydamagecalc(movecategory, movepower, movetype, userattack, userspattack, opponentdefense, opponentspdefense, enemytype1, enemytype2 = 'None'):
    damagerange = random.uniform(0.85, 1.00)
    crit = random.randint(1, 16)
    if crit == 16:
        crit = 1.5
    else:
        crit = 1.0
    effectiveness = howeffective(movetype, enemytype1, enemytype2 = 'None')


    if movecategory == 'Physical':
        print('used a PHYSICAL move')
        #The 50 is the level, for now all pokes are level 50
        #damage pre modifiers:
        damage = ((2 * 50 / 5 + 2) * movepower * userattack / opponentdefense / 50 + 2)
        #now apply modifiers
        damage = damage * crit * damagerange * effectiveness

    elif movecategory == 'Special':
        print('used a SPECIAL move')
        damage = ((2 * 50 / 5 + 2) * movepower * userspattack / opponentspdefense / 50 + 2)
        damage = damage * crit * damagerange * effectiveness
    else:
        print('used a STATUS move')
        damage = 0
    return damage, crit, effectiveness




#END OF BATTLEGAME DEFINITIONS
############################################


#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
game_over2 = font_medium.render("Your score was: ", True, BLACK)

backgroundtop = pygame.image.load("pokebackground.png")
backgroundbottom = pygame.image.load("pokebackground2.png")
icon = pygame.image.load("icon.jpg")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((960,640))
# HBSURF = pygame.display.set_mode((80,80))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Pokemans")
pygame.display.set_icon(icon)

     
   
#Defining the move buttons (have to be seperate):
    
def move1():
    global enemyhp
    global moveused
    global playermove1
    global playerpoke
    global damage
    
    #Check of er een widget (knop) met opgegeven naam bestaat
    if postmovemenu1.get_widget('moveusedbutton') != None:
        postmovemenu1.remove_widget(postmovemenu1.get_widget('moveusedbutton'))
        print('knop bestaat al, deleting...')
    else:
        print('knop bestaat nog niet')
        
    
    print('chosen move 1')
    moveused = 1
    print('KIJK HIER, DE playerattack returned dit =', playerattack(playermove1, enemyhp))
    enemyhp, crit, effectiveness, damage, playermissed = playerattack(playermove1, enemyhp)
    print('DAMAGE IN DE VARIABLE IS NU:', damage)
    if crit == True:
        criticalhitmenu.toggle()
    if effectiveness == 0:
        doesntaffectmenu.toggle()
    if effectiveness == 0.5:
        notveryeffectivemenu.toggle()
    if effectiveness == 2:
        supereffectivemenu.toggle()
    if playermissed == True:
        movemissmenu.toggle()
    #End of choosing a move is toggling current menu off and next one on
    movemenu.toggle()
    moveusedstring = '%s used %s!' % (playerpoke[0], playermove1[0])
    postmovemenu1.add_button(moveusedstring, postmovemenu1.toggle, button_id='moveusedbutton')
    
    
    
def move2():
    global enemyhp
    global moveused
    global playermove2
    global playerpoke
    global damage
    #Check of er een widget (knop) met opgegeven naam bestaat
    if postmovemenu1.get_widget('moveusedbutton') != None:
        postmovemenu1.remove_widget(postmovemenu1.get_widget('moveusedbutton'))
        print('knop bestaat al, deleting...')
    else:
        print('knop bestaat nog niet')
        
    
    print('chosen move 2')
    moveused = 2
    enemyhp, crit, effectiveness, damage, playermissed = playerattack(playermove2, enemyhp)
    print('DAMAGE IN DE VARIABLE IS NU:', damage)
    if crit == True:
        criticalhitmenu.toggle()
    if effectiveness == 0:
        doesntaffectmenu.toggle()
    if effectiveness == 0.5:
        notveryeffectivemenu.toggle()
    if effectiveness == 2:
        supereffectivemenu.toggle()
    if playermissed == True:
        movemissmenu.toggle()
    movemenu.toggle()
    moveusedstring = '%s used %s!' % (playerpoke[0], playermove2[0])
    postmovemenu1.add_button(moveusedstring, postmovemenu1.toggle, button_id='moveusedbutton')
    
    
def move3():
    global enemyhp
    global moveused
    global playermove3
    global playerpoke
    global damage
    #Check of er een widget (knop) met opgegeven naam bestaat
    if postmovemenu1.get_widget('moveusedbutton') != None:
        postmovemenu1.remove_widget(postmovemenu1.get_widget('moveusedbutton'))
        print('knop bestaat al, deleting...')
    else:
        print('knop bestaat nog niet')
        
    
    print('chosen move 3')
    moveused = 3
    enemyhp, crit, effectiveness, damage, playermissed = playerattack(playermove3, enemyhp)
    print('DAMAGE IN DE VARIABLE IS NU:', damage)
    if crit == True:
        criticalhitmenu.toggle()
    if effectiveness == 0:
        doesntaffectmenu.toggle()
    if effectiveness == 0.5:
        notveryeffectivemenu.toggle()
    if effectiveness == 2:
        supereffectivemenu.toggle()
    if playermissed == True:
        movemissmenu.toggle()
    movemenu.toggle()
    moveusedstring = '%s used %s!' % (playerpoke[0], playermove3[0])
    postmovemenu1.add_button(moveusedstring, postmovemenu1.toggle, button_id='moveusedbutton')
    
def move4():
    global enemyhp
    global moveused
    global playermove4
    global playerpoke
    global damage
    #Check of er een widget (knop) met opgegeven naam bestaat
    if postmovemenu1.get_widget('moveusedbutton') != None:
        postmovemenu1.remove_widget(postmovemenu1.get_widget('moveusedbutton'))
        print('knop bestaat al, deleting...')
    else:
        print('knop bestaat nog niet')
        
    
    print('chosen move 4')
    moveused = 4
    enemyhp, crit, effectiveness, damage, playermissed = playerattack(playermove4, enemyhp)
    print('DAMAGE IN DE VARIABLE IS NU:', damage)
    if crit == True:
        criticalhitmenu.toggle()
    if effectiveness == 0:
        doesntaffectmenu.toggle()
    if effectiveness == 0.5:
        notveryeffectivemenu.toggle()
    if effectiveness == 2:
        supereffectivemenu.toggle()
    if playermissed == True:
        movemissmenu.toggle()
    movemenu.toggle()
    moveusedstring = '%s used %s!' % (playerpoke[0], playermove4[0])
    postmovemenu1.add_button(moveusedstring, postmovemenu1.toggle, button_id='moveusedbutton')
    

    

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        global enemynatdexnum
        super().__init__() 
        enemyfilenamestring = '/Users/Ivo/Desktop/pygame/Sprites/' + str(enemynatdexnum) +'.png'
        self.image = pygame.image.load(enemyfilenamestring)
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (590, 80))
        
        # return a width and height of an image
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
        
        ###############################
        #HERE IS THE HEALTH BAR:
        self.enemy_current_health = 200
        self.enemy_target_health = 500
        self.enemy_max_health = 1000
        self.enemy_health_bar_length = 400
        self.enemy_health_ratio = self.enemy_max_health / self.enemy_health_bar_length
        self.enemy_health_change_speed = 5
    
    def get_damage(self,amount):
        if self.enemy_target_health > 0:
            self.enemy_target_health -= amount
        if self.enemy_target_health < 0:
            self.enemy_target_health = 0

    def get_health(self,amount):
        if self.enemy_target_health < self.enemy_max_health:
            self.enemy_target_health += amount
        if self.enemy_target_health > self.enemy_max_health:
            self.enemy_target_health = self.enemy_max_health

    def update(self):
        self.advanced_health()    
        
    def advanced_health(self):
        enemy_health_bar_width =  self.enemy_current_health / self.enemy_health_ratio
        transition_width = 0
        transition_color = (255,0,0)

        if self.enemy_current_health < self.enemy_target_health:
            self.enemy_current_health += self.enemy_health_change_speed
            transition_width = int((self.enemy_target_health - self.enemy_current_health) / self.enemy_health_ratio)
            transition_color = (255,255,0)

        if self.enemy_current_health > self.enemy_target_health:
            enemy_health_bar_width = self.enemy_target_health / self.enemy_health_ratio
            self.enemy_current_health -= self.enemy_health_change_speed 
            transition_width = abs((self.enemy_target_health - self.enemy_current_health) / self.enemy_health_ratio)
            transition_color = (255,255,0)

        
        enemy_health_bar = pygame.Rect(10,45,enemy_health_bar_width,25)
        enemy_transition_bar = pygame.Rect(enemy_health_bar.right,45,transition_width,25)
        
        pygame.draw.rect(DISPLAYSURF,(255,0,0),enemy_health_bar)
        pygame.draw.rect(DISPLAYSURF,transition_color,enemy_transition_bar)    
        pygame.draw.rect(DISPLAYSURF,(255,255,255),(10,45,self.enemy_health_bar_length,25),4)       

        
    
    
      # def move(self):
      #   global SCORE
      #   global playerhp
      #   self.rect.move_ip(0,SPEED)
      #   if (self.rect.bottom > 600):
      #       SCORE += 1
      #       self.rect.top = 0
      #       self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
      #   elif pygame.sprite.spritecollideany(P1, enemies):
      #       self.rect.top = 0
      #       self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
      #       playerhp -= 10
      #       pygame.mixer.Sound('crash.wav').play()
            
     


class Player(pygame.sprite.Sprite):
    def __init__(self):
        global natdexnum
        super().__init__() 
        filenamestring = '/Users/Ivo/Desktop/pygame/Sprites/back/' + str(natdexnum) +'.png'
        print('FILENAMETEST:',filenamestring)
        self.image = pygame.image.load(filenamestring)
        self.surf = pygame.Surface((80, 75))
        self.rect = self.surf.get_rect(center = (140, 280))
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
        # draw bigger image to screen at x=100 y=100 position
        # self.surf.blit(self.bigger_img, [80,75])
        
         ###############################
        #HERE IS THE HEALTH BAR:
        self.current_health = 200
        self.target_health = 500
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 5

    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self):
        self.advanced_health()

    def advanced_health(self):
        health_bar_width =  self.current_health / self.health_ratio
        transition_width = 0
        transition_color = (255,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)

        if self.current_health > self.target_health:
            health_bar_width = self.target_health / self.health_ratio
            self.current_health -= self.health_change_speed 
            transition_width = abs((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (255,255,0)

        health_bar = pygame.Rect(520,380,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,380,transition_width,25)
        
        pygame.draw.rect(DISPLAYSURF,(255,0,0),health_bar)
        pygame.draw.rect(DISPLAYSURF,transition_color,transition_bar)    
        pygame.draw.rect(DISPLAYSURF,(255,255,255),(520,380,self.health_bar_length,25),4)  

            
        
       
    # def move(self):
    #     pressed_keys = pygame.key.get_pressed()
    #    #if pressed_keys[K_UP]:
    #         #self.rect.move_ip(0, -5)
    #    #if pressed_keys[K_DOWN]:
    #         #self.rect.move_ip(0,5)
        
    #     if self.rect.left > 0:
    #           if pressed_keys[K_LEFT]:
    #               self.rect.move_ip(-5, 0)
    #     if self.rect.right < SCREEN_WIDTH:        
    #           if pressed_keys[K_RIGHT]:
    #               self.rect.move_ip(5, 0)
    
    # def playerhpbar():
    #      global playerhp
    #      return playerhp
     

##### Blank background
def draw_background():
    
    
    DISPLAYSURF.blit(backgroundtop, (0,0))
    DISPLAYSURF.blit(backgroundbottom, (0,450))
    
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    healthleft = font_small.render(str(playerhp), True, BLACK)
    DISPLAYSURF.blit(healthleft, (10,30))
    

##### Background + enemy sprite
def draw_background1():
    
    DISPLAYSURF.blit(backgroundtop, (0,0))
    DISPLAYSURF.blit(backgroundbottom, (0,450))
    
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    healthleft = font_small.render(str(playerhp), True, BLACK)
    DISPLAYSURF.blit(healthleft, (10,30))
    
    for entity in enemy:  
        DISPLAYSURF.blit(entity.bigger_img, entity.rect)  
    enemy.update()
 
###### Background + enemy and player sprite
def draw_background2():

    DISPLAYSURF.blit(backgroundtop, (0,0))
    DISPLAYSURF.blit(backgroundbottom, (0,450))
    
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    healthleft = font_small.render(str(playerhp), True, BLACK)
    DISPLAYSURF.blit(healthleft, (10,30))
    
    for entity in enemy:  
        DISPLAYSURF.blit(entity.bigger_img, entity.rect)
    for entity in player:  
        DISPLAYSURF.blit(entity.bigger_img, entity.rect)
    enemy.update()
    player.update()
    
#Creating a moveresultmenu:
def createmoveresultmenu():
    global moveresultmenu
    moveresultmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Outcome:',
            width=960)   
    #Creating buttons which detail move results
    
    moveresultstring = 'You dealt %d damage!' % damage
    moveresultmenu.add_button(moveresultstring, enemyturn)  
    
def createenemymoveresultmenu():
    global enemymoveresultmenu
    enemymoveresultmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Outcome:',
            width=960)   
    #Creating buttons which detail move results
    
    enemymoveresultstring = 'Enemy %s dealt %d damage!' % (enemypoke[0], enemydamage)
    enemymoveresultmenu.add_button(enemymoveresultstring, enemymoveresultmenu.toggle)
              

#creating a enemy move menu
def createenemymovemenu():
    global enemymovemenu
    enemymovemenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Enemy move!',
            width=960)
    
    #creating button for enemy move menu
    enemymovestring = 'The enemy %s used %s!' % (enemypoke[0], enemymoveused)
    enemymovemenu.add_button(enemymovestring, enemymovemenu.toggle)
    
def enemyturn():
    #This function is called at the press of the player turn result button.
    #It processes the enemies turn before it is shown
    # The end of the function is the toggle to turn OFF the player turn result menu, so it can move on to the next thing
    
    global playerhp
    global enemymove1
    global enemymove2
    global enemymove3
    global enemymove4
    global enemymove1PP
    global enemymove2PP
    global enemymove3PP
    global enemymove4PP
    global enemypoke
    global enemydamage
    global enemymoveused
    
    while True:
        enemychoice = random.randint(1, 4)
        if enemychoice == 1 and enemymove1PP <= 0:
            continue
        if enemychoice == 2 and enemymove2PP <= 0:
            continue
        if enemychoice == 3 and enemymove3PP <= 0:
            continue
        if enemychoice == 4 and enemymove4PP <= 0:
            continue
        else:
            break

    if enemychoice == 1:
        playerhp, EnemyisCrit, effectiveness, enemydamage, movename, enemymissed = enemyattack(enemymove1, playerhp)
        enemymove1PP -= 1
        enemymoveused = enemymove1[0]
    elif enemychoice == 2:
        playerhp, EnemyisCrit, effectiveness, enemydamage, movename, enemymissed = enemyattack(enemymove2, playerhp)
        enemymove2PP -= 1
        enemymoveused = enemymove2[0]
    elif enemychoice == 3:
        playerhp, EnemyisCrit, effectiveness, enemydamage, movename, enemymissed = enemyattack(enemymove3, playerhp)
        enemymove3PP -= 1
        enemymoveused = enemymove3[0]
    else:
        playerhp, EnemyisCrit, effectiveness, enemydamage, movename, enemymissed = enemyattack(enemymove4, playerhp)
        enemymove4PP -= 1
        enemymoveused = enemymove4[0]
        
    #toggles for effect menu's:
        
    if EnemyisCrit == True:
        enemycriticalhitmenu.toggle()
    if effectiveness == 0:
        enemydoesntaffectmenu.toggle()
    if effectiveness == 0.5:
        enemynotveryeffectivemenu.toggle()
    if effectiveness == 2:
        enemysupereffectivemenu.toggle()
    if enemymissed == True:
        enemymovemissmenu.toggle()
    
        
    #toggle to turn off the moveresult menu, as end of the enemyturn() function        
    moveresultmenu.toggle()
    

print('GAME INITIALIZED')


#Game Loop
while True:
    print('STARTING GAME LOOP')
    ##############################################################
    #BATTLEGAME INITIALIZATION
    
    # Initialize enemy pokemon
    enemypoke = callanenemypoke()
    print('enemypoke:',enemypoke)
    
     # Initialize player pokemon
    playerpoke = callapoke()
    print('player: ',playerpoke)
    
    #Setting up Sprites        
    
    
    #Creating Sprites Groups
    player = pygame.sprite.GroupSingle(Player())
    enemy = pygame.sprite.GroupSingle(Enemy())

    
    # Adding a new User event 
    # INC_SPEED = pygame.USEREVENT + 1
    # pygame.time.set_timer(INC_SPEED, 1000)

    #get enemy pokemon stats
    enemystats = getpokestats(enemypoke[0])

    #get enemy pokemon moves, based on type(s)
    keeplooping = 1
    while keeplooping == 1:
        if len(enemypoke) == 4:
        #two types
            type1 = enemypoke[1]
            type2 = enemypoke[2]
            allenemymoves = getpokemoves(type1, type2)
        else:
        #one type
            type1 = enemypoke[1]
            allenemymoves = getpokemoves(type1)

    #Place enemy moves in mnemonic variable:

        enemymove1 = allenemymoves[0]
        enemymove2 = allenemymoves[1]
        enemymove3 = allenemymoves[2]
        enemymove4 = allenemymoves[3]



    # insert a check here for move power (move power is in slot 3, so for example: enemymove1[3])
    #if power is == 0 in all four moves, give new moves

        if enemymove1[3] == 0 and enemymove2[3] == 0 and enemymove3[3] == 0 and enemymove4[3] == 0:
            keeplooping = 1
        else:
            keeplooping = 0


   

    #get player pokemon stats

    playerstats = getpokestats(playerpoke[0])



    #get player pokemon moves, based on type(s)

    keeplooping = 1
    while keeplooping == 1:

        if len(playerpoke) == 4:
        #two types
            type1 = playerpoke[1]
            type2 = playerpoke[2]
            allplayermoves = getpokemoves(type1, type2)
        else:
        #one type
            type1 = playerpoke[1]
            allplayermoves = getpokemoves(type1)

    #Place player moves in mnemonic variable:

        playermove1 = allplayermoves[0]
        playermove2 = allplayermoves[1]
        playermove3 = allplayermoves[2]
        playermove4 = allplayermoves[3]




    # insert a check here for move power (move power is in slot 3, so for example: playermove1[3])
    #if power is == 0 in all four moves, give new moves

        if playermove1[3] == 0 and playermove2[3] == 0 and playermove3[3] == 0 and playermove4[3] == 0:
            # print("ALL YOUR MOVES WERE 0 POWER, LOOK!")
            # printmoveformatted(playermove1, 1)
            # printmoveformatted(playermove2, 2)
            # printmoveformatted(playermove3, 3)
            # printmoveformatted(playermove4, 4)
            # print("IMMA GIVE YOU NEW ONES :)")
            keeplooping = 1
        else:
            keeplooping = 0


    #Get PP from enemymoves and assign to seperate variable so it becomes mutable:
    enemymove1PP = enemymove1[2]
    enemymove2PP = enemymove2[2]
    enemymove3PP = enemymove3[2]
    enemymove4PP = enemymove4[2]

    #Get PP from playermoves and assign to seperate variable so it becomes mutable:
    playermove1PP = playermove1[2]
    playermove2PP = playermove2[2]
    playermove3PP = playermove3[2]
    playermove4PP = playermove4[2]

    #Get all enemy stats from enemystats and place in variables:

    enemyHP = enemystats[1]
    enemyAttack = enemystats[2]
    enemyDefense = enemystats[3]
    enemySpattack = enemystats[4]
    enemySpdefense = enemystats[5]
    enemySpeed = enemystats[6]
    enemyStattotal = enemystats[7]
    enemyStataverage = enemystats[8]
    enemySpecialform = enemystats[9]


    #Get all player stats from playerstats and place in variables:
    playerHP = playerstats[1]
    playerAttack = playerstats[2]
    playerDefense = playerstats[3]
    playerSpattack = playerstats[4]
    playerSpdefense = playerstats[5]
    playerSpeed = playerstats[6]
    playerStattotal = playerstats[7]
    playerStataverage = playerstats[8]
    playerSpecialform = playerstats[9]

    #starting HP:
    enemyhp = 300
    playerhp = 300
    
    
    #END OF BATTLEGAME INITIALIZATION
    ##########################################################################
    
    
    
    ##########################################################################
    #MENU INITIALIZATION
    
    #creating a first 'menu' for wild pokemon appeared
    openingmenu = pygame_menu.Menu(
        columns=1,
        height=190,
        menu_position=(100,100),
        onclose=pygame_menu.events.EXIT,
        rows=1,
        theme=pygame_menu.themes.THEME_GREEN,
        title='Prompt',
        width=960)

    #creating button for openingmenu:
    enemypokestring = 'A wild %s appeared!' % (enemypoke[0])
    openingmenu.add_button(enemypokestring, openingmenu.toggle)
    
    
    # creating a second menu for YOU SENT OUT:
        
    yousentmenu = pygame_menu.Menu(
        columns=1,
        height=190,
        menu_position=(100,100),
        onclose=pygame_menu.events.EXIT,
        rows=1,
        theme=pygame_menu.themes.THEME_GREEN,
        title='Prompt',
        width=960)

    #creating button for openingmenu:
    playerpokestring = 'You sent out %s!' % (playerpoke[0])
    yousentmenu.add_button(playerpokestring, yousentmenu.toggle)

    #creating a move menu:
    
    movemenu = pygame_menu.Menu(
            columns=2,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=2,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Choose a move!',
            width=960)

    #creating buttons for menu:
    movemenu.add_button(playermove1[0], move1)
    movemenu.add_button(playermove3[0], move3)
    movemenu.add_button(playermove2[0], move2)
    movemenu.add_button(playermove4[0], move4)
    
            
       
    #creating a postmovemenu1:
    postmovemenu1 = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Attack:',
            width=960)
    
      
    movemissmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    movemissstring = '%s\'s attack missed!' % playerpoke[0]
    movemissmenu.add_button(movemissstring, movemissmenu.toggle)
    
    enemymovemissmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    enemymovemissstring = '%s\'s attack missed!' % enemypoke[0]
    enemymovemissmenu.add_button(enemymovemissstring, enemymovemissmenu.toggle)
    
    
    criticalhitmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    
    criticalhitmenu.add_button('A CRITICAL HIT!', criticalhitmenu.toggle)
    
    enemycriticalhitmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    
    enemycriticalhitmenu.add_button('A CRITICAL HIT!', enemycriticalhitmenu.toggle)
    
    notveryeffectivemenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    
    notveryeffectivemenu.add_button('It\'s not very effective...', notveryeffectivemenu.toggle)
    
    enemynotveryeffectivemenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    
    enemynotveryeffectivemenu.add_button('It\'s not very effective...', enemynotveryeffectivemenu.toggle)
    
    supereffectivemenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    
    supereffectivemenu.add_button('It\'s super effective!', supereffectivemenu.toggle)
    
    enemysupereffectivemenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    
    enemysupereffectivemenu.add_button('It\'s super effective!', enemysupereffectivemenu.toggle)
    
    doesntaffectmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    doesntaffectstring = 'It doesn\'t affect the enemy %s' % enemypoke[0]
    doesntaffectmenu.add_button(doesntaffectstring, doesntaffectmenu.toggle)
    
    enemydoesntaffectmenu = pygame_menu.Menu(
            columns=1,
            height=190,
            menu_position=(100,100),
            onclose=pygame_menu.events.EXIT,
            rows=1,
            theme=pygame_menu.themes.THEME_GREEN,
            title='Effect:',
            width=960)
    enemydoesntaffectstring = 'It doesn\'t affect your %s' % playerpoke[0]
    enemydoesntaffectmenu.add_button(doesntaffectstring, enemydoesntaffectmenu.toggle)
    
    
    
    


    # END OF MENU INITIALIZATION
    ##########################################################################
    
    #run opening menu
    #First disable effect menu's:
    movemissmenu.toggle()
    criticalhitmenu.toggle()
    notveryeffectivemenu.toggle()
    supereffectivemenu.toggle()
    doesntaffectmenu.toggle()
    enemymovemissmenu.toggle()
    enemycriticalhitmenu.toggle()
    enemynotveryeffectivemenu.toggle()
    enemysupereffectivemenu.toggle()
    enemydoesntaffectmenu.toggle()
    
    
    while openingmenu.is_enabled():
    
       
        print('currently in opening menu')
        openingmenu.mainloop(DISPLAYSURF, bgfun=draw_background)
       
        print('STILL in opening menu')
        
        pygame.display.update()
        
    while yousentmenu.is_enabled():
    
        yousentmenu.mainloop(DISPLAYSURF, bgfun=draw_background1)
        pygame.display.update()
        
    while enemyhp > 0 and playerhp > 0:                

        while movemenu.is_enabled():
            print('Starting MOVEmenu')
            movemenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while postmovemenu1.is_enabled():
            print('Starting postmovemenu1')
            postmovemenu1.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while movemissmenu.is_enabled():
            print('Starting move miss menu')
            movemissmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while criticalhitmenu.is_enabled():
            print('Starting critical hit menu')
            criticalhitmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while notveryeffectivemenu.is_enabled():
            print('Starting not very effective menu')
            notveryeffectivemenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while supereffectivemenu.is_enabled():
            print('Starting super effective menu')
            supereffectivemenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while doesntaffectmenu.is_enabled():
            print('Starting doesnt affect menu')
            doesntaffectmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        createmoveresultmenu()
        while moveresultmenu.is_enabled():
            print('Starting moveresultmenu')
            moveresultmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
        
        createenemymovemenu()
        while enemymovemenu.is_enabled():
            enemymovemenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while enemymovemissmenu.is_enabled():
            print('Starting enemy move miss menu')
            enemymovemissmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while enemycriticalhitmenu.is_enabled():
            print('Starting enemy critical hit menu')
            enemycriticalhitmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while enemynotveryeffectivemenu.is_enabled():
            print('Starting enemy not very effective menu')
            enemynotveryeffectivemenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while enemysupereffectivemenu.is_enabled():
            print('Starting enemy super effective menu')
            enemysupereffectivemenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        while enemydoesntaffectmenu.is_enabled():
            print('Starting enemy doesnt affect menu')
            enemydoesntaffectmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
        
        createenemymoveresultmenu()
        while enemymoveresultmenu.is_enabled():
            print('Starting enemymoveresultmenu')
            enemymoveresultmenu.mainloop(DISPLAYSURF, bgfun=draw_background2)
            pygame.display.update()
            
        
            
            
        
        #re-enable menu's for when the loop starts again:    
        movemenu.toggle()
        postmovemenu1.toggle()
        enemymovemenu.toggle()
        
                    

    #Cycles through all events occuring  
    for event in pygame.event.get():
         
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                print("Player pressed enter!")
            elif event.key == pygame.K_a:
                print("Player moved left!")
            elif event.key == pygame.K_s:
                print("Player moved down!")
            elif event.key == pygame.K_d:
                print("Player moved right!")
            
            
            
   
    
        
    #run menu:
    
    

    #Moves and Re-draws all Sprites
    # for entity in all_sprites:
    #     DISPLAYSURF.blit(entity.image, entity.rect)
    #     entity.move()

    #To be run if collision occurs between Player and Enemy
    # if pygame.sprite.spritecollideany(P1, enemies):
          
    #       pygame.mixer.Sound('crash.wav').play()
    #       playerhp -= 10
    #       time.sleep(0.2)
    #       pygame.display.update()
    #       # for entity in enemies:
    #       #     entity.kill() 
              
              
    #       pygame.display.update()
          
    # if playes loses:        
    if playerhp <= 0:               
          DISPLAYSURF.fill(RED)
          scores = font_medium.render(str(SCORE), True, BLACK)
          DISPLAYSURF.blit(game_over, (30,250))
          DISPLAYSURF.blit(game_over2, (15,350))
          DISPLAYSURF.blit(scores, (340,352))
          
          pygame.display.update()
          for entity in enemy:
              entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
    # if enemy loses
    else:
        DISPLAYSURF.fill(BLUE)
        pygame.display.update()
    pygame.display.update()
    FramePerSec.tick(FPS)
    

