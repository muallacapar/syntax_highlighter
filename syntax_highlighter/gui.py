import tkinter as tk
from lexer import tokenize
from parser import Parser
from tkinter import messagebox

TOKEN_COLORS = {
    "KEYWORD": "blue",
    "IDENTIFIER": "black",
    "NUMBER": "green",
    "OPERATOR": "red",
    "PUNCTUATION": "orange",
    "TYPE": "purple",
    "UNKNOWN": "gray"
}

class SyntaxHighlighter:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerçek Zamanlı Syntax Highlighter")

        self.text = tk.Text(root, wrap="word", font=("Consolas", 14))
        self.text.pack(expand=1, fill="both")

        self.text.bind("<KeyRelease>", self.on_key_release)

        for token_type, color in TOKEN_COLORS.items():
            self.text.tag_configure(token_type, foreground=color)

    def on_key_release(self, event=None):
        content = self.text.get("1.0", "end-1c")
        tokens = tokenize(content)

        for tag in TOKEN_COLORS.keys():
            self.text.tag_remove(tag, "1.0", tk.END)

        for ttype, value, index in tokens:
            start = self.get_position_from_index(content, index)
            end = self.get_position_from_index(content, index + len(value))
            if ttype in TOKEN_COLORS:
                self.text.tag_add(ttype, start, end)

        try:
            parser = Parser(tokens)
            if parser.parse():
                print(" GEÇERLİ")
                self.root.title("✔ Geçerli ifade")
            else:
                print(" SÖZDİZİMİ HATASI")
                self.root.title(" Sözdizimi hatası")
        except Exception as e:
            print(" PARSER HATASI:", e)
            self.root.title(" Hata: " + str(e))

    def get_position_from_index(self, text, index):
        row = 1
        col = 0
        current = 0
        for ch in text:
            if current == index:
                break
            if ch == '\n':
                row += 1
                col = 0
            else:
                col += 1
            current += 1
        return f"{row}.{col}"

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlighter(root)
    root.mainloop()
