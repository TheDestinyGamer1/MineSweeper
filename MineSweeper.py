from tkinter import DISABLED, Tk, Button, messagebox, Label
from random import *
import pyglet.font
from numpy import *
from functools import partial
from PIL import Image, ImageTk
from time import *


def square_check(row, column):  # checks to see if a square is a bomb, also used to make bomb array on first click
    global bombArray, numBombs, lost, rows, columns, numSquaresUncovered, firstClick, numFlagsPlaced, startTime, timerStarted, gameWindow
    ####### First Click stuff, initialization basically
    if firstClick:
        if not timerStarted:
            gameWindow.after(1000, time_update())
            timerStarted = True
        firstClick = False
        startTime = time()
        gameWindow.after(1000, time_update)
        for m in range(numBombs):  # for loop to place bombs without repetition and outside a 3x3 area centered on where the user clicked
            randX = randint(0, rows - 1)  # done using randomly generated x and y values on the array, rand int is inclusive on both sides, so -1 necessary to not exceed array size
            randY = randint(0, columns - 1)
            while ((randX + 1 == row or randX == row or randX - 1 == row) and (randY + 1 == column or randY == column or randY - 1 == column)) or (bombArray[randX, randY] == 1):
                randX = randint(0, rows - 1)
                randY = randint(0, columns - 1)
            bombArray[randX, randY] = 1  # on is equal to a bomb in bomb array

        for m in range(rows):  # scanning bomb array to find bombs to make the array of numbers that the player will see
            for n in range(columns):
                if bombArray[m, n] == 1:
                    numArray[m, n] = 9  # a 9 in numArray correlates to a bomb in bomb array
                else:
                    for o in range(-1, 2):
                        for p in range(-1, 2):
                            if m + o < 0 or m + o > rows - 1 or n + p < 0 or n + p > columns - 1:  # if outside board area, do nothing
                                "dummy"
                            elif bombArray[m + o, n + p] == 1:  # if a bomb is found, add one to the counted nearby bobs
                                numArray[m, n] += 1
    #######
    ####### Begin regular click square stuff idk man you come up with a better title alright?
    clickedButton = buttons[(row, column)]  # finds the button that was clicked, used for config stuff
    if flagArray[row, column] == 1:  # remove the flag from the clicked square if there is one
        numFlagsPlaced -= 1
        flagArray[row, column] = 0
        clickedButton.configure(image=blankImage)
    elif bombArray[row, column] == 1:  # haha you lost bro. that's all it is, don't be mad though t's just a game. more stuff will be handled on loss in another function
        clickedButton.configure(state=DISABLED, image=bombImage, relief="sunken")
        lost = True
    else:  # if not a bomb, and not a flag, do regular minesweeper stuff
        numSquaresUncovered += 1  # used to find out if won
        if numArray[row, column] == 0:  # if the button pressed had no bombs nearby, invoke the buttons near it, invoking a button runs the function in the "command" kwarg of the button
            clickedButton.configure(state=DISABLED, image=blankImage, relief="sunken")
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if m == n == 0:
                        "dummy"
                    elif row + m < 0 or row + m > rows - 1 or column + n < 0 or column + n > columns - 1:
                        "dummy"
                    elif buttons[(row+m, column+n)]["state"] == DISABLED:
                        "dummy"
                    else:
                        if flagArray[row + m, column + n] == 1:
                            buttons[(row + m, column + n)].invoke()
                        buttons[(row + m, column + n)].invoke()
        # display the proper number on the button that was clicked if not a 0
        if numArray[row, column] == 1:
            clickedButton.configure(state=DISABLED, image=oneImage, relief="sunken")
        if numArray[row, column] == 2:
            clickedButton.configure(state=DISABLED, image=twoImage, relief="sunken")
        if numArray[row, column] == 3:
            clickedButton.configure(state=DISABLED, image=threeImage, relief="sunken")
        if numArray[row, column] == 4:
            clickedButton.configure(state=DISABLED, image=fourImage, relief="sunken")
        if numArray[row, column] == 5:
            clickedButton.configure(state=DISABLED, image=fiveImage, relief="sunken")
        if numArray[row, column] == 6:
            clickedButton.configure(state=DISABLED, image=sixImage, relief="sunken")
        if numArray[row, column] == 7:
            clickedButton.configure(state=DISABLED, image=sevenImage, relief="sunken")
        if numArray[row, column] == 8:  # bro if you see an 8 good luck LMAO
            clickedButton.configure(state=DISABLED, image=eightImage, relief="sunken")
    if not shownLossWin:  # the whole board is shown (invoked) when you lose, so this prevents errors of hidden bombs making it so you lost multiple times, mainly an error after the window closes itself
        win_loss_check()


def flag_maker(row, column, event):  # function to be called when a button is left clicked on
    global flagArray, numFlagsPlaced, bombs, firstClick, timerStarted, startTime, gameWindow
    if not timerStarted:
        startTime = time()
        timerStarted = True
        gameWindow.after(1000, time_update())
    if event.num == 2 or event.num == 3:  # this is to check if the button that was clicked on was clicked on using a right click, some OS's use 2, some use 3
        if buttons[(row, column)]["state"] != DISABLED:  # there was a time when you could place a flag on buttons you had revealed, so this became necessary
            if flagArray[row, column] == 1:  # you cannot stack flags, only place 1 or remove 1, sorry
                numFlagsPlaced -= 1
                buttons[(row, column)].configure(image=blankImage)
                flagArray[row, column] = 0
            else:
                numFlagsPlaced += 1
                buttons[(row, column)].configure(image=flagImage)
                flagArray[row, column] = 1
    bombs.configure(text=str(int(numBombs - numFlagsPlaced)))
    win_loss_check()  # winning or losing is based on having every bomb flagged and every other square uncovered. it took a few minutes to find out why I didn't win sometimes...


def win_loss_check():
    global lost, shownLossWin, numSquaresUncovered, rows, columns, flagArray, buttons, numArray, numFlagsPlaced
    if numFlagsPlaced == numBombs and numSquaresUncovered == rows*columns - numFlagsPlaced and not lost:
        shownLossWin = True
        messagebox.showinfo("MineSweeper", "You win!")
        gameWindow.destroy()
    elif lost and not shownLossWin:
        shownLossWin = True
        for m in range(rows):
            for n in range(columns):
                if flagArray[m, n] == 1:
                    buttons[(m, n)].invoke()
                buttons[(m, n)].invoke()
        messagebox.showinfo("MineSweeper", "You lost, Idiot!")
        sleep(1)
        gameWindow.destroy()


def time_update():
    global gameWindow, startTime, timer
    timerTime = str(int(time() - startTime))
    timer.configure(text=timerTime)
    if not shownLossWin:
        gameWindow.after(1000, time_update)


def main(numRows=10, numColumns=10, numberBombs=20, windowSizePx=800):
    global timer, timerWidth, bombs, numBombs, rows, columns, firstClick, lost, shownLossWin, numSquaresUncovered
    global numFlagsPlaced, startTime, timerWidth, bombArray, numArray, flagArray, gameWindow, blankImage, oneImage
    global twoImage, threeImage, fourImage, fiveImage, sixImage, sevenImage, eightImage, bombImage, flagImage
    global buttons, timerStarted

    buttons = {}  # dictionary to hold buttons so they can be configured later

    firstClick = True  # initialization
    lost = False
    shownLossWin = False
    timerStarted = False
    numSquaresUncovered = 0
    numFlagsPlaced = 0
    startTime = time()
    timerWidth = 3
    ####### Initialization done from menu function
    rows = numRows
    columns = numColumns
    boxWidth = windowSizePx
    boxHeight = windowSizePx*1.05

    numBombs = numberBombs
    #######
    pyglet.font.add_file("Assets/Fonts/font.ttf")
    blankImageFileName = "Assets/Images/blank.png"
    oneImageFileName = "Assets/Images/1.png"
    twoImageFileName = "Assets/Images/2.png"
    threeImageFileName = "Assets/Images/3.png"
    fourImageFileName = "Assets/Images/4.png"
    fiveImageFileName = "Assets/Images/5.png"
    sixImageFileName = "Assets/Images/6.png"
    sevenImageFileName = "Assets/Images/7.png"
    eightImageFileName = "Assets/Images/8.png"
    bombImageFileName = "Assets/Images/Bomb.png"
    flagImageFileName = "Assets/Images/Flag.png"

    bombArray = zeros((rows, columns))  # making arrays to use in background to keep track of the board
    numArray = zeros((rows, columns))
    flagArray = zeros((rows, columns))


    gameWindow = Tk()
    gameWindow.withdraw()
    gameWindow.geometry(str(windowSizePx) + "x" + str(int(windowSizePx*1.05)))
    with Image.open(blankImageFileName) as im:
        blankImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(oneImageFileName) as im:
        oneImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(twoImageFileName) as im:
        twoImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(threeImageFileName) as im:
        threeImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(fourImageFileName) as im:
        fourImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(fiveImageFileName) as im:
        fiveImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(sixImageFileName) as im:
        sixImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(sevenImageFileName) as im:
        sevenImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(eightImageFileName) as im:
        eightImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(bombImageFileName) as im:
        bombImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    with Image.open(flagImageFileName) as im:
        flagImage = ImageTk.PhotoImage(im.resize((int(boxWidth/rows), int(boxHeight/(columns+1)))))
    timer = Label(text="0", font=("digital dream", int(500*(1/(columns+1)))), fg="red", bg="black", anchor="e")
    timer.place(relwidth=1/4, relheight=1/(columns+1), relx=3/4, rely=0)

    bombs = Label(text=str(numBombs), font=("digital dream", int(500*(1/(columns+1)))), fg="red", bg="black", anchor="e")
    bombs.place(relwidth=1/4, relheight=1/(columns+1), relx=0, rely=0)

    quitButton = Button(text="Quit", font=("font", int(500*(1/(columns+1))), "bold"), command=gameWindow.destroy)
    quitButton.place(relwidth=1/4, relheight=1/(columns+1), relx=1/4, rely=0)


    for m in range(rows):
        for n in range(columns):
            button = Button(gameWindow, command=partial(square_check, m, n), image=blankImage)
            buttons[(m, n)] = button
            button.place(relwidth=1/rows, relheight=1/(columns+1), relx=m/rows, rely=((n+1)/(columns+1)))
            button.bind("<Button>", partial(flag_maker, m, n))

    gameWindow.deiconify()
    gameWindow.mainloop()


if __name__ == "__main__":
    main()