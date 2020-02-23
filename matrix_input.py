import tkinter as tk
from tkinter import ttk

class MatrixInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        
        self._entry = {}
        self.rows = rows
        self.columns = columns
        vcmd = (self.register(self._validate), "%P")
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = ttk.Entry(self, validate="key", width=5, validatecommand=vcmd)
                e.grid(row=row, column=column, stick="nsew", padx=3, pady=3)
                self._entry[index] = e
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        self.grid_rowconfigure(rows, weight=1)

    def get(self):        
        mat = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(int(self._entry[index].get()))
            mat.append(current_row)
        return mat

    def _validate(self, P):
        
        if P.strip() == "":
            return True

        try:
            f = int(P)
        except ValueError:
            self.bell()
            return False
        return True