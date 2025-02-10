import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import subprocess
import os
import shutil

# Global counter to keep track of the file number for local-to-remote backup
file_counter = 1

def backup_local_to_local(source_folder, destination_folder):
    rsync_command = f"rsync -zvr '{source_folder}/' '{destination_folder}/'"
    os.system(rsync_command)
    status_label.config(text="Local backup completed successfully.", foreground="green")

def backup_local_to_remote(operation_type):
    global file_counter

    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    username = username_entry.get()
    ip_address = ip_entry.get()
    operation_option = operation_option_var.get()

    if not source_folder or not destination_folder or not username or not ip_address:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Construct rsync command based on operation type and selected options
    rsync_command = f"rsync -avzi"
    if operation_option == "progress":
        rsync_command += " --progress"
    elif operation_option == "existing":
        rsync_command += " --existing"
    elif operation_option == "delete":
        rsync_command += " --delete"

    include_name = include_name_entry.get()
    if operation_type == "export":
        if option_include_var.get() in ["include", "exclude"]:
            rsync_command += f" --{option_include_var.get()} '{include_name}'"

        rsync_command += f" '{source_folder}/' {username}@{ip_address}:~/'{destination_folder}/'"
    else:  # operation_type == "import"
        if option_include_var.get() in ["include", "exclude"]:
            rsync_command += f" --{option_include_var.get()} '{include_name}'"

        rsync_command += f" {username}@{ip_address}:~/'{destination_folder}/' '{source_folder}/'"

    try:
        # Capture the output of the rsync command
        rsync_output = subprocess.check_output(rsync_command, shell=True, stderr=subprocess.STDOUT)
        rsync_output = rsync_output.decode("utf-8")

        # Save the data log to a text file in the home directory
        log_filename = f"file{file_counter}.txt"
        home_directory = os.path.expanduser("~")
        log_filepath = os.path.join(home_directory, log_filename)
        with open(log_filepath, "w") as log_file:
            log_file.write(rsync_output)

        status_label.config(text="Remote backup completed successfully.", foreground="green")

        # Increment the file counter for the next run
        file_counter += 1
    except subprocess.CalledProcessError as e:
        status_label.config(text=f"Error: Remote backup operation failed - {e.output.decode('utf-8')}", foreground="red")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", foreground="red")

def select_source_folder():
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_folder)

def select_destination_folder():
    destination_folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_folder)

def perform_backup():
    backup_type = backup_type_var.get()
    if backup_type == "local":
        source_folder = source_entry.get()
        destination_folder = destination_entry.get()
        if not os.path.exists(destination_folder):
            create_destination_folder(destination_folder)
        else:
            backup_local_to_local(source_folder, destination_folder)
    elif backup_type == "remote":
        backup_local_to_remote(operation_var.get())

def create_destination_folder(destination_folder):
    answer = messagebox.askyesno("Folder does not exist", "The destination folder does not exist. Do you want to create it?")
    if answer:
        location = simpledialog.askstring("Create Folder", "Enter the location where you want to create the folder (leave blank for current location):")
        if location:
            destination_folder = os.path.join(location, os.path.basename(destination_folder))
        os.makedirs(destination_folder)
        backup_local_to_local(source_entry.get(), destination_entry.get())

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
root.title("Backup Utility")

# Style
style = ttk.Style()
style.configure("TButton", padding=10, font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))

# Backup type selection
backup_type_var = tk.StringVar()
backup_type_var.set("local")  # Default to local backup

backup_type_frame = ttk.Frame(root, padding="20")
backup_type_frame.grid(row=0, column=0, sticky="ew")
ttk.Label(backup_type_frame, text="Backup Type:").grid(row=0, column=0, sticky="w")
local_backup_radio = ttk.Radiobutton(backup_type_frame, text="Local Backup", variable=backup_type_var, value="local")
local_backup_radio.grid(row=0, column=1, padx=5, sticky="w")
remote_backup_radio = ttk.Radiobutton(backup_type_frame, text="Remote Backup", variable=backup_type_var, value="remote")
remote_backup_radio.grid(row=0, column=2, padx=5, sticky="w")

# Source folder selection
source_frame = ttk.Frame(root, padding="20")
source_frame.grid(row=1, column=0, sticky="ew")
ttk.Label(source_frame, text="Source Folder:").grid(row=0, column=0, sticky="w")
source_entry = ttk.Entry(source_frame, width=40)
source_entry.grid(row=1, column=0, sticky="ew")
source_button = ttk.Button(source_frame, text="Choose Directory", command=select_source_folder)
source_button.grid(row=1, column=1, padx=5, sticky="e")

# Destination folder selection
destination_frame = ttk.Frame(root, padding="20")
destination_frame.grid(row=2, column=0, sticky="ew")
ttk.Label(destination_frame, text="Destination Folder:").grid(row=0, column=0, sticky="w")
destination_entry = ttk.Entry(destination_frame, width=40)
destination_entry.grid(row=1, column=0, sticky="ew")
destination_button = ttk.Button(destination_frame, text="Choose Directory", command=select_destination_folder)
destination_button.grid(row=1, column=1, padx=5, sticky="e")

# Remote backup options
remote_options_frame = ttk.Frame(root, padding="20")
remote_options_frame.grid(row=3, column=0, sticky="ew")

# Username entry for remote backup
username_label = ttk.Label(remote_options_frame, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
username_entry = ttk.Entry(remote_options_frame, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# IP address entry for remote backup
ip_label = ttk.Label(remote_options_frame, text="IP Address:")
ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
ip_entry = ttk.Entry(remote_options_frame, width=30)
ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Operation selection for remote backup
operation_label = ttk.Label(remote_options_frame, text="Operation:")
operation_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
operation_var = tk.StringVar()
operation_export_radio = ttk.Radiobutton(remote_options_frame, text="Export", variable=operation_var, value="export")
operation_export_radio.grid(row=2, column=1, padx=10, pady=5, sticky="w")
operation_import_radio = ttk.Radiobutton(remote_options_frame, text="Import", variable=operation_var, value="import")
operation_import_radio.grid(row=2, column=1, padx=10, pady=5, sticky="e")
operation_var.set("export")  # Default to export operation

# Options for remote backup
operation_option_label = ttk.Label(remote_options_frame, text="Options:")
operation_option_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

operation_option_var = tk.StringVar()
operation_option_var.set("none")  # Default to no option selected

operation_none_radio = ttk.Radiobutton(remote_options_frame, text="None", variable=operation_option_var, value="none")
operation_none_radio.grid(row=4, column=0, padx=10, pady=5, sticky="w")
operation_progress_radio = ttk.Radiobutton(remote_options_frame, text="Progress", variable=operation_option_var, value="progress")
operation_progress_radio.grid(row=4, column=1, padx=10, pady=5, sticky="w")
operation_existing_radio = ttk.Radiobutton(remote_options_frame, text="Existing", variable=operation_option_var, value="existing")
operation_existing_radio.grid(row=4, column=2, padx=10, pady=5, sticky="w")
operation_delete_radio = ttk.Radiobutton(remote_options_frame, text="Delete", variable=operation_option_var, value="delete")
operation_delete_radio.grid(row=5, column=0, padx=10, pady=5, sticky="w")

# Options for include/exclude for remote backup
option_include_label = ttk.Label(remote_options_frame, text="Include/Exclude:")
option_include_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

option_include_var = tk.StringVar()
option_include_var.set("none")  # Default to no option selected

option_none_radio = ttk.Radiobutton(remote_options_frame, text="None", variable=option_include_var, value="none")
option_none_radio.grid(row=7, column=0, padx=10, pady=5, sticky="w")
option_include_radio = ttk.Radiobutton(remote_options_frame, text="Include", variable=option_include_var, value="include")
option_include_radio.grid(row=7, column=1, padx=10, pady=5, sticky="w")
option_exclude_radio = ttk.Radiobutton(remote_options_frame, text="Exclude", variable=option_include_var, value="exclude")
option_exclude_radio.grid(row=7, column=2, padx=10, pady=5, sticky="w")

# Entry fields for include/exclude name for remote backup
include_name_label = ttk.Label(remote_options_frame, text="Include/Exclude Name:")
include_name_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
include_name_entry = ttk.Entry(remote_options_frame, width=20)
include_name_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

# Backup button
backup_button = ttk.Button(root, text="Perform Backup", command=perform_backup)
backup_button.grid(row=4, column=0, pady=10, sticky="ew")

# Create folder manually button
create_folder_button = ttk.Button(root, text="Create Folder", command=create_folder_manually)
create_folder_button.grid(row=5, column=0, pady=5, sticky="ew")

# Delete backup button
delete_button = ttk.Button(root, text="Delete Backup Folder", command=delete_backup)
delete_button.grid(row=6, column=0, pady=5, sticky="ew")

# Status label
status_label = ttk.Label(root, text="", foreground="green")
status_label.grid(row=7, column=0, pady=5, sticky="ew")

# Center the window
root.eval('tk::PlaceWindow . center')

root.mainloop()
