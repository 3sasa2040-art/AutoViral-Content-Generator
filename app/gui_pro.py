"""Human-reviewed dashboard for hybrid automation workflow."""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

ROOT = Path(__file__).resolve().parent.parent


class HybridDashboard(tk.Tk):
    """A lightweight desktop dashboard for review and scheduling."""

    def __init__(self) -> None:
        super().__init__()
        self.title("AutoViral Hybrid Studio")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self._build()

    def _build(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_tab, text="Generate & Review")

        top = ttk.Frame(self.generate_tab)
        top.pack(fill="x", padx=12, pady=12)

        ttk.Label(top, text="Niche:").grid(row=0, column=0, padx=(0, 8), sticky="w")
        self.niche_var = tk.StringVar(value="technology")
        ttk.Entry(top, textvariable=self.niche_var, width=25).grid(row=0, column=1, padx=(0, 12))

        ttk.Label(top, text="Count:").grid(row=0, column=2, padx=(0, 8), sticky="w")
        self.count_var = tk.IntVar(value=3)
        ttk.Spinbox(top, from_=1, to=10, textvariable=self.count_var, width=8).grid(row=0, column=3)

        ttk.Button(top, text="Generate Drafts", command=self.generate_drafts).grid(row=0, column=4, padx=(12, 0))

        self.log = scrolledtext.ScrolledText(self.generate_tab, bg="#0f172a", fg="#e2e8f0", insertbackground="white")
        self.log.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.log.insert("end", "Hybrid workflow ready. Generate drafts, then approve or reject before uploading.\n")

        self.schedule_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.schedule_tab, text="Schedule & Upload")

        ttk.Label(self.schedule_tab, text="Daily scheduling is configured manually for review before upload.", font=("Segoe UI", 12)).pack(padx=12, pady=16)
        ttk.Button(self.schedule_tab, text="Open Browser Login (YouTube)", command=lambda: self.run_module("app.youtube_uploader", "login")).pack(anchor="w", padx=12, pady=5)
        ttk.Button(self.schedule_tab, text="Open Browser Login (TikTok)", command=lambda: self.run_module("app.tiktok_uploader", "login")).pack(anchor="w", padx=12, pady=5)

        ttk.Button(self.schedule_tab, text="Create Batch + Drafts", command=self.generate_drafts).pack(anchor="w", padx=12, pady=20)

    def log_message(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def generate_drafts(self) -> None:
        try:
            self.log_message(f"Generating {self.count_var.get()} draft(s) for {self.niche_var.get()}...")
            subprocess.Popen([
                sys.executable,
                "-m",
                "app.full_pipeline",
                "--niche",
                self.niche_var.get(),
                "--count",
                str(self.count_var.get()),
            ], cwd=ROOT)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def run_module(self, module: str, *args: str) -> None:
        try:
            subprocess.Popen([sys.executable, "-m", module, *args], cwd=ROOT)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))


if __name__ == "__main__":
    HybridDashboard().mainloop()
