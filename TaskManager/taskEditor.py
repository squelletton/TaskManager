# -*- coding:utf-8 -*-
from task import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame


class TaskEditor(Frame):
    def __init__(self, master, menubar):
        Frame.__init__(self, master, bg="red")
        # Note : master est une référence vers Application
        self.menu = menubar

        self.taches = []

        self.mousepress = False

        self.frameInput = TaskAdder(self, menubar)
        self.frameInput.pack(side = TOP, fill = X)

        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        self.redessiner()
    def ajouter(self, tache):
        self.taches.append(tache)
        self.redessiner()
        if tache.statut != "Inconnu":
            self.master.getDonneeCalendrier().addTask(tache)
    def redessiner(self):
        self.tree.destroy()
        self.scrollbar.destroy()
        self.tree = Treeview(self, columns = ('Statut',), height = 0)
        self.tree.pack(expand = YES, fill = BOTH, side = LEFT)

        self.scrollbar = Scrollbar(self, orient = VERTICAL, command = self.tree.yview)
        self.scrollbar.pack(expand = NO, fill = BOTH, side = RIGHT)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # configuration des colones
        self.tree.column("#0", width = 0)
        self.tree.column(0,    width = 0)
        self.tree.heading("#0", text="Tâche", command = self.tri_alphabetique)
        self.tree.heading(0,    text="Statut", command = self.tri_priorite)

        self.NEW_ID = 0
        for t in self.taches:
            t.id = self.NEW_ID
            self.tree.insert("", END, text = t.nom, values = [t.statut], iid = "p%s"%self.NEW_ID, tags = "Couleur%s"%t.color) # p comme parent
            self.tree.insert("p%s"%self.NEW_ID, END, text = "Début :", values = [t.debut], iid = "p%se1"%self.NEW_ID, tags = "Couleur%s"%t.color) # e comme enfant.
            self.tree.insert("p%s"%self.NEW_ID, END, text = "Durée :", values = [t.duree], iid = "p%se2"%self.NEW_ID, tags = "Couleur%s"%t.color)
            self.tree.insert("p%s"%self.NEW_ID, END, text = "Fin :", values = [(t.debut + t.duree) if t.debut is not None else None], iid = "p%se3"%self.NEW_ID, tags = "Couleur%s"%t.color)
            self.tree.insert("p%s"%self.NEW_ID, END, text = "Description :", values = [t.desc], iid = "p%se4"%self.NEW_ID, tags = "Couleur%s"%t.color)
            self.tree.insert("p%s"%self.NEW_ID, END, text = "Nombre rep :", values = [t.nbrep], iid = "p%se5"%self.NEW_ID, tags = "Couleur%s"%t.color)
            self.tree.insert("p%s"%self.NEW_ID, END, text = "temps entre rep :", values = [t.rep], iid = "p%se6"%self.NEW_ID, tags = "Couleur%s"%t.color)
            self.tree.insert("p%s"%self.NEW_ID, END, text = "Dépendences", values = [t.dependences], iid = "p%se7"%self.NEW_ID, tags = "Couleur%s"%t.color)
            self.NEW_ID += 1
            self.tree.tag_configure("Couleur%s"%t.color, background = t.color)

        # Add binding :
        self.tree.bind("<ButtonPress-1>", self.__mousePressedBefore)
        self.tree.bind_all("ButtonReleased-1>", self.__mouseReleased)
        self.tree.bind("<B1-Motion>", self.__mouseDragged)
    def __mouseReleased(self, event):
        self.mousepress = False
    def __mousePressedBefore(self, event):
        self.mousepress = True
        for i in range(self.NEW_ID):
            self.tree.selection_remove("p%s"%i)
            self.tree.selection_remove("p%se1"%i)
            self.tree.selection_remove("p%se2"%i)
            self.tree.selection_remove("p%se3"%i)
            self.tree.selection_remove("p%se4"%i)
            self.tree.selection_remove("p%se5"%i)
            self.tree.selection_remove("p%se6"%i)
            self.tree.selection_remove("p%se7"%i)
        self.after(10, self.__mousePressed, event)
    def __mousePressed(self, event):
        pass
    def __mouseDragged(self, event):
        if self.mousepress:
            self.mousepress = False
            pos = (max(event.x_root - 100, 0), max(event.y_root - 25, 0))
            for i in self.tree.selection(): # Parcourir et obtenir tout les éléments sélectionnés.
                print(i)
                print(self.tree.item(i))
                for t in self.taches:
                    if t.statut == "Inconnu":
                        if i == "p%s"%t.id:
                            tdnd = TaskInDnd(pos, self, t, command = self.__trouverPositionTache)
    def __trouverPositionTache(self, tache, x, y):
        """
        Cette méthode doit trouver en fonction des coordonnées x et y par rapport à l'écran,
        où mettre la tâche reçue en argument.
        """
        panneau = self.master.getPanneauActif()
        x -= panneau.winfo_rootx() # transformer les coordonnées pour qu'elles soient relatives au panneau.
        y -= panneau.winfo_rooty()
        if x >= 0 and y >= 0 and x < panneau.winfo_width() and y < panneau.winfo_height(): # s'assurer qu'on est au-dessus du panneau :
            region = panneau.identify_region(x, y)
            # TODO : faire un dialogue pour l'heure exacte /
            # TODO : arrondir l'heure ?
            if region is not None:
                tache = panneau.addTask(tache, region = region)
                for p in self.master.getToutLesPanneaux():
                    if p != panneau:
                        p.addTask(tache, region)

    def tri_alphabetique(self):
        pass
    def tri_priorite(self):
        pass


if __name__=='__main__':
    import Application
    Application.main()
