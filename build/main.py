import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Rajnish SafeGuard AI")
    root.geometry("400x300")

    # macOS crash se bachne ke liye basic menu
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    label = tk.Label(root, text="System Running Safely")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()