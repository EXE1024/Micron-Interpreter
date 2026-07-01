
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os 
import subprocess
import time
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000 if os.name == 'nt' else 0

class MVE:
    def __init__(self,root):
        self.root = root
        self.root.title("Micron Visual Environment")
        self.root.geometry("980x490")
        self.root.resizable(True, False)

        self.act_dir = os.path.dirname(__file__)
        self.securedpath = os.path.join(self.act_dir, "resources", "mev_icon.png")
        self.icon = tk.PhotoImage(file=self.securedpath)
        self.root.iconphoto(True, self.icon)
        self.path = tk.StringVar()
        self.debug = tk.BooleanVar(value=False)
        self.code = tk.StringVar()

        self.start()

    def start(self):
        main = ttk.Frame(self.root, padding="20")
        main.pack(fill=tk.BOTH, expand=True)

        title_text = ttk.Label(
            main,
            text="Micron Visual Environment",
            font=("Verdana", 14),
            foreground="#FFFFFF"
        )
        title_text.pack(pady=(0,10))

        pathframe = ttk.LabelFrame(main, text=" Files ", padding="20")
        pathframe.pack(fill=tk.X, pady=(5,0))

        ttk.Label(pathframe, text="Script Path").pack(anchor=tk.W)

        entry = ttk.Frame(pathframe)
        entry.pack(fill=tk.X, pady=(5,0))

        self.entrypath = ttk.Entry(entry, textvariable=self.path)
        self.entrypath.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browser = ttk.Button(entry, text="Browse...", command=self.browse_file)
        browser.pack(side=tk.RIGHT)

        env = ttk.LabelFrame(main, text=" Executor ",padding=10)
        env.pack(fill=tk.X, pady=(0,20))

        versions = ttk.Frame(env)
        versions.pack(fill=tk.X, pady=(5, 5))

        version = ttk.Label(versions, text="Executor Version: 1.1.2")
        version.pack(side=tk.LEFT, pady=(5,0))

        intversion = ttk.Label(versions, text="          "+self.get_intversion())
        intversion.pack(side=tk.LEFT, pady=(5,0))

        self.run = ttk.Button(
            main,
            text="Execute",
            command=self.execute
        )
        self.run.pack(fill=tk.X, ipadx=5)

        cnsenv = ttk.Frame(env)
        cnsenv.pack(fill="both", expand=True, padx=10, pady=10)

        debugtools = ttk.Checkbutton(
            cnsenv,
            text="Debug Tools",
            variable=self.debug,
            style="Toolbutton"
        )
        debugtools.pack(side=tk.RIGHT, pady=(5,0))

        self.console = scrolledtext.ScrolledText(
            cnsenv, 
            width=40,            # Ancho en cantidad de caracteres
            height=8,            # Alto en cantidad de líneas
            font=("Consolas", 9),# Fuente y tamaño del texto interno
            wrap=tk.WORD,        # Corta las líneas por palabras enteras
            
            bg="#001838",        # Fondo del área de texto
            fg="#FFFFFF",        # Color de las letras
            padx=5,             # Margen interno izquierdo y derecho
            pady=1,             # Margen interno superior e inferior
            relief="flat",      # Tipo de borde (flat, solid, groove, sunken)
            borderwidth=0        # Grosor del borde
        )
        self.console.pack(anchor="s", fill="x", padx=10, pady=10, expand=True)
        self.console.insert(tk.INSERT, "------ Console ------\n")
        self.console.config(state="disabled")

    def get_intversion(self):
        folder = Path(__file__).parent
        files = [item.name for item in folder.iterdir() if item.is_file]

        unk = False
        incompatible = ""

        for f in files:
            if f.startswith("micron") and f.endswith(".py"):
                new = f.replace("micron", "").replace(".py","").strip()
                if new == "1.1.2":
                    return "Interpreter version: 1.1.2 [Stable]"
                elif new == "":
                    unk = False
                else: 
                    incompatible = new

        if incompatible:
            return f"Interpreter version: {incompatible} [Incompatible]"
        if unk:
            return "Interpreter version: Unknown"

        return "Interpreter core not found"

    def get_intversion_file(self):
        folder = Path(__file__).parent
        files = [item.name for item in folder.iterdir() if item.is_file()]

        unk = False
        incompatible = ""

        for f in files:
            if f.startswith("micron") and f.endswith(".py"):
                new = f.replace("micron", "").replace(".py","").strip()
                if new == "1.1.2":
                    return [f,"UNS"]
                elif new == "":
                    unk = True
                else: 
                    incompatible = new

        if unk:
            return [f,"UNK"]
        if incompatible:
            return [f,"INC"]

    def browse_file(self):

        file = filedialog.askopenfilename(
            title="Select Micron Script",
            filetypes=[("Micron Scripts", "*.mscript"), ("Plain Text", "*.txt"), ("All Files","*.*")]
        )

        if file:
            self.path.set(file)

    def update_console(self,stdout):
        self.console.config(state="normal")
        self.console.delete("1.0",tk.END)
        self.console.insert(tk.INSERT," \n"+stdout)
        self.console.config(state="disabled")
        self.root.update_idletasks()
    def execute(self):
        path = self.entrypath.get().strip()

        if not path:
            messagebox.showwarning("Warning", "Please select or type a valid file path first")
            return
        if not os.path.exists(path):
            messagebox.showerror("Error", f"The file '{path}' does not exist")
            return
        
        intfile = self.get_intversion_file()

        if intfile[1] == "UNK":
            messagebox.showwarning("Warning", f"The file detected as the interpreter has an unknown version: {intfile[0]}")
        if intfile[1] == "INC":
            messagebox.showwarning("Warning", f"The file detected as the interpreter has an incompatible version: {intfile[0]}")

        
        env = os.environ.copy()
        env["DEBUG"] = "1" if self.debug.get() else "0"

        
        try:
            self.run.configure(text="Loading...")
            time.sleep(0.1)

            if os.name == 'nt':

                process = subprocess.Popen(
                    ['python', self.get_intversion_file()[0], path], 
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True 
                )

                synced = False

                for _ in range(10):
                    if os.path.exists(".tmp\\sync.tmp"):
                        synced = True
                        break
                    time.sleep(0.1)

                self.run.configure(text="Execute")

                if not synced:
                    process.terminate()
                    process.wait()
                    messagebox.showwarning(" Security Alert ", "The detected interpreter did not synchronize correctly with the system.")
                    return

                if os.path.exists(".tmp\\sync.tmp"):
                    os.remove(".tmp\\sync.tmp")

                stdout, stderr = process.communicate()

                if stderr:
                    self.update_console(stdout=stderr)
                else:
                    self.update_console(stdout=stdout) 
                
            else:
                process = subprocess.Popen(['x-terminal-emulator', '-e', 'python3', script_interprete, ruta], env=env_actual)

        except Exception as e:
            messagebox.showerror("Execution Error", f"Could not launch Micron: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('alt')
    style.configure(
        "TFrame",
        background="#405AEB",      
        bordercolor="#0056b3",     
        lightcolor="#0056b3",     
        darkcolor="#0056b3",       
        borderwidth=0,             
        relief="solid" 
    )       
    style.configure(
        "TLabelframe",
        background="#405AEB",      
        bordercolor="#FFFFFF",     
        lightcolor="#002349",     
        darkcolor="#002349",       
        borderwidth=1,             
        relief="solid" 
    )
    style.configure(
        "TLabelframe.Label",
        background="#405AEB",      
        foreground="#ffffff",
        font=("Segoe UI",10,"bold")
    )
    style.configure(
        "TLabel", 
        background="#405AEB",
        foreground="#ffffff",
        font=("Segoe UI",10)
    )
    style.configure(
        "TEntry",
        fieldbackground="#647BA8", 
        foreground="#ffffff",        
        bordercolor="#0056b3",       
        lightcolor="#0056b3",        
        darkcolor="#0056b3",         
        borderwidth=1,               
        padding=5                    
    )
    style.configure(
        "TButton",
        background="#1b3975",     
        foreground="#FFFFFF",      
        bordercolor="#3f4e72",     
        lightcolor="#3f4e72",      
        darkcolor="#3f4e72",       
        borderwidth=1,
        padding=6,
        font=("Segoe UI", 9, "bold")
    )
    style.configure(
        "Toolbutton",
        background="#1b4497",
        foreground="#ffffff",
        font=("Segoe UI", 9),
        padding=6
    )
    style.map(
        "Toolbutton",
        background=[("selected", "#647BA8"), ("active", "#3e4452")],
        foreground=[("selected", "#ffffff")]
    )

    style.map(
        "TButton",
        background=[("pressed", "#1e222b"), ("active", "#3e4452")],
        bordercolor=[("active", "#0056b3")]
    )        
    app = MVE(root)
    root.mainloop()