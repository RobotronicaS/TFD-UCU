from os import execv
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import messagebox

import pickle
import serial
import time
import threading
import queue
import math
import tkinter.messagebox
import webbrowser
import numpy as np
import datetime
import tkinter as tk
from tkinter import StringVar
import serial.tools.list_ports


#def read_from_port(ser):
#    while True:
#        reading = ser.readline().decode('utf-8').strip()
#        text.set(reading)

#ports = serial.tools.list_ports.comports()
#for port in ports:
#    print(port)

#ser = serial.Serial('/dev/ttyS0')  # Reemplaza '/dev/ttyS0' con el nombre de tu puerto COM
ser = serial.Serial(
    port='COM8', 
    baudrate=9600, 
    bytesize=serial.EIGHTBITS, 
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE
)


#++++++++++++++++ Ventana Principal +++++++++++++++++++++
root = Tk()
root.wm_title("TFD UCU Ver 1.0")
root.iconbitmap(r'Logo-UCU-001-FINAL-03_ID_Uruguay.ico')
root.resizable(width=False, height=False)
root.geometry('1360x720+0+0')
root.runTrue = 0

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++ Pestañas +++++++++++++++++++++++++++++
nb = tkinter.ttk.Notebook(root, width=1360, height=700)
nb.place(x=0, y=0)

tab1 = tkinter.ttk.Frame(nb)
nb.add(tab1, text=' Main ')

tab2 = tkinter.ttk.Frame(nb)
nb.add(tab2, text='  Comunicacion  ')

tab3 = tkinter.ttk.Frame(nb)
nb.add(tab3, text=' Alarmas ')

tab5 = tkinter.ttk.Frame(nb)
nb.add(tab5, text='   Vision    ')

tab7 = tkinter.ttk.Frame(nb)
nb.add(tab7, text='   Info    ')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++ Apariencia +++++++++++++++++++++++++++++

def darkTheme():
  global curTheme
  curTheme = 0
  style = ThemedStyle(root)
  style.set_theme("black")
  style = ttk.Style()
  style.configure("Alarm.TLabel", foreground="IndianRed1", font = ('Arial','10','bold'))
  style.configure("Warn.TLabel", foreground="orange", font = ('Arial','10','bold'))
  style.configure("OK.TLabel", foreground="light green", font = ('Arial','10','bold'))
  style.configure("Jointlim.TLabel", foreground="light blue", font = ('Arial','8'))
  style.configure('AlarmBut.TButton', foreground ='IndianRed1')
  style.configure('Frame1.TFrame', background='white')

def lightTheme():
  global curTheme
  curTheme = 1
  style = ThemedStyle(root)
  style.set_theme("keramik")
  style = ttk.Style()
  style.configure("Alarm.TLabel", foreground="red", font = ('Arial','10','bold'))
  style.configure("Warn.TLabel", foreground="dark orange", font = ('Arial','10','bold'))
  style.configure("OK.TLabel", foreground="green", font = ('Arial','10','bold'))
  style.configure("Jointlim.TLabel", foreground="dark blue", font = ('Arial','8'))
  style.configure('AlarmBut.TButton', foreground ='red')
  style.configure('Frame1.TFrame', background='black')

darkTheme()     # Llamada a la función para cambiar el tema
lightTheme()    # Llamada a la función para cambiar el tema
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++ List Box Com +++++++++++++++++++++++++++++

def update_ports():
    # Listar los puertos COM disponibles
    ports = serial.tools.list_ports.comports()
    
    # Crear una lista con los nombres de los puertos
    port_list = [port.device for port in ports]
    
    # Asignar la lista al atributo 'values' del ComboBox
    cb['values'] = port_list

# Crear el Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack()

# Crear un marco para contener el ComboBox y el botón
frame = ttk.Frame(tab1)
frame.pack(side=tk.LEFT, anchor='n', pady=40, padx=20)

# Crear el ComboBox dentro del marco y ubicarlo arriba
cb = ttk.Combobox(frame)
cb.pack(side=tk.TOP)

# Crear el botón para actualizar los puertos debajo del ComboBox
btn = ttk.Button(frame, text="Actualizar", command=update_ports)
btn.pack(side=tk.TOP)

# Llamar a update_ports para llenar el ComboBox inicialmente
update_ports()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++




#text = StringVar()
#label = tk.Label(root, textvariable=text)
#label.pack()

#thread = threading.Thread(target=read_from_port, args=(ser,))
#thread.start()

root.mainloop()
