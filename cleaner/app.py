import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from pygments.styles.dracula import background

# Key folders to analyze
COMMON_PATHS = {
    'Documents': str(Path.home() / 'Documents'),
    'Applications': '/Applications',
    'Developer': str(Path.home() / 'Developer'),
    'System Data': [
        str(Path.home() / 'Library' / 'Caches'),
        str(Path.home() / 'Library' / 'Logs'),
        str(Path.home() / 'Library' / 'Application Support'),
        '/Library/Logs',
        '/Library/Caches',
        '/private/var/log',
        '/private/var/folders'
    ]
}

def get_total_size(paths):
    total = 0
    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        if not os.path.exists(path):
            continue
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, f))
                except Exception:
                    continue
    return total

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} P{suffix}"

def clean_selected(selected_items):
    for item in selected_items:
        if item == 'System Data':
            messagebox.showinfo("Notice", "System Data cannot be cleaned by this tool.")
            continue
        path = COMMON_PATHS.get(item)
        if path and os.path.exists(path):
            try:
                shutil.rmtree(path)
                os.makedirs(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clean {item}: {str(e)}")

class CleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MacBook Pro Cleaner")

        self._setup_styles()
        self._setup_widgets()

        self.label_list = list(COMMON_PATHS.keys())

    def _setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('aqua')
        style.configure('TButton',
                        font=('Segoe UI', 11),
                        padding=8,
                        foreground='white',
                        background='#0078D7',
                        borderwidth=0)
        style.map('TButton',
                  background=[('active', '#005A9E')])

    def _setup_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("size",), show='tree headings')
        self.tree.heading("#0", text="Folder / File")
        self.tree.heading("size", text="Size")
        self.tree.column("#0", width=260)
        self.tree.column("size", width=100, anchor='e')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.tree.bind("<<TreeviewOpen>>", self.on_expand)

        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.scan_btn = ttk.Button(self.root, text="Scan Storage", command=self.scan_storage)
        self.scan_btn.pack(pady=(0, 5))

        self.clean_btn = ttk.Button(self.root, text="Clean Selected", command=self.clean_selected_items)
        self.clean_btn.pack(pady=(0, 10))

    def scan_storage(self):
        self.scan_btn.config(state=tk.DISABLED)
        self.progress["maximum"] = len(self.label_list)
        self.progress["value"] = 0
        self.tree.delete(*self.tree.get_children())
        self._scan_next(0)

    def _scan_next(self, index):
        if index >= len(self.label_list):
            self.scan_btn.config(state=tk.NORMAL)
            return
        label = self.label_list[index]
        paths = COMMON_PATHS[label]
        size = get_total_size(paths)
        node = self.tree.insert('', 'end', iid=label, text=label, values=(sizeof_fmt(size),))
        self.tree.insert(node, 'end', text="Loading...", values=("...",))  # Lazy loading placeholder
        self.progress["value"] = index + 1
        self.root.after(100, lambda: self._scan_next(index + 1))

    def on_expand(self, event):
        node = self.tree.focus()
        children = self.tree.get_children(node)
        if children and self.tree.item(children[0], "text") == "Loading...":
            self.tree.delete(children[0])
            self.load_subitems(node)

    def load_subitems(self, parent_key):
        paths = COMMON_PATHS.get(parent_key)
        if not paths:
            # It's a subfolder, get its real path from the node's full path
            base_path = self.get_full_path(parent_key)
            if base_path:
                self.populate_folder(parent_key, base_path)
            return
        if isinstance(paths, str):
            paths = [paths]
        for path in paths:
            if os.path.exists(path):
                self.populate_folder(parent_key, path)

    def populate_folder(self, node, base_path):
        try:
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                display_name = f"[📁] {item}" if os.path.isdir(full_path) else item
                try:
                    size = get_total_size(full_path) if os.path.isdir(full_path) else os.path.getsize(full_path)
                    sub_id = self.tree.insert(node, 'end', text=display_name, values=(sizeof_fmt(size),))
                    if os.path.isdir(full_path):
                        self.tree.insert(sub_id, 'end', text="Loading...", values=("...",))  # Subfolder lazy load
                except Exception:
                    continue
        except Exception:
            pass

    def get_full_path(self, node_id):
        names = []
        current = node_id
        while current:
            name = self.tree.item(current)["text"]
            name = name.replace("[📁] ", "")
            names.insert(0, name)
            current = self.tree.parent(current)
        # Try to resolve to an actual full path from the root folders
        for label, path in COMMON_PATHS.items():
            if names[0] == label:
                base = path if isinstance(path, str) else path[0]
                return os.path.join(base, *names[1:])
        return None

    def clean_selected_items(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "No item selected to clean.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clean the selected items?")
        if confirm:
            clean_selected(selected)
            self.scan_storage()
            messagebox.showinfo("Success", "Selected items cleaned successfully.")

def main():
    root = tk.Tk()
    app = CleanerApp(root)
    root.geometry("900x700") # Set desired screen size here
    center_window(root, 800, 600)
    root.mainloop()

def center_window(window, width=800, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
