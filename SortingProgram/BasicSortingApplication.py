from functools import cmp_to_key as ctk
from tkinter import *
from tkinter import ttk
from openpyxl import Workbook

window = Tk()

window.title("Basic Sorting Application")
window.geometry('780x400')
window.configure(bg="black")

lst = []
counter = 0

def getElements():
    global lst
    lst = (entry.get()).split(";")
    for i,item in enumerate(lst):
        if len(item) > 0:

            if item[0] == " ":
                lst[i] = item[1:]
    entrylbl.destroy()
    enterbtn.destroy()
    entered.destroy()

entrylbl = Label(window,text="    Enter elements:", font = ("Helvetica",30), bg="black",fg="white")
entrylbl.pack(side=TOP,anchor='w')
entrylbl2 = Label(window,text="Separate with ;", font = ("Helvetica",15), bg="black",fg="white")
entrylbl2.pack(side=TOP,anchor='w')

entry = StringVar()

entered = ttk.Entry(window,width=50,font=("Helvetica",10),textvariable=entry)
entered.pack(side=TOP,anchor='w')

var = IntVar()

enterbtn = Button(window,text="Done",width=7,height=1,bg="black",fg="green2",bd=10,command = lambda: var.set(1))
enterbtn.pack(side=TOP,anchor='w',padx=135,pady=10)

enterbtn.wait_variable(var)
getElements()
lbl = Label(window, text=f"\n                    Which is greater?", font = ("Helvetica",30), bg="black",fg="green2")
lbl.pack(side=TOP,anchor='w')


val = -1
x = IntVar()
qlist,alist,blist,clist = [],[],[],[]

def chosen(a,b,c,counter):
    global qlist, alist,blist,clist
    alist.append(a)
    blist.append(b)
    question = ""
    if c == "1":
        question = f"{counter}) {a} > {b}"
        clist.append("1")
    else:
        question = f"{counter}) {a} < {b}"
        clist.append("0")
    qlist.append(question)

def onA():
    global val,x
    x.set("1")
    val = 1
def onB():
    global val,x
    x.set("0")
    val = 0

def Choice(a,b):
    global val,x,counter
    val = None
    btn_a = Button(window,text = a,bg = "sky blue",fg = "blue2", font = ("Helvetica",15), width = 25,height = 5,command=onA)
    btn_b = Button(window,text = b,bg = "sky blue",fg = "blue2", font = ("Helvetica",15), width = 25,height = 5,command=onB)
    btn_a.place(x=75,y=150)
    btn_b.place(x=400,y=150)

    btn_a.wait_variable(x)

    btn_a.destroy()
    btn_b.destroy()
    counter += 1
    chosen(a,b,str(val),counter)
    return str(val)



for i,item in enumerate(lst):
    lst[i] = item.capitalize()

k = ctk(lambda a, b: (Choice(a,b) == '1') * 2 - 1)
lst.sort(key=k)

lbl.destroy()

#results
# Create A Main Frame
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

my_canvas.configure(bg="black")

# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas)
second_frame.configure(bg="black")
# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")
lst.reverse()
for i,item in enumerate(lst):
    Label(second_frame,text=f"{i+1}. {item}",bg="black",fg="green2",font = ("Helvetica",15)).grid(row=i, column=0, pady=5)

def copylst():
    out = ""
    for item in lst:
        out += f"{item}\n"
    window.clipboard_append(out)
    window.update()
def downloadqs():
    global qlist,counter,alist,blist,clist
    if qschoice.get() == "Raw Text":
        copystr = ""
        for q in qlist:
            copystr += f"{q}\n"
        window.clipboard_append(copystr)
        window.update()
    elif qschoice.get() == "Excel":
        workbook = Workbook()
        sheet = workbook.active
        sheet.title="Questions"
        final = workbook.create_sheet("sheet2",1)
        final.title = "Final"
        final["A1"].value = "Number"
        final["B1"].value = "Item"
        for num in range(len(lst)):
            Acol = f"A{num+2}"
            final[Acol].value = num+1
        for num,item in enumerate(lst):
            Bcol = f"B{num+2}"
            final[Bcol].value = lst[num]
        sheet["A1"].value = "Question No."
        sheet["B1"].value = "Item"
        sheet["C1"].value = "vs"
        sheet["D1"].value = "Item"
        sheet["E1"].value = "Response"

        for num in range(counter):
            Acol = f"A{num+2}"
            sheet[Acol].value = num+1

        for num in range(counter):
            Bcol = f"B{num+2}"
            sheet[Bcol].value = alist[num]

        for num in range(counter):
            Ccol = f"C{num+2}"
            sheet[Ccol].value = "vs"

        for num in range(counter):
            Dcol = f"D{num+2}"
            sheet[Dcol].value = blist[num]

        for num in range(counter):
            Ecol = f"E{num+2}"
            if clist[num] == "0":
                sheet[Ecol].value = blist[num]
            elif clist[num] == "1":
                sheet[Ecol].value = alist[num]
        #autofit
        dims = {}
        for row in sheet.rows:
            for cell in row:
                if cell.value:
                    maxdim = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
                    dims[cell.column_letter] = max(maxdim,8)
        for col, value in dims.items():
            sheet.column_dimensions[col].width = value
        dims = {}
        for row in final.rows:
            for cell in row:
                if cell.value:
                    maxdim = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
                    dims[cell.column_letter] = max(maxdim,8)
        for col, value in dims.items():
            final.column_dimensions[col].width = value
        workbook.save(filename="Question_Responses.xlsx")

    else:
        print("select an option")



linelbl = Label(second_frame,text = "-"*107,bg="black",fg="green2",font = ("Helvetica",15))
linelbl.grid(row=len(lst),column=0,sticky='w')
export = Button(second_frame,width = 10, height=2,bd = 10,bg="black",fg="green2",text="Copy",font = ("Helvetica",15),command=copylst)
export.grid(row=len(lst)+1,column=0,sticky='w',pady=10,padx=10)
qs = Button(second_frame,width = 20, height=2,bd = 10,bg="black",fg="green2",text="Download Questions",font = ("Helvetica",15),command=downloadqs)
qs.grid(row=len(lst)+1,column=0,sticky='w',pady=10,padx=300)



qschoice = ttk.Combobox(second_frame,values =["Raw Text", "Excel"],state = "readonly")
combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'black',
                                       'fieldbackground': 'black',
                                       'background': 'white',
                                       'font' : 'Helvetica 20',
                                       'fg' : 'green2'

                                       }}}
                         )
combostyle.theme_use('combostyle')
qschoice.grid(row=len(lst)+2,column=0)


window.mainloop()
