"""One-click desktop control panel for the local content pipeline."""
from __future__ import annotations

import json
import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "settings.json"


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AutoViral Content Studio")
        self.geometry("820x560")
        self.minsize(700, 450)
        self.events: queue.Queue[str] = queue.Queue()
        self._build()
        self.after(200, self._drain_events)

    def _build(self) -> None:
        ttk.Label(self, text="AutoViral Content Studio", font=("Segoe UI", 20, "bold")).pack(pady=(18, 4))
        ttk.Label(self, text="Lokale workflow: ideeën → drafts → beoordeling → upload", font=("Segoe UI", 10)).pack()

        form = ttk.LabelFrame(self, text="Workflow")
        form.pack(fill="x", padx=20, pady=18)
        self.niche = tk.StringVar(value="tech")
        self.amount = tk.IntVar(value=3)
        ttk.Label(form, text="Niche:").grid(row=0, column=0, padx=10, pady=12, sticky="w")
        ttk.Entry(form, textvariable=self.niche, width=25).grid(row=0, column=1, padx=10, pady=12)
        ttk.Label(form, text="Aantal drafts:").grid(row=0, column=2, padx=10, pady=12, sticky="w")
        ttk.Spinbox(form, from_=1, to=20, textvariable=self.amount, width=8).grid(row=0, column=3, padx=10, pady=12)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=20)
        ttk.Button(buttons, text="1. Ideeën verzamelen", command=self.run_discovery).pack(side="left", padx=4)
        ttk.Button(buttons, text="2. Drafts maken", command=self.run_drafts).pack(side="left", padx=4)
        ttk.Button(buttons, text="Open output", command=lambda: self._open_path(ROOT / "output")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Browser-login instellen", command=self.run_login).pack(side="right", padx=4)

        self.log = tk.Text(self, height=20, state="disabled", bg="#111827", fg="#e5e7eb", insertbackground="white")
        self.log.pack(fill="both", expand=True, padx=20, pady=18)
        self._write("Klaar. Controleer drafts altijd voordat je publiceert.")

    def _write(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _drain_events(self) -> None:
        while not self.events.empty():
            self._write(self.events.get_nowait())
        self.after(200, self._drain_events)

    def _worker(self, command: list[str]) -> None:
        try:
            process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            assert process.stdout is not None
            for line in process.stdout:
                self.events.put(line.rstrip())
            code = process.wait()
            self.events.put(f"Proces beëindigd met code {code}.")
        except Exception as exc:
            self.events.put(f"Fout: {exc}")

    def _start(self, module: str, *args: str) -> None:
        threading.Thread(target=self._worker, args=([sys.executable, "-m", module, *args],), daemon=True).start()

    def run_discovery(self) -> None:
        self._start("app.pipeline", "discover", "--niche", self.niche.get(), "--limit", str(self.amount.get()))

    def run_drafts(self) -> None:
        self._start("app.pipeline", "drafts", "--niche", self.niche.get(), "--limit", str(self.amount.get()))

    def run_login(self) -> None:
        platform = messagebox.askquestion("Platform", "TikTok openen? Kies Nee voor YouTube.")
        self._start("app.uploader", "login", "--platform", "tiktok" if platform == "yes" else "youtube")

    @staticmethod
    def _open_path(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            subprocess.Popen(["explorer", str(path)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])


if __name__ == "__main__":
    App().mainloop()
