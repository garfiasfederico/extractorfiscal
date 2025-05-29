from customtkinter import CTk, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkRadioButton
from tkinter import PhotoImage,messagebox
import time
from zeep import Client
from requests.exceptions import HTTPError,ConnectionError

usuario_ = ""
password_ = ""
valido = True
usuario = ""
password = ""
errorl = ""
root = ""

def autenticarse():    
    global usuario_,password_,usuario,password,errorl,root
    usuario_ = usuario.get()    
    password_ = password.get()    
    print(f"Usuario: {usuario_} password: {password_}")
    if(valida()==True):        
        errorl.configure(text="Accediendo...",text_color="white")                    
        autentica = consumeautenticarse(usuario_,password_)
        if(autentica==True):
            errorl.configure(text="Cedenciales correctas!",text_color="green")
            #root.destroy()          
        else:
            if(autentica!=404):
                errorl.configure(text="Cedenciales incorrectas!",text_color="red")
        #import main_old
    else:
        errorl.configure(text="Datos incompletos!",text_color="red")

def valida():    
    valido = True    
    if(usuario_==""):        
        valido=False
        usuario.configure(border_color="red")
    else:
        usuario.configure(border_color=color_principal)

    if(password_==""):        
        valido=False
        password.configure(border_color="red")
    else:
        password.configure(border_color=color_principal)

    return valido

def main():
    global usuario,password,color_principal,errorl,root
    color_principal = "#e3e3e3"

    root = CTk();
    root.title("Extractor Fiscal V.1.0")
    root.geometry("400x500+800+150")
    root.minsize(400,500)
    root.resizable(False,False)
    root.config(bg=color_principal)

    principal = PhotoImage(file="public/images/main.png")

    #principal.config(width=150,height=150)

    frame = CTkFrame(root,fg_color=color_principal)
    frame.grid(column=0,row=0,sticky="nsew", padx=50,pady=50)

    frame.columnconfigure([0,1],weight=1)
    frame.rowconfigure([0,1,2,3,4,5],weight=1)

    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

    CTkLabel(frame, text="",image=principal).grid(columnspan=2, row=0)
    usuario = CTkEntry(frame,font=("Arial",12),placeholder_text="Usuario",border_color="gray",fg_color="white",width=220,height=40,text_color="black")
    usuario.grid(columnspan=2,row=1,padx=4,pady=4)

    password = CTkEntry(frame,font=("Arial",12),placeholder_text="Password",border_color="gray",fg_color="white",width=220,height=40,show="*",text_color="black")
    password.grid(columnspan=2,row=2,padx=4,pady=4)

    acceder = CTkButton(frame,text="Acceder", hover_color="gray", corner_radius=12, border_width=2,height=40,fg_color="#24B1E0",cursor="arrow",command=autenticarse,border_color="#24B1E0")
    acceder.grid(columnspan=2,row=3, padx=8,pady=8)

    errorl = CTkLabel(frame, text="",text_color="orange",font=("Arial",12))
    errorl.grid(columnspan=2, row=4)

    #Colocamos el icono a la aplicación
    root.call("wm",'iconphoto',root._w,principal)
    root.mainloop();

def consumeautenticarse(usuario,password):    
    global errorl
    #wsdl = 'http://127.0.0.1:8000/ws/autenticarse?wsdl'
    #client = zeep.Client(wsdl=wsdl)
    #plan_client = client.bind('RoutingService', 'BasicHttpBinding_LFCPaymentPlanDetailsServices')
    #plan_client.service.Autenticarse(usuario, password)
    #print(plan_client.service.Autenticarse(usuario, password))
    try:
        client = Client('http://127.0.0.1:8000/soap/wsdl')
        result = client.service.autenticarse(usuario, password)
        return result
    except HTTPError as err:
        messagebox.showerror("Autenticación de Usuario",f"Error en el servicio {err.args[0]}")
        errorl.configure(text="",text_color="white") 
        return 404
    except ConnectionError :
        messagebox.showerror("Autenticación de Usuario",f"No es posible conectarse al servicio")
        errorl.configure(text="",text_color="white") 
        return 404
main()
