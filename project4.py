import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Назва CSV файлу
FILENAME = 'parking_lot.csv'

def show_cars():
    result_window = tk.Toplevel(root)
    result_window.title("Список автомобілів на стоянці")
    result_window.geometry("600x400")
    
    tree = ttk.Treeview(result_window)
    tree["columns"] = ("Номер авто", "Місце паркування", "Час заїзду", "Час виїзду")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Номер авто", anchor=tk.W, width=100)
    tree.column("Місце паркування", anchor=tk.W, width=100)
    tree.column("Час заїзду", anchor=tk.W, width=180)
    tree.column("Час виїзду", anchor=tk.W, width=180)
    
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Номер авто", text="Номер авто", anchor=tk.W)
    tree.heading("Місце паркування", text="Місце паркування", anchor=tk.W)
    tree.heading("Час заїзду", text="Час заїзду", anchor=tk.W)
    tree.heading("Час виїзду", text="Час виїзду", anchor=tk.W)
    
    tree.tag_configure('myfont', font=('Arial', 12))
    
    def load_data():
        for item in tree.get_children():
            tree.delete(item)
        try:
            with open(FILENAME, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    tree.insert("", tk.END, values=row, tags=('myfont',))
        except FileNotFoundError:
            pass
    
    load_data()
    tree.pack(expand=True, fill='both')
    
    def edit_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Помилка", "Виберіть запис для редагування")
            return
        
        edit_window = tk.Toplevel(root)
        edit_window.title("Редагувати автомобіль")
        edit_window.geometry("400x300")
        
        item_values = tree.item(selected_item)["values"]
        
        tk.Label(edit_window, text="Номер авто", font=("Arial", 14)).pack()
        entry_car_number = tk.Entry(edit_window, font=("Arial", 14))
        entry_car_number.pack()
        entry_car_number.insert(0, item_values[0])
        
        tk.Label(edit_window, text="Місце паркування", font=("Arial", 14)).pack()
        entry_parking_place = tk.Entry(edit_window, font=("Arial", 14))
        entry_parking_place.pack()
        entry_parking_place.insert(0, item_values[1])
        
        tk.Label(edit_window, text="Час заїзду", font=("Arial", 14)).pack()
        entry_arrival_time = tk.Entry(edit_window, font=("Arial", 14))
        entry_arrival_time.pack()
        entry_arrival_time.insert(0, item_values[2])
        
        tk.Label(edit_window, text="Час виїзду", font=("Arial", 14)).pack()
        entry_departure_time = tk.Entry(edit_window, font=("Arial", 14))
        entry_departure_time.pack()
        entry_departure_time.insert(0, item_values[3])
        
        def save_car():
            car_number = entry_car_number.get()
            parking_place = entry_parking_place.get()
            arrival_time = entry_arrival_time.get()
            departure_time = entry_departure_time.get()
            if not (car_number and parking_place and arrival_time and departure_time):
                messagebox.showerror("Помилка", "Всі поля повинні бути заповнені")
                return
            
            df = pd.read_csv(FILENAME, index_col='Номер авто')
            df = df.drop(car_number)
            df.to_csv(FILENAME, index=True)

            file_exists = os.path.isfile(FILENAME)
            try:
                with open(FILENAME, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        writer.writerow(["Номер авто", "Місце паркування", "Час заїзду", "Час виїзду"])
                    writer.writerow([car_number, parking_place, arrival_time, departure_time])
                messagebox.showinfo("Успіх", "Автомобіль оновлено")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Помилка", str(e)) 
        
        tk.Button(edit_window, text="Зберегти", command=save_car, height=2, font=("Arial", 12)).pack()
    
    tk.Button(result_window, text="Редагувати вибраний запис", command=edit_selected, height=2, font=("Arial", 12)).pack()

def add_car():
    def save_car():
        car_number = entry_car_number.get()
        parking_place = entry_parking_place.get()
        arrival_time = entry_arrival_time.get()
        departure_time = entry_departure_time.get()
        if not (car_number and parking_place and arrival_time and departure_time):
            messagebox.showerror("Помилка", "Всі поля повинні бути заповнені")
            return
        
        file_exists = os.path.isfile(FILENAME)
        try:
            with open(FILENAME, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["Номер авто", "Місце паркування", "Час заїзду", "Час виїзду"])
                writer.writerow([car_number, parking_place, arrival_time, departure_time])
            messagebox.showinfo("Успіх", "Автомобіль успішно додано")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
    
    add_window = tk.Toplevel(root)
    add_window.title("Додати автомобіль")
    add_window.geometry("400x300")
    
    tk.Label(add_window, text="Номер авто", font=("Arial", 14)).pack()
    entry_car_number = tk.Entry(add_window, font=("Arial", 14))
    entry_car_number.pack()
    
    tk.Label(add_window, text="Місце паркування", font=("Arial", 14)).pack()
    entry_parking_place = tk.Entry(add_window, font=("Arial", 14))
    entry_parking_place.pack()
    
    tk.Label(add_window, text="Час заїзду", font=("Arial", 14)).pack()
    entry_arrival_time = tk.Entry(add_window, font=("Arial", 14))
    entry_arrival_time.pack()
    
    tk.Label(add_window, text="Час виїзду", font=("Arial", 14)).pack()
    entry_departure_time = tk.Entry(add_window, font=("Arial", 14))
    entry_departure_time.pack()
    
    tk.Button(add_window, text="Зберегти", command=save_car, height=2, font=("Arial", 12)).pack()

def search_car():
    def perform_search():
        search_term = entry_search.get()
        if not search_term:
            messagebox.showerror("Помилка", "Поле пошуку не може бути порожнім")
            return
        try:
            with open(FILENAME, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                cars = [car for car in reader if search_term.lower() in car[0].lower()]
        except FileNotFoundError:
            cars = []
        
        result_window = tk.Toplevel(root)
        result_window.title("Результати пошуку")
        result_window.geometry("600x400")
        
        tree = ttk.Treeview(result_window)
        tree["columns"] = ("Номер авто", "Місце паркування", "Час заїзду", "Час виїзду")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Номер авто", anchor=tk.W, width=100)
        tree.column("Місце паркування", anchor=tk.W, width=100)
        tree.column("Час заїзду", anchor=tk.W, width=180)
        tree.column("Час виїзду", anchor=tk.W, width=180)
        
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Номер авто", text="Номер авто", anchor=tk.W)
        tree.heading("Місце паркування", text="Місце паркування", anchor=tk.W)
        tree.heading("Час заїзду", text="Час заїзду", anchor=tk.W)
        tree.heading("Час виїзду", text="Час виїзду", anchor=tk.W)
        
        for car in cars:
            tree.insert("", tk.END, values=car)
        
        tree.pack(expand=True, fill='both')
    
    search_window = tk.Toplevel(root)
    search_window.title("Пошук автомобіля")
    search_window.geometry("400x200")
    
    tk.Label(search_window, text="Введіть номер авто", font=("Arial", 14)).pack()
    entry_search = tk.Entry(search_window, font=("Arial", 14))
    entry_search.pack()
    tk.Button(search_window, text="Пошук", command=perform_search, height=2, font=("Arial", 12)).pack()

def analyze_data():
    try:
        df = pd.read_csv(FILENAME)
        plt.figure(figsize=(10, 5))
        
        plt.subplot(1, 2, 1)
        df['Час заїзду'] = pd.to_datetime(df['Час заїзду'])
        df['Час виїзду'] = pd.to_datetime(df['Час виїзду'])
        df['Тривалість стоянки (год)'] = (df['Час виїзду'] - df['Час заїзду']).dt.total_seconds() / 3600
        df['Тривалість стоянки (год)'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black')
        plt.title('Розподіл тривалості стоянки')
        plt.xlabel('Тривалість (години)')
        plt.ylabel('Кількість авто')
        
        plt.subplot(1, 2, 2)
        df['Місце паркування'].value_counts().plot(kind='bar', color='lightgreen', edgecolor='black')
        plt.title('Розподіл за місцем паркування')
        plt.xlabel('Місце паркування')
        plt.ylabel('Кількість авто')
        
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showerror("Помилка", "Файл з даними не знайдено")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

root = tk.Tk()
root.title("Інформаційно-пошукова система автостоянки")

tk.Button(root, text="Показати автомобілі", command=show_cars, height=2, font=("Arial", 12)).pack(fill='x')
tk.Button(root, text="Додати автомобіль", command=add_car, height=2, font=("Arial", 12)).pack(fill='x')
tk.Button(root, text="Знайти автомобіль", command=search_car, height=2, font=("Arial", 12)).pack(fill='x')
tk.Button(root, text="Аналіз даних", command=analyze_data, height=2, font=("Arial", 12)).pack(fill='x')

root.mainloop()
