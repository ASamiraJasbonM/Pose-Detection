# src/main.py
from .gui import build_main_window

def main():
    app = build_main_window()
    app.mainloop()

if __name__ == "__main__":
    main()