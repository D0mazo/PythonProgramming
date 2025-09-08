import tkinter as tk
from gui import TaskManagerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()