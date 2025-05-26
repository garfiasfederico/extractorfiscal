import init
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Extractor Fiscal V.1")
root.resizable(width=False,height=False)
root.config(background="#2F6C68")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="RFC del contribuyente:",font=('Arial',12)).grid(column=0, row=0)
ttk.Label(frm, text=init.rfc,font=('Arial',16)).grid(column=1, row=0)
ttk.Label(frm, text="Nombre o razón social:",font=('Arial',12)).grid(column=0, row=1)
ttk.Label(frm, text=init.razon_social,font=('Arial',16)).grid(column=1, row=1)
ttk.Label(frm, text="Vigencia FIEL:",font=('Arial',12)).grid(column=0, row=2)
ttk.Label(frm, text="",font=('Arial',16)).grid(column=1, row=2)

root.mainloop()