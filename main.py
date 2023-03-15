from tkinter import *
from tkinter import messagebox
import sqlite3
import pickle
import pandas as pd
import sklearn


def predict_fraud(data):
    data = [float(x) for x in data]
    df = pd.DataFrame([data], columns=['Time', 'V1','V2','V3', 'V4', 'V5', 'V6', 'V7', 'V8','V9','V10', 'V11', 'V12', 'V13', 'V14',
     'V15','V16','V17', 'V18', 'V19', 'V20', 'V21',
      'V22','V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount'])
    
    with open('lr_model.pkl', 'rb') as file:
        model =pickle.load(file)

    result = model.predict(df)
    print(result)

    if result[0] == 0:
        return "No Fraud"
    else:
        return "Fraud"


# create the main window
root = Tk()
root.title("Credit Card Fraud Detection")
root.geometry("900x500")
root.configure(bg='#333333')





def init_db():
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       password TEXT,
                       email TEXT,
                       phone TEXT)''')
    conn.commit()
    conn.close()

# initialize the database
init_db()

def credit_entry_window():
    # create a new window
    # data_entry = Toplevel(root)
    data_entry = Tk()
    data_entry.title("Credit Entry Form")
    data_entry.geometry("1000x600")
    data_entry.configure(bg='#333333')

    v_entry_list = []

    # create a label and entry for the time
    time_label = Label(data_entry, fg='#FFFFFF',bg='#333333', text="Time:", font=("Arial",13))
    time_label.grid(row=0, column=0, pady= 10)
    time_entry = Entry(data_entry,font=("Arial",13))
    time_entry.grid(row=0, column=1)

    # for i in range(1, 29):
    #     v_label = Label(data_entry, text="V" + str(i) + ":",font=("Arial",13), fg='#FFFFFF',bg='#333333')
    #     v_label.grid(row=i, column=0, pady= 10)
    #     v_entry = Entry(data_entry,font=("Arial",13))
    #     v_entry.grid(row=i, column=1, pady=10)
    #     v_entry_list.append(v_entry)
    row = 1
    for i in range(1, 29, 3):
        v_label = Label(data_entry, text="V" + str(i) + ":",font=("Arial",13), fg='#FFFFFF',bg='#333333')
        v_label.grid(row=row, column=0, pady= 10)
        v_entry = Entry(data_entry,font=("Arial",13))
        v_entry.grid(row=row, column=1, pady=10)

        v_label_2 = Label(data_entry, text="V" + str(i+1) + ":",font=("Arial",13), fg='#FFFFFF',bg='#333333')
        v_label_2.grid(row=row, column=3, pady= 10)
        v_entry_2 = Entry(data_entry,font=("Arial",13))
        v_entry_2.grid(row=row, column=4, pady=10)

        v_label_3 = Label(data_entry, text="V" + str(i+2) + ":",font=("Arial",13), fg='#FFFFFF',bg='#333333')
        v_label_3.grid(row=row, column=5, pady= 10)
        v_entry_3 = Entry(data_entry,font=("Arial",13))
        v_entry_3.grid(row=row, column=6, pady=10)

        v_entry_list.append(v_entry)
        v_entry_list.append(v_entry_2)
        v_entry_list.append(v_entry_3)

        row += 1



    
    # create a label and entry for the amount
    amount_label = Label(data_entry, text="Amount:",font=("Arial",13),fg='#FFFFFF',bg='#333333')
    amount_label.grid(row=0, column=3, pady= 10)
    amount_entry = Entry(data_entry,font=("Arial",13))                    
    amount_entry.grid(row=0, column=4, pady=10)

    def save_data():
        data = [time_entry.get()]
        for i in range(1, 29):
            data.append(v_entry_list[i-1].get())
        data.append(amount_entry.get())

        result = predict_fraud(data)

        # show a message box to confirm the data has been saved
        messagebox.showinfo("Data Saved", "Your data has been saved." + str(result))

    save_button = Button(data_entry, text="Submit",bg='#FF3399', fg='#FFFFFF', font=("Arial",16), command=save_data)
    save_button.grid(row=33, column=4)


# create the login/register window
def login_window():
    # destroy the main window
    root.destroy()
    
    # create a new window
    login = Tk()
    login.title("Login/Register Form")
    login.geometry("900x500")
    login.configure(bg='#333333')
  
    

    # create a label and entry for the username
    username_label = Label(login, text="Username:",bg='#333333', fg='#FFFFFF', font=("Arial",16 ))
    username_label.grid(row=1, column=0)
    username_entry = Entry(login, font=("Arial",16))
    username_entry.grid(row=1, column=1, pady=20)

    # create a label and entry for the password
    password_label = Label(login, text="Password:", bg='#333333', fg='#FFFFFF', font=("Arial",16))
    password_label.grid(row=2, column=0)
    password_entry = Entry(login, show="*", font=("Arial",16))
    password_entry.grid(row=2, column=1, pady=20)

    # create a function to check if the login is valid
    def login_check():
        # check if the username and password match
        conn = sqlite3.connect('user_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username_entry.get(), password_entry.get()))
        user = cursor.fetchone()
        conn.close()

        if user is not None:
            messagebox.showinfo("Login Successful", "Welcome back, " + user[1] + "!")
            login.destroy()
            credit_entry_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    # create a login button
    login_button = Button(login, text="Login",bg='#FF3399', fg='#FFFFFF', font=("Arial",16), command=login_check)
    login_button.grid(row=3, column=0, pady=30, columnspan=1)


    def register_window():
            # create a new window
            register = Toplevel(login)
            register.title("Register Form")
            register.configure(bg='#333333')
            register.geometry("900x500")
            

            # create a label and entry for the username
            new_username_label = Label(register, text="New Username:",bg='#333333',fg="#FFFFFF",font=("Arial",16))
            new_username_label.grid(row=1, column=0)
            new_username_entry = Entry(register, font=("Arial",16))
            new_username_entry.grid(row=1, column=1,pady=20)

            # create a label and entry for the password
            new_password_label = Label(register, text="New Password:",bg='#333333',fg="#FFFFFF", font=("Arial",16))
            new_password_label.grid(row=2, column=0)
            new_password_entry = Entry(register, show="*", font=("Arial",16))
            new_password_entry.grid(row=2, column=1, pady=20)

            # create a label and entry for the email
            new_email_label = Label(register, text="New Email:", bg='#333333', fg="#FFFFFF", font=("Arial",16))
            new_email_label.grid(row=3, column=0)
            new_email_entry = Entry(register, font=("Arial",16))
            new_email_entry.grid(row=3, column=1, pady=20)

            # create a label and entry for the phone number
            new_phone_label = Label(register, text="New Phone Number:", bg='#333333', fg="#FFFFFF", font=("Arial",16))
            new_phone_label.grid(row=4, column=0)
            new_phone_entry = Entry(register, font=("Arial",16))
            new_phone_entry.grid(row=4, column=1, pady=20)

            def add_user():
                conn = sqlite3.connect('user_db.sqlite')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)", (new_username_entry.get(), new_password_entry.get(), new_email_entry.get(), new_phone_entry.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Registration Successful", "Your account has been created!")
                register.destroy()

            register_button = Button(register, text="Register", bg='#FF3399', fg='#FFFFFF', font=("Arial",16),command=add_user)
            register_button.grid(row=6, column=0, columnspan=2, pady=30)

    register_button = Button(login, text="Register", bg='#FF3399', fg='#FFFFFF', font=("Arial",16), command=register_window)
    register_button.grid(row=3, column=1, columnspan=3, pady=40)

    # run the window
    login.mainloop()
        

# create a label for the main window
welcome_label = Label(root, text="Welcome to the CCF System", bg='#333333', fg='#FF3399', font=("Arial",30))
welcome_label.pack()

# create a button to open the login/register window
login_button = Button(root, text="Login/Register", fg='#FF3399', font=("Arial",16),command=login_window, activebackground="grey")   
login_button.pack()


# run the main window
root.mainloop()