from unittest import removeResult
from flask import Flask,redirect,request,render_template
import pandas as pd
import numpy as np
import sqlite3



conn = sqlite3.connect("task.db")
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS pen_tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   pen_tasks TEXT)""")
try:
    cursor.execute("ALTER TABLE pen_tasks ADD COLUMN status TEXT DEFAULT 'PENDING'")
    conn.commit()
except:
    pass 
conn.commit()
conn.close()

import sqlite3

tasks = [
    "Study DSA - Arrays and Linked Lists",
    "Complete Python assignment",
    "Push portfolio project to GitHub",
    "Wake up at 6:00 AM",
    "Morning workout - 30 mins",
    "Apply for internships on Internshala",
    "Build Flask login system",
    "Review SQL joins and subqueries",
    "Update LinkedIn profile",
    "Check NIFTY 50 market open"
]

conn = sqlite3.connect("task.db")
cursor = conn.cursor()

for task in tasks:
    cursor.execute("INSERT INTO pen_tasks (pen_tasks, status) VALUES (?, ?)", (task, "PENDING"))

conn.commit()
conn.close()
print("Tasks inserted successfully!")


app = Flask(__name__)

#HOME PAGE, WHICH TAKES INPUT AS TASK AND STORES IT IN DATABASE CALLED PEN_TASK(PENDING TASKS)
@app.route("/",methods=["GET","POST"])
def home():
    result = None
    if request.method == "POST":
        add_task = request.form.get("task")
        conn = sqlite3.connect("task.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pen_tasks (pen_tasks) VALUES (?)",(add_task,))
        conn.commit()
        conn.close()
        result = "✅Task Added Sucesssfully"
        return render_template("index.html",result=result)
    return render_template("index.html")


#VIEW PAGE, ALL PENDING AND COMPLETED TASKS ARE VIEWED FETCHED FROM PEN_TASK(PENDING TASKS)
@app.route("/view",methods=["GET","POST"])
def view():
    result = ""
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pen_tasks")
    result = cursor.fetchall()
    conn.close()
    return render_template("view.html",task=result)


#PEN PAGE, 
# PENDING TASKS ARE VIEWED, 
# BUTTON MARKDOWN CHANGES THE STATUS TO COMPLETED, 
# FETCHED FROM PEN_TASKS WHERE STATUS="PENDING"
@app.route("/pen",methods=["GET","POST"])
def pen():
    result = ""
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pen_tasks WHERE status='PENDING'")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("pen.html",task=result)
    
#COM PAGE,
#COMPLETED TASKS ARE VIEWED FETCHED FROM PEN_TASK WHERE STATUS="completed",
#DELETE BUTTON DELETES THE TASK FROM DATABASE PEN_TASKS 
@app.route("/com",methods=["GET","POST"])
def com():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pen_tasks WHERE status='completed'")
    com_tasks = cursor.fetchall()
    conn.close()
    return render_template("com.html",com_tasks=com_tasks)

@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pen_tasks WHERE id=?",(id,))
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='pen_tasks'")
    conn.commit()
    conn.close()
    return redirect("/view")

@app.route("/deletecom/<int:id>",methods=["GET","POST"])
def deletepen(id):
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pen_tasks WHERE id=?",(id,))
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='pen_tasks'")
    conn.commit()
    conn.close()
    return redirect("/com")

@app.route("/clear",methods=["GET","POST"])
def clear():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pen_tasks")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='pen_tasks'")
    conn.commit()
    conn.close()
    return redirect("/view")

@app.route("/done/<int:id>",methods=["GET","POST"])
def done(id):
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE pen_tasks SET status = 'completed' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/pen")

if __name__ == "__main__":
    app.run(debug=True)





