import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd

global tasks_df
tasks_df = pd.DataFrame(columns=['Task Name', 'Task Description', 'Task Deadline', 'Task Status'])

# Create the table
table_columns = ttk.Treeview(root, columns=['#', 'Task Name', 'Task Description', 'Task Deadline', 'Task Status'], show='headings', height=15)
table_columns.grid(row=1, column=0, padx=10, pady=10)

# Create the status filter dropdown
def filter_by_status(filtered_df=None):
    if filtered_df is None:
        filtered_df = tasks_df
    selected_status = status_var.get()
    if selected_status == 'All':
        return filtered_df
    else:
        return filtered_df[filtered_df['Task Status'] == selected_status]

# Define the load_tasks function
def load_tasks():
    try:
        with open('tasks.csv', 'r') as file:
            tasks_df = pd.read_csv(file)
            update_table(tasks_df)
            task_count_label.config(text=f'Task Count: {len(tasks_df)}')
            status_var.set('Tasks Loaded Successfully')
            return tasks_df
    except FileNotFoundError:
        tasks_df = pd.DataFrame(columns=['Task Name', 'Task Description', 'Task Deadline', 'Task Status'])
        return tasks_df

def save_tasks():
    try:
        tasks_df.to_csv('tasks.csv', index=False)
        status_var.set('Tasks Saved Successfully')
    except:
        messagebox.showerror('Error: Tasks could not be saved!')

def add_task():
    # Get the input field values
    task_name = task_name_entry.get()
    task_description = task_description_entry.get()
    task_deadline = task_deadline_entry.get()

    # Add the task to the DataFrame
    if task_name != '' and task_deadline != '':
        tasks_df.loc[len(tasks_df)] = [task_name, task_description, task_deadline, 'New']
        task_name_entry.delete(0, 'end')
        task_description_entry.delete(0, 'end')
        task_deadline_entry.delete(0, 'end')
        task_count_label.config(text=f'Task Count: {len(tasks_df)}')
        status_var.set('Task Added Successfully')
        update_table()
    else:
        messagebox.showerror('Error: Task Name and Deadline are required')

# Define the remove_task function
def remove_task():
    try:
        selected_rows = table_columns.selection()
        for row in selected_rows:
            tasks_df.drop(row, inplace=True)
        task_count_label.config(text=f'Task Count: {len(tasks_df)}')
        status_var.set('Task Removed Successfully')
        update_table()
    except IndexError:
        messagebox.showerror('Error: No task selected to remove')

def clear_tasks():
    tasks_df.drop(tasks_df.index, inplace=True)
    task_count_label.config(text=f'Task Count: {len(tasks_df)}')
    status_var.set('Tasks Cleared Successfully')
    update_table()

def clear_input_fields():
    task_name_entry.delete(0, 'end')
    task_deadline_entry.delete(0, 'end')

def update_task():
    # Get the current selection in the table_columns
    selection = table_columns.selection()
    if len(selection) == 0:
        return

    # Update the task status in the DataFrame
    selected_rows = table_columns.selection()
    for row in selected_rows:
        tasks_df.at[int(row), 'Task Status'] = status_var.get()

    # Update the table display
    update_table()

# Define the update_table function
def update_table(filtered_df=None):
    table_columns.delete(*table_columns.get_children())
    if filtered_df is None:
        filtered_df = tasks_df

    for i, (name, desc, deadline, status) in filtered_df.iterrows():
        table_columns.insert('', 'end', values=[i+1, name, desc, deadline, status])

    task_count_label.config(text=f'Task Count: {len(filtered_df)}')



    # Update the task count label
    update_task_count_label()
    
# Define the update_task_count_label function
def update_task_count_label():
        task_count = len(tasks_df.get_children())
        task_count_label.config(text=f"Total Tasks: {task_count}")
        task_count_label.pack(side="top", padx=10, pady=5)
        
        

def delete_task():
    # Get the current selection in the table_columns
    selection = tasks_df.selection()
    if len(selection) == 0:
        return

    # Delete the selected task from the DataFrame
    selected_rows = tasks_df.selection()
    for row in selected_rows:
        tasks_df.drop(row, inplace=True)

    # Update the table_columns display
    update_table()

# Define the update_table function
def update_table(tasks_df):
    global table_columns
    # Clear the current table_columns display
    table_columns.delete(*table_columns.get_children())

    # Filter the DataFrame based on the current status filter
    filtered_df = filter_by_status(tasks_df)

    # Add the tasks to the table_columns
    for i, row in filtered_df.iterrows():
        table_columns.insert('', 'end', values=(i, row['Task Name'], row['Task Description'], row['Task Deadline'], row['Task Status']))

    # Update the task count label
    tasks_df = load_tasks()
    update_table(tasks_df)
    task_count_label.config(text=f'Task Count: {len(tasks_df)}')
    status_var.set('Tasks Loaded Successfully')


def pick_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        global tasks_df
        tasks_df = pd.read_csv(file_path)
        update_table()

tasks_df = load_tasks()



# Create the main window
root = tk.Tk()
root.title("Task Manager")

# Create the task count label
task_count_label = tk.Label(root, text="Total Tasks: 0")
task_count_label.pack(side="top", padx=10, pady=5)

# Define the status options and variable
status_options = ['All', 'New', 'In Progress', 'Complete']
status_var = tk.StringVar(value='All')


# Create the input frame
input_frame = tk.Frame(root)
input_frame.pack(side="top", padx=10, pady=10)

# Create the task name input field
task_name_label = tk.Label(input_frame, text="Task Name")
task_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
task_name_entry = tk.Entry(input_frame)
task_name_entry.grid(row=0, column=1, padx=5, pady=5)

# Create the task description input field
task_description_label = tk.Label(input_frame, text="Task Description")
task_description_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
task_description_entry = tk.Entry(input_frame)
task_description_entry.grid(row=1, column=1, padx=5, pady=5)

# Create the task deadline input field
task_deadline_label = tk.Label(input_frame, text="Task Deadline")
task_deadline_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
task_deadline_entry = tk.Entry(input_frame)
task_deadline_entry.grid(row=1, column=1, padx=5, pady=5)

# Create the add task button
add_task_button = tk.Button(input_frame, text="Add Task", command=add_task)
add_task_button.grid(row=2, column=1, padx=5, pady=5)

# Create the table_columns frame
table_frame = tk.Frame(root)
table_frame.pack(side="top", padx=10, pady=10)

# Create the status filter frame
status_filter_frame = tk.Frame(root)
status_filter_frame.pack(side="top", padx=10, pady=10)

# Create the control buttons
control_frame = tk.Frame(root)
control_frame.pack(side="top", padx=10, pady=10)

# Create the status filter
status_filter_frame = tk.Frame(root)
status_filter_frame.pack(side="top", padx=10, pady=10)

# Add the button to add a task
add_task_button = tk.Button(control_frame, text="Add Task", command=add_task)
add_task_button.pack(side="right", padx=5)

# Add status filter label
status_filter_label = tk.Label(status_filter_frame, text="Status Filter:")
status_filter_label.pack(side="left")

# Status filter entry
status_filter_entry = tk.Entry(status_filter_frame)
status_filter_entry.pack(side="left" , padx=5)

# Add status filter button
status_filter_button = tk.Button(status_filter_frame, text="Filter", command=update_table)
status_filter_button.pack(side="left", padx=5)

# Add tasks table_columns
table_columns = ['Task ID', 'Task Name', 'Task Description',  "Task Deadline", "Task Status"]
tasks_df = ttk.Treeview(table_frame, columns=table_columns, show='headings',
                           selectmode='browse')
for col in table_columns:
    tasks_df.heading(col, text=col)
    tasks_df.pack(side="left")
    
#  Add the scroll bar
scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=tasks_df.yview)
scrollbar.pack(side="right", fill="y")
tasks_df.configure(yscrollcommand=scrollbar.set)

# Add button to update task status
update_status_button = tk.Button(control_frame, text="Update Status", command=update_task)
update_status_button.pack(side="bottom", pady=10)

# Add button to delete task
delete_task_button = tk.Button(control_frame, text="Delete Task", command=delete_task)
delete_task_button.pack(side="bottom", pady=10)
