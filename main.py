import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3 as sq
from datetime import datetime
from tkinter import ttk
import re

def login_success():
    try:
        # conn = sq.connect('users')
        # cursor = conn.cursor()
        # def parse_and_insert_logs(log_file):
        #     with open(log_file, 'r') as file:
        #         logs = file.readlines()
        #
        #     for log_line in logs:
        #         match = re.match(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) \d+ "(.*?)" "(.*?)"', log_line)
        #         if match:
        #             ip = match.group(1)
        #             timestamp_str = match.group(2)
        #             request = match.group(3)
        #             status_code = int(match.group(4))
        #
        #             request_parts = request.split()
        #             if len(request_parts) == 3:
        #                 method = request_parts[0]
        #                 path = request_parts[1]
        #             else:
        #                 method = ""
        #                 path = ""
        #
        #             try:
        #                 timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
        #             except ValueError:
        #                 timestamp = None
        #
        #             cursor.execute(f'INSERT INTO logs (timestamp, ip, method, status_code) VALUES ({timestamp}, {ip}, {method}, {status_code})')
        #
        #     conn.commit()
        #     conn.close()
        # parse_and_insert_logs("access_logs.log")

        log_window = ctk.CTkToplevel()
        log_window.geometry('900x600')
        log_window.resizable(False, False)
        log_window.configure(fg_color="white")

        table = ttk.Treeview(log_window)
        table['columns'] = ('column1', 'column2', 'column3', 'column4')
        table.heading('column1', text='Timestamp')
        table.heading('column2', text='IP')
        table.heading('column3', text='Method')
        table.heading('column4', text='Status_code')

        table.pack(pady=30)

        try:
            with sq.connect('users') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT timestamp, ip, method, status_code FROM logs')
                rows = cursor.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
        except sq.Error as e:
            print("Ошибка SQLite:", e)

        def sort_post():
            table.delete(*table.get_children())
            conn = sq.connect('users')
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT timestamp, ip, method, status_code FROM logs WHERE method='POST'")
                rows = cursor.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
            except sq.Error as e:
                print("Ошибка SQLite:", e)
            finally:
                cursor.close()
                conn.close()

        def sort_get():
            table.delete(*table.get_children())
            conn = sq.connect('users')
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT timestamp, ip, method, status_code FROM logs WHERE method='GET'")
                rows = cursor.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
            except sq.Error as e:
                print("Ошибка SQLite:", e)
            finally:
                cursor.close()
                conn.close()

        def sort_date():
            table.delete(*table.get_children())
            conn = sq.connect('users')
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT timestamp, ip, method, status_code FROM logs ORDER BY timestamp DESC")
                rows = cursor.fetchall()
                for row in rows:
                    table.insert('', 'end', values=row)
            except sq.Error as e:
                print("Ошибка SQLite:", e)
            finally:
                cursor.close()
                conn.close()

        btn_yes = ctk.CTkButton(master=log_window, text='POST SORT', command=sort_post)
        btn_yes.pack()
        btn_yes = ctk.CTkButton(master=log_window, text='GET SORT', command=sort_get)
        btn_yes.pack()
        btn_yes = ctk.CTkButton(master=log_window, text='DATE SORT', command=sort_date)
        btn_yes.pack()
        log_window.mainloop()

    except Exception as ex:
        messagebox.showerror("Ошибка", f"{str(ex)}")


# Функция логина
def login():
    try:
        connection = sq.connect("users")
        cursor = connection.cursor()

        login_input = entry_login.get()
        password_input = entry_password.get()

        if login_input == '' or password_input == '':
            messagebox.showerror('Ошибка', 'Заполните все поля!')
        else:
            cursor.execute(f'SELECT login, pass FROM auth WHERE login = "{login_input}"')
            result = cursor.fetchone()

            if result and result[1] == password_input:
                messagebox.showinfo('Успех', 'Успешная авторизация!')
                login_success()
            else:
                messagebox.showerror('Ошибка', 'Неверный логин или пароль!')

    except Exception as e:
        messagebox.showerror('Ошибка', str(e))


# Функция регистрации аккаунта
def registration():
    window = ctk.CTkToplevel(root)
    window.geometry("800x600")
    window.resizable(False, False)
    window.configure(fg_color="white")

    def reg():
        if entry_password_reg.get() == "" or entry_email_reg.get() == "" or entry_login_reg.get() == "":
            messagebox.showerror("Ошибки", "Вам требуется заполнить все поля")

        else:
            try:
                connect = sq.connect("users")
                connect.cursor().execute(f"insert into auth(login,pass,email)"
                                         f" values('{entry_login_reg.get()}','{entry_password_reg.get()}','{entry_email_reg.get()}')")
                connect.commit()
                connect.close()
                messagebox.showinfo('Успех', 'Аккаунт зарегистрирован')

                window.destroy()
            except:
                messagebox.showerror('Ошибка', 'Возникла непредвиденная ошибка')

    def clear_field():
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, 'end')


    frame = ctk.CTkFrame(master=window, width=600, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    entry_login_reg = ctk.CTkEntry(master=frame, width=220, placeholder_text='Логин', font=('Century Gothic', 16))
    entry_login_reg.place(relx=0.3, y=90)
    entry_login_reg.configure(fg_color="blue")

    entry_password_reg = ctk.CTkEntry(master=frame, width=220, placeholder_text='Пароль', font=('Century Gothic', 16))
    entry_password_reg.place(relx=0.3, y=140)
    entry_password_reg.configure(fg_color="blue")

    entry_email_reg = ctk.CTkEntry(master=frame, width=220, placeholder_text='Почта', font=('Century Gothic', 16))
    entry_email_reg.place(relx=0.3, y=190)
    entry_email_reg.configure(fg_color="blue")

    button_register = ctk.CTkButton(master=frame, text='Готово', width=150, corner_radius=6, command=reg)
    button_register.place(relx=0.70, rely=0.7)
    button_register.configure(fg_color="red")

    button_clear = ctk.CTkButton(master=frame, text='Сброс', width=150, corner_radius=6, command=clear_field)
    button_clear.place(relx=0.05, rely=0.7)
    button_clear.configure(fg_color="red")

    window.mainloop()


root = ctk.CTk()
root.geometry("600x600")
root.resizable(False, False)
root.configure(fg_color="white")

frame_log = ctk.CTkFrame(master=root, width=360, height=360)
frame_log.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

entry_login = ctk.CTkEntry(master=frame_log, width=220, placeholder_text='Логин', font=('Times New Romar', 16))
entry_login.place(x=50, y=110)
entry_login.configure(fg_color="blue")

entry_password = ctk.CTkEntry(master=frame_log, width=220, placeholder_text='Пароль', font=('Times New Romar', 16))
entry_password.place(x=50, y=160)
entry_password.configure(fg_color="blue")

button_title = ctk.CTkButton(master=frame_log, text='Регистрация', font=('Times New Romar', 12), command=registration)
button_title.place(x=50, y=210)
button_title.configure(fg_color="red")

button_login = ctk.CTkButton(master=frame_log, text='Войти', width=220, corner_radius=6, command=login)
button_login.place(x=50, y=260)
button_login.configure(fg_color="red")

root.mainloop()