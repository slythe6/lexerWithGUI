import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
currentLine = -1
fontChoice = 'Shunsine 16 italic'


def singleLineLexer(input):
    output = []
    tokenList = {r'\b(if|else|int|float)(?=\s|\t)': 'keyword',
                 r'[A-Za-z]+\d+|[A-Za-z]+': 'identifier',
                 r'[=+>*]': 'operator',
                 r'^\d+(?![\d+\.])': 'literal', #int literal
                 r'\d+\.\d+': 'literal', #float literal
                 r'[():\";]': 'seperator',
                 r'[\t]+|[ ]+': 'space'}

    temp = input
    try:
      while len(temp) != 0:
        for x in tokenList:
            token = re.match(x, temp)
            if token:
                if tokenList[x] == 'space':
                    pos = token.end()
                    temp = temp[pos:]
                elif tokenList[x] == 'sep' and temp[0] == '\"':
                    output.append('<' + tokenList[x] + ',' + token.group() + '>')
                    pos = token.end()
                    temp = temp[pos:]
                    regExStr = re.match(r'^(.)+?(?=\")', temp)
                    if regExStr:
                        output.append('<' + 'lit' + ',' + regExStr.group() + '>')
                        pos = regExStr.end()
                    output.append('<' + tokenList[x] + ',' + token.group() + '>')
                    pos += 1
                    temp = temp[pos:]
                else:
                    output.append('<' + tokenList[x] + ',' + token.group() + '>')
                    pos = token.end()
                    temp = temp[pos:]
    
    except:
      print("ERROR")

    return output




def next_line():
  temp = ""
  global currentLine
  text = inputTextBox.get('1.0', 'end-1c').split('\n')
  if currentLine >= len(text) - 1:
    return
 ## inputTextBox.tag_add("start", '{}.0'.format(currentLine+1), "{}.{}".format(currentLine+1, len(text)+1))
## inputTextBox.tag_config("start", background= "yellow", foreground= "black")
    
  lineStuff.delete(0, tk.END)
  lineStuff.insert(tk.END, currentLine+2)
 # print(singleLineLexer(text[currentLine]))
  current = singleLineLexer(text[currentLine+1])
# print(currentLine)
  for x in range(0, len(current)):
    outputTextBox.insert(tk.END, "{}\n".format(current[x]))
  
  currentLine += 1

def quit():
  app.quit()

  

app = tk.Tk()
style = ttk.Style(app)  
#print("Current available themes are {}".format(style.theme_names()))
style.theme_use('clam')
title = app.title('Lexical Analyzer for TinyPie')
app.geometry("1500x600+20+50")
app.configure(bg = "black")
#app.resizable(False, False)


container = ttk.Frame(app, width=6, height=1)
container.grid_propagate(False)
container.pack(side="left", fill="both", expand=True)

inputLabel = ttk.Label(app, text='Source Code Input:')
inputLabel.configure(font = fontChoice)
inputLabel.place(x=50, y=50)

inputTextBox = tk.Text(container)
#inputTextBox.configure(font = 'hack')
inputTextBox.place(x=50, y=80)


inputLineLabel = ttk.Label(app, text='Current Processing Line:')
inputLineLabel.place(x=400, y=500)

lineStuff = tk.Entry(app)
lineStuff.size()
lineStuff.place(x=550, y=500)

nextButton = ttk.Button(app, text='Next Line', command=next_line)
nextButton.place(x=550, y=550)

outputContainer = ttk.Frame(app, width=10, height=10)
outputContainer.grid_propagate(False)
outputContainer.pack(side="right", fill="both", expand=True)

outputLabel = ttk.Label(app, text='Lexical Analysed Result:')
outputLabel.configure(font = fontChoice)
outputLabel.place(x=790, y=50)

outputTextBox = tk.Text(outputContainer)
outputTextBox.place(x=50,y=80)

quitButton = ttk.Button(app, text='Quit', command=quit)
quitButton.place(x=1350, y=550)

app.mainloop()