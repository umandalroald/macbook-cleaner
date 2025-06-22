import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

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

# Recursively calculate folder sizes
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

# Convert bytes to human-readable format
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} P{suffix}"

# Safely delete selected directories
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

# Main GUI class
class CleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MacBook Pro Cleaner")

        self._setup_styles()
        self._setup_widgets()

        self.label_list = list(COMMON_PATHS.keys())

    def _setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TButton',
                        font=('Segoe UI', 11),
                        padding=8,
                        foreground='white',
                        background='#0078D7',
                        borderwidth=0)
        style.map('TButton',
                  background=[('active', '#005A9E')])

    def _setup_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("name", "size"), show='headings')
        self.tree.heading("name", text="Folder")
        self.tree.heading("size", text="Size")
        self.tree.column("name", width=200)
        self.tree.column("size", width=100, anchor='e')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

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
        self.tree.insert('', 'end', iid=label, values=(label, sizeof_fmt(size)))
        self.progress["value"] = index + 1
        self.root.after(100, lambda: self._scan_next(index + 1))

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

# Entrypoint for CLI and GUI
def main():
    root = tk.Tk()
    app = CleanerApp(root)
    root.geometry("400x500")
    root.mainloop()
