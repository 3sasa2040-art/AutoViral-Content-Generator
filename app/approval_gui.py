"""Simple approval window for the hybrid workflow."""
from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "queue.json"


class ApprovalWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AutoViral — Draft approval")
        self.geometry("1050x650")
        self.items: list[dict] = []
        self._build()
        self.load()

    def _build(self) -> None:
        ttk.Label(self, text="Controleer elke draft vóór publicatie", font=("Segoe UI", 16, "bold")).pack(pady=12)
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=16, pady=8)
        self.listbox = tk.Listbox(body, width=48, height=25)
        self.listbox.pack(side="left", fill="y", padx=(0, 12))
        self.listbox.bind("<<ListboxSelect>>", self.show)
        self.details = tk.Text(body, wrap="word", state="disabled")
        self.details.pack(side="right", fill="both", expand=True)
        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=16, pady=12)
        ttk.Button(buttons, text="Goedkeuren", command=lambda: self.set_status("approved")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Afwijzen", command=lambda: self.set_status("rejected")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Vernieuwen", command=self.load).pack(side="right", padx=4)

    def load(self) -> None:
        self.listbox.delete(0, tk.END)
        if QUEUE.exists():
            try:
                data = json.loads(QUEUE.read_text(encoding="utf-8"))
                self.items = data.get("pending", [])
            except (OSError, json.JSONDecodeError):
                self.items = []
        else:
            self.items = []
        for item in self.items:
            self.listbox.insert(tk.END, item.get("youtube_title", "Untitled")[:65])
        if self.items:
            self.listbox.selection_set(0)
            self.show()
        else:
            self.set_details("Geen pending drafts. Start eerst: python -m app.production generate --niche technology --count 3")

    def show(self, _event=None) -> None:
        selected = self.listbox.curselection()
        if selected:
            self.set_details(json.dumps(self.items[selected[0]], indent=2, ensure_ascii=False))

    def set_details(self, text: str) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, text)
        self.details.configure(state="disabled")

    def set_status(self, status: str) -> None:
        selected = self.listbox.curselection()
        if not selected or not QUEUE.exists():
            return
        data = json.loads(QUEUE.read_text(encoding="utf-8"))
        item = data.get("pending", []).pop(selected[0])
        data.setdefault(status, []).append(item)
        QUEUE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        self.load()
        messagebox.showinfo("Opgeslagen", f"Draft is {status}.")


if __name__ == "__main__":
    ApprovalWindow().mainloop()
