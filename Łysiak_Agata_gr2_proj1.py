# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 12:22:01 2019

@author: Agata1
"""

import sys
import numpy as np

from PyQt5.QtWidgets  import QLineEdit, QPushButton, QLabel, QWidget, QApplication, QGridLayout,QColorDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class AppWindow(QWidget): #appwidnow dziedziczy po qwidget
    def __init__(self):
        super().__init__()
        self.title = "Położenie odcinków" #nadanie nazwy okna aplikacji
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(200, 200, 500, 400) #rozmiar okienk
        self.show()

    def initWidgets(self):
        btn = QPushButton("Wykonaj działanie i rysuj", self) #przyciski
        btnCol = QPushButton("Zmień kolor odcinka CD", self)
    
        #dodanie etykiet
        xaLabel = QLabel("Xa", self)
        yaLabel = QLabel("Ya", self)
        xbLabel = QLabel("Xb", self)
        ybLabel = QLabel("Yb", self)
        xcLabel = QLabel("Xc", self)
        ycLabel = QLabel("Yc", self)
        xdLabel = QLabel("Xd", self)
        ydLabel = QLabel("Yd", self)
        xpLabel = QLabel("Xp", self)
        ypLabel = QLabel("Yp", self)
        punktLabel = QLabel("Położenie punkty P \nwzględem odcinków ", self)
        
        
        self.xaEdit = QLineEdit()
        self.yaEdit = QLineEdit()
        self.xbEdit = QLineEdit()
        self.ybEdit = QLineEdit()
        self.xcEdit = QLineEdit()
        self.ycEdit = QLineEdit()
        self.xdEdit = QLineEdit()
        self.ydEdit = QLineEdit()
        self.xpEdit = QLineEdit()
        self.ypEdit = QLineEdit()
        self.xpEdit.readonly = True
        self.ypEdit.readonly = True
        self.punktEdit = QLineEdit()
       
       
        
        #wykresy 
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
       
        
        #wywietlenie #rozmieszczenie elementów w oknie aplikacji
        grid = QGridLayout()
        grid.addWidget(xaLabel, 1, 0)
        grid.addWidget(self.xaEdit, 1, 1)
        grid.addWidget(yaLabel, 2, 0)
        grid.addWidget(self.yaEdit, 2, 1)
        grid.addWidget(xbLabel, 3, 0)
        grid.addWidget(self.xbEdit, 3, 1)
        grid.addWidget(ybLabel, 4, 0)
        grid.addWidget(self.ybEdit, 4, 1)
        grid.addWidget(xcLabel, 5, 0)
        grid.addWidget(self.xcEdit, 5, 1)
        grid.addWidget(ycLabel, 6, 0)
        grid.addWidget(self.ycEdit, 6, 1)
        grid.addWidget(xdLabel, 7, 0)
        grid.addWidget(self.xdEdit, 7, 1)
        grid.addWidget(ydLabel, 8, 0)
        grid.addWidget(self.ydEdit, 8, 1)
        grid.addWidget(self.xpEdit, 10, 1)
        grid.addWidget(xpLabel, 10, 0)
        grid.addWidget(self.ypEdit, 11, 1)
        grid.addWidget(ypLabel, 11, 0)
        grid.addWidget(self.punktEdit, 2, 3, 1, 20)
        grid.addWidget(punktLabel, 2, 2)
        grid.addWidget(btn, 9, 0, 1, 2)
        grid.addWidget(btnCol, 1, 2, 1, 1)
        self.setLayout(grid)
        
        grid.addWidget(self.canvas, 3, 2, 10, -1) #1 wiersz 2 kolunmna, dokonca okna aplikacji
#        grid.addWidget(self.azcanvas, 5, 10, -1, -1)
        
        #przyciski
        btn.clicked.connect(self.oblicz)
        btnCol.clicked.connect(self.zmienkolor)
        
        
    #zmiana koloru odcinka CD   
    def zmienkolor(self):
        kolor = QColorDialog.getColor() 
        if kolor.isValid():
            print(kolor.name())
            self.rysuj(kol=kolor.name())
            
 
      
        
    #sprawdzeie czy wprowadzona dana jest liczba 
    def sprawdzLiczbe(self, element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            element.setFocus()
            return None
        
    def oblicz(self):
        self.rysuj()
            
   #obliczenie punktu przeciecia i rysowanie wykresu
    def rysuj(self, kol = 'red'): # jesli nie wybierzemy koloru, automatycznie bedzie rysował na czerowno 
        xa = self.sprawdzLiczbe(self.xaEdit)
        ya = self.sprawdzLiczbe(self.yaEdit)
        xb = self.sprawdzLiczbe(self.xbEdit)
        yb = self.sprawdzLiczbe(self.ybEdit)
        xc = self.sprawdzLiczbe(self.xcEdit)
        yc = self.sprawdzLiczbe(self.ycEdit)
        xd = self.sprawdzLiczbe(self.xdEdit)
        yd = self.sprawdzLiczbe(self.ydEdit)
        
        #if self.xEdit.text().lstrip('-').replace('.','',1).isdigit() and self.yEdit.text().lstrip('-').replace('.','',1).isdigit():
        #if (x is not None) and (y is not None): 
        if None not in [xa, ya, xb, yb, xc, yc, xd, yd]:
            xa = float(self.xaEdit.text())
            ya = float(self.yaEdit.text())
            xb = float(self.xbEdit.text())
            yb = float(self.ybEdit.text())
            xc = float(self.xcEdit.text())
            yc = float(self.ycEdit.text())
            xd = float(self.xdEdit.text())
            yd = float(self.ydEdit.text())
            
        #wyznaczenie wspólrzednych punktu przecięcia odcinków
        dXab = xb - xa
        dYab = yb - ya
        dXcd = xd - xc
        dYcd = yd - yc
        dXac = xc - xa
        dYac = yc - ya
        mian = dXab*dYcd - dYab*dXcd

        if mian!= 0:
            t1 = (dXac*dYcd - dYac*dXcd)/mian
            t2 = (dXac*dYab - dYac*dXab)/mian
            if 0<= t1 <=1 and 0<= t2 <=1:
                xp = xa + t1*dXab
                yp = ya + t1*dYab
                a = "{0:.3f}".format(xp)
                b = "{0:.3f}".format(yp)
                self.xpEdit.setText(str(a))
                self.ypEdit.setText(str(b))
                self.punktEdit.setText(str("Przecięcie odcinków"))
            elif 0<= t1 <=1 or 0<= t2 <=1:
                xp = xa + t1*dXab
                yp = ya + t1*dYab
                c = "{0:.3f}".format(xp)
                d = "{0:.3f}".format(yp)
                self.xpEdit.setText(str(c))
                self.ypEdit.setText(str(d))
                self.punktEdit.setText(str("Przecięcie na przedłużeniu jednego z odcinków"))
            else:
                xp = xa + t1*dXab
                yp = ya + t1*dYab
                e = "{0:.3f}".format(xp)
                f = "{0:.3f}".format(yp)
                self.xpEdit.setText(str(e))
                self.ypEdit.setText(str(f))
                self.punktEdit.setText(str("Przecięcie przedłużeń dwóch odcinków"))
        elif mian == 0:
            self.punktEdit.setText(str("Odcinki są równoległe"))
            
        
        #zapisanie współrzędnych punktów do pliku
        plik = open('projekt1.txt', 'w')
        plik.write("|{:^15}|{:^15}|{:^15}|\n".format("Nazwa pkt", "X [m]", "Y [m]" ))
        plik.write("|{:^15}|{:15.3f}|{:15.3f}|\n".format("A",xa, ya)) 
        plik.write("|{:^15}|{:15.3f}|{:15.3f}|\n".format("B",xb, yb))
        plik.write("|{:^15}|{:15.3f}|{:15.3f}|\n".format("C",xc, yc))
        plik.write("|{:^15}|{:15.3f}|{:15.3f}|\n".format("D",xd, yd))
        if self.xaEdit == None:
            plik.write("|{:^15.3f}|{:^15.3f}|{:^15.3f}|\n".format("P","brak", "brak"))
        else:
            plik.write("|{:^15}|{:^15.3f}|{:^15.3f}|\n".format("P", xp, yp))
        plik.close()
       
        #wykres przedstwiający odcinki i punkt przecięcia odcinkóW
        self.figure.clear() #czyszczenie pozsotałowsci
        ax = self.figure.add_subplot(111)
        ax.plot([yp, yb], [xp, xb], 'go:')
        ax.plot([ya, yp], [xa, xp], 'go:')
        ax.plot([yp, yd], [xp, xd], 'go:')
        ax.plot([yc, yp], [xc, xp], 'go:')
        ax.plot([ya, yb], [xa, xb], 'bo-')
        ax.plot([yc, yd], [xc, xd], color=kol, marker ='o')
        ax.plot(yp, xp, color = 'green', marker= 'o')
        ax.text(ya, xa, "Ya " + str(ya) + "\n Xa" + str(xa), fontsize = 10, color = "black")
        ax.text(yb, xb, "Yb " + str(yb) + "\n Xb" + str(xb), fontsize = 10, color = "black")
        ax.text(yc, xc, "Yc " + str(yc) + "\n Xc" + str(xc), fontsize = 10, color = "black")
        ax.text(yd, xd, "Yd " + str(yd) + "\n Xd" + str(xd), fontsize = 10, color = "black")
        ax.text(yp, xp, "Yp " + str(yp) + "\n Xp" + str(xp), fontsize = 10, color = "black")
        self.canvas.draw()
        
    
        self.xaEdit.setText("1")
        
        

def main(): # w funkcji main bd oczekiwać na nasze zdarzenia 
   app = QApplication(sys.argv)
   window = AppWindow()
   app.exec_()
    
if __name__ == '__main__':
    main()