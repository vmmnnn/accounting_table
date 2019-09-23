"""
https://gist.github.com/uroshekic/11078820
Inspired by http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/

! При нажатии кнопкой мыши на вариант, он не выбирается без выбора клавишами

"""
from tkinter import font
from tkinter import *
import re

class CustomListBox(Listbox):

    def __init__(self, master=None, *args, **kwargs):
        Listbox.__init__(self, master, *args, **kwargs)

        self.bg = "white"
        self.fg = "black"
        self.h_bg = "#eee8aa"
        self.h_fg = "blue"

        self.current = -1  # current highlighted item

        self.fill()

        self.bind("<Motion>", self.on_motion)
        self.bind("<Leave>", self.on_leave)

    def fill(self, number=15):
        """Fills the listbox with some numbers"""
        for i in range(number):
            self.insert(END, i)
            self.itemconfig(i, {"bg": self.bg})
            self.itemconfig(i, {"fg": self.fg})

    def reset_colors(self):
        """Resets the colors of the items"""
        for item in self.get(0, END):
            self.itemconfig(item, {"bg": self.bg})
            self.itemconfig(item, {"fg": self.fg})

    def set_highlighted_item(self, index):
        """Set the item at index with the highlighted colors"""
        self.itemconfig(index, {"bg": self.h_bg})
        self.itemconfig(index, {"fg": self.h_fg})

    def on_motion(self, event):
        """Calls everytime there's a motion of the mouse"""
        index = self.index("@%s,%s" % (event.x, event.y))
        if self.current != -1 and self.current != index:
            self.reset_colors()
            self.set_highlighted_item(index)
        elif self.current == -1:
            self.set_highlighted_item(index)
        self.current = index

    def on_leave(self, event):
        self.reset_colors()
        self.current = -1




##################################################################################


class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, window, *args, **kwargs):
        # Listbox length

        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 6

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches
        self.scroll_offset = 0
        self.listbox_font = font.Font(size=8)
        self.window = window
        self.entry = Entry.__init__(self, *args, **kwargs)

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Button-1>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.entry.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(self.window, width=self["width"], height=self.listboxLength, selectmode=SINGLE, font=self.listbox_font)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.bind("<Escape>", self.listbox.destroy)
                    self.listbox.bind("<Motion>", self.mouse_move)
                    self.listbox.bind("<MouseWheel>", self.mouse_scroll)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END,w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.scroll_offset = 0
            self.listboxUp = False
            self.icursor(END)

    def mouse_move(self, event):
        abs_coord_x = self.listbox.winfo_pointerx() - self.listbox.winfo_rootx()    # Координаты мыши в listbox
        abs_coord_y = self.listbox.winfo_pointery() - self.listbox.winfo_rooty()    # Высота пункта в listbox = 20
        #if self.listbox.curselection() == ():
        #    index = '0'
        #else:
    #        index = self.listbox.curselection()[0]
        ind = abs_coord_y // 12
        if ind == 0:
            ind = (abs_coord_y + 1) // 12
        print(abs_coord_y)
        #print(ind, self.scroll_offset)
        ind = ind + self.scroll_offset
        #ind = ind + int(index)
        self.listbox.activate(ind)

    def mouse_scroll(self, event):
        if event.num == 5 or event.delta == -120:   # Down
            self.scroll_down(event)
        #    if self.listbox.curselection() == ():
    #            index = '0'
#            else:
#                index = self.listbox.curselection()[0]
#
#            if index != END:
#                self.listbox.selection_clear(first=index)
#                index = str(int(index) + 1)
#
#                self.listbox.see(index) # Scroll!
#                self.listbox.selection_set(first=index)
#                self.listbox.activate(index)
        if event.num == 4 or event.delta == 120:    # Up
            self.scroll_up(event)

    def scroll_down(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
            print(self.listbox.size())
            if index != END:
                print(index, END)
                if str(int(index) + 1) != END and str(int(index) + 2) != END and str(int(index) + 3) != END:
                    self.scroll_offset = self.scroll_offset + 4
                else:
                    self.scroll_offset = self.scroll_offset + 2
                self.listbox.selection_clear(first=index)
                index = str(int(index) + self.scroll_offset)
                #self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def scroll_up(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
            if index != '0':
                if str(int(index) - 1) != '0' and str(int(index) - 2) != '0' and str(int(index) - 3) != '0':
                    self.scroll_offset = self.scroll_offset - 4
                else:
                    self.scroll_offset = self.scroll_offset - 2
                self.listbox.selection_clear(first=index)
                index = str(int(index) - self.scroll_offset)
                #self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]



class AutocompleteEntry1(Entry):
    def __init__(self, autocompleteList, window, *args, **kwargs):
        # Listbox length

        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 6

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        self.window = window
        self.entry = Entry.__init__(self, *args, **kwargs)

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Button-1>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.listboxUp = False

    def mouse_move(self, event):
        abs_coord_x = self.listbox.winfo_pointerx() - self.listbox.winfo_rootx()    # Координаты мыши в listbox
        abs_coord_y = self.listbox.winfo_pointery() - self.listbox.winfo_rooty()    # Высота пункта в listbox = 20
        if self.listbox.curselection() == ():
            index = '0'
        else:
            index = self.listbox.curselection()[0]
        #print(index)
        ind = abs_coord_y // 20
        if ind == 0:
            ind = (abs_coord_y + 1) // 20
        ind = ind + int(index)
        self.listbox.activate(ind)

    def mouse_scroll(self, event):
        if event.num == 5 or event.delta == -120:   # Down
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)
        if event.num == 4 or event.delta == 120:    # Up
            print(222222)

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.entry.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(self.window, width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.bind("<Motion>", self.mouse_move)
                    self.listbox.bind("<MouseWheel>", self.mouse_scroll)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END,w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]

def matches(fieldValue, acListEntry):
    pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
    return re.match(pattern, acListEntry)


'''
if __name__ == '__main__':
    autocompleteList = [ 'Dora Lyons (7714)', 'Hannah Golden (6010)', 'Walker Burns (9390)', 'Dieter Pearson (6347)', 'Allen Sullivan (9781)', 'Warren Sullivan (3094)', 'Genevieve Mayo (8427)', 'Igor Conner (4740)', 'Ulysses Shepherd (8116)', 'Imogene Bullock (6736)', 'Dominique Sanchez (949)', 'Sean Robinson (3784)', 'Diana Greer (2385)', 'Arsenio Conrad (2891)', 'Sophia Rowland (5713)', 'Garrett Lindsay (5760)', 'Lacy Henry (4350)', 'Tanek Conley (9054)', 'Octavia Michael (5040)', 'Kimberly Chan (1989)', 'Melodie Wooten (7753)', 'Winter Beard (3896)', 'Callum Schultz (7762)', 'Prescott Silva (3736)', 'Adena Crane (6684)', 'Ocean Schroeder (2354)', 'Aspen Blevins (8588)', 'Allegra Gould (7323)', 'Penelope Aguirre (7639)', 'Deanna Norman (1963)', 'Herman Mcintosh (1776)', 'August Hansen (547)', 'Oscar Sanford (2333)', 'Guy Vincent (1656)', 'Indigo Frye (3236)', 'Angelica Vargas (1697)', 'Bevis Blair (4354)', 'Trevor Wilkinson (7067)', 'Kameko Lloyd (2660)', 'Giselle Gaines (9103)', 'Phyllis Bowers (6661)', 'Patrick Rowe (2615)', 'Cheyenne Manning (1743)', 'Jolie Carney (6741)', 'Joel Faulkner (6224)', 'Anika Bennett (9298)', 'Clayton Cherry (3687)', 'Shellie Stevenson (6100)', 'Marah Odonnell (3115)', 'Quintessa Wallace (5241)', 'Jayme Ramsey (8337)', 'Kyle Collier (8284)', 'Jameson Doyle (9258)', 'Rigel Blake (2124)', 'Joan Smith (3633)', 'Autumn Osborne (5180)', 'Renee Randolph (3100)', 'Fallon England (6976)', 'Fallon Jefferson (6807)', 'Kevyn Koch (9429)', 'Paki Mckay (504)', 'Connor Pitts (1966)', 'Rebecca Coffey (4975)', 'Jordan Morrow (1772)', 'Teegan Snider (5808)', 'Tatyana Cunningham (7691)', 'Owen Holloway (6814)', 'Desiree Delaney (272)', 'Armand Snider (8511)', 'Wallace Molina (4302)', 'Amela Walker (1637)', 'Denton Tillman (201)', 'Bruno Acevedo (7684)', 'Slade Hebert (5945)', 'Elmo Watkins (9282)', 'Oleg Copeland (8013)', 'Vladimir Taylor (3846)', 'Sierra Coffey (7052)', 'Holmes Scott (8907)', 'Evelyn Charles (8528)', 'Steel Cooke (5173)', 'Roth Barrett (7977)', 'Justina Slater (3865)', 'Mara Andrews (3113)', 'Ulla Skinner (9342)', 'Reece Lawrence (6074)', 'Violet Clay (6516)', 'Ainsley Mcintyre (6610)', 'Chanda Pugh (9853)', 'Brody Rosales (2662)', 'Serena Rivas (7156)', 'Henry Lang (4439)', 'Clark Olson (636)', 'Tashya Cotton (5795)', 'Kim Matthews (2774)', 'Leilani Good (5360)', 'Deirdre Lindsey (5829)', 'Macy Fields (268)', 'Daniel Parrish (1166)', 'Talon Winters (8469)' ]

    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)

    root = Tk()
    entry = AutocompleteEntry(autocompleteList, root, listboxLength=6, width=32, matchesFunction=matches)
    entry.grid(row=0, column=0)
    Button(text='Python').grid(column=0)
    Button(text='Tkinter').grid(column=0)
    Button(text='Regular Expressions').grid(column=0)
    Button(text='Fixed bugs').grid(column=0)
    Button(text='New features').grid(column=0)
    Button(text='Check code comments').grid(column=0)
    root.mainloop()
'''
