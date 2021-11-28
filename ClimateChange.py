#Program for IHACK!!
#Programmed by Team 'Data Pirates'
#Justin George, Anamika C, Salvin Jose K, Jibin PB
#Designed on 28-11-2021

import tkinter as tk
import numpy as np
from scipy.integrate import odeint
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os

w,h = (1000, 800)

frameW = w//3-20
frameH =  h-20

canvasW = 2*w//3-10
canvasH = frameH//2

sigma, tlw,tsw, s, T0,T1  = (5.67037*10**(-8),0.2,0.9,342,237.15,237.15)
e = 0.01
def create_circle(x, y, r, canvasName,col = "black"): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill=col,outline=col)

def eqn1(co2, a, s, sigma): #  Static energy balance
    #a, s, e, sigma = parms
    e = 0.633 - 7.1*10**(-5)*co2
    Ts =  ((1-a)*s /(e* sigma)) **(1/4)
    return Ts

def s_shape(T,s,sigma):
    return (1-at(T))*s/(sigma*(T**4))
def at(T):
    return 0.495 - 0.205*np.tanh(0.133*(T-275))
def et(t):
  return 0.65 - 0.1*t

def et_up(t):
    return 0.1 + 0.1*t

def eqn2( T,e, s, sigma):
   # s, e, sigma = parms

    dTdt = 10*((1.0-at(T))*s - e* sigma * (T**4)) #+np.random.normal(0, 1)
    return dTdt

def eqn3( T,t, s, sigma,lamd,down=True):  #  Dynamic energy balance (differential equations)
   # s, e, sigma = parms
    if down:
        dTdt = lamd*((1.0-at(T))*s - et(t)* sigma * (T**4) )#+ np.random.normal(0,1)
    else:
        dTdt = lamd*((1.0-at(T))*s - et_up(t)* sigma * (T**4) )
    return dTdt


root = tk.Tk()   #  Set up the user interface
root.title("Simple Climate Models")
root.geometry(f"{w}x{h}")
root.configure(background='silver')

# bg= ImageTk.PhotoImage(file="plot.png")

choice = tk.Frame(root,width = frameW, height = frameH, bd = 0,bg = "lightgray")
choice.grid(row=0,column = 0, padx = 5, pady = 5)

graph = tk.Frame(root,width =canvasW, height =canvasH,bd=0,bg = "lightgray")
graph.grid(row=0,column = 1,padx=5,pady = 5)

title = tk.Label(graph,text = "CO2 Concentration in Atmosphere",font = ('arial', 14, 'bold')).grid(row=0,column=0)

canvas1 = tk.Canvas(graph,width =canvasW-80, height =canvasH-20, bg = "ivory")
canvas1.grid(row=1,column = 0,padx=5,pady = 5)

gif1 = ImageTk.PhotoImage(file = 'CO2.png') #  This is the image of the CO2 rise over the last hundrad years


canvas1.create_image(0,0,image=gif1, anchor=tk.NW)
canvas2 = tk.Canvas(graph,width =canvasW-80, height =canvasH-20, bg = "ivory")
canvas2.grid(row=2,column = 0,padx=5,pady = 5)




ch1 = tk.Frame(choice,width = frameW,height = frameH//3,bd = 0, bg = "ivory")
ch1.grid(row=0,column= 0,padx = 5, pady = 5 )

ch3 = tk.Frame(choice,width = frameW,height = frameH//3,bd = 0, bg = "ivory")
ch3.grid(row=2,column= 0,padx = 5, pady = 5 )

fontsize =11


string_label = tk.Label(ch1, text=" A Simple Energy Balance Model",font = ('arial', fontsize, 'bold')).grid(row=0, column=0, pady=5, padx = 5)

string_label = tk.Label(ch1, text="The albedo: a",font = ('arial', fontsize)).grid(row=1, column=0, pady=5, padx = 5)
par_a = tk.Scale(ch1, from_=0, to =1,font = ('arial', fontsize),tickinterval= 0.5,resolution= 0.01,orient = tk.HORIZONTAL,width = 10,length = 100)
par_a.set(0.31)
par_a.grid(row=1,column=1,columnspan=5,padx = 5,pady=5)

string_label = tk.Label(ch1, text="The lowest value of CO2 (ppm)",font = ('arial', fontsize)).grid(row=2, column=0, pady=5, padx = 5)
par_ts = tk.Scale(ch1, from_=200, to =430,font = ('arial', fontsize),orient = tk.HORIZONTAL,width = 10,length = 100)
par_ts.set(280)
par_ts.grid(row=2,column=2,columnspan=5,padx = 5,pady=5)

string_label = tk.Label(ch1, text="The highest value of CO2 (ppm)",font = ('arial', fontsize)).grid(row=3, column=0, pady=5, padx = 5)
par_tl = tk.Scale(ch1, from_=par_ts.get(), to =1000,font = ('arial', fontsize),orient = tk.HORIZONTAL,width = 10,length = 100)
par_tl.set(430)
par_tl.grid(row=3,column=2,columnspan=5,padx = 5,pady=5)

string_label = tk.Label(ch3, text=" A more complex Model with changing albedo ",font = ('arial', fontsize, 'bold')).grid(row=0, column=0,columnspan=2, pady=5, padx = 2)

string_label = tk.Label(ch3, text="cimate response rate choice 1",font = ('arial', fontsize)).grid(row=1, column=0, pady=5, padx = 2)
par_1 = tk.Scale(ch3, from_=1, to= 500,font = ('arial', fontsize),orient = tk.HORIZONTAL,width = 10,length = 100)
par_1.set(1)
par_1.grid(row=1,column=1,padx = 5,pady=10)


string_label = tk.Label(ch3, text="cimate response rate choice 2",font = ('arial', fontsize)).grid(row=2, column=0, pady=5, padx = 2)
par_2 = tk.Scale(ch3, from_=1, to =500,font = ('arial', fontsize),orient = tk.HORIZONTAL,width = 10,length = 100)
par_2.set(10)
par_2.grid(row=2,column=1,padx = 5,pady=10)

string_label = tk.Label(ch3, text="cimate response rate choice 3",font = ('arial', fontsize)).grid(row=3, column=0, pady=5, padx = 2)
par_3 = tk.Scale(ch3, from_=1, to =500,font = ('arial', fontsize),orient = tk.HORIZONTAL,width = 10,length = 100)
par_3.set(500)
par_3.grid(row=3,column=1,padx = 2,pady=10)

def slide():
    global a, sigma, s, e
    #my_label = tk.Label(choice,text=angle1.get())
    #my_label.grid(row=6,column=1)
    a = par_a.get()
    e0 = par_tl.get()
    e1 = par_ts.get()
    co2 = np.linspace(e0,e1,100)
    #y0 = par_T.get()
    Ts = eqn1(co2, a, s, sigma)
    #sol = odeint(eqn1, y0, e, args=(a,s, sigma))
    plt.figure()
    plt.plot(co2, Ts, 'b')
    plt.title("Temperature vs CO2 - simple model")
    #plt.legend(loc='best')
    plt.ylabel("T")
    plt.xlabel('CO2-Atmosphere radiation absorption ability')
    #plt.xticks(np.arange(2),['Low CO2','High CO2'])
    plt.grid()
    plt.show()
    plt.close()


def plot3():
    global sigma, s

    t = np.linspace(0,3.5,200)
    y0 = 237
    lamd1 = par_1.get()
    lamd2 = par_2.get()
    lamd3 = par_3.get()

#  Solve the differential equations of Model 2
#

    sol1 = odeint(eqn3,y0,t, args=(s,sigma,lamd1))
    sol2 = odeint(eqn3,y0,t, args=(s,sigma,lamd2))
    sol3 = odeint(eqn3,y0,t, args=(s,sigma,lamd3))

    es = et(t)
    Tss = np.linspace(220,350,100)
    ess= s_shape(Tss,s,sigma)

    plt.figure(figsize=(10,6))
    plt.plot(ess,Tss,'gray', label = "tipping lines")
    plt.plot(es, sol1, 'coral',label=f"Reaction rate {lamd1}")
    plt.plot(es, sol2, 'orange',label=f"Reaction rate  {lamd2}")
    plt.plot(es, sol3, 'red',label=f"Reaction rate  {lamd3}")

    plt.title("Climate change with increasing CO2 concentration")

    #  plt.axis('equal')

    plt.ylabel('T')
    plt.ylim(220,380)
    plt.yticks(np.arange(200, 380, step=20),np.arange(200, 380, step=20))
    plt.xlabel('e')

    plt.xlim(0.2,0.8)
    plt.grid()
    plt.legend()
    plt.show()
    plt.close()

    return


def plot2():
    global sigma, s
    t = np.linspace(0,8,200)
    y0 = 237
    lamd1 = par_1.get()
    lamd2 = par_2.get()
    lamd3 = par_3.get()
    sol4 = odeint(eqn3,y0,t,args = (s,sigma,lamd1,False))
    sol5 = odeint(eqn3,y0,t,args = (s,sigma,lamd2,False))
    sol6 = odeint(eqn3,y0,t,args = (s,sigma,lamd3,False))
    Tss = np.linspace(220,350,100)
    ess= s_shape(Tss,s,sigma)
    es2 = et_up(t)

    plt.figure(figsize=(10,6))
    plt.title("Climate Start with high CO2 to low CO2")
    plt.plot(ess,Tss,'gray', label = "tipping lines")
    plt.plot(es2[1:], sol4[1:], 'coral',label=f"Reaction rate {lamd1}")
    plt.plot(es2[1:], sol5[1:], 'orange',label=f"Reaction rate  {lamd2}")
    plt.plot(es2[1:], sol6[1:], 'red',label=f"Reaction rate  {lamd3}")

    plt.legend()
    plt.ylabel('T')
    plt.ylim(220,380)
    plt.yticks(np.arange(200, 380, step=20),np.arange(200, 380, step=20))
    plt.xlabel('e')
    plt.xlim(0.2,0.8)
    plt.grid()
    plt.show()
    plt.close()
    return

def snd1():
    path = os.getcwd()
    os.system(path +"/movie.mp4")


my_btn = tk.Button(ch1,text="Graph the Simple Model", command = slide,padx=5,pady=5,font = ('arial', 14, 'bold'))
my_btn.grid(row=6,column=0,padx=5,pady=5)



my_btn = tk.Button(ch3,text="Graph - increasing CO2", command = plot3,padx=5,pady=5,font = ('arial', 14, 'bold'))
my_btn.grid(row=6,column=0,padx=5,pady=5)

my_btn = tk.Button(ch3,text="Graph - decreasing CO2", command = plot2,padx=5,pady=5,font = ('arial', 14, 'bold'))
my_btn.grid(row=7,column=0,padx=5,pady=5)
# var = tk.IntVar()
my_btn = tk.Button(canvas2,text="Play the video", command = snd1,padx=5,pady=5,font = ('arial', 14, 'bold'))
my_btn.grid(row=0,column=0, columnspan= 4,padx=5,pady=10)



root.mainloop()




