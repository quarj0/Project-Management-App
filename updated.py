import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import dialog

class AddProjectDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        tk.Label(top, text="Project Name").pack()
        self.project_name_entry = tk.Entry(top)
        self.project_name_entry.pack()

        tk.Label(top, text="Due Date (mm/dd/yyyy)").pack()
        self.project_date_entry = tk.Entry(top)
        self.project_date_entry.pack()

        tk.Button(top, text="OK", command=self.ok).pack()

    def ok(self):
        self.project_name = self.project_name_entry.get()
        self.project_date = self.project_date_entry.get()
        self.top.destroy()

class EditProjectDialog:
    def __init__(self, master, name, date):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.title("Edit Project")

        # Create the project name entry widget
        self.project_name_label = tk.Label(self.top, text="Project Name:")
        self.project_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.project_name_entry = tk.Entry(self.top, width=30)
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.project_name_entry.insert(0, name)

        # Create the project due date entry widget
        self.project_date_label = tk.Label(self.top, text="Due Date (YYYY-MM-DD):")
        self.project_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.project_date_entry = tk.Entry(self.top, width=30)
        self.project_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.project_date_entry.insert(0, date)

        # Calculate progress based on start and due date
        self.start_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.ttk.Progressbar(self.top, orient="horizontal", length=200, mode="determinate", variable=self.progress_var)
        self.progress_bar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Set the progress bar value based on the difference between the start and due dates
        self.current_date = datetime.date.today()
        time_delta = self.start_date - self.current_date
        total_days = abs(time_delta.days)
        progress_days = total_days - (total_days // 3)
        progress_percent = progress_days / total_days * 100
        self.progress_var.set(progress_percent)

        # Create the buttons
        self.ok_button = tk.Button(self.top, text="OK", command=self.ok)
        self.ok_button.grid(row=3, column=0, padx=5, pady=5)
        self.cancel_button = tk.Button(self.top, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=3, column=1, padx=5, pady=5)

        # Set the focus to the project name entry widget
        self.project_name_entry.focus_set()

        # Initialize the project name and date
        self.project_name = None
        self.project_date = None

    def ok(self):
        # Get the project name and date
        self.project_name = self.project_name_entry.get()
        self.project_date


class AddProjectDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        tk.Label(top, text="Project Name").pack()
        self.project_name_entry = tk.Entry(top)
        self.project_name_entry.pack()

        tk.Label(top, text="Due Date (mm/dd/yyyy)").pack()
        self.project_date_entry = tk.Entry(top)
        self.project_date_entry.pack()

        tk.Button(top, text="OK", command=self.ok).pack()

    def ok(self):
        self.project_name = self.project_name_entry.get()
        self.project_date = self.project_date_entry.get()
        self.top.destroy()




class ProjectManager:
    def __init__(self, master):
        self.master = master
        master.title("Project Manager")

        # Create and set up the project list box
        self.projects_lb = tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
        self.projects_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.projects_lb.bind("<Double-Button-1>", self.edit_project)

        # Create the project data dictionary and load data if available
        self.projects = {}
        self.load_data()
        

        # Create and set up the project scroll bar
        self.projects_sb = tk.Scrollbar(master)
        self.projects_sb.pack(side=tk.LEFT, fill=tk.Y)
        self.projects_sb.config(command=self.projects_lb.yview)
        self.projects_lb.config(yscrollcommand=self.projects_sb.set)
        
        # Create and set up the project details frame
        self.details_frame = tk.Frame(master)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.details_frame.pack_propagate(0)
        self.details_frame.config(padx=10, pady=10)
        self.details_frame.config(bg="#ccc")
        
        
        # Create and set up the project control frame
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the project control buttons
        self.add_button = tk.Button(self.control_frame, text="Add Project", command=self.add_project)
        self.add_button.pack(side=tk.TOP, padx=10, pady=10)

        self.delete_button = tk.Button(self.control_frame, text="Delete Project", command=self.delete_project)
        self.delete_button.pack(side=tk.TOP, padx=10, pady=10)

        self.sort_label = tk.Label(self.control_frame, text="Sort by:")
        self.sort_label.pack(side=tk.TOP, padx=10, pady=5)

        self.sort_var = tk.StringVar(value="Name")
        self.sort_name_rb = tk.Radiobutton(self.control_frame, text="Name", variable=self.sort_var, value="Name", command=self.sort_projects)
        self.sort_name_rb.pack(side=tk.TOP, padx=10, pady=5)

        self.sort_date_rb = tk.Radiobutton(self.control_frame, text="Date", variable=self.sort_var, value="Date", command=self.sort_projects)
        self.sort_date_rb.pack(side=tk.TOP, padx=10, pady=5)
        
        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_data)
        self.save_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
    def add_project(self):
        # Create the add project dialog
        self.add_project_dialog = AddProjectDialog(self.master)
        self.master.wait_window(self.add_project_dialog.top)
            
        # Get the project name and date
        project_name = self.add_project_dialog.project_name
        project_date = self.add_project_dialog.project_date

        # Add the project to the project data dictionary
        self.project_data[project_name] = project_date

        # Add the project to the project list box
        self.projects_lb.insert(tk.END, project_name)
        self.save_data()
        self.load_data()
    
    def edit_project(self, event):
        # Get the selected project
        selected_index = self.projects_lb.curselection()[0]
        project_name = self.projects_lb.get(selected_index)

        # Create the edit project dialog
        dialog = EditProjectDialog(self.master, project_name, self.project_data[project_name])

        # Wait for the dialog to close
        self.master.wait_window(dialog.top)

        # Get the project name and date
        project_name = dialog.project_name
        project_date = dialog.project_date

        # Update the project data dictionary
        self.project_data[project_name] = project_date

        # Update the project list box
        self.projects_lb.delete(selected_index)
        self.projects_lb.insert(selected_index, project_name)
        self.projects_lb.selection_set(selected_index)
        
        self.save_data()
        self.load_data()
    
    def delete_project(self):
        # Get the selected project
        selected_index = self.projects_lb.curselection()[0]
        project_name = self.projects_lb.get(selected_index)

        # Delete the project from the project data dictionary
        del self.project_data[project_name]

        # Delete the project from the project list box
        self.projects_lb.delete(selected_index)
        self.save()
        self.load()
    
    def sort_projects(self):
        # Get the sort by value
        sort_by = self.sort_var.get()

        # Get the project names
        project_names = list(self.project_data.keys())

        # Sort the project names
        if sort_by == "Name":
            project_names.sort()
        else:
            project_names.sort(key=lambda project_name: self.project_data[project_name])

        # Clear the project list box
        self.projects_lb.delete(0, tk.END)

        # Add the project names to the project list box
        for project_name in project_names:
            self.projects_lb.insert(tk.END, project_name)
        
    def load_data(self):
        # Clear the project list box
        self.projects_lb.delete(0, tk.END)

        # Load the project data from the file
        if os.path.exists("project_data.json"):
            with open("project_data.json", "r") as f:
                self.project_data = json.load(f)

        # Add the project names to the project list box
        for project_name in self.project_data:
            self.projects_lb.insert(tk.END, project_name)
    
    def save_data(self):
        # Save the project data to the file
        with open("project_data.json", "w") as f:
            json.dump(self.project_data, f)
    
    def exit_app(self):
        exit_button = tk.Button(self.control_frame, text="Exit", command=exit_button)
        exit_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        exit_button.config(bg="#f00")
        self.master.destroy()
        self.master.quit()
        
            
root = tk.Tk()
my_gui = ProjectManager(root)
root.mainloop()