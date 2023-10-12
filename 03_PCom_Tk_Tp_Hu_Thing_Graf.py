from os import execv
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import messagebox
import paho.mqtt.client as mqtt
import json
import os
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


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
import wmi

#def read_from_port(ser):
#    while True:
#        reading = ser.readline().decode('utf-8').strip()
#        text.set(reading)

#ports = serial.tools.list_ports.comports()
#for port in ports:
#    print(port)

#ser = serial.Serial('/dev/ttyS0')  # Reemplaza '/dev/ttyS0' con el nombre de tu puerto COM
#ser = serial.Serial(
#    port='COM9', 
#    baudrate=9600, 
#    bytesize=serial.EIGHTBITS, 
#    parity=serial.PARITY_NONE, 
#    stopbits=serial.STOPBITS_ONE
#)


#++++++++++++++++ Ventana Principal +++++++++++++++++++++
root = Tk()
root.wm_title("TFD UCU Ver 1.0")
root.iconbitmap(r'Logo-UCU-001-FINAL-03_ID_Uruguay.ico')
root.resizable(width=False, height=False)
root.geometry('1360x720+0+0')
root.runTrue = 0



#+++++++++++++++++ Pestañas +++++++++++++++++++++++++++++
nb = tkinter.ttk.Notebook(root, width=1360, height=700)
nb.place(x=0, y=0)

tab1 = tkinter.ttk.Frame(nb)
nb.add(tab1, text=' Main ')

tab2 = tkinter.ttk.Frame(nb)
nb.add(tab2, text='  Thingsboard  ')

tab3 = tkinter.ttk.Frame(nb)
nb.add(tab3, text=' Comunicacion ')

tab5 = tkinter.ttk.Frame(nb)
nb.add(tab5, text='   Alarmas  ')

tab7 = tkinter.ttk.Frame(nb)
nb.add(tab7, text='   Info    ')




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



#+++++++++++++++++ List Box Com +++++++++++++++++++++++++++++

# Crea un widget de texto para mostrar los datos
text_widget = tk.Text(tab3)
# Ubica el widget de texto en una posición específica
text_widget.place(x=10, y=50, width=400, height=200)
#text_widget.pack()

def update_ports():
    # Listar los puertos COM disponibles
    ports = serial.tools.list_ports.comports()
    # Si hay al menos un puerto COM disponible, abre el primero
    if ports:
        ser = serial.Serial(ports[0].device, 9600)
        # Crear una lista con los nombres de los puertos
        port_list = [port.device for port in ports]
        # Asignar la lista al atributo 'values' del ComboBox
        cb['values'] = port_list
        # Lee una línea del puerto COM
        line = ser.readline().decode('utf-8').strip()

        # Añade la línea al widget de texto
        text_widget.insert('end', line + '\n')
    else:
        raise Exception("No se encontraron puertos COM disponibles")
    

#def read_from_port():
    #while True:
        # Lee una línea del puerto COM
        #line = ser.readline().decode('utf-8').strip()

        # Añade la línea al widget de texto
        #text_widget.insert('end', line + '\n')

# Crear el Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack()

# Crear un marco para contener el ComboBox y el botón
frame = ttk.Frame(tab3)
frame.pack(side=tk.LEFT, anchor='n', pady=250, padx=10)

# Crear el ComboBox dentro del marco y ubicarlo arriba
cb = ttk.Combobox(frame)
cb.pack(side=tk.TOP)

# Crear el botón para actualizar los puertos debajo del ComboBox
btn = ttk.Button(frame, text="Actualizar", command=update_ports)
btn.pack(side=tk.TOP)

# Llamar a update_ports para llenar el ComboBox inicialmente
update_ports()

# Crea y comienza un nuevo hilo para leer del puerto COM
#thread = threading.Thread(target=read_from_port)
#thread.start()

#+++++++++++++++++++++++++ Things +++++++++++++++++++++++++++++

# Datos del servidor Thingsboard
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'yFLwocekzsRJQuEEmePg'

# Datos a enviar
#data = {"temperature": update_temperature(), "humidity": 80}

# Crear el cliente MQTT
client = mqtt.Client()

# Establecer el token de acceso
client.username_pw_set(ACCESS_TOKEN)

# Conectar al servidor Thingsboard
client.connect(THINGSBOARD_HOST, 1883, 60)

# Enviar los datos
#client.publish('v1/devices/me/telemetry', json.dumps(data), 1)

# Desconectar del servidor
#client.disconnect()


#++++++++++++++++++++++++ Temp ++++++++++++++++++++++++++++++++
mi_variable = random.randint(80, 100)

def get_cpu_temperature():
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType==u'Temperature' and "cpu" in sensor.Name.lower():
            return sensor.Value

def update_temperature():
    # Conectar al servidor Thingsboard
    client.connect(THINGSBOARD_HOST, 1883, 60)
    temp = get_cpu_temperature()
    label.config(text="Temperatura CPU: " + str(temp) + " °C")
    data = {"temperature": temp, "humidity": mi_variable}
    #label.config(text="Humedad ambiente: " + "80" + "%")
    client.publish('v1/devices/me/telemetry', json.dumps(data), 1)
    root.after(1000, update_temperature)  # Actualizar la temperatura cada segundo

# Crear un marco para contener el label
frame2 = ttk.Frame(tab1)
frame2.pack(side=tk.LEFT, anchor='nw', pady=50, padx=50)

label = tk.Label(frame2, font=("Roboto", 20))
label.pack(side=tk.TOP)

update_temperature()  # Llamar a update_temperature para mostrar la temperatura inicialmente

# Desconectar del servidor
client.disconnect()
#++++++++++++++++++++++++ Graficos ++++++++++++++++++++++++++++++++

#def imou():
#    humidity = mi_variable
#    sv.set(humidity)
#    tab2.after(1000, imou)

#tab2 = Tk()
#sv = StringVar()
#e = Entry(tab2,width=10, textvariable=sv)
#e.pack()
#imou()
#update_temperature()

# Genera una lista de valores para la humedad
humidity2 = np.random.uniform(0, 100, 10)
temperature2 = np.random.uniform(0, 100, 10)

x8 = list(humidity2)
x9 = list(temperature2)



fig1 = Figure(figsize=(5, 4), dpi=100)
# Crea el primer subgráfico
ax1 = fig1.add_subplot(111)  # 211 significa "2 filas, 1 columna, primer gráfico"
ax1.plot(x8)
ax1.set_title('Gráfico de Humedad')

canvas1 = FigureCanvasTkAgg(fig1, master=tab2)
canvas1.draw()
canvas1.get_tk_widget().place(relx=0, rely=0.05, relwidth=0.4, relheight=0.4)

toolbar1 = NavigationToolbar2Tk(canvas1, tab2)
toolbar1.update()

# Crea la segunda figura y subgráfico
fig2 = Figure(figsize=(5, 4), dpi=100)
ax2 = fig2.add_subplot(111)
ax2.plot(x9)
ax2.set_title('Gráfico de Temperatura')

canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
canvas2.draw()
canvas2.get_tk_widget().place(relx=0, rely=0.45, relwidth=0.4, relheight=0.4)

toolbar2 = NavigationToolbar2Tk(canvas2, tab2)
toolbar2.update()









#++++++++++++++++++++++++  ++++++++++++++++++++++++++++++++

root.mainloop()
