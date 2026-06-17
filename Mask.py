import pandas as pd
import statistics
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt

df=None
variables=[]
plotTypes=['Line plot', 'Scatter plot', 'Bar Chart', 'Pie Chart']
chosen_variables=[]
currentVarNumber=0


def importFile():
    path=filedialog.askopenfilename(title='Select the file', filetypes=[('CSV files', '*.csv')])
    if path:
        readFile(path)

def readFile(path):
    global df
    global variables
    try:
        df = pd.read_csv(path)
        filePathLabel.config(text=f'Used file: {path}')
        variables=list(df.columns)

        diagramTypeLabel.pack(side='left')
        plotType.pack(side='left')
        varNumber.pack(side='left')
        variableNumberScrblr.pack(side='left')
        createChartBtn.pack(side='left')

    except Exception as e:
        filePathLabel.config(text=f'Error: {e}')


def updateVariablesInScrollbar(variables, scrollbar):
    '''
    :param variables: The new list of chosable items in the scrollbar
    :param scrollbar: The scrollbar which variables will be set to the variables list
    '''

    scrollbar.config(values=variables)
    scrollbar.pack(side='left')
    

def createChart():

    global currentVarNumber
    global chosen_variables

    if df is None:
        return
    if chosen_variables==[] or currentVarNumber==0:
        return
    
    type=plotType.get()
    x_vars=df[chosen_variables[0].get()]
    y_vars=[]
    for i in range(1,currentVarNumber):
        y_vars.append(df[chosen_variables[i].get()])

    match type:
        case 'Line plot':
            createLinePlot(x_vars, y_vars)
        case 'Bar Chart':
            createBarChart(x_vars, y_vars)
        case 'Pie Chart':
            createPieChart(x_vars, y_vars)
        case _:
            createScatterPlot(x_vars, y_vars)
            

def createLinePlot(x_vars, y_vars):
    global df
    global currentVarNumber
    global chosen_variables

    plt.xlabel(chosen_variables[0].get())
    for i in range(0, len(y_vars)):
        plt.plot(x_vars, y_vars[i], marker='o', label=chosen_variables[i+1].get())
    
    plt.legend()

    plt.grid(axis='x', alpha=0.6)
    plt.grid(axis='y', alpha=0.6)
    plt.xticks(x_vars)

    plt.show()

def createScatterPlot(x_vars, y_vars):
    global df
    global currentVarNumber
    global chosen_variables

    plt.xlabel(chosen_variables[0].get())
    for i in range(0, len(y_vars)):
        plt.scatter(x_vars, y_vars[i], marker='o', label=chosen_variables[i+1].get())
    
    plt.legend()

    plt.grid(axis='x', alpha=0.6)
    plt.grid(axis='y', alpha=0.6)
    plt.xticks(x_vars)

    plt.show()

def createBarChart(x_vars, y_vars):
    global df
    global currentVarNumber
    global chosen_variables

    tickLabels=()

    for i in range(0, len(x_vars)):
        addedElement=(str(x_vars[i]),)
        tickLabels=tickLabels+addedElement
        print(tickLabels)

    dictionary = {}
    for o in y_vars:
        values=()
        for p in range(0, len(o)):
            addedElement=(float(o[p]),)
            values=values+addedElement
        dictionary[o[0]]=values
    
    fig, ax = plt.subplots(layout='constrained')
    res=ax.grouped_bar(dictionary, tick_labels=tickLabels, group_spacing=1)
    for container in res.bar_containers:
        ax.bar_label(container, padding=3)
    
    plt.show()


def createPieChart(x_vars, y_vars):
    global df

    labels=x_vars
    sizes=y_vars[0]
    fig, ax=plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')

    plt.show()

def updateVarNumber(event):
    if variableNumberScrblr.get()=='':
        return
    
    number = int(variableNumberScrblr.get())
    global currentVarNumber
    global chosen_variables

    if currentVarNumber==number or number =='':
        return
    if currentVarNumber<number:
        while currentVarNumber<number:
            chosen_variables.append(ttk.Combobox(
                variablesBar,
                values=variables,
                state="readonly"))
            currentVarNumber=currentVarNumber+1
    else:
        while currentVarNumber>number:
            last_element=chosen_variables[currentVarNumber-1]
            chosen_variables.pop()
            last_element.destroy()
            currentVarNumber=currentVarNumber-1

    updateInterface()

def updateInterface():
    global currentVarNumber
    global chosen_variables

    baseSettingsBar.pack(side='top', anchor='nw', pady=20, padx=20)
    variablesBar.pack(side='top', anchor='nw', pady=20, padx=20)
    uploadButton.pack(side='left')
    diagramTypeLabel.pack(side='left')
    plotType.pack(side='left')

    filePathLabel.pack(side='right')
    varNumber.pack(side='left')
    variableNumberScrblr.pack(side='left')
    xLabel.pack(side='left')
    for i in range(0,currentVarNumber):
        chosen_variables[i].pack(side='left')
        updateVariablesInScrollbar(variables, chosen_variables[i])
        if i==0:
            yLabel.pack(side='left')

    createChartBtn.pack(side='right')

def plotTypeChanged(event):
    if plotType.get()=='Pie Chart':
        variableNumberScrblr.set('2')
        updateVarNumber(event)
    
window=tk.Tk()
window.geometry("750x750")
window.title('Mask')

baseSettingsBar=tk.Frame(window)

variablesBar=tk.Frame(window)

baseSettingsBar.pack(side='top', anchor='nw', pady=20, padx=20)
variablesBar.pack(side='top', anchor='nw', pady=20, padx=20)

uploadButton=tk.Button(baseSettingsBar, text='Import CSV File', command=importFile)
uploadButton.pack(side='left')

variableNumberScrblr = ttk.Combobox(
    baseSettingsBar,
    values=[1,2,3,4,5],
    state="readonly"
)
variableNumberScrblr.bind("<<ComboboxSelected>>", updateVarNumber)

plotType = ttk.Combobox(
    baseSettingsBar,
    values=plotTypes,
    state="readonly",
)
plotType.bind("<<ComboboxSelected>>", plotTypeChanged)

createChartBtn=tk.Button(baseSettingsBar, text='Create Chart', command=createChart)


filePathLabel = tk.Label(baseSettingsBar, text='')
filePathLabel.pack(side='right')

xLabel = tk.Label(variablesBar, text='X axis:')
yLabel = tk.Label(variablesBar, text='Y axis:')
varNumber = tk.Label(baseSettingsBar, text='Total variables:')

diagramTypeLabel = tk.Label(baseSettingsBar, text='Diagram type:')

window.mainloop()