import tkinter as tk
from tkinter import ttk
import hungarian_method as hm
from matrix_input import *


class main(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.win1 = tk.Toplevel()
        self.win1.geometry("350x50")
        self.win1.attributes('-topmost', 'true')
        btn = ttk.Button(self.win1, text="Create", command=self.win1_submit)
        self.e1 = tk.Entry(self.win1, width = 5)
        self.lbl = tk.Label(self.win1, text = "Enter the size of the matrix: ")
        self.lbl.grid(row=1, column=1)
        self.e1.grid(row=1, column=2)
        btn.grid(row=1, column=3, padx=10, pady=2)
        
    
    def win1_submit(self):
        self.table = MatrixInput(self, int(self.e1.get()), int(self.e1.get()))
        self.solve = ttk.Button(self, text="Solve", width=6, command=self.on_submit)
        self.parser = ttk.Button(self, text="Parser", width=6, command=self.on_parser)
        self.resultLabel = tk.Label(self, text = "", font=("Helvetica", 13), padx=30)
        self.table.grid(row=1, column=1, padx=30, pady=20)
        self.solve.grid(row=1, column= 2)
        self.parser.grid(row=1, column= 3, padx=20)
        self.resultLabel.grid(row=5,column= 1)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=2, weight=1)
        self.win1.destroy()

    def on_submit(self):
        solver = hm.Hungarian()
        sol = solver.solve(self.table.get())
        self.resultLabel["text"] = 'The Assignment is:  \n'
        for i in range(solver.n):
            self.resultLabel["text"] += ("Assignee #"+str(sol[i][0]+1)+" --> Task #"+str(sol[i][1]+1)+"\n")
        
        
    def on_parser(self):
        self.win2 = tk.Toplevel()
        self.win2.attributes('-topmost', 'true')
        self.tb = tk.Text(self.win2, height=10, width=30)
        self.parse = ttk.Button(self.win2, text="Parse", width=5, command=self.on_parse)
        self.tb.grid(row=1, column=1, padx=30, pady=30)
        self.parse.grid(row=1, column=2, padx=30)
        self.win2.grid_columnconfigure(index=0, weight=1)
        self.win2.grid_rowconfigure(index=2, weight=1)

        
    def on_parse(self):
        matStr = self.tb.get("1.0",'end-1c').split("--")
        row = 0
        col = 0
        for j in range(len(matStr)):
            elements = matStr[j].split("-")
            for i in elements:
                self.table._entry[(row, col)].insert(0, str(i))
                col =col+1
            row = row + 1
            col = 0
            
            
root = tk.Tk()
root.title("Hungarian Method")
#root.geometry("400x400")
main(root).pack(side="top", fill="both", expand=True)
root.mainloop()