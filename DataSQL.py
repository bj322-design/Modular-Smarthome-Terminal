import sqlite3



def addWidgets():
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    a = True
    while(a):
        corec = True
        while(corec):
            id = input("ID: ")
            name = input("NAME: ")
            widClass = input("CLASS: ")
            css_name = input("CSS NAME: ")
            wrongInfo = input(f"\n\nIS THIS CORRECT\nID: {id}\nNAME: {name}\nCLASS: {widClass}\nCSS NAME: {css_name}\nY or N: ")
            if(wrongInfo == "y" or wrongInfo == "Y"):
                corec = False

        query = "INSERT INTO widgets (id, name, class, css_name) VALUES (?, ?, ?, ?)"
        data = (id, name, widClass, css_name)
        cursor.execute(query, data)

        stop = input("Add more (Q) to quit: ")
        if(stop == "q" or stop == "Q"):
            a = False


    conn.commit() 
    conn.close()



def add_layout(client_id, widget_id, row, col):
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    query = "INSERT INTO client_layouts (client_id, widget_id, row, col) VALUES (?, ?, ?, ?)"
    data = (client_id, widget_id, row, col)
    cursor.execute(query, data)
    conn.commit()
    conn.close()


    

def del_widget(widgetID):
    conn = sqlite3.connect('smt_database.db')
    cursor = conn.cursor()
    query = "DELETE FROM widgets WHERE id = ?"
    cursor.execute(query, (widgetID,)) 
    conn.commit()
    conn.close()


