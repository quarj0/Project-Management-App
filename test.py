from tkinter import *
from tkinter import messagebox
import sqlite3

# create database connection
conn = sqlite3.connect('address_book.db')

# create cursor
c = conn.cursor()

# create table
c.execute("""CREATE TABLE IF NOT EXISTS addresses (
            first_name text,
            last_name text,
            address text,
            city text,
            state text,
            zipcode text
            )""")

# function to insert record into database
def insert_record():
    # get input values from user
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    address = address_entry.get()
    city = city_entry.get()
    state = state_entry.get()
    zipcode = zipcode_entry.get()

    # insert values into database
    c.execute("INSERT INTO addresses VALUES (:first_name, :last_name, :address, :city, :state, :zipcode)",
            {'first_name': first_name, 'last_name': last_name, 'address': address, 'city': city, 'state': state, 'zipcode': zipcode})

    # commit changes
    conn.commit()

    # clear input fields
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    state_entry.delete(0, END)
    zipcode_entry.delete(0, END)

    # show success message
    messagebox.showinfo("Success", "Record added successfully!")

# function to search for record in database
def search_record():
    # get input values from user
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    # search for record in database
    c.execute("SELECT * FROM addresses WHERE first_name=:first_name AND last_name=:last_name",
            {'first_name': first_name, 'last_name': last_name})
    record = c.fetchone()

    # show record if found, otherwise show error message
    if record:
        address_entry.delete(0, END)
        address_entry.insert(0, record[2])
        city_entry.delete(0, END)
        city_entry.insert(0, record[3])
        state_entry.delete(0, END)
        state_entry.insert(0, record[4])
        zipcode_entry.delete(0, END)
        zipcode_entry.insert(0, record[5])
    else:
        messagebox.showerror("Error", "Record not found.")

# function to update record in database
def update_record():
    # get input values from user
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    address = address_entry.get()
    city = city_entry.get()
    state = state_entry.get()
    zipcode = zipcode_entry.get()

    # update record in database
    c.execute("""UPDATE addresses SET
                address = :address,
                city = :city,
                state = :state,
                zipcode = :zipcode
                WHERE first_name = :first_name AND last_name = :last_name""",
            {'first_name': first_name, 'last_name': last_name, 'address': address, 'city': city, 'state': state, 'zipcode': zipcode})

    # commit changes
    conn.commit()

    # clear input fields
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    state_entry.delete(0, END)
    zipcode_entry.delete(0, END)

    # show success message
    messagebox.showinfo("Success", "Record updated successfully")
