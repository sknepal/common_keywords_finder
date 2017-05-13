import csv
import glob
import sys
from itertools import combinations
from collections import Counter
import Tkinter, tkFileDialog
from Tkinter import *
import tkMessageBox

class simpleapp_tk(Tkinter.Tk):

    def __init__(self,parent):
            """
            Initializes Tkinter
            """
            Tkinter.Tk.__init__(self,parent)
            self.parent = parent
            self.Lb1 = Tkinter.Listbox(parent)
            self.list = []
            self.initialize()
            
    def initialize(self):
            """
            Adds button, entry and grid layout
            """
            self.grid()
            self.entry = Tkinter.Entry(self)
            
            button_choose = Tkinter.Button(self,text=u"Choose a directory", command=self.OnChooseButtonClick)
            
            button_txt = Tkinter.Button(self, text=u"Export To TXT", command=self.OnExportTXTClick)
            
            button_csv = Tkinter.Button(self, text=u"Export To CSV", command=self.OnExportCSVClick)
            
            self.grid_columnconfigure(1,weight=1)
            
            self.Lb1.grid(row=1, column=0,columnspan=4, padx=13, pady=(10,4), sticky="nsew")
            
            button_txt.grid(row=4, column=0)
            button_csv.grid(row=4, column=1)
            button_choose.grid(row=4, column=2)
            
            self.resizable(True,False)

             
    def read_csv(self,directory):
        """
        Reads all the CSV files in the given directory and creates a nested list of the keywords from it.
    
        Args:
            directory: Directory where the CSV files exist.
    
        Returns:
            A nested list that consists of keywords that were found inside every CSV file.
            Number of files that were read.
        """
        files = glob.glob(directory + '/*.csv')
        number_of_files = len(files)
        print "Reading " + str(number_of_files) + " files. Please wait."
        keywords_list = []
        for file in files:
            f = open(file)
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            keywords = []
            for row in reader:
                keywords.append(row[1])
            keywords_list.append(keywords)
        return keywords_list, number_of_files

    def counters(self, keywords):
        """
        Takes as input a nested list of keywords, converts them to set, sorts them and returns those keywords as Counter objects.
    
        Args:
            keywords: A nested list of keywords.
    
        Returns:
            Counter objects.
        """
        pair_counter = Counter()
        for keyword in keywords:
            unique_tokens = sorted(set(keyword))
            pair_counter += Counter(unique_tokens)
        return pair_counter

        
    def OnChooseButtonClick(self):
            """
            Opens up the choose directory dialog. Calls the read_csv function and inserts the common keywords returned into the listbox.
            """
            try:
                directory = tkFileDialog.askdirectory(initialdir='.',title='Choose a directory')
                keywords, number_of_files = self.read_csv(directory)
                pairs = self.counters(keywords)
            
                list = []
            
                for common in pairs.most_common():
                    if common[1] >= (number_of_files/2):
                        list.append(common[0])
                    
                if not (list[0]=='0'):  
                    self.Lb1.insert("end", *list)
                else:
                    tkMessageBox.showinfo("Done","No common keywords found.")
                    
            except Exception as e:
                if isinstance(e, IndexError):
                    tkMessageBox.showwarning("Error","No CSV files found in the directory.")
                    
            self.list = list 
                         
                    
    def OnExportTXTClick(self):
        """
        Exports the common keywords to a txt file.    
        """
        if len(self.list)>0:
            f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt", initialfile="common.txt")
            if f is None: 
                return
            for item in self.list:
                f.write(item + "\n")
            f.close() 
            tkMessageBox.showinfo("Done", "File exported as TXT!")
        else:
            tkMessageBox.showwarning("Error","No keywords to export.")
        
    def OnExportCSVClick(self):
        """
        Exports the common keywords to a csv file.
        """
        if len(self.list)>0:
            f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv", initialfile="common.csv")
            if f is None:
                return
            writer = csv.writer(f)
            for keyword in self.list:
                writer.writerow([keyword])
            f.close   
            tkMessageBox.showinfo("Done", "File exported as CSV!")
        else:
            tkMessageBox.showwarning("Error","No keywords to export.")
   
            
    
if __name__ == "__main__":
    app = simpleapp_tk(None)
    w = 400 
    h = 240
    ws = app.winfo_screenwidth() 
    hs = app.winfo_screenheight() 
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app.title('Common Keywords Finder')
    app.mainloop()
    
    