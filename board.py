import Tkinter as tk
import time
import random
from random import randint
BROWS=32
BCOLUMNS=32
from enum import Enum


def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"



class Direction(Enum):
    up = 0
    right = 1
    down = 2
    left =3

class Predator():
    def __init__(self,name,initX,initY,rows=BROWS,columns=BCOLUMNS):
        self.name = name
        self.rows = rows
        self.columns = columns
        self.X = initX
        self.Y = initY

    def randomizeMov(self):
        directionX=randint(-1,1)
        directionY=randint(-1,1)
        self.X = (self.X + directionX) % self.rows
        self.Y = (self.Y + directionY) % self.columns
    def follow(self,X,Y):
        if(self.X > X): 
            self.X = self.X-1
        elif (self.X < X):
            self.X = self.X+ 1
        if(self.Y > Y): 
            self.Y = self.Y-1
        elif (self.Y < Y):
            self.Y = self.Y+1
            
        if (self.X==X and self.Y==Y):
            print "REACHED!!"
            
    def evade(self,X,Y):    
        if(self.X > X): 
            eX = +1
        elif (self.X < X):
            eX = -1
        else:
            eX= random.choice([-1, 1])
        if(self.Y > Y): 
            eY = +1
        elif (self.Y < Y):
            eY = -1
        else:
            eY= random.choice([-1, 1])      
        directionX=randint(-1,1)
        directionY=randint(-1,1)
        self.X = (self.X + random.choice([eX,eX,eX,eX,eX, directionX])) % self.rows
        self.Y = (self.Y + random.choice([eY,eY,eY,eY,eY, directionY])) % self.columns        
        
class GameBoard(tk.Frame):
    def __init__(self, parent, rows=BROWS, columns=BCOLUMNS, size=8, color1="white", color2="blue"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


# image comes from the silk icon set which is under a Creative Commons
# license. For more information see http://www.famfamfam.com/lab/icons/silk/
imagedata = '''
    R0lGODlhEAAQAOeSAKx7Fqx8F61/G62CILCJKriIHM+HALKNMNCIANKKANOMALuRK7WOVLWPV9eR
    ANiSANuXAN2ZAN6aAN+bAOCcAOKeANCjKOShANKnK+imAOyrAN6qSNaxPfCwAOKyJOKyJvKyANW0
    R/S1APW2APW3APa4APe5APm7APm8APq8AO28Ke29LO2/LO2/L+7BM+7BNO6+Re7CMu7BOe7DNPHA
    P+/FOO/FO+jGS+/FQO/GO/DHPOjBdfDIPPDJQPDISPDKQPDKRPDIUPHLQ/HLRerMV/HMR/LNSOvH
    fvLOS/rNP/LPTvLOVe/LdfPRUfPRU/PSU/LPaPPTVPPUVfTUVvLPe/LScPTWWfTXW/TXXPTXX/XY
    Xu/SkvXZYPfVdfXaY/TYcfXaZPXaZvbWfvTYe/XbbvHWl/bdaPbeavvadffea/bebvffbfbdfPvb
    e/fgb/Pam/fgcvfgePTbnfbcl/bfivfjdvfjePbemfjelPXeoPjkePbfmvffnvbfofjlgffjkvfh
    nvjio/nnhvfjovjmlvzlmvrmpvrrmfzpp/zqq/vqr/zssvvvp/vvqfvvuPvvuvvwvfzzwP//////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////yH+FUNyZWF0ZWQgd2l0aCBU
    aGUgR0lNUAAh+QQBCgD/ACwAAAAAEAAQAAAIzAD/CRxIsKDBfydMlBhxcGAKNIkgPTLUpcPBJIUa
    +VEThswfPDQKokB0yE4aMFiiOPnCJ8PAE20Y6VnTQMsUBkWAjKFyQaCJRYLcmOFipYmRHzV89Kkg
    kESkOme8XHmCREiOGC/2TBAowhGcAyGkKBnCwwKAFnciCAShKA4RAhyK9MAQwIMMOQ8EdhBDKMuN
    BQMEFPigAsoRBQM1BGLjRIiOGSxWBCmToCCMOXSW2HCBo8qWDQcvMMkzCNCbHQga/qMgAYIDBQZU
    yxYYEAA7
'''



if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    player1 = tk.PhotoImage(data=imagedata)
    p1=Predator("player1",10,10)
    p2=Predator("player2",16,16)
    board.addpiece(p1.name, player1, p1.X,p1.Y)
    board.addpiece(p2.name, player1, p2.X,p2.Y)
    while 1:
        p1.evade(p2.X,p2.Y)
        p2.follow(p1.X,p1.Y)
        time.sleep(0.1)
        board.placepiece(p1.name,p1.X,p1.Y)
        board.placepiece(p2.name,p2.X,p2.Y)
        root.update_idletasks()
        root.update()
    root.mainloop()
