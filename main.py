import os
import webbrowser
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class VenvManager(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.app_name = 'WinVenv'
        self.ver_no = '0.1.1'
        self.py_ext = ('.py', '.pyw', '.pyc')
        self.root_dir = os.getcwd()

        self.master.title(f'{self.app_name}')
        self.file_menu()
        self.master.bind('<F1>', self.help_about)
        self.master.bind('<Control-r>', self.init_treeview)
        self.master.bind('<Control-n>', self.create_venv)

        self.treeview = ttk.Treeview(self, show='tree')
        self.treeview.pack(fill='both', expand=True)
        self.treeview.bind('<Double-1>', self.open_file)
        self.treeview.bind("<Button-3>", self.popup_menu)
        self.init_treeview()
        self.treeview_scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar.set)
        self.treeview.pack(side='left', fill='both', expand=True)
        self.treeview_scrollbar.pack(side='right', fill='y')

    # file menu system
    def file_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
       # create a "File" menu
        self.file_bar = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='File', menu=self.file_bar)
        # add options to the "File" menu
        self.file_bar.add_command(label='Reload FileTree', command=self.init_treeview, accelerator='Ctrl+R')
        self.file_bar.add_command(label='Create Venv', command=self.create_venv, accelerator='Ctrl+N')
        self.file_bar.add_separator()
        self.file_bar.add_command(label='Exit', command=self.master.quit, accelerator='Alt+F4')
        # create "Environments" menu
        self.venv_bar = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Environments', menu=self.venv_bar)
        # add dynamic options to the "Environments" menu
        self.venv_menu()
        # create "Help" menu
        self.help_bar = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Help', menu=self.help_bar)
        # add options to the "Help" menu
        self.help_bar.add_command(label='About', command=self.help_about, accelerator='F1')
        self.help_bar.add_separator()
        self.help_bar.add_command(label='Developer Website', command=lambda: self.help_link(link='lanecrest'))
        self.help_bar.add_command(label='GitHub Project', command=lambda: self.help_link(link='github'))

    # dynamic "Environments" menu options
    def venv_menu(self):
        # clear existing options
        self.venv_bar.delete(0, tk.END)
        # find folders with activate.bat script and add as menu options
        venv_exist = False
        for folder in os.listdir(self.root_dir):
            script_folder_path = os.path.join(self.root_dir, folder)
            activate_path = os.path.join(script_folder_path, 'Scripts', 'activate.bat')
            if os.path.exists(activate_path):
                self.venv_bar.add_command(label=folder, command=lambda name=folder, path=script_folder_path: self.activate_venv(name, path))
                venv_exist = True
        if not venv_exist:
                self.venv_bar.add_command(label='No Environments')

    # about message box
    def help_about(self, event=None):
        tk.messagebox.showinfo(f'About {self.app_name}',
                               f'{self.app_name} is a Python virtual environment (venv) manager for Windows. The goal is to make it easy to maintain and execute Python files in different venvs.\n\n'
                               'If you place a Python script into a venv folder, you can execute it easily using that venv through the simple GUI by double clicking it.\n\n'
                               'You can also launch a shell using a venv through the "Environments" menu which will display what packages are installed and you can launch files through the shell.\n\n'
                               'Please note that renaming a venv folder will break it, so it is recommended to just create a new venv if you must change the name.\n\n'
                               f'{self.app_name} {self.ver_no} © 2023 Lanecrest Tech')
    
    # define links for "Help" menu options
    def help_link(self, link):
        if link == 'lanecrest':
            url = 'https://lanecrest.com'
            webbrowser.open_new(url)
        if link == 'github':
            url = 'https://github.com/Lanecrest/WinVenv'
            webbrowser.open_new(url)

    # create a pop-up context menu for right click
    def popup_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Copy Selected Path', command=self.copy_path)
        menu.post(event.x_root, event.y_root)

    # copy path of tree node to clipboard
    def copy_path(self):
        item = self.treeview.selection()[0]
        values = self.treeview.item(item, 'values')
        if values:
            file_name = os.path.abspath(os.path.join(*values))
            self.clipboard_clear()
            self.clipboard_append(f'"{file_name}"')
            print(f'Copied \033[96m{file_name}\033[0m to clipboard.')

    # open a command window with the activated environment
    def activate_venv(self, venv_name, venv_path):
        # activate selected virtual environment in command prompt
        activate_path = os.path.join(venv_path, 'Scripts', 'activate.bat')
        print(f'Opening \033[93m{venv_name}\033[0m virtual environment in a new shell...')
        os.system(f'start cmd /k ""{activate_path}" && pip freeze"')  # list the installed packages
        print('Done.')

    # function to initialize/reload the file tree
    def init_treeview(self, event=None):
        print('Loading file tree...')
        self.load_treeview(self.root_dir)
        self.venv_menu()  # refresh the "Environments" menu
        print('Done.')

    # clear current display and then list files, if file is a directory, more file trees are made
    def load_treeview(self, path, parent=''):
        self.treeview.delete(*self.treeview.get_children(parent))
        for item in os.listdir(path):
            # check if path is a directory
            if os.path.isdir(os.path.join(path, item)):
                node = self.treeview.insert(parent, 'end', text=item, tags=('folder',))
                self.load_treeview(os.path.join(path, item), node)
            else:
                # check if file is a .py file
                if item.endswith(self.py_ext):
                    tags = ('python',)
                else:
                    tags = ()
                self.treeview.insert(parent, 'end', text=item, values=[path, item], tags=tags)
        self.treeview.tag_configure('folder', font=('', 8, 'bold'))
        self.treeview.tag_configure('python', foreground='blue')
        
    # function to handle opening files from the file tree    
    def open_file(self, event):
        item = self.treeview.selection()[0]
        values = self.treeview.item(item, 'values')
        if values:
            file_name = os.path.join(*values)
            folder_path = os.path.dirname(file_name)
            print(f'Opening file \033[96m{file_name}\033[0m...')
            # if python file, open using the venv of the folder the file is in
            if os.path.isfile(file_name) and file_name.endswith(self.py_ext):
                script_folder_path = os.path.dirname(file_name)
                # keep going up a directory until a Scripts\activate.bat is found
                while script_folder_path:
                    activate_path = os.path.join(script_folder_path, 'Scripts', 'activate.bat')
                    if os.path.exists(activate_path):
                        venv_name = os.path.basename(script_folder_path)
                        print(f'Loading with \033[93m{venv_name}\033[0m virtual environment...')
                        os.chdir(script_folder_path)  # change working directory to script folder
                        os.system(f'start cmd /k "cd /d "{script_folder_path}" && call "{activate_path}" && cd "{folder_path}" && python "{file_name}" && exit"')
                        break
                    # open the file if no activate.bat file is found
                    elif script_folder_path == os.path.dirname(self.root_dir):
                        os.startfile(file_name)
                        break
                    script_folder_path = os.path.dirname(script_folder_path)
            # open any other file type normally
            elif os.path.isfile(file_name):
                os.chdir(folder_path)
                os.startfile(file_name)
            print('Done.')

    # function to create a new virtual environment
    def create_venv(self, event=None):
        # prompt for virtual environment name
        venv_name = tk.simpledialog.askstring('Create Virtual Environment', 'Enter a name for the new virtual environment:')
        if venv_name:
            # create the venv in the venv manager directory
            venv_path = os.path.join(self.root_dir, venv_name)
            print(f'Creating \033[93m{venv_name}\033[0m virtual environment...')
            os.system(f'py -m venv "{venv_path}"')
            self.init_treeview()

# main loop
if __name__ == '__main__':
    root = tk.Tk()
    app = VenvManager(root)
    app.pack(fill='both', expand=True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app_width = 640
    app_height = 480
    x = (screen_width // 2) - (app_width // 2)
    y = (screen_height // 2) - (app_height // 2)
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    root.mainloop()
