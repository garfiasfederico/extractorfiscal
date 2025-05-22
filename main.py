import init
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Extractor Fiscal V.1");
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="RFC del contribuyente:",font=('Arial',12)).grid(column=0, row=0)
ttk.Label(frm, text=init.rfc,font=('Arial',16),anchor="w").grid(column=1, row=0)
ttk.Label(frm, text="Nombre o razón social:",font=('Arial',12)).grid(column=0, row=1)
ttk.Label(frm, text=init.razon_social,font=('Arial',16),anchor="w").grid(column=1, row=1)
root.mainloop()