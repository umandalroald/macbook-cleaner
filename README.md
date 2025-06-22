
# 🧹 MacBook Cleaner

> A simple GUI-based cleaner for macOS built with Python and Tkinter.

MacBook Cleaner helps you analyze and manage your disk space by displaying folder and file sizes in an expandable tree view. It gives you insights into what’s consuming storage and allows you to safely clean non-critical folders like `Documents`, `Developer`, `Applications`, `System Data`.

---
**IMPORTANT NOTE:** THIS IS STILL IN ACTIVE DEVELOPMENT USE AT YOUR OWN RISK
## 📸 Demo

<img src="screenshot.png" alt="MacBook Cleaner UI" width="600">

> 📌 Expand folders to inspect subfiles/folders and sizes before cleaning!

---

## ✨ Features

- ✅ Clean, intuitive UI using Tkinter
- ✅ View top-level folders with real-time storage usage
- ✅ Expand folders to see files/subfolders and their sizes
- ✅ Clean up specific non-system directories with one click
- ✅ Progress bar while scanning
- ✅ System Data cleaning is enabled (WARNING: USE AT YOUR OWN RISK - NOT TESTED YET)

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Tkinter** (built-in GUI module)
- Styled with `ttk.Style` for a native macOS look and feel

---

## 📦 Installation Guide

### ✅ Prerequisites

- macOS Ventura or later
- Python 3.10 or higher  
- Homebrew (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/macbook-cleaner.git
cd macbook-cleaner
```

### 2. Create Virtual Environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> `requirements.txt` is minimal and may look like this:
> ```
> # Only needed if you add more deps
> ```

### 4. Run the App

```bash
python -m cleaner.app
```

If you’ve built and installed the app using `setuptools`, you can also run:

```bash
macbook-cleaner
```

---

## 🧪 Optional: Build and Install as CLI Tool

### 1. Build the Package

```bash
pip install build
python -m build
```

### 2. Install Locally

```bash
pip install dist/macbook_cleaner-*.whl
```

### 3. Run from Anywhere

```bash
macbook-cleaner
```

---

## 📁 Project Structure

```
macbook-cleaner/
├── cleaner/
│   ├── __init__.py
│   └── app.py          # Main app UI
├── README.md
├── setup.py            # Packaging config
├── requirements.txt
├── .gitignore
└── venv/               # Your virtual environment
```

---

## 🧹 How to Use

1. Launch the app with `python -m cleaner.app`
2. Click **Scan Storage** to analyze folders
3. Expand any folder to explore files and their sizes
4. Select folders and click **Clean Selected** to remove their contents  
   _(System Data is read-only for safety)_

---

## 🧯 Troubleshooting

### `ModuleNotFoundError: No module named '_tkinter'`

Tkinter may not be available by default on some macOS systems. Fix with:

```bash
brew install tcl-tk
export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
```

Then recompile Python with:

```bash
brew install python-tk
```

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to suggest improvements:

1. Fork the repo
2. Create a feature branch
3. Commit changes and open a PR

---

## 📄 License

MIT License. See [`LICENSE`](LICENSE) for details.

---

## 🔮 Roadmap

- [ ] File/folder size sorting
- [ ] Exclude hidden/system files
- [ ] Dark mode support
- [ ] Support for more macOS folders
- [ ] Right-click “Open in Finder” support

---

## 👨‍💻 Author

Built by [Roald Umandal](https://github.com/umandalroald)

Happy Cleaning! 🍏✨
