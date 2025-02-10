import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import subprocess
import os

# Global counter to keep track of the file number
file_counter = 1

def perform_operation(operation_type):
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

        status_label.config(text="Operation completed successfully.", foreground="green")

        # Increment the file counter for the next run
        file_counter += 1
    except subprocess.CalledProcessError as e:
        status_label.config(text=f"Error: Operation failed - {e.output.decode('utf-8')}", foreground="red")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", foreground="red")

def select_source_folder():
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_folder)

def create_source_folder():
    folder_location = filedialog.askdirectory()
    if folder_location:
        folder_name = simpledialog.askstring("Create Folder", "Enter the name of the folder:")
        if folder_name:
            folder_path = os.path.join(folder_location, folder_name)
            os.makedirs(folder_path)
            status_label.config(text="Folder created successfully.", foreground="green")

# Create SSH connection
def create_ssh_connection():
    username = simpledialog.askstring("SSH Connection", "Enter username:")
    if not username:
        return
    ip_address = simpledialog.askstring("SSH Connection", "Enter IP address:")
    if not ip_address:
        return
    ssh_command = f"ssh {username}@{ip_address}"
    subprocess.Popen(ssh_command, shell=True)

# Create main window
root = tk.Tk()
root.title("Local to Remote Backup/Restore Using rsync")
root.geometry("600x550")
root.resizable(False, False)

# Frame to contain all widgets
frame = ttk.Frame(root, padding=10)
frame.pack(expand=True, fill='both')

# Username entry
username_label = ttk.Label(frame, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
username_entry = ttk.Entry(frame, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# IP address entry
ip_label = ttk.Label(frame, text="IP Address:")
ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
ip_entry = ttk.Entry(frame, width=30)
ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Source folder selection
source_label = ttk.Label(frame, text="Source Folder:")
source_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
source_entry = ttk.Entry(frame, width=40)
source_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
source_button = ttk.Button(frame, text="Choose Directory", command=select_source_folder)
source_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

# Destination folder entry
destination_label = ttk.Label(frame, text="Destination Folder:")
destination_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
destination_entry = ttk.Entry(frame, width=40)
destination_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Operation selection
operation_label = ttk.Label(frame, text="Operation:")
operation_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
operation_var = tk.StringVar()
operation_export_radio = ttk.Radiobutton(frame, text="Export", variable=operation_var, value="export")
operation_export_radio.grid(row=4, column=1, padx=10, pady=5, sticky="w")
operation_import_radio = ttk.Radiobutton(frame, text="Import", variable=operation_var, value="import")
operation_import_radio.grid(row=4, column=1, padx=10, pady=5, sticky="e")
operation_var.set("export")  # Default to export operation

# Options for operation
operation_option_label = ttk.Label(frame, text="Options:")
operation_option_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

operation_option_var = tk.StringVar()
operation_option_var.set("none")  # Default to no option selected

operation_none_radio = ttk.Radiobutton(frame, text="None", variable=operation_option_var, value="none")
operation_none_radio.grid(row=6, column=0, padx=10, pady=5, sticky="w")
operation_progress_radio = ttk.Radiobutton(frame, text="Progress", variable=operation_option_var, value="progress")
operation_progress_radio.grid(row=6, column=1, padx=10, pady=5, sticky="w")
operation_existing_radio = ttk.Radiobutton(frame, text="Existing", variable=operation_option_var, value="existing")
operation_existing_radio.grid(row=6, column=2, padx=10, pady=5, sticky="w")
operation_delete_radio = ttk.Radiobutton(frame, text="Delete", variable=operation_option_var, value="delete")
operation_delete_radio.grid(row=7, column=0, padx=10, pady=5, sticky="w")

# Options for include/exclude
option_include_label = ttk.Label(frame, text="Include/Exclude:")
option_include_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

option_include_var = tk.StringVar()
option_include_var.set("none")  # Default to no option selected

option_none_radio = ttk.Radiobutton(frame, text="None", variable=option_include_var, value="none")
option_none_radio.grid(row=9, column=0, padx=10, pady=5, sticky="w")
option_include_radio = ttk.Radiobutton(frame, text="Include", variable=option_include_var, value="include")
option_include_radio.grid(row=9, column=1, padx=10, pady=5, sticky="w")
option_exclude_radio = ttk.Radiobutton(frame, text="Exclude", variable=option_include_var, value="exclude")
option_exclude_radio.grid(row=9, column=2, padx=10, pady=5, sticky="w")

# Entry fields for include/exclude name
include_name_label = ttk.Label(frame, text="Include/Exclude Name:")
include_name_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
include_name_entry = ttk.Entry(frame, width=20)
include_name_entry.grid(row=10, column=1, padx=10, pady=5, sticky="w")

# Perform Operation button
operation_button = ttk.Button(frame, text="Perform Operation", command=lambda: perform_operation(operation_var.get()))
operation_button.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# DesCreation button
descreation_button = ttk.Button(frame, text="DesCreation", command=create_ssh_connection, width=15)
descreation_button.grid(row=12, column=0, padx=10, pady=10, sticky="ew")

# SouCreation button
soucreation_button = ttk.Button(frame, text="SouCreation", command=create_source_folder, width=15)
soucreation_button.grid(row=12, column=1, padx=10, pady=10, sticky="ew")

# Status label
status_label = ttk.Label(frame, text="", font=('Helvetica', 12))
status_label.grid(row=13, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# Center the window
root.eval('tk::PlaceWindow . center')

root.mainloop()
