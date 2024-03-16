#Imports tkinter
from tkinter import *
#Allows images to be used for tkinter
from PIL import Image, ImageTk
#For random values
import random
#These variables are defined here since they will not be changed throughout while the program is running
#boundaries for the board wow
boundY = 8
boundX = 10
#Variable for the number of bombs
numBombs = 10

def get_options():
  ''' Prints the menu into the console and gets user input to navigate the menu.
  '''
  while True:
    print("\n Welcome to minesweeper: \n 1.Play \n 2.Game Instructions \n 3.Exit")
    try:
      option = int(input())
    except ValueError:
      print("Invalid value try again ")
      continue
    if option == 1:
      start_game()
      break
    elif option == 2:
      file = open("Instructions.txt", "r")
      print(file.read())
      continue
    elif option == 3:
      print("Bye Bye")
      break
    else:
      print("Invalid value try again")
      continue

def print_table(table):
  ''' This function prints a 2D list in a easy to understand format. Is used for testing
  
  Arguments:
  table: is a 2D list that the function prints
  '''
  print("   1 2 3 4 5 6 7 8 9 10")
  print("   --------------------")
  count = 0
  for row in table:
    count += 1
    output = ''
    for column in row:
      output += str(column) + ' '
    print(str(count)+ " |" + output)
    ''

def removeEmpties(table, x ,y):

  '''This function takes a 2D list as an argument (board) and a position in the board It then progressively searches each tile around that position to find and clear boxs that contain a 0 value. This is used to save the player time so they dont have to clear too many zero values.
  Arguments:
  table: takes in a 2D list that represents the minesweeper board
  x: represents the x value of the position where all zeros adjacent to that position should be removed
  y: represents the y value of the position where all zeros adjacent to that position should be removed
  '''
  #Saves the position of the zero being checked
  checkedX.append(x)
  checkedY.append(y)
  #Resets popIndex
  popIndex = []

  #This for loop checks all adjacents boxs around the position passed in the arguments. It is from -1 to 2 to easily use the iterator i to check under and over the position passed into the function.
  for i in range(-1, 2):
    #Checks if it is possible to search 1 unit under the position passed
    if (y - 1) >= 0:
        #Checks if it is possible to search 1 unit under and 1 unit left and right of the position passed
        if (x + i) >= 0 and (x + i) < len(table[y]):
          # update player_board to display the zero,  and saves its position in adjZeroX and adjZeroY
          if table[y - 1][x + i] == 0:
            player_board[y - 1][x + i] = 0
            adjZeroY.append(y-1)
            adjZeroX.append(x + i)
          if table[y - 1][x + i] != 0 and table[y - 1][x + i] != "X":
            player_board[y - 1][x + i] = table[y - 1][x + i]
    #Checks if it is possible to search 1 unit above the position passed
    if (y + 1) < len(table):
      #Checks if it is possible to search 1 unit above and 1 unit left and right of the position passed
      if (x + i) >= 0 and (x + i) < len(table[y]):
        if table[y + 1][x + i] == 0:
          player_board[y + 1][x + i] = 0
          adjZeroY.append(y + 1)
          adjZeroX.append(x + i)
        if table[y + 1][x + i] != 0 and table[y + 1][x + i] != "X":
          player_board[y + 1][x + i] = table[y + 1][x + i]
    #Checks if it is possible to search 1 unit to the right and left the position passed
    if (x + i) < len(table[y]) and (x + i) >= 0:
      #update player_board to display the zero,  and saves its position in adjZeroX and adjZeroY
      if table[y][x + i] == 0 and (x + i) != x:
        player_board[y][x + i] = table[y][x + i]
        adjZeroY.append(y)
        adjZeroX.append(x + i)
      if table[y][x + i] != 0 and table[y][x + i] != "X":
        player_board[y][x + i] = table[y][x + i]

  #This for loop runs through all the values in adjZeroX and adjZeroY. If a position has already been checked in adjZeroX or adjZeroY, we mark it to be removed using popIndex. This is done to avoid poping a element of the list adjZero while it is being iterated through.
  for n in range(len(adjZeroX)):
    for i in range(len(checkedX)):
      #If a position has already been checked, mark it for removal from adjZeroX.
      if checkedX[i] == adjZeroX[n] and checkedY[i] == adjZeroY[n]:
        popIndex.append(n)
  #pops all the needed values in reverse, to avoid index errors
  for i in sorted(popIndex, reverse=True):
    adjZeroX.pop(i)
    adjZeroY.pop(i)



def bombNumbers(table, x, y):
  '''
  This function is used to assign number values around bombs after they've been randomly assigned.

  Arguments:
  x: the x value of the position of a bomb
  y: the y value of the position of a bomb
  table: the 2D list for the games boar
  '''
  value = 1
  #This for loop checks all adjacents boxs around the position passed in the arguments. It is from -1 to 2 to easily use the iterator i to check under and over the position passed into the function.
  for i in range(-1, 2):
    #Checks if it is possible to search under the position passed
    if (y - 1) >= 0:
      #checks if it is possible to check 1 unit down and 1 unit left and right of the position passed. Also ensures the value there is a number, not a bomb.
      if (x + i) >= 0 and (x + i) < boundX and type(table[y - 1][x + i]) is int:
        #Adds to the value there
        table[y - 1][x + i] += value
    #Checks if it is possible to search above the position passed
    if (y + 1) < boundY:
      #checks if it possible to search 1 unit above and 1 unit left and right of the position passed. Also ensures the value there is a number, not a bomb.
        if (x + i) >= 0 and (x + i) < boundX and type(table[y + 1][x + i]) is int:
          table[y + 1][x + i] += value
  #Checks if left and right of the position passed can is a number, if it is, its adds 1 to it
  if (x - 1) >= 0 and table[y][x - 1] != "X":
    table[y][x - 1] += value
  if (x + 1) < boundX and table[y][x + 1] != "X":
    table[y][x + 1] += value 

#This function uses the position the player selected and finds whether or not what they selected was a bomb, a whitespace, or a number. Then it calls the appropriate functions based on whichever they selected. The function returns False if the player has lost (clicked on a bomb) and true if they are still playing.
def player_move(x ,y):
  global board
  global player_board
  #If the player clicked a whitespace, remove all whitespaces adjacent to it.
  if board[y][x] == 0:
    player_board[y][x] = board[y][x]
    removeEmpties(board, x,y)
    #This while loop ensures that all zeros adjacent to zeros found are removed until all of them are found.
    while len(adjZeroX) != 0:
      removeEmpties(board, adjZeroX[0], adjZeroY[0])
    return True
  #Checks whether or not the box selected is a bomb, and updates player_board
  elif type(board[y][x]) is int:
    player_board[y][x] = board[y][x]
    return True
  else:
    player_board[y][x] = board[y][x]
    return False

    

def game_board():


  '''Generates the gameboard for the display in tkinter. '''
  
  #List comprehension to store the names of multiple objects (buttons, labels, images) for Tkinter
  widgets = [[str(x)  for x in range(boundX)] for x in range(boundY)]
  #Loop is used to create and display labels, buttons, and images based on the generated board
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == "X":
      #Creates a bomb
        widgets[i][j] = Label( image = img1)
        widgets[i][j].grid(row = i, column = j)
      #Creates a number label
      elif type(board[i][j]) is int:
        widgets[i][j] = Label(text=str(board[i][j]),font=("Arial Bold", 15))
        widgets[i][j].grid(row = i, column = j)
      #Creates a button
      if player_board[i][j] == "_":
        widgets[i][j] = Button(window, bg = "green")
        widgets[i][j].grid(row = i, column = j)
        widgets[i][j].bind("<Button-1>", left_click_gb)
        widgets[i][j].bind("<Button-3>", right_click_gb)


def left_click_sb(event):
  '''This function is used before the player has started the game, it can start the game at any position on the board. It uses the players initial move to generate a random board in board and player_board.
  
  Arguments:
  event is an argument required by tkinter, represents the object/widget that is being clicked in order to call the function.
  '''
  #Global board and player_board to ensure that the 2D lists are stored for use in all other functions
  global board
  global player_board
  #This is the players initial selection stored in x and y
  y = event.widget.grid_info()['row']
  x = event.widget.grid_info()['column']

  #Board Creation
  board = [[0 for x in range(boundX)] for x in range(boundY)]
  bombY = []
  bombX = []
  #Creates a board that gives a fair start to the player
  while True:
    #Randomly assigns bombs to board using the imported random module
    for i in range(numBombs):
      bombY.append(random.randrange(0,boundY))
      bombX.append(random.randrange(0,boundX))
      #This if statement ensures no two bombs are placed on the same position
      if board[bombY[i]][bombX[i]] != "X":
        board[bombY[i]][bombX[i]] = "X"
      else:
        bombY.pop(-1)
        bombX.pop(-1)
        break
      #Function call to assign the bombs numbers surrounding each bomb
      bombNumbers(board, bombX[i], bombY[i])
    #Resets variables if the board created either loses the player on the first move or if there arent enough bombs created.
    if board[y][x] != 0 or len(bombX) != numBombs:
      bombY = []
      bombX = []
      board = [[0 for x in range(boundX)] for x in range(boundY)]
      continue
    else:
      break
  #Reveals the players initial selection
  player_board[y][x] = board[y][x]
  #Clears the initial whitespaces around the initial selection of the player
  removeEmpties(board, x,y)
  #This while loop ensures that zeros surrounding zeros are also removed iteratively
  while len(adjZeroX) != 0:
    removeEmpties(board, adjZeroX[0], adjZeroY[0])
  #Deletes the inital display of the board after the players first move has been made
  for i in range(len(board)):
    for j in range(len(board[0])):
      widgets[i][j].destroy()

  #Prepares the initial board
  game_board()

def play_again():
  ''' Resets the game if the user decides to play again'''
  window.destroy()
  start_game()


def left_click_gb(event):
  '''Function for a left click after the initial starting selection is made. Also handles win loss conditions if once the player makes their move.
   Arguments:
  event is an argument required by tkinter, represents the object/widget that is being clicked in order to call the function.'''
  #Only allows the player to click green squares, so they dont accidentally reveal a box they flagged.
  if event.widget.cget('bg') == "green":
    y = event.widget.grid_info()['row']
    x = event.widget.grid_info()['column']
    for widget in window.winfo_children():
      if "button" in str(widget):
        widget.destroy()

    move = player_move(x, y)
    #checks if the player clicked a bomb using the player_move function
    if move == True:   
      #Resets the buttons for the boxes
      for i in range(boundY):
        for j in range(boundX):
          if player_board[i][j] == "_":
            widgets[i][j] = Button(window, bg = "green")
            widgets[i][j].grid(row = i, column = j)
            widgets[i][j].bind("<Button-1>", left_click_gb)
            widgets[i][j].bind("<Button-3>", right_click_gb)
          elif player_board[i][j] == "B":
            widgets[i][j] = Button(window, bg = "red")
            widgets[i][j].grid(row = i, column = j)
            widgets[i][j].bind("<Button-1>", left_click_gb)
            widgets[i][j].bind("<Button-3>", right_click_gb)
    else:
      #Displays the lose screen and a button that allows the player to restart
      for widget in window.winfo_children():
        if "button" in str(widget):
          widget.destroy()
      restart = Button(window, text = "You lose!", command = play_again)
      restart.grid(row = boundY + 2, column = boundX + 2 )

    #Checks if the player has one by checking if the number of unopened buttons is equal to the number of bombs.
    #For loop finds number of unopened buttons.
    unopened = 0
    for row in player_board:
      for col in row:
        if col == "_" or col == "B":
          unopened += 1
    #checks if the player has won
    if unopened == numBombs:
      #If the player has one, display the win screen and allow the player to restart
      for widget in window.winfo_children():
        if "button" in str(widget):
          widget.destroy()
        restart = Button(window, text = "You win!", command = play_again)
        restart.grid(row = boundY + 2, column = boundX + 2 )
  
    event.widget.destroy()

def right_click_gb(event):
  '''Function changes the color of a right clicked button from red to green or green to red.
   Arguments:
  event is an argument required by tkinter, represents the object/widget that is being clicked in order to call the function.'''

  #If the button is red, make it green, if the button is green, make it red
  if event.widget.cget('bg') == "red":
    event.widget.configure(bg='green')
    #Makes sure the player_board is updated to show that the position isn't flagged
    player_board[event.widget.grid_info()["row"]][ event.widget.grid_info()["column"]] = "_"
  else:
    event.widget.configure(bg="red")
        #Makes sure the player_board that the position is flagged
    player_board[event.widget.grid_info()["row"]][ event.widget.grid_info()["column"]] = "B"

def start_game():
  '''Starts and resets the game. Function does this by reseting all variables  and creating the initial board so the player can select their first move, and the board can be generated.'''
  global window
  global widgets
  global board
  global player_board
  global img1
  global adjZeroX
  global adjZeroY
  global checkedX
  global checkedY
  global bombX
  global bombY
  global popIndex
  #Board is used for board generation, stores the value for every position
  board = [[0 for x in range(boundX)] for x in range(boundY)]
  #Player_board stores the current moves the player has made
  player_board = [["_" for x in range(boundX)] for x in range(boundY)]
  #Position of bombs
  bombX = []
  bombY = []
  #Variables for the removal empty functions
  #adjZeroX and adjZeroY are used to check the zeros adjacent to other zeros found by the function removeEmpties()
  adjZeroX = []
  adjZeroY = []
  #checkedX and checkedY are used to save the position of zeros that have already been found by the function removeEmpties()
  checkedX = []
  checkedY = []
  #popIndex is a temporary variable for removal of positions already checked by removeEmpties()
  popIndex = []

  #Creates the Tkinter window
  window = Tk()
  window.title("Minesweeper")
  window.geometry("350x350")

  #Resizes the image 
  image = Image.open("Bomb.png")
  resize_image = image.resize((25, 25))
  img1 = ImageTk.PhotoImage(resize_image)

  #Creates the initial board for the game
  widgets = [["_" + str(x) for x in range(boundX)] for x in range(boundY)]
  for i in range(len(board)):
    for j in range(len(board[0])):
      widgets[i][j] = Button(window, bg = "green")
      widgets[i][j].grid(row = i, column = j)
      widgets[i][j].bind("<Button-1>", left_click_sb)

  myCanvas = Canvas(window)

#Calls the main menu to start the game.
get_options()