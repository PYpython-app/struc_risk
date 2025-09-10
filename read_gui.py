from tkinter import *
from tkinter import filedialog

def open_file():
    filepath=filedialog.askopenfilename(filetypes=[("Structured Product Termsheet File","*.pdf")])
    struc_fs=filepath
# GUI avec Tkinter
window=Tk()
window.geometry("1600x800")
window.title("Structured Product Analysis")
window.config(background = "black")
label_txt=Label(window,
            text='Stuctured Product Analysis',
            font=('arial',70,'bold'),
            fg='black',
            bg='#008aa6',
            relief=RAISED,
            bd=10)
label_txt.place(x=350,y=10)
label_instr=Label(window,
            text='To run the analysis you must select a file first and then press run the analysis',
            font=('arial',30,'bold'),
            fg='black',
            bg='white',
            relief=RAISED,
            bd=10)
label_instr.place(x=300,y=250)
label_warning=Label(window,
            text='WARNING! The termsheets files must be in the same directory as the program',
            font=('arial',50,'bold'),
            fg='red',
            bg='white',
            relief=RAISED,
            bd=10,
            wraplength=1500)
label_warning.place(x=20,y=650)
but_openf=Button(window, text='1. Click to select termsheet')
but_openf.config(font=('arial',25,'bold'))
but_openf.config(command=open_file)
but_openf.place(x=300, y=400)
but_run=Button(window, text='2. Run the analysis')
but_run.config(font=('arial',25,'bold'))
but_run.place(x=300, y=500)
window.mainloop()