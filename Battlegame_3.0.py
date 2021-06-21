from art import *
import random
import time
import sqlite3

rollresult = 0
strongaccroll = 0
carefulaccroll = 0
recklessaccroll = 0
enemyroll = 0
enemychoice = 0
playerscore = 0
enemyscore = 0
par = list()
cacount = 0
cahit = 0
camiss = 0
sacount = 0
sahit = 0
samiss = 0
racount = 0
ramiss = 0
rahit = 0
type1 = ''
type2 = ''

def accroll(accuracy):

    accroll = random.randint(1, 100)
    if accroll <= accuracy:
        rollresult = 1
        return rollresult
    else:
        rollresult = 0
        return rollresult

def logandprint(strinput,fhandname):
    print(strinput)
    fhandname.write(strinput)
    fhandname.write("\n")



randfilenumb = time.ctime()
randfilenumb = randfilenumb.replace(":","")
randfilename = randfilenumb + ' log.txt'
fhand = open(randfilename, 'w')

fhand.write("Start of new log:\n")

conn = sqlite3.connect('pokeDB.sqlite')
cur = conn.cursor()



## returns a random pokemon and what types it has
def callapoke():

    #pokemon ID number:
    pnum = random.randint(1, 876)
    type1 = ''
    type2 = ''
    alolan = False

    #get poke from DB:
    pokeinfo = cur.execute('SELECT Pokémon, Type, Type2, LocalDex FROM Pokedex WHERE id = ?' , (pnum, ))
    for i in pokeinfo:
        poke = i[0]
    if i[3] == None:
        alolan = True
    if i[2] == None:
        type1 = i[1]
        type2 = None
    else:
        type1 = i[1]
        type2 = i[2]


    return poke, type1, type2, alolan

# def randomizepokeletters(poke):



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



def printmoveformatted(move, movenum, currentpp):
    ## Takes in which move, which move number and the current value of the PP variable of that move
    ## Checks length of move and prints out properly formatted line
    if len(move[0]) < 10:
        if len(move[1]) < 7:
            print(movenum,': ', move[0], '\t\t\t[Type:', move[1]+']','\t\t\t[PP:',currentpp,'/', str(move[2])+']', '\t\t[Power:', str(move[3])+']', '\t\t[Accuracy:', str(move[4])+']', '\t\t[Category:', str(move[5])+']')
        else:
            print(movenum,': ', move[0], '\t\t\t[Type:', move[1]+']','\t\t[PP:',currentpp,'/', str(move[2])+']', '\t\t[Power:', str(move[3])+']', '\t\t[Accuracy:', str(move[4])+']', '\t\t[Category:', str(move[5])+']')
    elif len(move[0]) <= 19:
        if len(move[1]) < 7:
            print(movenum,': ', move[0], '\t\t[Type:', move[1]+']','\t\t\t[PP:',currentpp,'/', str(move[2])+']', '\t\t[Power:', str(move[3])+']', '\t\t[Accuracy:', str(move[4])+']', '\t\t[Category:', str(move[5])+']')
        else:
            print(movenum,': ', move[0], '\t\t[Type:', move[1]+']','\t\t[PP:',currentpp,'/', str(move[2])+']', '\t\t[Power:', str(move[3])+']', '\t\t[Accuracy:', str(move[4])+']', '\t\t[Category:', str(move[5])+']')
    else:
        if len(move[1]) < 7:
            print(movenum,': ', move[0], '\t[Type:', move[1]+']','\t\t\t[PP:',currentpp,'/', str(move[2])+']', '\t\t[Power:', str(move[3])+']', '\t\t[Accuracy:', str(move[4])+']', '\t\t[Category:', str(move[5])+']')
        else:
            print(movenum,': ', move[0], '\t[Type:', move[1]+']','\t\t[PP:',currentpp,'/', str(move[2])+']', '\t\t[Power:', str(move[3])+']', '\t\t[Accuracy:', str(move[4])+']', '\t\t[Category:', str(move[5])+']')
    print('-'*170)


def playerattack(move, enemyhp):
    ## Takes in a move number and prints the results of the move
    logandprint("Your %s used %s!" % (playerpoke[0],move[0]) ,fhand)
    time.sleep(0.4)
    sillystring = ':' * move[3]
    logandprint('o==[]%s>' % sillystring  ,fhand)
    time.sleep(1)
    rollresult = accroll(move[4])
    if rollresult == 1:
        logandprint("Your %s\'s attack was a HIT! You dealt %d damage!" % (playerpoke[0],move[3]),fhand)
        enemyhp = enemyhp - move[3]
        par.append('sh')
        if enemyhp < 0:
            enemyhp = 0
    else:
        logandprint("Your %s\'s attack was a MISS! You dealt NO damage!" % playerpoke[0],fhand)
        par.append('sm')
    return enemyhp

def enemyattack(move, playerhp):
    ## Takes in a move number and prints the results of the move
    logandprint("The enemy %s used %s!" % (enemypoke[0],move[0]) ,fhand)
    time.sleep(0.4)
    sillystring = ':' * move[3]
    logandprint('o==[]%s>' % sillystring  ,fhand)
    time.sleep(1)
    rollresult = accroll(move[4])
    if rollresult == 1:
        logandprint("%s\'s attack was a HIT! it dealt %d damage!" % (enemypoke[0], move[3]),fhand)
        playerhp = playerhp - move[3]
        if playerhp < 0:
            playerhp = 0
    else:
        logandprint("%s\'s attack was a MISS! It dealt NO damage!" % enemypoke[0],fhand)
    return playerhp

def howeffective(movetype, enemytype1, enemytype2 = 'None'):
    # NORMAL

    # FIGHTING

    # FLYING

    # POISON

    # GROUND

    # ROCK

    # BUG

    # GHOST

    # STEEL

    # FIRE

    # WATER

    # GRASS

    # ELECTRIC

    # PSYCHIC

    # ICE

    # DRAGON

    # DARK

    # FAIRY








def damagecalc(whoisattacking, movecategory, movepower, userattack, userspattack, opponentdefense, opponentspdefense):
    damagerange = random.uniform(0.85, 1.00)
    crit = random.randint(1, 16)
    if crit == 16:
        crit = 1.5
    else:
        crit = 1.0


    if movecategory == 'Physical':
        print('used a PHYSICAL move')
        #The 50 is the level, for now all pokes are level 50
        damage = ((2 * 50 / 5 + 2) * movepower * attack / defense / 50 + 2) *

    elif movecategory == 'Special':
        print('used a SPECIAL move')

    else:
        print('used a STATUS move')



    return damage

while True:

    # Initialize enemy pokemon
    enemypoke = callapoke()
    print('enemypoke:',enemypoke)

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


    # Initialize player pokemon
    playerpoke = callapoke()
    print('player: ',playerpoke)

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


    #Get PP from enemymoves and assign to seperate varianle so it becomes mutable:
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
    time.sleep(1)
    fhand.write("START OF NEW ROUND\n")

    tprint("A   wild    %s     appeared!" % enemypoke[0])
    time.sleep(1.5)
    print('its stats are:', enemystats)
    tprint("You    sent    out:     %s" % playerpoke[0])
    print('its stats are:', playerstats)


    while enemyhp > 0 and playerhp > 0:

        # PLAYER'S TURN

        while True:


            time.sleep(1.5)
            print('Your %s\'s moves are:' % playerpoke[0])
            print('-'*170)
            printmoveformatted(playermove1, 1, playermove1PP)
            printmoveformatted(playermove2, 2, playermove2PP)
            printmoveformatted(playermove3, 3, playermove3PP)
            printmoveformatted(playermove4, 4, playermove4PP)

            userchoice = input("Choose an attack; 1, 2, 3 or 4:\n")
            if userchoice in ('1', '2', '3', '4'):
                break

            else:
                time.sleep(0.5)
                print("...")
                time.sleep(0.5)
                print("That's not an attack, silly")
                continue

        time.sleep(0.5)

        if userchoice == '1':
            enemyhp = playerattack(playermove1, enemyhp)
            playermove1PP -= 1

        elif userchoice == '2':
            enemyhp = playerattack(playermove2, enemyhp)
            playermove2PP -= 1

        elif userchoice == '3':
            enemyhp = playerattack(playermove3, enemyhp)
            playermove3PP -= 1

        elif userchoice == '4':
            enemyhp = playerattack(playermove4, enemyhp)
            playermove4PP -= 1


        time.sleep(1)
        print("The enemy %s has %d HP left" % (enemypoke[0], enemyhp))
        time.sleep(1)

# ENEMY TURN

        if enemyhp > 0 and playerhp > 0:

            logandprint("Now it's %s\'s turn, look out!" % enemypoke[0],fhand)

            print('Its moves are:')
            print('-'*170)
            printmoveformatted(enemymove1, 1, enemymove1PP)
            printmoveformatted(enemymove2, 2, enemymove2PP)
            printmoveformatted(enemymove3, 3, enemymove3PP)
            printmoveformatted(enemymove4, 4, enemymove4PP)


            time.sleep(1)
            enemychoice = random.randint(1, 4)

            if enemychoice == 1:
                playerhp = enemyattack(enemymove1, playerhp)
                enemymove1PP -= 1
            elif enemychoice == 2:
                playerhp = enemyattack(enemymove2, playerhp)
                enemymove2PP -= 1
            elif enemychoice == 3:
                playerhp = enemyattack(enemymove3, playerhp)
                enemymove3PP -= 1
            else:
                playerhp = enemyattack(enemymove4, playerhp)
                enemymove4PP -= 1

            print("Your %s has %d HP left!" % (playerpoke[0], playerhp))
            time.sleep(1)
        else:
            time.sleep(1)
            break

    if enemyhp <= 0:
        tprint("AMAZING")
        time.sleep(1)
        tprint("YOU      WON!")
        playerscore = playerscore + 1
        logandprint("After that smashing victory...",fhand)
    else:
        tprint("  :  (  ")
        tprint("YOU     LOST")
        enemyscore = enemyscore + 1
        logandprint("After that crushing defeat...",fhand)


    logandprint("The current score is:",fhand)
    print("Enemy   ",enemyscore," - ",playerscore,"     You")

    while True:
        answer = str(input("Do you want to play again? (y/n): "))
        if answer in ('y', 'n'):
            break
        print ("Invalid input mate")
    if answer == 'y':
        continue
    else:

        # cacount = 0
        # cahit = 0
        # camiss = 0
        # sacount = 0
        # sahit = 0
        # samiss = 0
        # racount = 0
        # rmiss = 0
        # rhit = 0

        for i in par:
            if i == 'ch':
                cacount = cacount + 1
                cahit = cahit + 1
            if i == 'cm':
                cacount = cacount + 1
                camiss = camiss + 1
            if i == 'sh':
                sacount = sacount + 1
                sahit = sahit + 1
            if i == 'sm':
                sacount = sacount + 1
                samiss = samiss + 1
            if i == 'rh':
                racount = racount + 1
                rahit = rahit + 1
            if i == 'rm':
                racount = racount + 1
                ramiss = ramiss + 1

        time.sleep(0.5)
        print("Before you go, let's look at your stats!")
        time.sleep(0.5)
        print("You attempted %d careful attacks, of which %d were hits and %d were misses!" % (cacount, cahit, camiss))
        time.sleep(0.5)
        print("You attempted %d strong attacks, of which %d were hits and %d were misses!" % (sacount, sahit, samiss))
        time.sleep(0.5)
        print("You attempted %d reckless attacks, of which %d were hits and %d were misses!" % (racount, rahit, ramiss))
        time.sleep(0.5)
        print("Thank you for playing! Bye bye")
        break

fhand.close()
