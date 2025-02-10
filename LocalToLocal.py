import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import os
import shutil

def backup(source_folder, destination_folder):
    rsync_command = f"rsync -zvr '{source_folder}/' '{destination_folder}/'"
    os.system(rsync_command)
    status_label.config(text="Backup completed successfully.", foreground="green")

def select_source_folder():
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_folder)

def select_destination_folder():
    destination_folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_folder)

def perform_backup():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    if not os.path.exists(destination_folder):
        create_destination_folder(destination_folder)
    else:
        backup(source_folder, destination_folder)

def create_destination_folder(destination_folder):
    answer = messagebox.askyesno("Folder does not exist", "The destination folder does not exist. Do you want to create it?")
    if answer:
        location = simpledialog.askstring("Create Folder", "Enter the location where you want to create the folder (leave blank for current location):")
        if location:
            destination_folder = os.path.join(location, os.path.basename(destination_folder))
        os.makedirs(destination_folder)
        backup(source_entry.get(), destination_entry.get())

def create_folder_manually():
    location = filedialog.askdirectory()
    if location:
        folder_name = simpledialog.askstring("Create Folder", "Enter the folder name:")
        if folder_name:
            folder_path = os.path.join(location, folder_name)
            os.makedirs(folder_path)
            status_label.config(text="Folder created successfully.", foreground="green")

def delete_backup():
    destination_folder = destination_entry.get()
    shutil.rmtree(destination_folder)
    status_label.config(text="Backup folder deleted successfully.", foreground="green")

# Create main window
root = tk.Tk()
root.title("Local Backup Using rsync")

# Style
style = ttk.Style()
style.configure("TButton", padding=10, font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))

# Source folder selection
source_frame = ttk.Frame(root, padding="20")
source_frame.grid(row=0, column=0, sticky="ew")
ttk.Label(source_frame, text="Source Folder:").grid(row=0, column=0, sticky="w")
source_entry = ttk.Entry(source_frame, width=40)
source_entry.grid(row=1, column=0, sticky="ew")
source_button = ttk.Button(source_frame, text="Choose Directory", command=select_source_folder)
source_button.grid(row=1, column=1, padx=5, sticky="e")

# Destination folder selection
destination_frame = ttk.Frame(root, padding="20")
destination_frame.grid(row=1, column=0, sticky="ew")
ttk.Label(destination_frame, text="Destination Folder:").grid(row=0, column=0, sticky="w")
destination_entry = ttk.Entry(destination_frame, width=40)
destination_entry.grid(row=1, column=0, sticky="ew")
destination_button = ttk.Button(destination_frame, text="Choose Directory", command=select_destination_folder)
destination_button.grid(row=1, column=1, padx=5, sticky="e")

# Backup button
backup_button = ttk.Button(root, text="Perform Backup", command=perform_backup)
backup_button.grid(row=2, column=0, pady=10, sticky="ew")

# Create folder manually button
create_folder_button = ttk.Button(root, text="Create Folder", command=create_folder_manually)
create_folder_button.grid(row=3, column=0, pady=5, sticky="ew")

# Delete backup button
delete_button = ttk.Button(root, text="Delete Backup Folder", command=delete_backup)
delete_button.grid(row=4, column=0, pady=5, sticky="ew")

# Status label
status_label = ttk.Label(root, text="", foreground="green")
status_label.grid(row=5, column=0, pady=5, sticky="ew")

# Center the window
root.eval('tk::PlaceWindow . center')

root.mainloop()
