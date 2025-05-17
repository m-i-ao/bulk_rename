import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class RenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Переименование файлов")
        self.root.geometry("900x600")
        
        # Переменные
        self.folder_path = tk.StringVar(value="Не выбрана")
        self.file_count = tk.StringVar(value="0")
        self.char_entries = []
        self.remove_spaces = tk.BooleanVar(value=False)
        self.replace_spaces = tk.BooleanVar(value=False)
        self.theme_var = tk.StringVar(value="Светлая")
        self.language_var = tk.StringVar(value="Русский")
        self.new_filename = tk.StringVar(value="")
        self.extension_vars = {}
        self.select_all_var = tk.BooleanVar(value=False)
        self.analysis_done = False
        
        # Локализация
        self.texts = {
            "ru": {
                "title": "Переименование файлов",
                "select_folder": "Выбрать папку",
                "select_files": "Выбрать файлы",
                "folder_label": "Выбранная папка:",
                "files_label": "Выбранные файлы:",
                "chars_label": "Символы для удаления (по одному в каждом поле):",
                "new_name_label": "Новое имя файла:",
                "remove_spaces": "Удалить пробелы",
                "replace_spaces": "Заменить пробелы на _",
                "rename": "Переименовать",
                "analyze": "Анализировать",
                "select_all": "Выбрать все",
                "no_selection": "Выберите папку или файлы!",
                "nothing_renamed": "Ничего не переименовано.",
                "error": "Ошибка",
                "theme_label": "Тема:",
                "language_label": "Язык:",
                "file_exists": "Файл уже существует. Заменить?",
                "replace": "Заменить",
                "append_same": "Добавить (same)",
                "no_folder": "Не выбрана"
            },
            "en": {
                "title": "File Renamer",
                "select_folder": "Select Folder",
                "select_files": "Select Files",
                "folder_label": "Selected Folder:",
                "files_label": "Selected Files:",
                "chars_label": "Characters to remove (one per field):",
                "new_name_label": "New file name:",
                "remove_spaces": "Remove Spaces",
                "replace_spaces": "Replace Spaces with _",
                "rename": "Rename",
                "analyze": "Analyze",
                "select_all": "Select All",
                "no_selection": "Please select a folder or files!",
                "nothing_renamed": "Nothing was renamed.",
                "error": "Error",
                "theme_label": "Theme:",
                "language_label": "Language:",
                "file_exists": "File already exists. Replace it?",
                "replace": "Replace",
                "append_same": "Append (same)",
                "no_folder": "Not selected"
            }
        }
        
        # Стили
        self.style = ttk.Style()
        self.light_theme = {
            "background": "#f0f0f0",
            "foreground": "#333333",
            "entry_bg": "#ffffff",
            "button_bg": "#2563eb",
            "button_fg": "#000000",
            "frame_bg": "#f0f0f0",
            "checkbutton_bg": "#f0f0f0",
            "checkbutton_fg": "#333333"
        }
        self.dark_theme = {
            "background": "#2d2d2d",
            "foreground": "#ffffff",
            "entry_bg": "#3c3c3c",
            "button_bg": "#4b5563",
            "button_fg": "#000000",
            "frame_bg": "#2d2d2d",
            "checkbutton_bg": "#2d2d2d",
            "checkbutton_fg": "#ffffff"
        }
        
        # Основной контейнер с использованием grid
        self.main_frame = ttk.Frame(root, padding=20, style="Main.TFrame")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        
        # Контейнер для левого и правого фреймов
        self.content_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
        self.content_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)
        
        # Левый фрейм для основных элементов
        self.left_frame = ttk.Frame(self.content_frame, style="Main.TFrame")
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        # Правый фрейм для расширений
        self.extension_frame = ttk.Frame(self.content_frame, style="Main.TFrame", width=200)
        self.extension_frame.pack(side="right", fill="y", padx=10)
        
        # Заголовок
        self.title_label = ttk.Label(self.left_frame, text=self.texts["ru"]["title"], font=("Arial", 18, "bold"), style="TLabel")
        self.title_label.pack(pady=10)
        
        # Кнопки выбора
        self.button_frame = ttk.Frame(self.left_frame, style="Main.TFrame")
        self.button_frame.pack(pady=5, anchor="w")
        self.style.configure("Accent.TButton", padding=(10, 5), font=("Comic Sans MS", 10))
        self.select_folder_button = ttk.Button(self.button_frame, text=self.texts["ru"]["select_folder"], command=self.select_folder, 
                                              style="Accent.TButton")
        self.select_folder_button.pack(side="left", padx=2)
        self.select_files_button = ttk.Button(self.button_frame, text=self.texts["ru"]["select_files"], command=self.select_files, 
                                             style="Accent.TButton")
        self.select_files_button.pack(side="left", padx=2)
        
        # Информация о выборе
        self.folder_label = ttk.Label(self.left_frame, text=self.texts["ru"]["folder_label"], style="TLabel")
        self.folder_label.pack()
        self.folder_path_label = ttk.Label(self.left_frame, textvariable=self.folder_path, style="Info.TLabel")
        self.folder_path_label.pack()
        self.files_label = ttk.Label(self.left_frame, text=self.texts["ru"]["files_label"], style="TLabel")
        self.files_label.pack()
        self.files_count_label = ttk.Label(self.left_frame, textvariable=self.file_count, style="Info.TLabel")
        self.files_count_label.pack(pady=10)
        
        # Поле для нового имени файла
        self.new_name_label = ttk.Label(self.left_frame, text=self.texts["ru"]["new_name_label"], style="TLabel")
        self.new_name_label.pack()
        self.new_name_entry = ttk.Entry(self.left_frame, textvariable=self.new_filename, style="TEntry")
        self.new_name_entry.pack(pady=5)
        
        # Поля для символов
        self.chars_label = ttk.Label(self.left_frame, text=self.texts["ru"]["chars_label"], style="TLabel")
        self.chars_label.pack()
        self.char_frame = ttk.Frame(self.left_frame, style="Main.TFrame")
        self.char_frame.pack(pady=5)
        for i in range(10):
            entry = ttk.Entry(self.char_frame, width=3, justify="center", style="TEntry")
            entry.grid(row=0, column=i, padx=3)
            self.char_entries.append(entry)
        
        # Галочки для пробелов
        self.space_frame = ttk.Frame(self.left_frame, style="Main.TFrame")
        self.space_frame.pack(pady=10)
        self.remove_spaces_check = ttk.Checkbutton(self.space_frame, text=self.texts["ru"]["remove_spaces"], variable=self.remove_spaces, 
                                                 command=lambda: self.toggle_checkboxes(self.remove_spaces, self.replace_spaces), 
                                                 style="Custom.TCheckbutton")
        self.remove_spaces_check.pack(side="left", padx=10)
        self.replace_spaces_check = ttk.Checkbutton(self.space_frame, text=self.texts["ru"]["replace_spaces"], variable=self.replace_spaces, 
                                                   command=lambda: self.toggle_checkboxes(self.replace_spaces, self.remove_spaces), 
                                                   style="Custom.TCheckbutton")
        self.replace_spaces_check.pack(side="left", padx=10)
        
        # Выпадающие меню для темы и языка
        self.settings_frame = ttk.Frame(self.left_frame, style="Main.TFrame")
        self.settings_frame.pack(pady=10)
        
        # Тема
        self.theme_label = ttk.Label(self.settings_frame, text=self.texts["ru"]["theme_label"], style="TLabel")
        self.theme_label.pack(side="left", padx=5)
        theme_combo = ttk.Combobox(self.settings_frame, textvariable=self.theme_var, values=["Светлая", "Тёмная"], 
                                  state="readonly", width=10, style="TCombobox")
        theme_combo.pack(side="left", padx=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda event: self.toggle_theme())
        
        # Язык
        self.language_label = ttk.Label(self.settings_frame, text=self.texts["ru"]["language_label"], style="TLabel")
        self.language_label.pack(side="left", padx=5)
        lang_combo = ttk.Combobox(self.settings_frame, textvariable=self.language_var, values=["Русский", "English"], 
                                 state="readonly", width=10, style="TCombobox")
        lang_combo.pack(side="left", padx=5)
        lang_combo.bind("<<ComboboxSelected>>", lambda event: self.toggle_language())
        
        # Кнопка переименования
        self.rename_button = ttk.Button(self.left_frame, text=self.texts["ru"]["rename"], command=self.rename_files, 
                                       style="Accent.TButton")
        self.rename_button.pack(pady=10, anchor="w", padx=2)
        
        # Результат
        self.result_text = tk.Text(self.left_frame, height=6, width=60, state="disabled", wrap="word")
        self.result_text.pack(pady=10, fill="x")
        
        # Элементы для анализа расширений
        self.analyze_button = ttk.Button(self.extension_frame, text=self.texts["ru"]["analyze"], command=self.analyze_extensions, 
                                        style="Accent.TButton")
        self.analyze_button.pack(pady=5)
        
        # Галочка "Выбрать все"
        self.select_all_check = ttk.Checkbutton(self.extension_frame, text=self.texts["ru"]["select_all"], 
                                               variable=self.select_all_var, command=self.toggle_select_all, 
                                               style="Custom.TCheckbutton", state="disabled")
        self.select_all_check.pack(pady=5)
        
        # Фрейм для списка расширений
        self.extensions_list_frame = ttk.Frame(self.extension_frame, style="Main.TFrame")
        self.extensions_list_frame.pack(fill="both", expand=True)
        
        # Текст "dev. by MIAO with AI" внизу по центру
        self.dev_label = ttk.Label(self.main_frame, text="dev. by MIAO with AI", style="TLabel")
        self.dev_label.grid(row=1, column=0, columnspan=2, sticky="s", pady=5)
        
        # Применение темы после создания всех виджетов
        self.apply_theme(self.light_theme)
        
        self.selected_files = []

    def apply_theme(self, theme):
        self.root.configure(bg=theme["background"])
        
        self.style.configure("Main.TFrame", background=theme["frame_bg"])
        self.main_frame.configure(style="Main.TFrame")
        self.content_frame.configure(style="Main.TFrame")
        self.left_frame.configure(style="Main.TFrame")
        self.extension_frame.configure(style="Main.TFrame")
        self.button_frame.configure(style="Main.TFrame")
        self.char_frame.configure(style="Main.TFrame")
        self.space_frame.configure(style="Main.TFrame")
        self.settings_frame.configure(style="Main.TFrame")
        self.extensions_list_frame.configure(style="Main.TFrame")

        self.style.configure("TLabel", background=theme["background"], foreground=theme["foreground"])
        self.style.configure("Info.TLabel", background=theme["background"], foreground=theme["foreground"], font=("Arial", 10, "italic"))

        self.style.configure("Accent.TButton", background=theme["button_bg"], foreground=theme["button_fg"], 
                           relief="flat", borderwidth=0, font=("Comic Sans MS", 10))
        self.style.map("Accent.TButton", 
                      background=[("active", "#1e40af" if theme["button_bg"] == "#2563eb" else "#374151")],
                      foreground=[("active", theme["button_fg"])])

        self.style.configure("TEntry", fieldbackground=theme["entry_bg"], background=theme["entry_bg"], 
                           foreground="#000000" if theme["background"] == "#2d2d2d" else theme["foreground"], 
                           insertcolor="#000000" if theme["background"] == "#2d2d2d" else theme["foreground"])
        self.style.map("TEntry", 
                      fieldbackground=[("active", theme["entry_bg"]), ("disabled", theme["entry_bg"])],
                      background=[("active", theme["entry_bg"]), ("disabled", theme["entry_bg"])],
                      foreground=[("active", "#000000" if theme["background"] == "#2d2d2d" else theme["foreground"]), 
                                 ("disabled", "#000000" if theme["background"] == "#2d2d2d" else theme["foreground"])])

        self.style.configure("Custom.TCheckbutton", background=theme["checkbutton_bg"], foreground=theme["checkbutton_fg"])
        self.style.map("Custom.TCheckbutton", 
                      background=[("active", theme["checkbutton_bg"]), ("disabled", theme["checkbutton_bg"])],
                      foreground=[("active", theme["checkbutton_fg"]), ("disabled", theme["checkbutton_fg"])])

        self.style.configure("TCombobox", fieldbackground=theme["entry_bg"], background=theme["entry_bg"], 
                           foreground="#000000" if theme["background"] == "#2d2d2d" else theme["foreground"])
        self.style.map("TCombobox", 
                      fieldbackground=[("readonly", theme["entry_bg"]), ("active", theme["entry_bg"]), ("disabled", theme["entry_bg"])],
                      background=[("readonly", theme["entry_bg"]), ("active", theme["entry_bg"]), ("disabled", theme["entry_bg"])],
                      foreground=[("readonly", "#000000" if theme["background"] == "#2d2d2d" else theme["foreground"]), 
                                 ("active", "#000000" if theme["background"] == "#2d2d2d" else theme["foreground"]), 
                                 ("disabled", "#000000" if theme["background"] == "#2d2d2d" else theme["foreground"])])

        self.result_text.configure(bg=theme["entry_bg"], fg=theme["foreground"], insertbackground=theme["foreground"])

        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style="TLabel" if widget.cget("style") != "Info.TLabel" else "Info.TLabel")
            elif isinstance(widget, ttk.Entry):
                widget.configure(style="TEntry")
            elif isinstance(widget, ttk.Button):
                widget.configure(style="Accent.TButton")
            elif isinstance(widget, ttk.Checkbutton):
                widget.configure(style="Custom.TCheckbutton")
            elif isinstance(widget, ttk.Combobox):
                widget.configure(style="TCombobox")
            elif isinstance(widget, ttk.Frame):
                widget.configure(style="Main.TFrame")
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, ttk.Label):
                        subwidget.configure(style="TLabel")
                    elif isinstance(subwidget, ttk.Entry):
                        subwidget.configure(style="TEntry")
                    elif isinstance(subwidget, ttk.Button):
                        subwidget.configure(style="Accent.TButton")
                    elif isinstance(subwidget, ttk.Checkbutton):
                        subwidget.configure(style="Custom.TCheckbutton")
                    elif isinstance(subwidget, ttk.Combobox):
                        subwidget.configure(style="TCombobox")
                    elif isinstance(subwidget, tk.Text):
                        subwidget.configure(bg=theme["entry_bg"], fg=theme["foreground"], insertbackground=theme["foreground"])

    def toggle_theme(self):
        theme = self.dark_theme if self.theme_var.get() == "Тёмная" else self.light_theme
        self.apply_theme(theme)

    def toggle_language(self):
        lang = "en" if self.language_var.get() == "English" else "ru"
        self.root.title(self.texts[lang]["title"])
        self.title_label.configure(text=self.texts[lang]["title"])
        self.select_folder_button.configure(text=self.texts[lang]["select_folder"])
        self.select_files_button.configure(text=self.texts[lang]["select_files"])
        self.folder_label.configure(text=self.texts[lang]["folder_label"])
        self.files_label.configure(text=self.texts[lang]["files_label"])
        self.chars_label.configure(text=self.texts[lang]["chars_label"])
        self.new_name_label.configure(text=self.texts[lang]["new_name_label"])
        self.remove_spaces_check.configure(text=self.texts[lang]["remove_spaces"])
        self.replace_spaces_check.configure(text=self.texts[lang]["replace_spaces"])
        self.theme_label.configure(text=self.texts[lang]["theme_label"])
        self.language_label.configure(text=self.texts[lang]["language_label"])
        self.rename_button.configure(text=self.texts[lang]["rename"])
        self.analyze_button.configure(text=self.texts[lang]["analyze"])
        self.select_all_check.configure(text=self.texts[lang]["select_all"])
        self.dev_label.configure(text="dev. by MIAO with AI")
        
        current_folder = self.folder_path.get()
        if current_folder in ["Не выбрана", "Not selected"]:
            self.folder_path.set(self.texts[lang]["no_folder"])

    def toggle_checkboxes(self, selected, other):
        if selected.get():
            other.set(False)

    def toggle_select_all(self):
        for ext in self.extension_vars:
            self.extension_vars[ext].set(self.select_all_var.get())

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.selected_files = []
            self.file_count.set("0")
            self.analysis_done = False
            self.clear_extensions()

    def select_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.selected_files = list(files)
            self.file_count.set(str(len(self.selected_files)))
            lang = "en" if self.language_var.get() == "English" else "ru"
            self.folder_path.set(self.texts[lang]["no_folder"])
            self.analysis_done = False
            self.clear_extensions()

    def clear_extensions(self):
        for widget in self.extensions_list_frame.winfo_children():
            widget.destroy()
        self.extension_vars.clear()
        self.select_all_var.set(False)
        self.select_all_check.configure(state="disabled")

    def analyze_extensions(self):
        lang = "en" if self.language_var.get() == "English" else "ru"
        if self.folder_path.get() == self.texts[lang]["no_folder"] and not self.selected_files:
            messagebox.showwarning(self.texts[lang]["error"], self.texts[lang]["no_selection"])
            return

        self.clear_extensions()

        extensions = set()
        if self.selected_files:
            for file_path in self.selected_files:
                ext = os.path.splitext(file_path)[1].lower()
                if ext:
                    extensions.add(ext)
        elif self.folder_path.get() != self.texts[lang]["no_folder"]:
            for file_name in os.listdir(self.folder_path.get()):
                file_path = os.path.join(self.folder_path.get(), file_name)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file_name)[1].lower()
                    if ext:
                        extensions.add(ext)

        for idx, ext in enumerate(sorted(extensions)):
            var = tk.BooleanVar(value=False)
            self.extension_vars[ext] = var
            row_frame = ttk.Frame(self.extensions_list_frame, style="Main.TFrame")
            row_frame.pack(fill="x", pady=2)
            ttk.Checkbutton(row_frame, variable=var, style="Custom.TCheckbutton").pack(side="left")
            ext_text = tk.Text(row_frame, height=1, width=10, state="normal")
            ext_text.insert("1.0", ext)
            ext_text.configure(state="disabled")
            ext_text.pack(side="left", padx=5)

        self.analysis_done = True
        self.select_all_check.configure(state="normal")

    def rename_files(self):
        lang = "en" if self.language_var.get() == "English" else "ru"
        if self.folder_path.get() == self.texts[lang]["no_folder"] and not self.selected_files:
            messagebox.showwarning(self.texts[lang]["error"], self.texts[lang]["no_selection"])
            return

        new_base_name = self.new_filename.get().strip()
        chars_to_remove = [entry.get().strip() for entry in self.char_entries if entry.get().strip()]
        
        selected_extensions = {ext for ext, var in self.extension_vars.items() if var.get()} if self.analysis_done else set()

        result = ""
        counter = 1
        try:
            if self.selected_files:
                for file_path in self.selected_files:
                    ext = os.path.splitext(file_path)[1].lower()
                    if self.analysis_done and selected_extensions and ext not in selected_extensions:
                        continue
                    dir_name, file_name = os.path.split(file_path)
                    base_name = file_name
                    for char in chars_to_remove:
                        base_name = base_name.replace(char, "")
                    if self.remove_spaces.get():
                        base_name = base_name.replace(" ", "")
                    elif self.replace_spaces.get():
                        base_name = base_name.replace(" ", "_")
                    new_name = base_name if not new_base_name else f"{new_base_name}{counter}"
                    counter += 1 if new_base_name else 0
                    new_full_name = new_name + os.path.splitext(file_name)[1]
                    new_path = os.path.join(dir_name, new_full_name)
                    if os.path.exists(new_path):
                        response = messagebox.askyesno(self.texts[lang]["error"], self.texts[lang]["file_exists"],
                                                     default="no", parent=self.root)
                        if response:
                            os.remove(new_path)
                            os.rename(file_path, new_path)
                        else:
                            new_full_name = f"{new_name}(same)" + os.path.splitext(file_name)[1]
                            new_path = os.path.join(dir_name, new_full_name)
                            os.rename(file_path, new_path)
                    else:
                        os.rename(file_path, new_path)
                    result += f"Файл {file_name} переименован в {new_full_name}\n" if lang == "ru" else f"File {file_name} renamed to {new_full_name}\n"
            elif self.folder_path.get() != self.texts[lang]["no_folder"]:
                files = [f for f in os.listdir(self.folder_path.get()) if os.path.isfile(os.path.join(self.folder_path.get(), f))]
                for file_name in files:
                    file_path = os.path.join(self.folder_path.get(), file_name)
                    ext = os.path.splitext(file_name)[1].lower()
                    if self.analysis_done and selected_extensions and ext not in selected_extensions:
                        continue
                    base_name = file_name
                    for char in chars_to_remove:
                        base_name = base_name.replace(char, "")
                    if self.remove_spaces.get():
                        base_name = base_name.replace(" ", "")
                    elif self.replace_spaces.get():
                        base_name = base_name.replace(" ", "_")
                    new_name = base_name if not new_base_name else f"{new_base_name}{counter}"
                    counter += 1 if new_base_name else 0
                    new_full_name = new_name + os.path.splitext(file_name)[1]
                    new_path = os.path.join(self.folder_path.get(), new_full_name)
                    if os.path.exists(new_path):
                        response = messagebox.askyesno(self.texts[lang]["error"], self.texts[lang]["file_exists"],
                                                     default="no", parent=self.root)
                        if response:
                            os.remove(new_path)
                            os.rename(file_path, new_path)
                        else:
                            new_full_name = f"{new_name}(same)" + os.path.splitext(file_name)[1]
                            new_path = os.path.join(dir_name, new_full_name)
                            os.rename(file_path, new_path)
                    else:
                        os.rename(file_path, new_path)
                    result += f"Файл {file_name} переименован в {new_full_name}\n" if lang == "ru" else f"File {file_name} renamed to {new_full_name}\n"

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