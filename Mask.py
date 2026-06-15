import pandas as pd
import statistics
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt

df=None
variables=[]
plotTypes=['Line plot', 'Scatter plot', 'Bar Chart']

def importFile():
    path=filedialog.askopenfilename(title='Select the file', filetypes=[('CSV files', '*.csv')])
    if path:
        readFile(path)

def readFile(path):
    global df
    global variables
    try:
        df = pd.read_csv(path)
        label.config(text=f'Used file: {path}')
        variables=list(df.columns)

        updateVariablesInScrollbar(variables, variable1)
        updateVariablesInScrollbar(variables, variable2)
        plotType.pack(side='left')

    except Exception as e:
        label.config(text=f'Error: {e}')


def updateVariablesInScrollbar(variables, scrollbar):
    '''
    :param variables: The new list of chosable items in the scrollbar
    :param scrollbar: The scrollbar which variables will be set to the variables list
    '''

    scrollbar.config(values=variables)
    scrollbar.pack(side='left')
    

def createChart(event):

    if df is None:
        return
    if not variable1.get() or not variable2.get() or not plotType.get():
        return
    
    type=plotType.get()
    x_vars=df[variable1.get()]
    y_vars=df[variable2.get()]

    match type:
        case 'Line plot':
            createLinePlot(x_vars, y_vars)
        case 'Bar Chart':
            createBarChart(x_vars, y_vars)
        case _:
            createScatterPlot(x_vars, y_vars)
            

def createLinePlot(x_vars, y_vars):
    global df
    plt.plot(x_vars, y_vars, marker='o')
    plt.show()

def createScatterPlot(x_vars, y_vars):
    global df
    plt.scatter(x_vars, y_vars, marker='o')
    plt.show()

def createBarChart(x_vars, y_vars):
    global df
    plt.bar(x_vars, y_vars)
    plt.show()

window=tk.Tk()
window.geometry("750x750")
window.title('Mask')
panelBar=tk.Frame(window)
panelBar.pack(side='top', anchor='nw', pady=20, padx=20)

uploadButton=tk.Button(panelBar, text='Import CSV File', command=importFile)
uploadButton.pack(side='left')


variable1 = ttk.Combobox(
    panelBar,
    values=variables,
    state="readonly"
)

variable2 = ttk.Combobox(
    panelBar,
    values=variables,
    state="readonly"
)

plotType = ttk.Combobox(
    panelBar,
    values=plotTypes,
    state="readonly",
)

variable1.bind("<<ComboboxSelected>>", createChart)
variable2.bind("<<ComboboxSelected>>", createChart)
plotType.bind("<<ComboboxSelected>>", createChart)


label = tk.Label(panelBar, text='')
label.pack(side='right')
window.mainloop()