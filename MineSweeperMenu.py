import MineSweeper
from tkinter import *
from pyautogui import size
from math import e

screenWidth, screenHeight = size()
windowSize = screenHeight*0.85
acceptable = False
quitting = True

numRows = 0
numColumns = 0
numBombs = 0

lim = 50
m = -0.0022
h = 1000


def value_checker():
    global rowBox, columnBox, bombBox, submitButton, menu, warningText, acceptable, windowSize
    global numRows, numColumns, numBombs, percentBombText
    rowInt = False
    columnInt = False
    bombInt = False
    acceptable = False

    row = rowBox.get()
    column = columnBox.get()
    bomb = bombBox.get()

    for i in range(len(row)):
        try:
            int(row[i])
        except ValueError:
            rowBox.delete(i)
            rowInt = False
            break
        else:
            if i == 0 and row[i] == "0":
                rowBox.delete(i)
                rowInt = False
                break
            else:
                rowInt = True
        if i == len(row) - 1:
            numRows = int(row)

    for i in range(len(column)):
        try:
            int(column[i])
        except ValueError:
            columnBox.delete(i)
            columnInt = False
            break
        else:
            if i == 0 and column[i] == "0":
                columnBox.delete(i)
                columnInt = False
                break
            else:
                columnInt = True
        if i == len(column) - 1:
            numColumns = int(column)

    for i in range(len(bomb)):
        try:
            int(bomb[i])
        except ValueError:
            bombBox.delete(i)
            bombInt = False
            break
        else:
            if i == 0 and bomb[i] == "0":
                bombBox.delete(i)
                bombInt = False
                break
            else:
                bombInt = True
        if i == len(bomb) - 1:
            numBombs = int(bomb)

    if rowInt and columnInt and bombInt:
        percentBombs = (numBombs / (numRows * numColumns)) * 100
        percentBombText.configure(text="Percent of board that is bombs: " + str(int(percentBombs)) + "%")
        if numBombs > numRows * numColumns - 9:
            acceptable = False
            warningText.configure(text="Too many bombs")
        elif numRows*numColumns >= 9747:
            acceptable = False
            warningText.configure(text="Board size exceeds maximum")
        elif numRows > windowSize/8:
            acceptable = False
            warningText.configure(text="Row size exceeds maximum")
        elif numColumns > windowSize/8:
            acceptable = False
            warningText.configure(text="Column size exceeds maximum")
        elif percentBombs < lim/(1 + (e**(m*(numRows*numColumns-h)))):
            acceptable = False
            warningText.configure(text="Not enough bombs")
        else:
            acceptable = True
    else:
        warningText.configure(text="Please fill all boxes with numbers")

    if acceptable:
        submitButton.configure(state=NORMAL)
        if numRows*numColumns >= 225 and numBombs < numRows*numColumns*0.20:
            warningText.configure(text="Warning: too large of a board with few bombs may lead to instability")
        elif numBombs < numRows*numColumns*0.10:
            warningText.configure(text="Warning: too few bombs may lead to instability")
        else:
            warningText.configure(text="")
    else:
        submitButton.configure(state=DISABLED)

    menu.after(25, value_checker)


def run_minesweeper():
    global quitting
    menu.destroy()
    quitting = False


def quitButton():
    global quitting
    menu.destroy()
    quitting = True


menu = Tk()

menu.geometry(str(int(screenWidth*0.5)) + "x" + str(int(screenHeight*0.5)))
rowText = Label(menu, text="Number of Rows", anchor="c")
rowText.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.7/4)
rowBox = Entry(menu)
rowBox.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.7/4+0.05)

columnText = Label(menu, text="Number of columns", anchor="c")
columnText.place(relheight=0.05, relwidth=0.2, relx=0.6, rely=0.7/4)
columnBox = Entry(menu)
columnBox.place(relheight=0.05, relwidth=0.2, relx=0.6, rely=0.7/4+0.05)

bombText = Label(menu, text="Number of bombs", anchor="c")
bombText.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.7*2/4+0.05)
bombBox = Entry(menu)
bombBox.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.7*2/4+0.1)

percentBombText = Label(menu, text="Percent of board that is bombs: N/A%", wraplength=150)
percentBombText.place(relheight=0.05, relwidth=0.2, relx=0.6, rely=0.7*2/4+0.075)

submitButton = Button(menu, text="Submit", state=DISABLED, command=run_minesweeper)
submitButton.place(relheight=0.05, relwidth=0.2, relx=0.5, rely=0.7*3/4+0.1)

warningText = Label(menu, text="", fg="red", justify="center", height=3, wraplength=150)
warningText.place(relheight=0.1, relwidth=0.2, relx=0.5, rely=0.7*3/4+0.15)

value_checker()

exitButton = Button(menu, text="Quit", command=quitButton)
exitButton.place(relheight=0.05, relwidth=0.2, relx=0.3, rely=0.7*3/4+0.1)

menu.mainloop()

if quitting:
    "dummy"
else:
    MineSweeper.main(numRows, numColumns, numBombs, int(windowSize))