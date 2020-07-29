import tkinter as tk
import tkinter.ttk
from tkinter import messagebox
import pymysql

#DB내의 학번과 비밀번호를 조회하기 위한 select문
def createMainWindow():
    mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="Vitol0928!?^^",
        database="pydb"
    )
    mc = mydb.cursor()
    sql = "SELECT * FROM 학생 Where 학번 = %s and 비밀번호 = %s"
    val = (int(logInId.get()),logInPw.get())
    mc.execute(sql,val)
    if mc.rowcount:
        messagebox.showinfo("알림", "Login 하였습니다.")
        newWindow = tk.Toplevel(app)
        newWindow.geometry("300x200")
        mypageButton = tk.Button(newWindow, text="My page", command=mypageWindow)
        mypageButton.place(x=120, y=50)
        tk.Label(newWindow, text="도서검색", font=(50)).pack()
        tk.Label(newWindow, text="책이름").place(x=30, y=100)
        tk.Entry(newWindow, width=20, textvariable=searchBookName).place(x=100, y=100)
        searchButton = tk.Button(newWindow, text="검색", command=searchBook)
        searchButton.place(x=250, y=100)
    else :
        messagebox.showerror("에러", "잘못된 학번 or 비밀번호 입니다!")
        return;

#대출도서 및 신청도서 목록 select문 - treeview
def mypageWindow():
    newWindow = tk.Toplevel(app)
    newWindow.geometry("500x500")
    tk.Label(newWindow, text="My Page", font=(50)).pack()
    lbf1=tk.LabelFrame(newWindow, text="대출도서목록")
    lbf1.pack(fill="both", expand="yes")
    mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="Vitol0928!?^^",
        database="pydb"
    )
    mc = mydb.cursor()
    asql = "SELECT 책id, 도서명, 대출일, 반납일 FROM 대출 d, 책목록 c Where d.책id=c.목록id"
    bsql = "SELECT 도서명, 저자, 출판사 from 신청도서"
    mc.execute(asql)
    mr=mc.fetchall()
    borrowList=[]
    for x in mr:
        borrowList.append(x)
    mc.execute(bsql)
    ms=mc.fetchall()
    requestList=[]
    for x in ms:
        requestList.append(x)

    treeview=tk.ttk.Treeview(newWindow, columns=["index","책id","도서명","대출일","반납예정일"]
                             , displaycolumns=["index","책id","도서명","대출일","반납예정일"])
    treeview.place(y=50)
    treeview.column("#0", width=50)
    treeview.heading("#0", text="index")
    treeview.column("#1", width=100,anchor="center")
    treeview.heading("#1", text="책id",anchor="center")
    treeview.column("#2", width=100, anchor="center")
    treeview.heading("#2", text="도서명", anchor="center")
    treeview.column("#3", width=100, anchor="center")
    treeview.heading("#3", text="대출일", anchor="center")
    treeview.column("#4", width=100, anchor="center")
    treeview.heading("#4", text="반납예정일", anchor="center")
    for i in range(len(borrowList)):
        treeview.insert('','end',text=i+1,values=borrowList[i])

    lbf2=tk.LabelFrame(newWindow, text="신청도서목록")
    lbf2.pack(fill="both", expand="yes")

    requestButton=tk.Button(newWindow, text="도서신청하기", command=requestBookWindow)
    requestButton.place(x=410,y=272)

    atreeview=tk.ttk.Treeview(newWindow, columns=["index","도서명","저자","출판사"]
                             , displaycolumns=["index","도서명","저자","출판사"])
    atreeview.place(y=300)
    atreeview.column("#0", width=50)
    atreeview.heading("#0", text="index")
    atreeview.column("#1", width=100, anchor="center")
    atreeview.heading("#1", text="도서명", anchor="center")
    atreeview.column("#2", width=100, anchor="center")
    atreeview.heading("#2", text="저자", anchor="center")
    atreeview.column("#3", width=100, anchor="center")
    atreeview.heading("#3", text="출판사", anchor="center")
    for i in range(len(requestList)):
        atreeview.insert('','end',text=i+1,values=requestList[i])

#신청도서 insert문
def insertToRequestBookTable():
    mydb = pymysql.connect(
        host="localhost",
        port=3306,

        user="root",
        passwd="Vitol0928!?^^",
        database="pydb"
    )
    mc = mydb.cursor()
    sql = "INSERT INTO 신청도서 (도서명, 저자, 출판사, 학번) VALUES (%s, %s, %s, %s)"
    val = (bookName.get(),author.get(),publish.get(), 2015104046)
    mc.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("알림", "도서 신청 완료!")

def requestBookWindow():
    newWindow = tk.Toplevel(app)
    newWindow.geometry("300x200")
    tk.Label(newWindow, text="도서신청", font=(50)).pack()
    tk.Label(newWindow, text="도서명").place(x=30, y=50)
    tk.Entry(newWindow, width=20, textvariable=bookName).place(x=100, y=50)
    tk.Label(newWindow, text="저자").place(x=30, y=90)
    tk.Entry(newWindow, width=20, textvariable=author).place(x=100, y=90)
    tk.Label(newWindow, text="출판사").place(x=30, y=130)
    tk.Entry(newWindow, width=20, textvariable=publish).place(x=100, y=130)

    tk.Button(newWindow, text="입력", command=insertToRequestBookTable).place(x=130, y=160)

#책에대한 정보를 검색하기 위한 select문
def searchBook():
    messagebox.showinfo("알림", "검색을 완료하였습니다.")
    newWindow = tk.Toplevel(app)
    newWindow.geometry("550x300")
    tk.Label(newWindow, text="검색된 도서", font=(50)).pack()
    tk.Label(newWindow, text="도서명").place(x=10, y=20)
    tk.Entry(newWindow, width=15, textvariable=bookNameForLoc).place(x=60, y=20)
    searchButton = tk.Button(newWindow, text="위치 검색", command=searchBookLoc)
    searchButton.place(x=180, y=20)
    treeview=tk.ttk.Treeview(newWindow, columns=["index","책id","도서명","저자","출판사", "권수"]
                             , displaycolumns=["index","책id","도서명","저자","출판사", "권수"])
    treeview.place(y=50)
    treeview.column("#0", width=50)
    treeview.heading("#0", text="index")
    treeview.column("#1", width=100,anchor="center")
    treeview.heading("#1", text="책id",anchor="center")
    treeview.column("#2", width=100, anchor="center")
    treeview.heading("#2", text="도서명", anchor="center")
    treeview.column("#3", width=100, anchor="center")
    treeview.heading("#3", text="저자", anchor="center")
    treeview.column("#4", width=100, anchor="center")
    treeview.heading("#4", text="출판사", anchor="center")
    treeview.column("#5", width=100, anchor="center")
    treeview.heading("#5", text="권수", anchor="center")

    mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="Vitol0928!?^^",
        database="pydb"
    )
    mc = mydb.cursor()
    sql = "SELECT 목록id, 도서명, 저자, 출판사, 권수 FROM 책목록 Where 도서명 like %s"
    val = "%"+searchBookName.get()+"%"
    mc.execute(sql,val)
    mr=mc.fetchall()
    searchList=[]
    for x in mr:
        searchList.append(x)
    for i in range(len(searchList)):
        treeview.insert('','end',text=i+1,values=searchList[i])

#책의 위치를 검색하기 위한 select문
def searchBookLoc():
    messagebox.showinfo("알림", "검색을 완료하였습니다.")
    newWindow = tk.Toplevel(app)
    newWindow.geometry("480x300")
    tk.Label(newWindow, text="도서 위치", font=(50)).pack()
    treeview=tk.ttk.Treeview(newWindow, columns=["index","책id","도서명","서고이름","서가id", "행", "열"]
                             , displaycolumns=["index","책id","도서명","서고이름","서가id", "행", "열"])
    treeview.place(y=50)
    treeview.column("#0", width=50)
    treeview.heading("#0", text="index")
    treeview.column("#1", width=70,anchor="center")
    treeview.heading("#1", text="책id",anchor="center")
    treeview.column("#2", width=100, anchor="center")
    treeview.heading("#2", text="도서명", anchor="center")
    treeview.column("#3", width=100, anchor="center")
    treeview.heading("#3", text="서고이름", anchor="center")
    treeview.column("#4", width=50, anchor="center")
    treeview.heading("#4", text="서가id", anchor="center")
    treeview.column("#5", width=50, anchor="center")
    treeview.heading("#5", text="행", anchor="center")
    treeview.column("#6", width=50, anchor="center")
    treeview.heading("#6", text="열", anchor="center")

    mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="Vitol0928!?^^",
        database="pydb"
    )
    mc = mydb.cursor()
    sql = "SELECT a.책id, b.도서명, c.서고이름, a.서가id, a.행, a.열 FROM 책 a,책목록 b,서고 c Where a.책id=b.목록id and a.서고id=c.서고id and b.도서명 like %s"
    val = "%"+bookNameForLoc.get()+"%"
    mc.execute(sql,val)
    mr=mc.fetchall()
    searchList=[]
    for x in mr:
        searchList.append(x)
    for i in range(len(searchList)):
        treeview.insert('','end',text=i+1,values=searchList[i])

app = tk.Tk()
app.geometry("300x200")
bookName = tk.StringVar()
author = tk.StringVar()
publish = tk.StringVar()
searchBookName=tk.StringVar()
logInId=tk.StringVar()
logInPw=tk.StringVar()
bookNameForLoc=tk.StringVar()
tk.Label(app, text = "도서대출관리", font=(50)).pack()
tk.Label(app, text = "학번").place(x = 30, y = 50)
tk.Entry(app, width = 20, textvariable=logInId).place(x = 100, y = 50)

tk.Label(app, text = "비밀번호").place(x = 30, y = 90)
tk.Entry(app, width = 20, show='*', textvariable=logInPw).place(x = 100, y = 90)

loginButton = tk.Button(app,text="로그인",command=createMainWindow)
loginButton.place(x = 120, y = 135)

app.mainloop()