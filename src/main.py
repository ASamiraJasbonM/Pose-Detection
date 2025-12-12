# src/main.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gui import build_main_window

def main():
    app = build_main_window()
    app.mainloop()

if __name__ == "__main__":
    main()