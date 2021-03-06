# -*- coding:utf-8 -*-
from tkinter import *
import time
import math



class Horloge(Canvas):
    def __init__(self, master = None, number = True, width = 200, height = 200, **kwargs):
        Canvas.__init__(self, master, width=width, height=height, **kwargs)
        self.number = number
        self.auto = True
        self.__after = None
        self.setnow()
    def set(self, heure, minute):
        self.heure = heure
        self.minute = minute
        self.delete(ALL)
        self.create_oval(10, 10, 190, 190, fill = "white", width = 2)
        sin = math.sin
        cos = math.cos
        pi = math.pi
        for angle in range(0, 360, 6):
            x1 = 100 + 80*sin(angle*2*pi/360)
            y1 = 100 + 80*cos(angle*2*pi/360)
            if angle%5==0:
                #line:
                if self.number:
                    x2 = 100 + 80*sin(angle*2*pi/360)
                    y2 = 100 - 80*cos(angle*2*pi/360)
                    self.create_text(x2, y2, text=str(int((angle if angle!= 0 else 360)/30)))
                else:
                    x2 = 100 + 72*sin(angle*2*pi/360)
                    y2 = 100 + 72*cos(angle*2*pi/360)
                    self.create_line(x1, y1, x2, y2)
            else:
                #point
                x2 = 100 + 82*sin(angle*2*pi/360)
                y2 = 100 + 82*cos(angle*2*pi/360)
                self.create_line(x1, y1, x2, y2)
        heure = self.heure+self.minute/60
        x2 = 100 + 50*cos((heure-3)*2*pi/12)
        y2 = 100 + 50*sin((heure-3)*2*pi/12)
        x3 = 100 - 15*cos((heure-3)*2*pi/12)
        y3 = 100 - 15*sin((heure-3)*2*pi/12)
        self.create_line(x3, y3, x2, y2, width=3)
        x2 = 100 + 70*cos((self.minute-15)*2*pi/60)
        y2 = 100 + 70*sin((self.minute-15)*2*pi/60)
        x3 = 100 - 25*cos((self.minute-15)*2*pi/60)
        y3 = 100 - 25*sin((self.minute-15)*2*pi/60)
        self.create_line(x3, y3, x2, y2, width=2)
        self.create_oval(97, 97, 103, 103, fill="white")
    def setnow(self):
        self.set(time.localtime().tm_hour, time.localtime().tm_min)
        if self.auto:
            self.__after = self.after(1000, self.setnow)
    def setAuto(self, auto):
        if auto:
            self.auto = True
            self.setnow()
        else:
            self.auto = False
            self.after_cancel(self. __after)


def main():
    hor = Horloge()
    hor.pack()
    hor.mainloop()


if __name__=='__main__':
    main()
