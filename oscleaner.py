#!/usr/bin/env python3
import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext

class OSCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OScleaner - Broken Launcher Cleaner")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", foreground="#ffffff", background="#2e2e2e", padding=6)
        self.style.configure("TLabel", foreground="#ffffff", background="#1e1e1e")
        self.style.configure("TFrame", background="#1e1e1e")

        ttk.Label(root, text="OScleaner", font=("Helvetica", 16)).pack(pady=10)

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg="#121212", fg="#00ff00", insertbackground="#ffffff")
        self.output.pack(fill="both", expand=True, padx=10)

        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(pady=10)

        ttk.Button(self.btn_frame, text="Scan", command=self.scan_broken_launchers).grid(row=0, column=0, padx=10)
        ttk.Button(self.btn_frame, text="Remove Selected", command=self.remove_broken).grid(row=0, column=1, padx=10)
        ttk.Button(self.btn_frame, text="Exit", command=root.quit).grid(row=0, column=2, padx=10)

        self.broken_files = []

    def scan_broken_launchers(self):
        self.output.delete(1.0, tk.END)
        self.broken_files.clear()

        search_dirs = ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]
        self.output.insert(tk.END, "[*] Scanning for broken .desktop launchers...\n")

        for directory in search_dirs:
            for root_dir, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".desktop"):
                        full_path = os.path.join(root_dir, file)
                        exec_cmd = self.extract_exec(full_path)
                        if exec_cmd and not shutil.which(exec_cmd.split()[0]):
                            self.output.insert(tk.END, f"[!] Missing: {exec_cmd} → {full_path}\n")
                            self.broken_files.append(full_path)

        if not self.broken_files:
            self.output.insert(tk.END, "[✓] No broken launchers found.\n")

    def extract_exec(self, desktop_file):
        try:
            with open(desktop_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Exec="):
                        return line.split("=", 1)[1].strip().split()[0]
        except Exception:
            return None
        return None

    def remove_broken(self):
        if not self.broken_files:
            messagebox.showinfo("OScleaner", "No broken launchers to remove.")
            return

        confirm = messagebox.askyesno("Confirm", f"Remove {len(self.broken_files)} broken launcher(s)?")
        if confirm:
            for path in self.broken_files:
                try:
                    os.remove(path)
                    self.output.insert(tk.END, f"[✓] Removed: {path}\n")
                except Exception as e:
                    self.output.insert(tk.END, f"[X] Failed to remove {path}: {e}\n")
            self.broken_files.clear()

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = OSCleanerApp(root)
    root.mainloop()
