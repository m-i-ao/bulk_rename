import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class RenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Переименование файлов")
        self.root.geometry("700x500")
        
        # Переменные
        self.folder_path = tk.StringVar(value="Не выбрана")
        self.file_count = tk.StringVar(value="0")
        self.char_entries = []
        self.remove_spaces = tk.BooleanVar(value=False)
        self.replace_spaces = tk.BooleanVar(value=False)
        self.is_dark_theme = tk.BooleanVar(value=False)
        self.is_english = tk.BooleanVar(value=False)
        
        # Локализация
        self.texts = {
            "ru": {
                "title": "Переименование файлов",
                "select_folder": "Выбрать папку",
                "select_files": "Выбрать файлы",
                "folder_label": "Выбранная папка:",
                "files_label": "Выбранные файлы:",
                "chars_label": "Символы для удаления (по одному в каждом поле):",
                "remove_spaces": "Удалить пробелы",
                "replace_spaces": "Заменить пробелы на _",
                "rename": "Переименовать",
                "no_selection": "Выберите папку или файлы!",
                "nothing_renamed": "Ничего не переименовано.",
                "error": "Ошибка",
                "theme": "Тёмная тема",
                "language": "English"
            },
            "en": {
                "title": "File Renamer",
                "select_folder": "Select Folder",
                "select_files": "Select Files",
                "folder_label": "Selected Folder:",
                "files_label": "Selected Files:",
                "chars_label": "Characters to remove (one per field):",
                "remove_spaces": "Remove Spaces",
                "replace_spaces": "Replace Spaces with _",
                "rename": "Rename",
                "no_selection": "Please select a folder or files!",
                "nothing_renamed": "Nothing was renamed.",
                "error": "Error",
                "theme": "Dark Theme",
                "language": "Русский"
            }
        }
        
        # Стили
        self.style = ttk.Style()
        self.light_theme = {
            "background": "#f0f0f0",
            "foreground": "#333333",
            "entry_bg": "#ffffff",
            "button_bg": "#4a90e2",
            "button_fg": "#ffffff",
            "frame_bg": "#f0f0f0"
        }
        self.dark_theme = {
            "background": "#2d2d2d",
            "foreground": "#ffffff",
            "entry_bg": "#3c3c3c",
            "button_bg": "#6b7280",
            "button_fg": "#ffffff",
            "frame_bg": "#2d2d2d"
        }
        
        # Основной контейнер
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Применение темы после создания main_frame
        self.apply_theme(self.light_theme)
        
        # Заголовок
        self.title_label = ttk.Label(self.main_frame, text=self.texts["ru"]["title"], font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)
        
        # Кнопки выбора
        ttk.Button(self.main_frame, text=self.texts["ru"]["select_folder"], command=self.select_folder, 
                  style="Accent.TButton").pack(pady=5, fill="x")
        ttk.Button(self.main_frame, text=self.texts["ru"]["select_files"], command=self.select_files, 
                  style="Accent.TButton").pack(pady=5, fill="x")
        
        # Информация о выборе
        ttk.Label(self.main_frame, text=self.texts["ru"]["folder_label"]).pack()
        ttk.Label(self.main_frame, textvariable=self.folder_path, style="Info.TLabel").pack()
        ttk.Label(self.main_frame, text=self.texts["ru"]["files_label"]).pack()
        ttk.Label(self.main_frame, textvariable=self.file_count, style="Info.TLabel").pack(pady=10)
        
        # Поля для символов
        ttk.Label(self.main_frame, text=self.texts["ru"]["chars_label"]).pack()
        char_frame = ttk.Frame(self.main_frame)
        char_frame.pack(pady=5)
        for i in range(10):
            entry = ttk.Entry(char_frame, width=3, justify="center")
            entry.grid(row=0, column=i, padx=3)
            self.char_entries.append(entry)
        
        # Галочки для пробелов
        space_frame = ttk.Frame(self.main_frame)
        space_frame.pack(pady=10)
        ttk.Checkbutton(space_frame, text=self.texts["ru"]["remove_spaces"], variable=self.remove_spaces, 
                       command=lambda: self.toggle_checkboxes(self.remove_spaces, self.replace_spaces)).pack(side="left", padx=10)
        ttk.Checkbutton(space_frame, text=self.texts["ru"]["replace_spaces"], variable=self.replace_spaces, 
                       command=lambda: self.toggle_checkboxes(self.replace_spaces, self.remove_spaces)).pack(side="left", padx=10)
        
        # Переключатели темы и языка
        settings_frame = ttk.Frame(self.main_frame)
        settings_frame.pack(pady=10)
        ttk.Checkbutton(settings_frame, text=self.texts["ru"]["theme"], variable=self.is_dark_theme, 
                       command=self.toggle_theme).pack(side="left", padx=10)
        ttk.Checkbutton(settings_frame, text=self.texts["ru"]["language"], variable=self.is_english, 
                       command=self.toggle_language).pack(side="left", padx=10)
        
        # Кнопка переименования
        ttk.Button(self.main_frame, text=self.texts["ru"]["rename"], command=self.rename_files, 
                  style="Accent.TButton").pack(pady=10, fill="x")
        
        # Результат
        self.result_text = tk.Text(self.main_frame, height=6, width=60, state="disabled", wrap="word")
        self.result_text.pack(pady=10, fill="x")
        
        self.selected_files = []

    def apply_theme(self, theme):
        self.root.configure(bg=theme["background"])
        self.main_frame.configure(style="Main.TFrame")
        self.style.configure("Main.TFrame", background=theme["frame_bg"])
        self.style.configure("TLabel", background=theme["background"], foreground=theme["foreground"])
        self.style.configure("Info.TLabel", background=theme["background"], foreground=theme["foreground"], font=("Arial", 10, "italic"))
        self.style.configure("Accent.TButton", background=theme["button_bg"], foreground=theme["button_fg"])
        self.style.configure("TEntry", fieldbackground=theme["entry_bg"])
        self.result_text.configure(bg=theme["entry_bg"], fg=theme["foreground"])

    def toggle_theme(self):
        theme = self.dark_theme if self.is_dark_theme.get() else self.light_theme
        self.apply_theme(theme)

    def toggle_language(self):
        lang = "en" if self.is_english.get() else "ru"
        self.title_label.configure(text=self.texts[lang]["title"])
        self.root.title(self.texts[lang]["title"])
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                text = widget.cget("text")
                if text == self.texts["ru"]["select_folder"] or text == self.texts["en"]["select_folder"]:
                    widget.configure(text=self.texts[lang]["select_folder"])
                elif text == self.texts["ru"]["select_files"] or text == self.texts["en"]["select_files"]:
                    widget.configure(text=self.texts[lang]["select_files"])
                elif text == self.texts["ru"]["rename"] or text == self.texts["en"]["rename"]:
                    widget.configure(text=self.texts[lang]["rename"])
            elif isinstance(widget, ttk.Label):
                text = widget.cget("text")
                if text == self.texts["ru"]["folder_label"] or text == self.texts["en"]["folder_label"]:
                    widget.configure(text=self.texts[lang]["folder_label"])
                elif text == self.texts["ru"]["files_label"] or text == self.texts["en"]["files_label"]:
                    widget.configure(text=self.texts[lang]["files_label"])
                elif text == self.texts["ru"]["chars_label"] or text == self.texts["en"]["chars_label"]:
                    widget.configure(text=self.texts[lang]["chars_label"])
            elif isinstance(widget, ttk.Frame):
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, ttk.Checkbutton):
                        text = subwidget.cget("text")
                        if text == self.texts["ru"]["remove_spaces"] or text == self.texts["TJ
                            subwidget.configure(text=self.texts[lang]["remove_spaces"])
                        elif text == self.texts["ru"]["replace_spaces"] or text == self.texts["en"]["replace_spaces"]:
                            subwidget.configure(text=self.texts[lang]["replace_spaces"])
                        elif text == self.texts["ru"]["theme"] or text == self.texts["en"]["theme"]:
                            subwidget.configure(text=self.texts[lang]["theme"])
                        elif text == self.texts["ru"]["language"] or text == self.texts["en"]["language"]:
                            subwidget.configure(text=self.texts[lang]["language"])

    def toggle_checkboxes(self, selected, other):
        if selected.get():
            other.set(False)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.selected_files = []
            self.file_count.set("0")

    def select_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.selected_files = list(files)
            self.file_count.set(str(len(self.selected_files)))
            self.folder_path.set("Не выбрана" if not self.is_english.get() else "Not selected")

    def rename_files(self):
        lang = "en" if self.is_english.get() else "ru"
        if not self.folder_path.get() != ("Не выбрана" if not self.is_english.get() else "Not selected") and not self.selected_files:
            messagebox.showwarning(self.texts[lang]["error"], self.texts[lang]["no_selection"])
            return

        chars_to_remove = [entry.get().strip() for entry in self.char_entries if entry.get().strip()]
        
        result = ""
        try:
            if self.selected_files:
                for file_path in self.selected_files:
                    dir_name, file_name = os.path.split(file_path)
                    new_name = file_name
                    for char in chars_to_remove:
                        new_name = new_name.replace(char, "")
                    if self.remove_spaces.get():
                        new_name = new_name.replace(" ", "")
                    elif self.replace_spaces.get():
                        new_name = new_name.replace(" ", "_")
                    if new_name != file_name:
                        new_path = os.path.join(dir_name, new_name)
                        os.rename(file_path, new_path)
                        result += f"File {file_name} renamed to {new_name}\n"
            elif self.folder_path.get() != ("Не выбрана" if not self.is_english.get() else "Not selected"):
                for file_name in os.listdir(self.folder_path.get()):
                    file_path = os.path.join(self.folder_path.get(), file_name)
                    if os.path.isfile(file_path):
                        new_name = file_name
                        for char in chars_to_remove:
                            new_name = new_name.replace(char, "")
                        if self.remove_spaces.get():
                            new_name = new_name.replace(" ", "")
                        elif self.replace_spaces.get():
                            new_name = new_name.replace(" ", "_")
                        if new_name != file_name:
                            new_path = os.path.join(self.folder_path.get(), new_name)
                            os.rename(file_path, new_path)
                            result += f"File {file_name} renamed to {new_name}\n"

            if not result:
                result = self.texts[lang]["nothing_renamed"]
        except Exception as e:
            result = f"{self.texts[lang]['error']}: {str(e)}"

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = RenameApp(root)
    root.mainloop()