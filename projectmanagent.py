import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
import os

# Create a data frame to store project tasks
tasks_df =pd.read_csv('tasks.csv') if os.path.exists('tasks.csv') else pd.DataFrame(columns=['Task Name', 'Task Description', 'Start Date', 'End Date', 'Assigned To', 'Status'])

# Create a function to add new tasks to the data frame
def add_task():
    task_name = task_name_entry.get()
    task_description = task_description_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    assigned_to = assigned_to_entry.get()
    status = status_entry.get()
    new_task = pd.DataFrame([[task_name, task_description, start_date, end_date, assigned_to, status]],
                            columns=['Task Name', 'Task Description', 'Start Date', 'End Date', 'Assigned To', 'Status'])
    if task_name == '' or task_description == '' or start_date == '' or end_date == '' or assigned_to == '' or status == '':
        messagebox.showerror('Please fill all the fields to add task.')
        
    global tasks_df
    tasks_df = pd.concat([tasks_df, new_task], ignore_index=True)
    tasks_df.to_csv('tasks.csv', index=False) # save the tasks to a CSV file
    update_table()
    task_name_entry.delete(0, tk.END)
    task_description_entry.delete(0, tk.END)
    start_date_entry.delete(0, tk.END)
    end_date_entry.delete(0, tk.END)
    assigned_to_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

# Create a function to update the status of tasks
def update_status():
    selected_task = tasks_table.selection()
    if selected_task:
        task_index = int(selected_task[0])-1
        tasks_df.at[task_index, 'Status'] = status_entry.get()
        tasks_df.to_csv('tasks.csv', index=False) # save the tasks to a CSV file
        update_table()

# Create a function to update the tasks table
def update_table():
    tasks_table.delete(*tasks_table.get_children())
    for i, row in tasks_df.iterrows():
        tasks_table.insert("", tk.END, values=(i+1, row['Task Name'], row['Task Description'], row['Start Date'], row['End Date'], row['Assigned To'], row['Status']))
        delete_button = tk.Button(tasks_table, text='Delete', command=lambda i=i: delete_task(i))
        tasks_table.create_window(tasks_table.index(0, 0, root=delete_button, padx=2, pady=2))

def delete_task(index):
    global tasks_df
    tasks_df = tasks_df.drop(index=index)
    tasks_df.reset_index(drop=True, inplace=True)
    update_table()

# Create a GUI for the project management app
root = tk.Tk()
root.title("Project Management App")
root.configure(background="#ccc")


# Create input fields for new tasks
task_name_label = tk.Label(root, text="Task Name:")
task_name_entry = tk.Entry(root)
task_description_label = tk.Label(root, text="Task Description:")
task_description_entry = tk.Entry(root)
start_date_label = tk.Label(root, text="Start Date:")
start_date_entry = tk.Entry(root)
end_date_label = tk.Label(root, text="End Date:")
end_date_entry = tk.Entry(root)
assigned_to_label = tk.Label(root, text="Assigned To:")
assigned_to_entry = tk.Entry(root)
status_label = tk.Label(root, text="Status:")
status_entry = tk.Entry(root)

# Add a button to add new tasks
add_task_button = tk.Button(root, text="Add Task", command=add_task)

# Create a table to display project tasks
tasks_table = tk.ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=10,)
tasks_table.heading(1, text="ID")
tasks_table.heading(2, text="Task Name")
tasks_table.heading(3, text="Task Description")
tasks_table.heading(4, text="Start Date")
tasks_table.heading(5, text="End Date")
tasks_table.heading(6, text="Assigned To")
tasks_table.heading(7, text="Status")

# Add a button to update task status
update_status_button = tk.Button(root, text="Update Status", command=update_status)

# create a function to sort the data frame by the start date column
def sort_by_start_date():
    global tasks_df
    tasks_df = tasks_df.sort_values(by='Start Date')
    update_table()
    
# Add a button to sort the tasks by start date
sort_by_start_date_button = tk.Button(root, text="Sort by Start Date", command=sort_by_start_date)

# Create a chart to display project timeline
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlabel('Date')
ax.set_ylabel('Task Name')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# Add GUI elements to the window
task_name_label.grid(row=0,column=0)
task_name_entry.grid(row=0, column=1)
task_description_label.grid(row=1, column=0)
task_description_entry.grid(row=1, column=1)
start_date_label.grid(row=2, column=0)
start_date_entry.grid(row=2, column=1)
end_date_label.grid(row=3, column=0)
end_date_entry.grid(row=3, column=1)
assigned_to_label.grid(row=4, column=0)
assigned_to_entry.grid(row=4, column=1)
status_label.grid(row=5, column=0)
status_entry.grid(row=5, column=1)
add_task_button.grid(row=6, column=1)
tasks_table.grid(row=7, columnspan=2)
update_status_button.grid(row=8, column=1)
# delete_button.grid(row=8, column=2)
sort_by_start_date_button.grid(row=8, column=0)
canvas.get_tk_widget().grid(row=9, columnspan=2)


root.mainloop()