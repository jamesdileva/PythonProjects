# news_tracker_gui.py
# News Tracker with GUI — Tkinter, Threading, and NewsAPI

import os
import json
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

BASE_URL = "https://newsapi.org/v2"
ENV_FILE = ".env"
CATEGORIES = ["general", "business", "entertainment",
              "health", "science", "sports", "technology"]

# ── API Layer ────────────────────────────────────────────────
def get_api_key():
    return os.environ.get("NEWS_API_KEY", "")

def fetch_headlines(category="general", api_key=None):
    params = {
        "apiKey": api_key or get_api_key(),
        "country": "us",
        "category": category,
        "pageSize": 20
    }
    response = requests.get(f"{BASE_URL}/top-headlines", params=params)
    return response.json()

def fetch_keyword(keyword, api_key=None):
    params = {
        "apiKey": api_key or get_api_key(),
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20
    }
    response = requests.get(f"{BASE_URL}/everything", params=params)
    return response.json()

def parse_articles(data):
    if data.get("status") != "ok":
        return None, data.get("message", "Unknown error")
    articles = data.get("articles", [])
    return articles, None

# ── Main Application ─────────────────────────────────────────
class NewsTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Tracker")
        self.root.geometry("1100x720")
        self.root.resizable(True, True)

        self.articles       = []
        self.saved_articles = []
        self.theme          = "light"
        self.marquee_active = False
        self.marquee_text   = ""
        self.marquee_pos    = 0
        self.auto_refresh   = False
        self.refresh_interval = 30
        self.refresh_after_id = None

        self.THEMES = {
            "light": {
                "bg": "#F0F0F0", "fg": "#1A1A1A",
                "toolbar_bg": "#2E75B6", "toolbar_fg": "white",
                "status_bg": "#E0E0E0", "status_fg": "#555555",
                "marquee_bg": "#1A1A1A", "marquee_fg": "#00FF88",
                "tree_bg": "white", "tree_fg": "#1A1A1A",
                "select_bg": "#2E75B6"
            },
            "dark": {
                "bg": "#1E1E1E", "fg": "#F0F0F0",
                "toolbar_bg": "#1A3A5C", "toolbar_fg": "white",
                "status_bg": "#2D2D2D", "status_fg": "#AAAAAA",
                "marquee_bg": "#0A0A0A", "marquee_fg": "#00FF88",
                "tree_bg": "#2D2D2D", "tree_fg": "#F0F0F0",
                "select_bg": "#1A3A5C"
            }
        }

        self._build_ui()
        self._check_api_key()

    # ── UI Construction ──────────────────────────────────────
    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self._build_toolbar()
        self._build_notebook()
        self._build_buttons()
        self._build_status_bar()
        self._build_marquee()

    def _build_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg="#2E75B6", pady=10)
        self.toolbar.grid(row=0, column=0, sticky="ew")
        self.toolbar.columnconfigure(3, weight=1)

        tk.Label(self.toolbar, text="Category:",
                 font=("Arial", 10, "bold"),
                 bg="#2E75B6", fg="white").grid(row=0, column=0, padx=(12,4))

        self.var_category = tk.StringVar(value="general")
        cat_menu = ttk.Combobox(self.toolbar,
                                textvariable=self.var_category,
                                values=CATEGORIES, state="readonly", width=14)
        cat_menu.grid(row=0, column=1, padx=(0,12))

        tk.Button(self.toolbar, text="🔍 Get Headlines",
                  command=self._fetch_headlines,
                  font=("Arial", 10, "bold"),
                  bg="#27AE60", fg="white",
                  padx=10, pady=3,
                  cursor="hand2").grid(row=0, column=2, padx=(0,16))

        tk.Label(self.toolbar, text="Search:",
                 font=("Arial", 10, "bold"),
                 bg="#2E75B6", fg="white").grid(row=0, column=4, padx=(0,4))

        self.var_search = tk.StringVar()
        search_entry = tk.Entry(self.toolbar,
                                textvariable=self.var_search, width=22,
                                font=("Arial", 10))
        search_entry.grid(row=0, column=5, padx=(0,6))
        search_entry.bind("<Return>", lambda e: self._fetch_keyword())

        tk.Button(self.toolbar, text="🔎 Search",
                  command=self._fetch_keyword,
                  font=("Arial", 10, "bold"),
                  bg="#8E44AD", fg="white",
                  padx=10, pady=3,
                  cursor="hand2").grid(row=0, column=6, padx=(0,12))

        tk.Button(self.toolbar, text="⚙ Settings",
                  command=self._show_settings,
                  font=("Arial", 10, "bold"),
                  bg="#555555", fg="white",
                  padx=10, pady=3,
                  cursor="hand2").grid(row=0, column=7, padx=(0,12))

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)

        self.tab_headlines = tk.Frame(self.notebook)
        self.tab_live      = tk.Frame(self.notebook)
        self.tab_saved     = tk.Frame(self.notebook)

        self.notebook.add(self.tab_headlines, text="  📰 Headlines  ")
        self.notebook.add(self.tab_live,      text="  🔴 Live Feed  ")
        self.notebook.add(self.tab_saved,     text="  🔖 Saved Articles  ")

        self._build_headlines_tab()
        self._build_live_tab()
        self._build_saved_tab()

    def _build_headlines_tab(self):
        self.tab_headlines.columnconfigure(0, weight=1)
        self.tab_headlines.rowconfigure(0, weight=1)

        cols = ("title", "source", "date")
        self.tree_headlines = ttk.Treeview(self.tab_headlines,
                                            columns=cols,
                                            show="headings", height=22)
        self.tree_headlines.heading("title",  text="Headline")
        self.tree_headlines.heading("source", text="Source")
        self.tree_headlines.heading("date",   text="Date")

        self.tree_headlines.column("title",  width=700, anchor="w")
        self.tree_headlines.column("source", width=160, anchor="center")
        self.tree_headlines.column("date",   width=100, anchor="center")

        sb = ttk.Scrollbar(self.tab_headlines, orient="vertical",
                           command=self.tree_headlines.yview)
        self.tree_headlines.configure(yscrollcommand=sb.set)
        self.tree_headlines.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self.tree_headlines.bind("<Double-1>", self._open_article)
        self.tree_headlines.bind("<Return>",   self._open_article)

        tk.Label(self.tab_headlines,
                 text="Double-click or press Enter to open article in browser",
                 font=("Arial", 9, "italic"),
                 fg="#888888").grid(row=1, column=0, pady=(4,2))

    def _build_live_tab(self):
        self.tab_live.columnconfigure(0, weight=1)
        self.tab_live.rowconfigure(1, weight=1)

        ctrl_frame = tk.Frame(self.tab_live, pady=8)
        ctrl_frame.grid(row=0, column=0, sticky="ew", padx=8)

        tk.Label(ctrl_frame, text="Refresh every:",
                 font=("Arial", 10)).pack(side="left", padx=(0,6))

        self.var_interval = tk.StringVar(value="30 minutes")
        interval_menu = ttk.Combobox(ctrl_frame,
                                      textvariable=self.var_interval,
                                      values=["15 minutes",
                                              "30 minutes",
                                              "60 minutes"],
                                      state="readonly", width=12)
        interval_menu.pack(side="left", padx=(0,12))

        self.btn_live = tk.Button(ctrl_frame, text="▶ Start Live Feed",
                                   command=self._toggle_live_feed,
                                   font=("Arial", 10, "bold"),
                                   bg="#27AE60", fg="white",
                                   padx=10, pady=3, cursor="hand2")
        self.btn_live.pack(side="left", padx=(0,12))

        self.lbl_next = tk.Label(ctrl_frame, text="",
                                  font=("Arial", 9, "italic"), fg="#888888")
        self.lbl_next.pack(side="left")

        cols = ("title", "source", "date")
        self.tree_live = ttk.Treeview(self.tab_live, columns=cols,
                                       show="headings", height=20)
        self.tree_live.heading("title",  text="Headline")
        self.tree_live.heading("source", text="Source")
        self.tree_live.heading("date",   text="Date")

        self.tree_live.column("title",  width=700, anchor="w")
        self.tree_live.column("source", width=160, anchor="center")
        self.tree_live.column("date",   width=100, anchor="center")

        sb2 = ttk.Scrollbar(self.tab_live, orient="vertical",
                             command=self.tree_live.yview)
        self.tree_live.configure(yscrollcommand=sb2.set)
        self.tree_live.grid(row=1, column=0, sticky="nsew")
        sb2.grid(row=1, column=1, sticky="ns")
        self.tree_live.bind("<Double-1>", self._open_live_article)

    def _build_saved_tab(self):
        self.tab_saved.columnconfigure(0, weight=1)
        self.tab_saved.rowconfigure(0, weight=1)

        cols = ("title", "source", "date")
        self.tree_saved = ttk.Treeview(self.tab_saved, columns=cols,
                                        show="headings", height=22)
        self.tree_saved.heading("title",  text="Headline")
        self.tree_saved.heading("source", text="Source")
        self.tree_saved.heading("date",   text="Date")

        self.tree_saved.column("title",  width=700, anchor="w")
        self.tree_saved.column("source", width=160, anchor="center")
        self.tree_saved.column("date",   width=100, anchor="center")

        sb3 = ttk.Scrollbar(self.tab_saved, orient="vertical",
                             command=self.tree_saved.yview)
        self.tree_saved.configure(yscrollcommand=sb3.set)
        self.tree_saved.grid(row=0, column=0, sticky="nsew")
        sb3.grid(row=0, column=1, sticky="ns")
        self.tree_saved.bind("<Double-1>", self._open_saved_article)

        tk.Label(self.tab_saved,
                 text="Double-click to open saved article in browser",
                 font=("Arial", 9, "italic"),
                 fg="#888888").grid(row=1, column=0, pady=(4,2))

    def _build_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=2, column=0, pady=(0,6))

        btn_style = {"font": ("Arial", 10, "bold"), "width": 18,
                     "pady": 5, "cursor": "hand2"}

        tk.Button(btn_frame, text="🔖 Save Selected",
                  command=self._save_article,
                  bg="#2E75B6", fg="white",
                  **btn_style).grid(row=0, column=0, padx=6)

        tk.Button(btn_frame, text="💾 Export Saved",
                  command=self._export_saved,
                  bg="#E67E22", fg="white",
                  **btn_style).grid(row=0, column=1, padx=6)

        tk.Button(btn_frame, text="🗑 Clear Saved",
                  command=self._clear_saved,
                  bg="#E74C3C", fg="white",
                  **btn_style).grid(row=0, column=2, padx=6)

        tk.Button(btn_frame, text="🌙 Dark Mode",
                  command=self._toggle_theme,
                  bg="#2C3E50", fg="white",
                  **btn_style).grid(row=0, column=3, padx=6)

    def _build_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg="#E0E0E0", pady=3)
        self.status_frame.grid(row=3, column=0, sticky="ew")
        self.status_frame.columnconfigure(0, weight=1)

        self.lbl_status = tk.Label(self.status_frame,
                                    text="Ready — enter a category or search term",
                                    font=("Arial", 9),
                                    bg="#E0E0E0", fg="#555555",
                                    anchor="w", padx=10)
        self.lbl_status.grid(row=0, column=0, sticky="w")

        self.btn_marquee = tk.Button(self.status_frame,
                                      text="🎬 Marquee: OFF",
                                      command=self._toggle_marquee,
                                      font=("Arial", 9, "bold"),
                                      bg="#2C3E50", fg="white",
                                      pady=1, padx=8, cursor="hand2",
                                      relief="flat")
        self.btn_marquee.grid(row=0, column=1, padx=8)

    def _build_marquee(self):
        self.marquee_frame = tk.Frame(self.root, bg="#1A1A1A", pady=4)
        self.marquee_label = tk.Label(self.marquee_frame,
                                       text="",
                                       font=("Courier New", 10, "bold"),
                                       bg="#1A1A1A", fg="#00FF88",
                                       anchor="w")
        self.marquee_label.pack(fill="x", padx=8)

    # ── Status Bar Helper ────────────────────────────────────
    def _set_status(self, message, color="#555555"):
        self.lbl_status.config(text=message, fg=color)
        self.root.update_idletasks()

    # ── API Key Check ────────────────────────────────────────
    def _check_api_key(self):
        if not get_api_key():
            self._show_settings(first_run=True)

    def _show_settings(self, first_run=False):
        win = tk.Toplevel(self.root)
        win.title("Settings — API Key")
        win.geometry("440x200")
        win.resizable(False, False)
        win.grab_set()

        msg = ("Welcome! Please enter your NewsAPI key to get started.\n"
               "Get a free key at newsapi.org") if first_run else \
              "Update your NewsAPI key below."

        tk.Label(win, text=msg, font=("Arial", 10),
                 wraplength=400, pady=12).pack()

        key_frame = tk.Frame(win)
        key_frame.pack(pady=4)

        tk.Label(key_frame, text="API Key:",
                 font=("Arial", 10, "bold")).grid(row=0, column=0,
                 padx=(0,8), sticky="w")

        var_key = tk.StringVar(value=get_api_key())
        entry = tk.Entry(key_frame, textvariable=var_key,
                         width=34, font=("Arial", 10), show="*")
        entry.grid(row=0, column=1)

        self.show_key = False
        def toggle_show():
            self.show_key = not self.show_key
            entry.config(show="" if self.show_key else "*")
            btn_show.config(text="🙈 Hide" if self.show_key else "👁 Show")

        btn_show = tk.Button(key_frame, text="👁 Show",
                              command=toggle_show,
                              font=("Arial", 9), pady=2)
        btn_show.grid(row=0, column=2, padx=(6,0))

        def save_key():
            key = var_key.get().strip()
            if not key:
                messagebox.showwarning("Missing Key",
                    "Please enter an API key.", parent=win)
                return
            os.environ["NEWS_API_KEY"] = key
            set_key(ENV_FILE, "NEWS_API_KEY", key)
            self._set_status("✓ API key saved", "#27AE60")
            win.destroy()

        tk.Button(win, text="Save API Key",
                  command=save_key,
                  font=("Arial", 10, "bold"),
                  bg="#27AE60", fg="white",
                  width=16, pady=5).pack(pady=14)

    # ── Fetching ─────────────────────────────────────────────
    def _fetch_headlines(self):
        if not get_api_key():
            self._show_settings(first_run=True)
            return
        category = self.var_category.get()
        self._set_status(f"Fetching {category} headlines...", "#E67E22")
        threading.Thread(target=self._fetch_headlines_thread,
                         args=(category,), daemon=True).start()

    def _fetch_headlines_thread(self, category):
        try:
            data = fetch_headlines(category)
            articles, error = parse_articles(data)
            self.root.after(0, self._on_headlines_loaded,
                            articles, error)
        except Exception as e:
            self.root.after(0, self._on_fetch_error, str(e))

    def _on_headlines_loaded(self, articles, error):
        if error:
            self._set_status(f"⚠ Error: {error}", "#E74C3C")
            return
        self.articles = articles
        self._populate_headlines(self.tree_headlines, articles)
        self._update_marquee_text(articles)
        timestamp = datetime.now().strftime("%I:%M %p")
        self._set_status(
            f"✓ {len(articles)} articles loaded — "
            f"Last updated: {timestamp}", "#27AE60")

    def _fetch_keyword(self):
        if not get_api_key():
            self._show_settings(first_run=True)
            return
        keyword = self.var_search.get().strip()
        if not keyword:
            messagebox.showwarning("Empty Search",
                "Please enter a keyword to search.")
            return
        self._set_status(f"Searching for '{keyword}'...", "#E67E22")
        threading.Thread(target=self._fetch_keyword_thread,
                         args=(keyword,), daemon=True).start()

    def _fetch_keyword_thread(self, keyword):
        try:
            data = fetch_keyword(keyword)
            articles, error = parse_articles(data)
            self.root.after(0, self._on_headlines_loaded,
                            articles, error)
        except Exception as e:
            self.root.after(0, self._on_fetch_error, str(e))

    def _on_fetch_error(self, message):
        self._set_status(f"⚠ Connection error: {message}", "#E74C3C")
        messagebox.showerror("Connection Error",
            f"Could not fetch news:\n{message}")

    # ── Populate Tables ──────────────────────────────────────
    def _populate_headlines(self, tree, articles):
        for row in tree.get_children():
            tree.delete(row)
        for article in articles:
            title   = article.get("title", "No title") or "No title"
            source  = article.get("source", {}).get("name", "Unknown")
            date    = article.get("publishedAt", "")[:10]
            tree.insert("", "end", values=(title, source, date))

    # ── Open in Browser ──────────────────────────────────────
    def _open_article(self, event=None):
        selected = self.tree_headlines.selection()
        if not selected:
            return
        index = self.tree_headlines.index(selected[0])
        if index < len(self.articles):
            url = self.articles[index].get("url", "")
            if url:
                self._set_status(f"Opening article in browser...",
                                  "#2E75B6")
                webbrowser.open(url)

    def _open_live_article(self, event=None):
        selected = self.tree_live.selection()
        if not selected:
            return
        index = self.tree_live.index(selected[0])
        if index < len(self.articles):
            url = self.articles[index].get("url", "")
            if url:
                webbrowser.open(url)

    def _open_saved_article(self, event=None):
        selected = self.tree_saved.selection()
        if not selected:
            return
        index = self.tree_saved.index(selected[0])
        if index < len(self.saved_articles):
            url = self.saved_articles[index].get("url", "")
            if url:
                webbrowser.open(url)

    # ── Save Articles ────────────────────────────────────────
    def _save_article(self):
        selected = self.tree_headlines.selection()
        if not selected:
            messagebox.showwarning("Nothing Selected",
                "Please select one or more articles to save.")
            return
        saved_count = 0
        for item in selected:
            index = self.tree_headlines.index(item)
            if index < len(self.articles):
                article = self.articles[index]
                if article not in self.saved_articles:
                    self.saved_articles.append(article)
                    saved_count += 1
        if saved_count > 0:
            self._populate_headlines(self.tree_saved, self.saved_articles)
            self._set_status(
                f"✓ {saved_count} article(s) saved — "
                f"{len(self.saved_articles)} saved total", "#27AE60")
        else:
            self._set_status("Selected articles already saved", "#E67E22")

    def _export_saved(self):
        if not self.saved_articles:
            messagebox.showinfo("No Saved Articles",
                "Save some articles first.")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Export Saved Articles"
        )
        if not filepath:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Saved Articles — {timestamp}\n")
            f.write("=" * 50 + "\n\n")
            for i, article in enumerate(self.saved_articles, 1):
                title  = article.get("title", "No title")
                source = article.get("source", {}).get("name", "Unknown")
                date   = article.get("publishedAt", "")[:10]
                url    = article.get("url", "")
                desc   = article.get("description", "") or ""
                f.write(f"{i}. {title}\n")
                f.write(f"   Source: {source} | Date: {date}\n")
                f.write(f"   {desc}\n")
                f.write(f"   URL: {url}\n\n")
        messagebox.showinfo("Exported",
            f"Saved articles exported to:\n{filepath}")
        self._set_status(f"✓ Articles exported to file", "#27AE60")

    def _clear_saved(self):
        if not self.saved_articles:
            return
        if messagebox.askyesno("Confirm",
                "Clear all saved articles?"):
            self.saved_articles = []
            for row in self.tree_saved.get_children():
                self.tree_saved.delete(row)
            self._set_status("Saved articles cleared", "#555555")

    # ── Live Feed ────────────────────────────────────────────
    def _toggle_live_feed(self):
        if self.auto_refresh:
            self.auto_refresh = False
            self.btn_live.config(text="▶ Start Live Feed",
                                  bg="#27AE60")
            if self.refresh_after_id:
                self.root.after_cancel(self.refresh_after_id)
            self.lbl_next.config(text="")
            self._set_status("Live feed stopped", "#555555")
        else:
            interval_str = self.var_interval.get()
            self.refresh_interval = int(interval_str.split()[0])
            self.auto_refresh = True
            self.btn_live.config(text="⏹ Stop Live Feed",
                                  bg="#E74C3C")
            self._set_status("Live feed started", "#27AE60")
            self._run_live_fetch()

    def _run_live_fetch(self):
        if not self.auto_refresh:
            return
        category = self.var_category.get()
        self._set_status("🔴 Live feed refreshing...", "#E74C3C")
        threading.Thread(target=self._live_fetch_thread,
                         args=(category,), daemon=True).start()

    def _live_fetch_thread(self, category):
        try:
            data = fetch_headlines(category)
            articles, error = parse_articles(data)
            self.root.after(0, self._on_live_loaded, articles, error)
        except Exception as e:
            self.root.after(0, self._on_fetch_error, str(e))

    def _on_live_loaded(self, articles, error):
        if error:
            self._set_status(f"⚠ Live feed error: {error}", "#E74C3C")
        else:
            self.articles = articles
            self._populate_headlines(self.tree_live, articles)
            self._update_marquee_text(articles)
            timestamp = datetime.now().strftime("%I:%M %p")
            next_time = f"Next refresh in {self.refresh_interval} min"
            self.lbl_next.config(text=f"Updated {timestamp} — {next_time}")
            self._set_status(
                f"🔴 Live — {len(articles)} articles — "
                f"Updated {timestamp}", "#E74C3C")

        if self.auto_refresh:
            ms = self.refresh_interval * 60 * 1000
            self.refresh_after_id = self.root.after(ms, self._run_live_fetch)

    # ── Marquee ──────────────────────────────────────────────
    def _toggle_marquee(self):
        if self.marquee_active:
            self.marquee_active = False
            self.btn_marquee.config(text="🎬 Marquee: OFF")
            if hasattr(self, "marquee_win") and self.marquee_win.winfo_exists():
                self.marquee_win.destroy()
        else:
            if not self.marquee_text:
                messagebox.showinfo("No Headlines",
                    "Fetch some headlines first then enable the marquee.")
                return
            self.marquee_active = True
            self.btn_marquee.config(text="🎬 Marquee: ON")
            self._open_marquee_window()
            self._scroll_marquee()

    def _update_marquee_text(self, articles):
        titles = [a.get("title", "") or "" for a in articles if a.get("title")]
        self.marquee_text = "    ●    ".join(titles) + "    ●    "
        self.marquee_pos  = 0

    def _scroll_marquee(self):
        if not self.marquee_active or not self.marquee_text:
            return
        if not hasattr(self, "marquee_win") or \
           not self.marquee_win.winfo_exists():
            self.marquee_active = False
            self.btn_marquee.config(text="🎬 Marquee: OFF")
            return
        try:
            win_width = self.marquee_win.winfo_width()
            char_width = 8
            display_width = max(60, win_width // char_width)
            text = self.marquee_text
            double = text + text
            snippet = double[self.marquee_pos:self.marquee_pos + display_width]
            self.marquee_label.config(text=snippet)
            self.marquee_pos = (self.marquee_pos + 1) % len(text)
        except tk.TclError:
            return
        self.root.after(150, self._scroll_marquee)

    def _open_marquee_window(self):
        self.marquee_win = tk.Toplevel(self.root)
        self.marquee_win.title("📰 News Ticker")
        self.marquee_win.geometry("900x50+100+100")
        self.marquee_win.resizable(True, False)
        self.marquee_win.attributes("-topmost", True)
        self.marquee_win.configure(bg="#1A1A1A")

        self.marquee_win.protocol("WM_DELETE_WINDOW", self._toggle_marquee)

        self.marquee_label = tk.Label(self.marquee_win,
                                       text="",
                                       font=("Courier New", 12, "bold"),
                                       bg="#1A1A1A", fg="#00FF88",
                                       anchor="w")
        self.marquee_label.pack(fill="both", expand=True, padx=8)

    # ── Dark Mode ────────────────────────────────────────────
    def _toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        t = self.THEMES[self.theme]
        self.root.configure(bg=t["bg"])
        self.toolbar.configure(bg=t["toolbar_bg"])
        self.status_frame.configure(bg=t["status_bg"])
        self.lbl_status.configure(bg=t["status_bg"], fg=t["status_fg"])
        self.marquee_frame.configure(bg=t["marquee_bg"])
        self.marquee_label.configure(bg=t["marquee_bg"],
                                      fg=t["marquee_fg"])
        self._apply_theme_recursive(self.root, t)

    def _apply_theme_recursive(self, widget, t):
        try:
            wc = widget.winfo_class()
            if wc in ("Frame", "Label"):
                widget.configure(bg=t["bg"], fg=t["fg"])
            elif wc == "Button":
                pass
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._apply_theme_recursive(child, t)

# ── Entry Point ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = NewsTrackerApp(root)
    root.mainloop()