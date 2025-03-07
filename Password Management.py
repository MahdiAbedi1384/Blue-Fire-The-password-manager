import tkinter as tk
import tkinter.messagebox as messagebox
from email.generator import Generator
from tkinter import ttk, PhotoImage
import generator
from pyperclip import copy
import backend


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.selected_title = None

        self.title('Blue Fire')
        self.iconphoto(False, PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/fire.png'))

        self.dark_mode = False
        self.style = ttk.Style()

        self.username = None
        self.password = None
        self.restore_key = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (App, Login, SignUp, Vault, AddItem,Generator,Settings,RestoreAcc):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(App)

    def show_frame(self, cont):
        frame = self.frames[cont]

        if cont == Vault:
            frame.load_cards(self)

        if cont == AddItem and self.selected_title is None:
            frame.titleInput.config(state="normal")
            frame.titleInput.delete(0, "end")
            frame.usernameInput.delete(0, "end")
            frame.passwordInput.delete(0, "end")

        frame.tkraise()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            bg_color = "#2D2D2D"
            fg_color = "white"
            btn_bg = "#444"
            entry_bg = "#3E3E3E"
        else:
            bg_color = "white"
            fg_color = "black"
            btn_bg = "lightgray"
            entry_bg = "white"

        self.style.configure("TLabel", background=bg_color, foreground=fg_color)
        self.style.configure("TButton", foreground=fg_color)
        self.style.map("TButton", background=[("active", btn_bg), ("!disabled", btn_bg)])

        self.style.configure("TEntry", background=fg_color)
        self.style.map("TEntry", fieldbackground=[("readonly", entry_bg), ("!disabled", entry_bg)])

        for frame in self.frames.values():
            frame.configure(bg=bg_color)


class App(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Sign Up or Login")
        label.grid(row=0, column=1, padx=5, pady=5)
        loginBtn = ttk.Button(self, text="Login",
                              command=lambda: controller.show_frame(Login))
        loginBtn.grid(row=1, column=1, padx=2, pady=2)
        signupBtn = ttk.Button(self, text="Sign Up",
                               command=lambda: controller.show_frame(SignUp))
        signupBtn.grid(row=2, column=1, padx=2, pady=2)

        restoreBtn = ttk.Button(self, text="Restore Account",command=lambda : controller.show_frame(RestoreAcc))
        restoreBtn.grid(row=3, column=1, padx=2, pady=2)

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login")
        label.grid(row=0, column=1, padx=5, pady=11)
        Uname = ttk.Label(self, text="Username")
        Uname.grid(row=1, column=1, padx=5, pady=2)
        self.UnameInput = ttk.Entry(self, width=20,style="TEntry")
        self.UnameInput.grid(row=2, column=1, padx=5, pady=5)
        Password = ttk.Label(self, text="Password")
        Password.grid(row=3, column=1, padx=5, pady=2)
        self.PasswordInput = ttk.Entry(self, show="*", width=20,style="TEntry")
        self.PasswordInput.grid(row=4, column=1, padx=5, pady=5)
        LoginBtn = ttk.Button(self, text="Login",
                              command=lambda: self.checker(controller))
        LoginBtn.grid(row=5, column=1, padx=2, pady=7)
        signupLabel = ttk.Label(self, text="You don't have an account?")
        signupLabel.grid(row=6, column=1, padx=5, pady=2)
        signupBtn = ttk.Button(self, text="Sign Up",
                               command=lambda: controller.show_frame(SignUp))
        signupBtn.grid(row=7, column=1, padx=2, pady=2)

        forgotLabel = ttk.Label(self, text="Forgot your username or password?")
        forgotLabel.grid(row=8, column=1, padx=5, pady=2)

        restoreBtn = ttk.Button(self, text="Restore Account",command=lambda : controller.show_frame(RestoreAcc))
        restoreBtn.grid(row=9, column=1, padx=2, pady=2)

    def checker(self, controller):
        if backend.main().search(self.UnameInput.get(), self.PasswordInput.get()):
            controller.username = self.UnameInput.get()
            controller.password = self.PasswordInput.get()

            # دریافت RestoreKey بعد از لاگین
            mainclass = backend.main()
            RSKey = mainclass.getRestoreKey(controller.username, controller.password)
            controller.restore_key = RSKey  # ذخیره در کنترلر

            backend.Account(controller.username, controller.password, RSKey).CreateDB()
            return controller.show_frame(Vault)
        else:
            messagebox.showwarning("Error", "Username or Password is incorrect")

    def getusername(self):
        return self.UnameInput.get()

    def getpassword(self):
        return self.PasswordInput.get()


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Sign Up")
        label.grid(row=0, column=1, padx=5, pady=10)
        Uname = ttk.Label(self, text="Username")
        Uname.grid(row=1, column=1, padx=5, pady=2)
        self.UnameInput = ttk.Entry(self, width=20,style="TEntry")
        self.UnameInput.grid(row=2, column=1, padx=5, pady=5)
        Password = ttk.Label(self, text="Password")
        Password.grid(row=3, column=1, padx=5, pady=2)
        self.PasswordInput = ttk.Entry(self, width=20,style="TEntry")
        self.PasswordInput.grid(row=4, column=1, padx=5, pady=5)
        signupBtn = ttk.Button(self, text="Sign Up",
                               command=lambda: self.AddAccount(controller))
        signupBtn.grid(row=5, column=1, padx=2, pady=7)
        loginLabel = ttk.Label(self, text="You have an account?")
        loginLabel.grid(row=6, column=1, padx=5, pady=2)
        loginBtn = ttk.Button(self, text="Login",
                              command=lambda: controller.show_frame(Login))
        loginBtn.grid(row=7, column=1, padx=2, pady=2)

    def AddAccount(self, controller):
        backend.main().insert(self.UnameInput.get(), self.PasswordInput.get())
        controller.username = self.UnameInput.get()
        controller.password = self.PasswordInput.get()

        mainclass = backend.main()
        RSKey = mainclass.getRestoreKey(controller.username, controller.password)
        controller.restore_key = RSKey

        controller.show_frame(Login)


class Vault(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Vault", font=("Helvetica", 15))
        label.grid(row=0, column=0, padx=30, pady=15, columnspan=3)

        self.AddIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/add.png')
        AddLoginBtn = ttk.Button(self, image=self.AddIcon, command=lambda: controller.show_frame(AddItem))
        AddLoginBtn.grid(row=0, column=4, padx=10, pady=15)

        self.Acc = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/account.png')
        switchAccBtn = ttk.Button(self, image=self.Acc, command=lambda: controller.show_frame(Login))
        switchAccBtn.grid(row=0, column=5, padx=0, pady=15)

        self.SearchBox = ttk.Entry(self, style="TEntry")
        self.SearchBox.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="ew")
        self.SearchBox.bind("<Return>", lambda event: self.SearchItems(controller))

        ItemsLabel = ttk.Label(self, text="All Items")
        ItemsLabel.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        self.canvas = tk.Canvas(self, height=300)
        self.canvas.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=3, column=3, sticky="ns")

        self.cards_frame = tk.Frame(self.canvas, bg="lightgray")
        self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.bottom_menu = tk.Frame(self, bg="gray")
        self.bottom_menu.grid(row=8, column=0, columnspan=3, sticky="nsew")

        self.HomeIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/lock.png')
        HomeBtn = ttk.Button(self.bottom_menu, image=self.HomeIcon, command=lambda: controller.show_frame(Vault))
        HomeBtn.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        self.generateIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/process.png')
        generateBtn = ttk.Button(self.bottom_menu, image=self.generateIcon, command=lambda: controller.show_frame(Generator))
        generateBtn.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        self.logoutIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/export.png')
        btn_logout = ttk.Button(self.bottom_menu, image=self.logoutIcon, command=lambda: self.quit())
        btn_logout.pack(side="right", expand=True, fill="x", padx=5, pady=5)

        self.settingIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/automatic.png')
        btn_settings = ttk.Button(self.bottom_menu, image=self.settingIcon, command=lambda: controller.show_frame(Settings))
        btn_settings.pack(side="right", expand=True, fill="x", padx=5, pady=5)

        self.load_cards(controller)

        self.cards_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def load_cards(self, controller, card_data=None):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if card_data is None:
            if not controller.username or not controller.password or not controller.restore_key:
                return
            AccData = backend.Account(controller.username, controller.password, controller.restore_key)
            card_data = AccData.View()

        for i, data in enumerate(card_data):
            title, username = data[:2]  # فقط title و username را بگیر

            card = ttk.Frame(self.cards_frame, relief="ridge", borderwidth=2)
            card.grid(row=i, column=0, padx=5, pady=5, sticky="ew")

            lbl_title = ttk.Label(card, text=title, font=("Arial", 12, "bold"))
            lbl_title.pack(side="top", anchor="w", padx=5, pady=2)

            lbl_username = ttk.Label(card, text=username, font=("Arial", 10))
            lbl_username.pack(side="bottom", anchor="w", padx=5, pady=2)

            card.bind("<Button-1>", lambda event, t=title: self.open_add_item(controller, t))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def SearchItems(self, controller):
        AccData = backend.Account(controller.username, controller.password, controller.restore_key)
        search_results = AccData.Search(self.SearchBox.get())
        self.load_cards(controller, search_results)

    def open_add_item(self, controller, title=None):
        add_item_page = controller.frames[AddItem]

        if title:
            controller.selected_title = title
            AccData = backend.Account(controller.username, controller.password, controller.restore_key)
            data = AccData.getItem(title)

            if data:
                add_item_page.titleInput.config(state="normal")
                add_item_page.titleInput.delete(0, "end")
                add_item_page.titleInput.insert("end", data[0])
                add_item_page.titleInput.config(state="readonly")

                add_item_page.usernameInput.delete(0, "end")
                add_item_page.usernameInput.insert("end", data[1])

                add_item_page.passwordInput.delete(0, "end")
                add_item_page.passwordInput.insert("end", data[2])
        else:
            controller.selected_title = None
            add_item_page.titleInput.config(state="normal")
            add_item_page.titleInput.delete(0, "end")
            add_item_page.usernameInput.delete(0, "end")
            add_item_page.passwordInput.delete(0, "end")

        controller.show_frame(AddItem)


class AddItem(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.backIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/return.png')
        backBtn = ttk.Button(self, image=self.backIcon, command=lambda: controller.show_frame(Vault))
        backBtn.grid(row=0, column=0, padx=10, pady=15)

        label = ttk.Label(self, text="View login", font=("Helvetica", 15))
        label.grid(row=0, column=1, padx=5, pady=15)

        titleLabel = ttk.Label(self, text="Item Name")
        titleLabel.grid(row=1, column=0, padx=5, pady=5)

        self.titleInput = ttk.Entry(self, width=20,style="TEntry")
        self.titleInput.grid(row=2, column=0, padx=5, pady=10)

        logincredentialsLabel = ttk.Label(self, text="Login Credentials")
        logincredentialsLabel.grid(row=3, column=0, padx=5, pady=15)

        usernameLabel = ttk.Label(self, text="Username")
        usernameLabel.grid(row=4, column=0, padx=5, pady=2)

        self.usernameInput = ttk.Entry(self, width=20,style="TEntry")
        self.usernameInput.grid(row=5, column=0, padx=5, pady=10)

        passwordLabel = ttk.Label(self, text="Password")
        passwordLabel.grid(row=6, column=0, padx=5, pady=2)

        self.passwordInput = ttk.Entry(self, width=20,style="TEntry")
        self.passwordInput.grid(row=7, column=0, padx=5, pady=10)

        copyBtn = ttk.Button(self, text="Copy", command=lambda: copy(self.passwordInput.get()))
        copyBtn.grid(row=7, column=1, padx=2, pady=15)

        self.bottom_menu = tk.Frame(self, bg="gray")
        self.bottom_menu.grid(row=8, column=0, columnspan=3, sticky="nsew")

        saveBtn = ttk.Button(self.bottom_menu,text="Save", command=lambda: self.addcard(controller))
        saveBtn.grid(row=8, column=0, padx=2, pady=5)

        if controller.username and self.titleInput.get():
            id = backend.Account(controller.username, controller.password, controller.restore_key).getId(
                self.titleInput.get())
        else:
            id = None

        editBtn = ttk.Button(self.bottom_menu,text='Edit',command=lambda : self.updatecard(controller))
        editBtn.grid(row=8, column=1, padx=2, pady=5)

        deleteBtn = ttk.Button(self.bottom_menu,text='Delete',command=lambda: self.deletecard(controller))
        deleteBtn.grid(row=8, column=2, padx=2, pady=5)

    def updatecard(self,controller):
        backend.Account(controller.username, controller.password, controller.restore_key).Update(id, self.titleInput.get(),self.usernameInput.get(), self.passwordInput.get())
        controller.frames[Vault].load_cards(controller)
        controller.show_frame(Vault)

    def addcard(self,controller):
        backend.Account(controller.username, controller.password, controller.restore_key).Insert(self.titleInput.get(),self.usernameInput.get(),self.passwordInput.get())
        controller.frames[Vault].load_cards(controller)
        controller.show_frame(Vault)

    def deletecard(self, controller):
        id = backend.Account(controller.username, controller.password, controller.restore_key).getId(
            self.titleInput.get())

        if id is None:
            messagebox.showwarning("Error", "Invalid item selected for deletion!")
            return

        backend.Account(controller.username, controller.password, controller.restore_key).Delete(id)

        controller.frames[Vault].cards_frame.destroy()
        controller.frames[Vault].cards_frame = tk.Frame(controller.frames[Vault], bg="lightgray")
        controller.frames[Vault].cards_frame.grid(row=3, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

        controller.frames[Vault].load_cards(controller)

        AccData = backend.Account(controller.username, controller.password, controller.restore_key)
        remaining_cards = AccData.View()

        if not remaining_cards:
            self.titleInput.config(state="normal")
            self.titleInput.delete(0, "end")
            self.usernameInput.delete(0, "end")
            self.passwordInput.delete(0, "end")

            controller.selected_title = None

        controller.show_frame(Vault)  


class Generator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Generator", font=("Helvetica", 15))
        label.grid(row=0, column=0, padx=30, pady=10)

        self.Acc = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/account.png')
        switchAccBtn = ttk.Button(
            self, image=self.Acc, command=lambda: controller.show_frame(Login))
        switchAccBtn.grid(row=0, column=5, padx=0, pady=15)

        labelPassGen = ttk.Label(self, text="Password Generator")
        labelPassGen.grid(row=1, column=0, padx=5, pady=3)

        self.passwordGen = ttk.Entry(self, width=20, state="readonly",style="TEntry")
        self.passwordGen.grid(row=2, column=0, padx=5, pady=5)

        GenBtn = ttk.Button(self, text="Generate", command=lambda: self.generate())
        GenBtn.grid(row=2, column=1, padx=2, pady=5, sticky="nsew")

        cpBtn = ttk.Button(self,text="Copy", command=lambda: copy(self.passwordGen.get()))
        cpBtn.grid(row=2, column=2, padx=2, pady=5)

        optionsLabel = ttk.Label(self, text="Options")
        optionsLabel.grid(row=3, column=0, padx=5, pady=15)

        lengthLabel = ttk.Label(self, text="Length")
        lengthLabel.grid(row=4, column=0, padx=5, pady=2)

        self.lengthEntry = ttk.Entry(self, width=20,style="TEntry")
        self.lengthEntry.grid(row=5, column=0, padx=5, pady=10)

        includeLabel = ttk.Label(self, text="Include")
        includeLabel.grid(row=6, column=0, padx=5, pady=2)

        CapitalsOption = ttk.Checkbutton(self,text='A-Z',command=lambda : self.activeOption.append(1))
        CapitalsOption.grid(row=7, column=0, padx=2, pady=5)

        smallsOption = ttk.Checkbutton(self, text='a-z',command=lambda : self.activeOption.append(2))
        smallsOption.grid(row=7, column=1, padx=2, pady=5)

        numsOption = ttk.Checkbutton(self, text='0-9',command=lambda : self.activeOption.append(3))
        numsOption.grid(row=7, column=2, padx=2, pady=5)

        self.bottom_menu = tk.Frame(self, bg="gray")
        self.bottom_menu.grid(row=8, column=0, columnspan=3, sticky="nsew")

        self.HomeIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/lock.png')
        HomeBtn = ttk.Button(self.bottom_menu, image=self.HomeIcon, command=lambda: controller.show_frame(Vault))
        HomeBtn.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        self.generateIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/process.png')
        generateBtn = ttk.Button(self.bottom_menu, image=self.generateIcon,
                                 command=lambda: controller.show_frame(Generator))
        generateBtn.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        self.logoutIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/export.png')
        btn_logout = ttk.Button(
            self.bottom_menu, image=self.logoutIcon, command=lambda: self.quit())
        btn_logout.pack(side="right", expand=True, fill="x", padx=5, pady=5)
        self.settingIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/automatic.png')
        btn_settings = ttk.Button(self.bottom_menu, image=self.settingIcon,
                                  command=lambda: controller.show_frame(Settings))
        btn_settings.pack(side="right", expand=True, fill="x", padx=5, pady=5)

        self.activeOption = []

    def generate(self):
        k = self.lengthEntry.get().strip()
        if not k.isdigit():
            messagebox.showwarning("Error", "Please enter a valid number for length.")
            return

        options = self.activeOption
        if not options:
            messagebox.showwarning("Error", "Please select at least one option.")
            return

        self.generated = generator.Generator(int(k), options).passwordGenerate()

        self.passwordGen.config(state="normal")
        self.passwordGen.delete(0, "end")
        self.passwordGen.insert("end", self.generated)
        self.passwordGen.config(state="readonly")

class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.style = ttk.Style()

        settingsLabel = ttk.Label(self, text="Settings",font=("Helvetica", 15))
        settingsLabel.grid(row=0, column=0, padx=5, pady=15)

        self.Acc = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/account.png')
        switchAccBtn = ttk.Button(
            self, image=self.Acc, command=lambda: controller.show_frame(Login))
        switchAccBtn.grid(row=0, column=5, padx=0, pady=15)

        uiModeLabel = ttk.Label(self, text="UI mode")
        uiModeLabel.grid(row=1, column=0, padx=5, pady=3)

        darkModeBtn = ttk.Button(self,text='Dark',command=lambda : self.DarkMode(controller))
        darkModeBtn.grid(row=2, column=1, padx=5, pady=5)

        lightModeBtn = ttk.Button(self,text='Light',command=lambda : self.LightMode(controller))
        lightModeBtn.grid(row=2, column=2, padx=5, pady=5)
        
        RestoreKeyLabel = ttk.Label(self, text="Restore Key")
        RestoreKeyLabel.grid(row=3, column=0, padx=5, pady=10)
        
        self.RestoreKey = ttk.Entry(self, width=25, state="readonly",style="TEntry")
        self.RestoreKey.grid(row=4, column=0, padx=5, pady=5)

        ShowRestoreKey = ttk.Button(self,text='Show',command=lambda :self.getRestoreKey(controller))
        ShowRestoreKey.grid(row=4, column=1, padx=5, pady=5)

        copyRestoreKey = ttk.Button(self,text="Copy",command=lambda :copy(controller.restore_key))
        copyRestoreKey.grid(row=4, column=2, padx=5, pady=5)

        self.bottom_menu = tk.Frame(self, bg="gray")
        self.bottom_menu.grid(row=8, column=0, columnspan=3, sticky="nsew")

        self.HomeIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/lock.png')
        HomeBtn = ttk.Button(self.bottom_menu, image=self.HomeIcon, command=lambda: controller.show_frame(Vault))
        HomeBtn.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        self.generateIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/process.png')
        generateBtn = ttk.Button(self.bottom_menu, image=self.generateIcon,
                                 command=lambda: controller.show_frame(Generator))
        generateBtn.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        self.logoutIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/export.png')
        btn_logout = ttk.Button(
            self.bottom_menu, image=self.logoutIcon, command=lambda: self.quit())
        btn_logout.pack(side="right", expand=True, fill="x", padx=5, pady=5)
        self.settingIcon = PhotoImage(file='C:/Users/Dell/PycharmProjects/pythonProject1/automatic.png')
        btn_settings = ttk.Button(self.bottom_menu, image=self.settingIcon,
                                  command=lambda: controller.show_frame(Settings))
        btn_settings.pack(side="right", expand=True, fill="x", padx=5, pady=5)

    def DarkMode(self, controller):
        controller.toggle_dark_mode()

    def LightMode(self, controller):
        controller.toggle_dark_mode()

    def getRestoreKey(self,controller):
        self.RestoreKey.config(state="normal")
        self.RestoreKey.delete(0, "end")
        self.RestoreKey.insert("end", controller.restore_key)
        self.RestoreKey.config(state="readonly")

class RestoreAcc(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Restore Account")
        label.grid(row=0, column=0, padx=5, pady=15)

        RSkeyLabel = ttk.Label(self, text="Restore Key")
        RSkeyLabel.grid(row=1, column=0, padx=5, pady=5)

        self.RSkeyInput = ttk.Entry(self, width=25)
        self.RSkeyInput.grid(row=2, column=0, padx=5, pady=15)

        RestoreBtn = ttk.Button(self,text="Restore",command= lambda :self.Restore(controller, self.RSkeyInput.get()))
        RestoreBtn.grid(row=2, column=1, padx=5, pady=5)

        usernameLabel = ttk.Label(self, text="Username")
        usernameLabel.grid(row=3, column=0, padx=5, pady=3)

        self.usernameInput = ttk.Entry(self, width=25,state="readonly")
        self.usernameInput.grid(row=4, column=0, padx=5, pady=15)

        cpUn = ttk.Button(self,text="copy",command=lambda : copy(self.Acc[1]))
        cpUn.grid(row=4, column=1, padx=5, pady=15)

        passwordLabel = ttk.Label(self, text="Password")
        passwordLabel.grid(row=5, column=0, padx=5, pady=3)

        self.passwordInput = ttk.Entry(self, width=25,state="readonly")
        self.passwordInput.grid(row=6, column=0, padx=5, pady=15)

        cpPass = ttk.Button(self,text="copy",command=lambda : copy(self.Acc[2]))
        cpPass.grid(row=6, column=1, padx=5, pady=15)

        exitBtn = ttk.Button(self,text="Exit",command=lambda : self.quit())
        exitBtn.grid(row=7, column=1, padx=5, pady=15)

        loginBtn = ttk.Button(self, text="Login", command=lambda: controller.show_frame(Login))
        loginBtn.grid(row=7, column=0, padx=5, pady=15)

    def Restore(self, controller, RSkey):
        self.Acc = backend.main.RestoreAcc(self,RSkey)

        if self.Acc:
            self.usernameInput.config(state="normal")
            self.usernameInput.delete(0, "end")
            self.usernameInput.insert("end", self.Acc[1])
            self.usernameInput.config(state="readonly")

            self.passwordInput.config(state="normal")
            self.passwordInput.delete(0, "end")
            self.passwordInput.insert("end", self.Acc[2])
            self.passwordInput.config(state="readonly")
        else:
            messagebox.showwarning("Error", "Invalid Restore Key!")


app = tkinterApp()
app.mainloop()
