from tkinter import *
from tkinter import ttk
import string
import random
import sqlite3
import hashlib
from tkinter import messagebox

# Constants
WINDOW_W = 390
WINDOW_H = 510
HEADER_H = 65
CARD_W = 325
CARD_H = 390
BG_COLOR = "#B5B5B5"
HEADER_COLOR = "#d85a3e"
FONT_TITLE = ("Arial", 18, "bold")
FONT_BUTTON = ("Arial", 12, "bold")

# Creation of database table
# Connect to the database and create a file (vault.db)
conn = sqlite3.connect("vault.db")
# Enable foreign keys
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# UserAccount table
cursor.execute("""
CREATE TABLE IF NOT EXISTS UserAccounts (
    UserID TEXT PRIMARY KEY,
    MasterPassword TEXT NOT NULL
);
""")

# Passwords table

cursor.execute("""
CREATE TABLE IF NOT EXISTS Passwords (
    PasswordID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL,
    ReferenceName TEXT NOT NULL,
    EncryptPassword TEXT NOT NULL,
    UserID TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES UserAccounts(UserID)
);
""")
# save and close database
conn.commit()
conn.close()

class BasePage(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.resizable(False, False)
        self.master.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(bg=BG_COLOR, borderwidth=3, relief="solid")

        # Header inside the page frame
        header = Frame(self, bg=HEADER_COLOR, width=WINDOW_W, height=HEADER_H)
        header.pack(side="top", fill="x")
        bottom_border = Frame(self, bg="black", height=2)
        bottom_border.pack(side="top", fill="x")
        Label(header, text="Password Vault", bg=HEADER_COLOR, fg="black", font=FONT_TITLE).pack(pady=20)

        # Card
        self.card = Frame(self, bg="white", width=CARD_W, height=CARD_H)
        self.card.place(x=(WINDOW_W - CARD_W) // 2,
                        y=(WINDOW_H - HEADER_H - CARD_H) // 2 + HEADER_H)
        self.inner = Frame(self.card, bg="white", width=CARD_W - 2, height=CARD_H - 2)
        self.inner.place(relx=0.5, rely=0.5, anchor="center")
        self.pack(fill="both", expand=True)

    def switch_page(self, page_class, *args):
        self.destroy()
        page_class(self.master, *args)


class HomePage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        Button(self.inner, text="Login", font=("Arial", 14, "bold"), width=20,
               command=lambda: self.switch_page(LoginPage)).pack(padx=15, pady=10)
        Label(self.inner, text="or", font=("Arial", 12), bg="white").pack()
        Button(self.inner, text="Create Account", font=("Arial", 14, "bold"), width=20,
               command=lambda: self.switch_page(CreateAccountPage)).pack(padx=15, pady=10)


class LoginPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        Label(self.inner, text="Login", font=("Arial", 16, "bold"), bg="white").pack(pady=30)

        # Username
        username_entry = Entry(self.inner, width=25, font=("Arial", 13), bd=0.5, relief="solid")
        username_entry.pack(pady=25, ipady=8)
        username_entry.insert(0, " Enter User ID")
        username_entry.config(fg="black")

        def on_click(event):
            if username_entry.get() == " Enter User ID":
                username_entry.delete(0, "end")

        username_entry.bind("<FocusIn>", on_click)

        # Password
        password_entry = Entry(self.inner, width=25, font=("Arial", 13), bd=0.5, relief="solid")
        password_entry.pack(pady=12, ipady=8)
        password_entry.insert(0, " Enter Master Password")
        password_entry.config(fg="black")

        def on_click(event):
            if password_entry.get() == " Enter Master Password":
                password_entry.delete(0, "end")

        password_entry.bind("<FocusIn>", on_click)

        # Process once user click the enter button
        def enter():
            user_id = username_entry.get()
            masterpassword = password_entry.get()

            def hash_password(password):
                return hashlib.sha256(password.encode()).hexdigest()

            conn = sqlite3.connect("vault.db")
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            cursor.execute("SELECT MasterPassword FROM UserAccounts WHERE UserID = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()

            if result is None:
                messagebox.showerror("Login Failed", "User ID not found.")
                return

            stored_hash = result[0]
            entered_hash = hash_password(masterpassword)

            if entered_hash == stored_hash:
                self.switch_page(Mainpage, user_id)
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")

        Button(self.inner, text="Enter", font=FONT_BUTTON, width=10, command=enter).pack(side="right", pady=45, padx=20)
        Button(self.inner, text="Back", font=FONT_BUTTON, width=10, command=lambda: self.switch_page(HomePage)).pack(side="left", pady=45, padx=20)

class CreateAccountPage(BasePage):
    def __init__(self, master):
        super().__init__(master)
        Label(self.inner, text="Create Account", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        # Username
        username_entry = Entry(self.inner, width=25, font=("Arial", 12), bd=1, relief="solid")
        username_entry.pack(pady=10, ipady=6)
        username_entry.insert(0, " Enter User ID here")
        username_entry.config(fg="black")

        def on_click(event):
            if username_entry.get() == " Enter User ID here":
                username_entry.delete(0, "end")

        username_entry.bind("<FocusIn>", on_click)

        # Password
        password_entry = Entry(self.inner, width=25, font=("Arial", 12), bd=1, relief="solid")
        password_entry.pack(pady=20, ipady=6)
        password_entry.insert(0, " Enter Master Password here")
        password_entry.config(fg="black")

        def on_click(event):
            if password_entry.get() == " Enter Master Password here":
                password_entry.delete(0, "end")

        password_entry.bind("<FocusIn>", on_click)

        # Validation rules label
        Label(self.inner, text="At least 8 characters", font=("Arial", 9, "bold")).pack(anchor="w", pady=5, padx=32)
        Label(self.inner, text="At least 1 special character", font=("Arial", 9, "bold")).pack(anchor="w", pady=5, padx=32)
        Label(self.inner, text="At least 1 Uppercase character", font=("Arial", 9, "bold")).pack(anchor="w", pady=5, padx=32)


        # Validation test function
        def validate_password(password):
            upper = string.ascii_uppercase
            symbols = "!@#$%^&*()-_=+[]{};:,.<>?"

            # linear search
            def linear_search(password, search_type):
                for i in range(len(password)):
                    for j in range(len(search_type)):
                        if password[i] == search_type[j]:
                            return "Found"

            # search Uppercase letter and symbols

            Upper_exist =linear_search(password, upper)
            Symbol_exist =linear_search(password, symbols)
            if len(password) < 8 or Upper_exist != "Found" or Symbol_exist != "Found":
                return False
            return True

        def save():
            # get user inputs
            user_id = username_entry.get()
            password = password_entry.get()

            if not validate_password(password):
                messagebox.showerror("Error", "Password does not meet the validation rules.")
                return

            # hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Database connection
            conn = sqlite3.connect("vault.db")
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Ensure table exists
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS UserAccounts (
                            UserID TEXT PRIMARY KEY,
                            MasterPassword TEXT NOT NULL
                        )
                    """)

            # Check if user exists
            cursor.execute("SELECT * FROM UserAccounts WHERE UserID=?", (user_id,))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "User ID already exists.")
                conn.close()
                return

            # Insert new user
            cursor.execute("INSERT INTO UserAccounts (UserID, MasterPassword) VALUES (?, ?)", (user_id, hashed_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            self.switch_page(LoginPage)

        # Buttons
        Button(self.inner, text="Save", font=FONT_BUTTON, width=10,
               command=save).pack(side="right", pady=20, padx=20)
        Button(self.inner, text="Back", font=FONT_BUTTON, width=10,
               command=lambda: self.switch_page(HomePage)).pack(side="left", pady=20, padx=20)

class Mainpage(BasePage):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.user_id = user_id
        self.card.configure(bg="#B5B5B5")
        self.inner.configure(bg="#B5B5B5")

        #Buttons
        lable=Label(self.inner, text=f"Welcome {user_id}", font=("Arial", 12, "bold"), bg="#B5B5B5")
        lable.place(x=90, y=0)
        Medicalbtn= Button(self.inner, text="Medical", bg="#D6274F", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid", command=lambda: self.switch_page(CategoryPage, self.user_id, "Medical"))
        Medicalbtn.place(x=5, y=30)
        Financebtn = Button(self.inner, text="Finance", bg="#E6C40D", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        Financebtn.place(x=180, y=30)
        Educationbtn = Button(self.inner, text="Education", bg="#15E518", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        Educationbtn.place(x=5, y=110)
        Workbtn = Button(self.inner, text="Work", bg="#FF69D5", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        Workbtn.place(x=180, y=110)
        SocialMediabtn = Button(self.inner, text="Social Media", bg="#1CC4E5", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        SocialMediabtn.place(x=5, y=190)
        Entertainmentbtn = Button(self.inner, text="Entertainment", bg="#BC38D6", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        Entertainmentbtn.place(x=180, y=190)
        Shoppingbtn = Button(self.inner, text="Shopping", bg="#D69A54", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        Shoppingbtn.place(x=5, y=270)
        Otherbtn = Button(self.inner, text="Other", bg="white", fg="black", font=("Arial", 14, "bold"), width=11, height=2, borderwidth=1, relief="solid")
        Otherbtn.place(x=180, y=270)
        Plusbtn= Button(self.inner, text="➕", bg="#d85a3e", fg="white", font=("Arial", 15, "bold"), command= lambda: self.switch_page(StorePasswordpage, user_id), width=3, borderwidth=1, relief="solid")
        Plusbtn.place(x=270, y=340)


class StorePasswordpage(BasePage):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.user_id = user_id

        #dropdown input
        options = ["Medical", "Finance", "Education", "Work", "Social Media", "Entertainment", "Shopping", "Other"]
        dropdown = ttk.Combobox(self.inner, values=options, width=23, font=("Arial", 13))
        dropdown.set("Category")
        dropdown.pack(pady=15, ipady=6)

        #Reference input
        Refname_entry = Entry(self.inner, width=25, font=("Arial", 12), bd=1, relief="solid")
        Refname_entry.pack(pady=15, ipady=6)
        Refname_entry.insert(0, " Reference name")
        Refname_entry.config(fg="grey")

        def on_click(event):
            if Refname_entry.get() == " Reference name":
                Refname_entry.delete( 0, "end")

        Refname_entry.bind("<FocusIn>", on_click)

        #Store Password input
        SPassword_entry = Entry(self.inner, width=25, font=("Arial", 12), bd=1, relief="solid")
        SPassword_entry.pack(pady=15, ipady=6)
        SPassword_entry.insert(0, " Password")
        SPassword_entry.config(fg="black")

        def on_click(event):
            if SPassword_entry.get() == " Password":
                SPassword_entry.delete(0, "end")
                SPassword_entry.config(fg="black")

        SPassword_entry.bind("<FocusIn>", on_click)

        def autofill():
            # Auto password generator function
            def AutoGenerate():

                # Each set of characters in a charatacter type is assigned a variable

                upper = string.ascii_uppercase
                lower = string.ascii_lowercase
                digits = string.digits
                symbols = "!@#$%^&*()-_=+[]{};:,.<>?"

                character_type = [upper, lower, digits, symbols]

                # Creation of password with 4 characters in each character type
                password_chars = []

                for i in range(0, 4):
                    for j in range(0, 4):
                        password_chars.append(random.choice(character_type[i]))

                # Shuffle code for password_chars
                shuffled = []
                while len(password_chars) > 0:
                    rand_index = random.randrange(0, len(password_chars))
                    shuffled.append(password_chars[rand_index])
                    password_chars.pop(rand_index)
                password_chars = shuffled

                # Combine the password characters to a string

                password = ""
                for i in range(0, len(password_chars)):
                    password = password + password_chars[i]
                return password

            Autopassword = AutoGenerate()

            SPassword_entry.delete(0, "end")
            SPassword_entry.insert(0, Autopassword)

        # Save function to save the data in the database
        def save():
            # get user inputs
            category = dropdown.get()
            reference = Refname_entry.get()
            password = SPassword_entry.get()

            # Encrypt the password
            def encryption(password):
                # hardcoded all user inputs
                Keyboard = "(l@p?si!3=g0Z5>2-TBUzx]7tGVHw8&.[4_n}F{O9^ENKhD6v:f$XdPeaAq1yYCmI,JojMk)*S%#u<bcRrLQ;W+"
                shift_key = len(password)

                # Shifting the whole keyboard
                shifted = Keyboard[shift_key:] + Keyboard[:shift_key]

                encrypted = []
                for char in password:
                    index = Keyboard.find(char)
                    encrypted.append(shifted[index])
                encrypted.append(str(password[0]))

                # Adding 4 random characters from keyboard to the encrypted password
                for i in range(4):
                    Temp = random.randrange(1, 86)  # temporary holds a random number
                    encrypted.append(str(Keyboard[Temp]))

                return "".join(encrypted)

            encrypted_pw = encryption(password)

            # Database connection
            conn = sqlite3.connect("vault.db")
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Ensure table exists
            cursor.execute("""CREATE TABLE IF NOT EXISTS Passwords (
                            PasswordID INTEGER PRIMARY KEY AUTOINCREMENT,
                            CategoryName TEXT NOT NULL,
                            ReferenceName TEXT NOT NULL,
                            EncryptPassword TEXT NOT NULL,
                            UserID TEXT NOT NULL,
                            FOREIGN KEY (UserID) REFERENCES UserAccounts(UserID) )""")

            # Insert data into the password table
            cursor.execute(
                "INSERT INTO Passwords (CategoryName, ReferenceName, EncryptPassword, UserID) VALUES (?, ?, ?, ?)",(category, reference, encrypted_pw, self.user_id))
            conn.commit()
            conn.close()
            self.switch_page(Mainpage, user_id)

        #Buttons
        AutoGenbtn = Button(self.inner, text="Auto Generate", font=FONT_BUTTON, width=15, command=autofill)
        AutoGenbtn.pack(pady=20)
        Button(self.inner, text="Save", font=FONT_BUTTON, width=10, command=save).pack(side="right", pady=20, padx=20)
        Button(self.inner, text="Back", font=FONT_BUTTON, width=10, command=lambda: self.switch_page(Mainpage)).pack(side= "left", pady=20, padx=20)

class Authenticationpage(BasePage):
    def __init__(self, master, user_id, category, reference, password_id):
        super().__init__(master)
        self.user_id = user_id
        self.category = category
        self.reference = reference
        PasswordID=password_id

        Label(
            self.inner, text="Master Password",font=("Arial", 15, "bold"),bg="white").place(x=70, y=60)

        # Master Password input
        MP_entry = Entry(self.inner, width=23, font=("Arial", 14), bd=1, relief="solid", show="*")
        MP_entry.place(x=30, y=120, height=40)

        def verification():
            entered_password = MP_entry.get()

            if entered_password.strip() == "":
                messagebox.showerror("Error", "Please enter master password")
                return

            entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()

            conn = sqlite3.connect("vault.db")
            cursor = conn.cursor()
            cursor.execute("SELECT MasterPassword FROM UserAccounts WHERE UserID=?",(self.user_id,))
            result = cursor.fetchone()
            conn.close()

            if result and entered_hash == result[0]:
                self.switch_page(Show_page, self.user_id, self.category, self.reference, PasswordID)
            else:
                messagebox.showerror("Access Denied", "Incorrect master password")

        # Buttons
        Button(self.inner, text="Enter", font=FONT_BUTTON, width=10, command=verification).place(x=185, y=310)
        Button(self.inner, text="Back",font=FONT_BUTTON,width=10, command=lambda: self.switch_page(CategoryPage, self.user_id, self.category)).place(x=30, y=310)

class CategoryPage(BasePage):
    def __init__(self, master, user_id, category):
        super().__init__(master)
        self.user_id = user_id
        self.category = category

        Label(self.inner, text=f"{category}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Query database for references
        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ReferenceName
            FROM Passwords
            WHERE UserID=? AND CategoryName=?
        """, (self.user_id, self.category))
        results1 = cursor.fetchall()
        conn.close()

        #Get the password id
        # Query database for references
        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT PasswordID
                    FROM Passwords
                    WHERE UserID=? AND CategoryName=?
                """, (self.user_id, self.category))
        results2 = cursor.fetchall()
        conn.close()

        password_id=results2

        # Display each reference
        for i, (ref_name,) in enumerate(results1):
            frame = Frame(self.inner, bg="white", relief="solid", borderwidth=1)
            frame.pack(pady=5, padx=10, fill="x")

            Label(frame, text=f"Name: {ref_name}", bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            Label(frame, text="Password: *****", bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=2)

            # View button
            Button(frame,text="View", command=lambda r=ref_name: self.switch_page(Authenticationpage, self.user_id, self.category, r, password_id)).grid(row=0, column=1, rowspan=2, padx=5, pady=5)
        # Back button
        Button(self.inner, text="Back", command=lambda: self.switch_page(Mainpage, self.user_id)).pack(pady=15)


class Show_page(BasePage):
    def __init__(self, master, user_id, category, reference, PasswordID):
        super().__init__(master)
        self.user_id = user_id
        self.category = category
        self.reference = reference
        password_id= PasswordID

        name_label = Label(self, text=f"Name: {reference}", font=("Arial", 14, "bold"))
        name_label.place(x=60, y=120)

        # retrieve encrypted password form the database
        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT EncryptPassword
                    FROM Passwords
                    WHERE UserID=? AND PasswordID=?
                """, (self.user_id, password_id))
        results = cursor.fetchall()
        conn.close()

        # decrypt the encrytped password:
        def decryption(encrypted_password):
            length = len(encrypted_password)
            Keyboard = "(l@p?si!3=g0Z5>2-TBUzx]7tGVHw8&.[4_n}F{O9^ENKhD6v:f$XdPeaAq1yYCmI,JojMk)*S%#u<bcRrLQ;W+"

            encrypted_text = encrypted_password[:-4]  # Removal of unnessesary last 4 characters

            # Linear search function to find position
            def linear_search(char):
                find = str(char)
                for i in range(len(Keyboard)):
                    if Keyboard[i] == find:
                        position = i + 1
                        break
                return position

            first_char = encrypted_text[- 1]  # first character of the actual password
            FCA = linear_search(first_char)  # first character of the actual password
            FCE = linear_search(encrypted_text[0])  # position of first character of encrypted password

            shift_key = FCE - FCA  # Difference gives the shift key (length of actual password)

            shifted = Keyboard[shift_key:] + Keyboard[:shift_key]

            decrypted = []

            for char in encrypted_text:
                index = shifted.find(char)
                decrypted.append(Keyboard[index])
            decrypted.pop()  # remove the first character of the actual password

            return "".join(decrypted)

        decrypted_text = decryption(results)

        Password_label = Label(self, text=f"Password: {decrypted_text}", font=("Arial", 14, "bold"))
        Password_label.place(x=60, y=170)

        #Change input box
        Change_entry = Entry(self.inner, width=22, font=("Arial", 14), bd=1, relief="solid")
        Change_entry.place(x=40, y=140)
        Change_entry.insert(0, " Change Password here")
        Change_entry.config(fg="grey")

        def on_click(event):
            if Change_entry.get() == " Change Password here":
                Change_entry.delete(0, "end")

        Change_entry.bind("<FocusIn>", on_click)

        Button(self.inner, text="Change", font=("Arial", 12, "bold"), bg="White", bd=1, width=10).place(x=100, y=200)

        Strength_status_label = Label(self.inner, text="Strength status: ", width=15, font=("Arial", 14, "bold"))
        Strength_status_label.place(x=20, y=270)

        Button(self.inner, text="Back", font=("Arial", 12, "bold"), bg="White", bd=1, width=10).place(x=100, y=325)


if __name__ == "__main__":
    root = Tk()
    HomePage(root)
    root.mainloop()
