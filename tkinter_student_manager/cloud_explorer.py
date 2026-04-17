import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import random
import datetime

class CloudStorageMock:
    """Mock backend to simulate a cloud file system like Google Cloud Storage."""
    def __init__(self):
        self.file_system = {
            "Buckets": {
                "production-assets": {
                    "images": {
                        "logo.png": {"size": "45 KB", "type": "Image", "modified": "2026-04-15 10:23"},
                        "banner.jpg": {"size": "1.2 MB", "type": "Image", "modified": "2026-04-10 14:00"},
                    },
                    "css": {
                        "main.css": {"size": "12 KB", "type": "Stylesheet", "modified": "2026-04-16 09:12"},
                    },
                    "index.html": {"size": "5 KB", "type": "HTML Document", "modified": "2026-04-16 11:45"}
                },
                "backup-bucket-vw": {
                    "db_dumps": {
                        "users_20260416.sql": {"size": "250 MB", "type": "SQL Dump", "modified": "2026-04-16 00:00"},
                        "sales_20260416.sql": {"size": "800 MB", "type": "SQL Dump", "modified": "2026-04-16 00:30"},
                    }
                },
                "personal-drive": {
                    "Documents": {
                        "Q1_Report.pdf": {"size": "2.4 MB", "type": "PDF", "modified": "2026-02-28 16:20"},
                        "ideas.txt": {"size": "1 KB", "type": "Text", "modified": "2026-04-17 08:00"},
                    },
                    "Downloads": {},
                    "temp_file.tmp": {"size": "0 B", "type": "Temporary File", "modified": "2026-04-17 12:00"}
                }
            }
        }

    def get_contents(self, path):
        """Navigate the mock dict based on a list of keys (path)."""
        if not path:
            return self.file_system["Buckets"]
        
        current = self.file_system["Buckets"]
        for p in path:
            if p in current:
                current = current[p]
            else:
                return {}
        return current


class CloudExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cloud Storage Explorer Pro")
        self.geometry("1100x700")
        self.minsize(800, 500)
        
        # Configure themes/styles
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        
        self.cloud = CloudStorageMock()
        self.current_path = []
        
        self.setup_menu()
        self.setup_toolbar()
        self.setup_main_layout()
        self.setup_statusbar()
        self.setup_context_menu()
        
        self.populate_sidebar("", self.cloud.file_system["Buckets"])
        self.refresh_file_view()

    def setup_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Folder...", command=self.create_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Upload File...", command=self.upload_file)
        file_menu.add_command(label="Download File...", command=self.download_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Rename...", command=self.rename_item)
        edit_menu.add_command(label="Delete", command=self.delete_item)

        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_file_view)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_toolbar(self):
        toolbar = ttk.Frame(self, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_up = ttk.Button(toolbar, text="⬆ Up", command=self.go_up)
        self.btn_up.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_refresh = ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_file_view)
        self.btn_refresh.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.btn_upload = ttk.Button(toolbar, text="☁ Upload", command=self.upload_file)
        self.btn_upload.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_download = ttk.Button(toolbar, text="⬇ Download", command=self.download_file)
        self.btn_download.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_new_folder = ttk.Button(toolbar, text="📁 New Folder", command=self.create_folder)
        self.btn_new_folder.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.btn_delete = ttk.Button(toolbar, text="🗑 Delete", command=self.delete_item)
        self.btn_delete.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Search Entry at the right
        self.search_var = tk.StringVar()
        self.entry_search = ttk.Entry(toolbar, textvariable=self.search_var, width=30)
        self.entry_search.pack(side=tk.RIGHT, padx=5, pady=2)
        ttk.Label(toolbar, text="Search:").pack(side=tk.RIGHT)
        self.entry_search.bind("<Return>", self.search_files)

    def setup_main_layout(self):
        # PanedWindow for resizable split between sidebar and main content
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Sidebar (Directory Tree) ---
        sidebar_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(sidebar_frame, weight=1)

        self.dir_tree = ttk.Treeview(sidebar_frame, selectmode="browse")
        self.dir_tree.heading("#0", text="Buckets & Folders", anchor=tk.W)
        self.dir_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        dir_scrollbar = ttk.Scrollbar(sidebar_frame, orient=tk.VERTICAL, command=self.dir_tree.yview)
        dir_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dir_tree.configure(yscrollcommand=dir_scrollbar.set)
        
        self.dir_tree.bind("<<TreeviewSelect>>", self.on_dir_select)

        # --- Main Content Area (Tabs for Files and Logs) ---
        self.notebook = ttk.Notebook(self.paned_window)
        self.paned_window.add(self.notebook, weight=4)

        # Tab 1: File List
        file_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_frame, text="File Explorer")

        columns = ("Name", "Size", "Type", "Last Modified")
        self.file_list = ttk.Treeview(file_frame, columns=columns, selectmode="extended")
        
        self.file_list.heading("#0", text="")
        self.file_list.column("#0", width=0, stretch=tk.NO) # Hide phantom column
        
        self.file_list.heading("Name", text="Name", anchor=tk.W)
        self.file_list.heading("Size", text="Size", anchor=tk.E)
        self.file_list.heading("Type", text="Type", anchor=tk.W)
        self.file_list.heading("Last Modified", text="Last Modified", anchor=tk.W)
        
        self.file_list.column("Name", width=250)
        self.file_list.column("Size", width=80, anchor=tk.E)
        self.file_list.column("Type", width=120)
        self.file_list.column("Last Modified", width=150)

        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        file_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_list.yview)
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list.configure(yscrollcommand=file_scrollbar.set)
        
        self.file_list.bind("<Double-1>", self.on_file_double_click)
        self.file_list.bind("<Button-3>", self.show_context_menu_event) # Right click

        # Tab 2: Transfer Logs
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Transfer Logs")
        
        self.log_listbox = tk.Listbox(log_frame, bg="black", fg="lightgreen", font=("Courier", 11))
        self.log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_listbox.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_listbox.configure(yscrollcommand=log_scrollbar.set)
        
        self.log("System initialized. Connected to CloudStorageMock.")

    def setup_statusbar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        statusbar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.on_file_double_click)
        self.context_menu.add_command(label="Download", command=self.download_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Rename...", command=self.rename_item)
        self.context_menu.add_command(label="Delete", command=self.delete_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Properties", command=self.show_properties)

    # --- Core Logic & Data Binding ---

    def populate_sidebar(self, parent_node, data_dict, path_so_far=None):
        if path_so_far is None:
            path_so_far = []
            
        for key, value in data_dict.items():
            if isinstance(value, dict) and "type" not in value.keys():
                # It's a folder/bucket
                current_path = path_so_far + [key]
                node_id = self.dir_tree.insert(parent_node, "end", text=f"📁 {key}", values=(current_path,))
                self.populate_sidebar(node_id, value, current_path)

    def refresh_file_view(self):
        # Clear current items
        for item in self.file_list.get_children():
            self.file_list.delete(item)
            
        contents = self.cloud.get_contents(self.current_path)
        
        if not isinstance(contents, dict):
            return
            
        # Separate folders and files for sorting
        folders = []
        files = []
        
        for name, data in contents.items():
            if isinstance(data, dict) and "type" not in data.keys():
                folders.append(name)
            elif isinstance(data, dict) and "type" in data.keys():
                files.append((name, data))
                
        folders.sort()
        files.sort(key=lambda x: x[0])
        
        for folder in folders:
            self.file_list.insert("", "end", values=(f"📁 {folder}", "-", "Folder", "-"), tags=("folder",))
            
        for name, data in files:
            self.file_list.insert("", "end", values=(f"📄 {name}", data["size"], data["type"], data["modified"]), tags=("file",))
            
        path_str = " / ".join(self.current_path) if self.current_path else "Root (Buckets)"
        self.status_var.set(f"Current Path: {path_str} | Items: {len(folders) + len(files)}")

    # --- Event Handlers ---

    def on_dir_select(self, event):
        selected = self.dir_tree.selection()
        if selected:
            item = self.dir_tree.item(selected[0])
            path = item["values"][0] if item["values"] else []
            # Tkinter parses string representations of lists sometimes if not careful,
            # but since we stored it as tuple in values, we evaluate it.
            if isinstance(path, str):
                path = eval(path) # Safe here as we control input
            self.current_path = path
            self.refresh_file_view()

    def go_up(self):
        if self.current_path:
            self.current_path.pop()
            self.refresh_file_view()

    def on_file_double_click(self, event=None):
        selected = self.file_list.selection()
        if not selected: return
        
        item_values = self.file_list.item(selected[0], "values")
        name = item_values[0][2:] # strip icon
        item_type = item_values[2]
        
        if item_type == "Folder":
            self.current_path.append(name)
            self.refresh_file_view()
        else:
            messagebox.showinfo("Preview", f"Previewing file:\n{name}\n\nType: {item_type}\nSize: {item_values[1]}")

    def show_context_menu_event(self, event):
        item = self.file_list.identify_row(event.y)
        if item:
            self.file_list.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def search_files(self, event=None):
        query = self.search_var.get().lower()
        if not query:
            self.refresh_file_view()
            return

        self.status_var.set(f"Searching for '{query}'...")
        # Simple client-side search in current view
        for item in self.file_list.get_children():
            values = self.file_list.item(item, "values")
            name = values[0][2:].lower()
            if query not in name:
                self.file_list.detach(item) # Temporarily hide
            
    # --- Toolbar Actions ---

    def upload_file(self):
        if not self.current_path:
            messagebox.showwarning("Warning", "Please navigate inside a bucket to upload.")
            return
            
        filepath = filedialog.askopenfilename(title="Select File to Upload to Cloud")
        if filepath:
            filename = filepath.split('/')[-1]
            contents = self.cloud.get_contents(self.current_path)
            
            # Simulate upload
            contents[filename] = {
                "size": f"{random.randint(1, 1000)} KB", 
                "type": "Unknown", 
                "modified": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.log(f"UPLOAD: Successfully uploaded {filename} to /{' / '.join(self.current_path)}")
            self.refresh_file_view()
            messagebox.showinfo("Upload Complete", f"{filename} has been uploaded to the cloud.")

    def download_file(self):
        selected = self.file_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a file to download.")
            return
            
        item_values = self.file_list.item(selected[0], "values")
        if item_values[2] == "Folder":
            messagebox.showwarning("Warning", "Folder downloads are not supported in this demo.")
            return
            
        filename = item_values[0][2:]
        save_path = filedialog.asksaveasfilename(initialfile=filename, title="Save File As")
        if save_path:
            self.log(f"DOWNLOAD: Downloaded {filename} to local machine.")
            messagebox.showinfo("Download Complete", f"{filename} saved successfully.")

    def create_folder(self):
        if not self.current_path:
            messagebox.showwarning("Warning", "Please navigate into a bucket first.")
            return
            
        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            contents = self.cloud.get_contents(self.current_path)
            if folder_name not in contents:
                contents[folder_name] = {}
                self.log(f"CREATE: Folder '{folder_name}' created in /{' / '.join(self.current_path)}.")
                self.refresh_file_view()

    def delete_item(self):
        selected = self.file_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to delete.")
            return

        item_values = self.file_list.item(selected[0], "values")
        name = item_values[0][2:]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}' from the cloud?")
        if confirm:
            contents = self.cloud.get_contents(self.current_path)
            if name in contents:
                del contents[name]
                self.log(f"DELETE: Removed '{name}' from /{' / '.join(self.current_path)}.")
                self.refresh_file_view()

    def rename_item(self):
        selected = self.file_list.selection()
        if not selected: return
        
        item_values = self.file_list.item(selected[0], "values")
        old_name = item_values[0][2:]
        
        new_name = simpledialog.askstring("Rename", f"Enter new name for '{old_name}':", initialvalue=old_name)
        if new_name and new_name != old_name:
            contents = self.cloud.get_contents(self.current_path)
            contents[new_name] = contents.pop(old_name)
            self.log(f"RENAME: '{old_name}' -> '{new_name}'")
            self.refresh_file_view()

    def show_properties(self):
        selected = self.file_list.selection()
        if not selected: return
        item_values = self.file_list.item(selected[0], "values")
        
        prop_win = tk.Toplevel(self)
        prop_win.title(f"Properties: {item_values[0][2:]}")
        prop_win.geometry("300x200")
        
        ttk.Label(prop_win, text=f"File Name: {item_values[0][2:]}", font=("Arial", 10, "bold")).pack(pady=10)
        ttk.Label(prop_win, text=f"Size: {item_values[1]}").pack()
        ttk.Label(prop_win, text=f"Type: {item_values[2]}").pack()
        ttk.Label(prop_win, text=f"Last Modified: {item_values[3]}").pack()
        
        ttk.Button(prop_win, text="Close", command=prop_win.destroy).pack(side=tk.BOTTOM, pady=10)

    def show_about(self):
        messagebox.showinfo("About", "Cloud Storage Explorer Pro\nA comprehensive Tkinter demonstration mimicking a cloud file manager.\n\nCreated with Python and Tkinter.")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_listbox.insert(tk.END, f"[{timestamp}] {message}")
        self.log_listbox.see(tk.END) # Auto-scroll


if __name__ == "__main__":
    app = CloudExplorerApp()
    app.mainloop()
