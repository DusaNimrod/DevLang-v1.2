import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import re
import subprocess

# I hope yall like it :p

class SimpleEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DevLang v1.3")
        self.geometry("1000x700")

        # Szerkesztő terület
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Consolas", 12))
        self.text_area.pack(expand=True, fill='both')

        # Gombok
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Run", command=self.run_code).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_file).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Open", command=self.open_file).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="New", command=self.new_file).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.quit).grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="Cut", command=lambda: self.text_area.event_generate("<<Cut>>")).grid(row=1,
                                                                                                            column=0,
                                                                                                            padx=5)
        ttk.Button(button_frame, text="Copy", command=lambda: self.text_area.event_generate("<<Copy>>")).grid(row=1,
                                                                                                              column=1,
                                                                                                              padx=5)
        ttk.Button(button_frame, text="Paste", command=lambda: self.text_area.event_generate("<<Paste>>")).grid(row=1,
                                                                                                                column=2,
                                                                                                                padx=5)
        ttk.Button(button_frame, text="Undo", command=lambda: self.text_area.event_generate("<<Undo>>")).grid(row=1,
                                                                                                              column=3,
                                                                                                              padx=5)
        ttk.Button(button_frame, text="Redo", command=lambda: self.text_area.event_generate("<<Redo>>")).grid(row=1,
                                                                                                              column=4,
                                                                                                              padx=5)

        self.console = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Consolas", 12), height=10)
        self.console.pack(expand=True, fill='both')

        # Szintaxiskiemelés
        self.configure_tags()
        self.text_area.bind('<KeyRelease>', self.on_key_release)

    def configure_tags(self):
        self.text_area.tag_configure('keyword', foreground='#0000FF')  # Blue color
        self.text_area.tag_configure('string', foreground='#008000')  # Green color
        self.text_area.tag_configure('number', foreground='#FF0000')  # Red color

    def on_key_release(self, event=None):
        self.highlight_syntax()

    def highlight_syntax(self):
        text = self.text_area.get(1.0, tk.END)
        self.text_area.tag_remove('keyword', 1.0, tk.END)
        self.text_area.tag_remove('string', 1.0, tk.END)
        self.text_area.tag_remove('number', 1.0, tk.END)

        for pattern, tag in self.syntax_patterns():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                start_index = self.text_area.index(f'1.0 + {start} chars')
                end_index = self.text_area.index(f'1.0 + {end} chars')
                self.text_area.tag_add(tag, start_index, end_index)

    def syntax_patterns(self):
        keywords = [
            'PROGRAM', 'DATA SECTION', 'DECLARE', 'AS', 'WITH VALUE', 'INTEGER', 'PROCEDURE SECTION',
            'ADD', 'TO', 'GIVING', 'PRINT', 'END PROGRAM', 'SEND', 'PRINT1', 'LOADSCRIPT', 'UPDOWN',
            'DOWNUP', 'EXECUTE', 'PRINT2', 'VARIABLE1', 'VARIABLE2', 'VARIABLE3', 'VARIABLE4',
            'VARIABLE5', 'VARIABLE6', 'VARIABLE7', 'A_B_C', 'PRINT1', 'DATATYPE', 'DATA', 'REPEAT',
            'EQUAL', 'MINUS', 'MULTIPLICATION', 'DIVISION', 'IDENTIFICATION', 'ID', 'VERSION',
            'IMPORT', 'DVLG', 'CONSOLE', 'MAIN_DATABASE', 'UNTIL', 'ELSE', 'IF', 'END',
            'EXAMPLE@GMAIL.COM', 'WHEN', 'TRANSLATE', 'INSTALL', 'LUA', 'JAVASCRIPT', 'PYTHON',
            'DATA_LOAD', 'RIGHTLEFT', 'LEFTRIGHT', 'BRACKET-START', 'TAKE', 'IS', 'TRUE', 'FALSE',
            'SENT', 'GET', 'THEN', 'ON', 'OFF', 'SOURCE', 'A_DATABASE', 'B_DATABASE', 'THE',
            'Y_FUNCTION', 'X_FUNCTION', 'BRACKET-END', 'WHILE', 'CONTINUE', 'FUNCTION', 'RETURN',
            'MODULE', 'EVENT', 'GET_EVENT', 'TEST_MODULE', 'CALL', 'STACK', 'SWITCH', 'CASE',
            'DEFAULT', 'INCREMENT', 'DECREMENT', 'PLUS', 'EXPORT', 'DATA_RECEIVED', 'RESULT',
            'REVERSE', 'BREAK', 'LOOP', 'PROCESS', 'USERDATA', 'DATACORRECT', 'WAIT-1-MIN',
            'WAIT-5-MIN', 'WAIT-1-SEC', 'WAIT-5-SEC', 'FROM', 'FROM-INPUT', 'TO-INPUT', 'USERINPUT',
            'COMPILE', 'AUTHOR', 'PROGRAM-ID', 'INPUT', 'TEXTBOX', 'LABEL', 'MAINGUI', 'BUTTON',
            'TEXT', 'RED', 'BLUE', 'GREEN', 'WHITE', 'COLOR', 'AND', 'CIRCLE', 'CONTROL', 'LEFT',
            'RIGHT', 'UP', 'DOWN', 'SERVERSIDE', 'SS', 'CLIENTSIDE', 'CS', 'MOVE', 'DATABASE',
            'DESTROY-A_B_C', 'WHEN-A-PRESSED', 'PERMISSION-TO-DEVICE', 'DELETEDATA', 'DEVICE',
            'PERMISSION', 'DESTROY', 'DELETE', 'COMMENT', 'ALLOW', 'GOTO', 'GO', 'USER', 'OUTPUT',
            'AFTER', 'BEFORE', 'RANDOM', 'CONSOLE.KEY', 'TEXT', 'INTERPRETS', 'GUI-REQUEST', 'DEVLANG-REQUEST',
            'LUA-REQUEST', 'PYTHON-REQUEST', 'JAVASCRIPT-REQUEST', 'DATA-REQUEST', 'NODE-REQUEST',
            'APPLICATION', 'USERS-MORE', 'MORE', 'REQUEST', 'Y', 'X', 'Z', 'NODE', 'MODIFY',
            'TYPE', 'TASK', 'DUSA-NIMROD', 'HTTP-REQUEST', 'SERVICE']
        return [
            (r'\b(' + '|'.join(keywords) + r')\b', 'keyword'),
            (r'\".*?\"', 'string'),
            (r'\b\d+\b', 'number')
        ]

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        try:
            result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=10)
            output = result.stdout.strip() + '\n' + result.stderr.strip()
            self.console.delete(1.0, tk.END)
            self.console.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            self.console.delete(1.0, tk.END)
            self.console.insert(tk.END, e.stderr)
        except subprocess.TimeoutExpired:
            self.console.delete(1.0, tk.END)
            self.console.insert(tk.END, "Execution timed out.")


if __name__ == "__main__":
    editor = SimpleEditor()
    editor.mainloop()
