import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests

# ------------------ CONFIGURACIÓN DE BASE DE DATOS ------------------
def crear_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT,
            password TEXT
        )
    ''')
    # Inserta un usuario demo si no existe
    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchall():
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ('admin', '1234'))
    conn.commit()
    conn.close()

# ------------------ VALIDAR LOGIN ------------------
def validar_login():
    usuario = entry_usuario.get()
    clave = entry_contraseña.get()

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (usuario, clave))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        ventana_login.destroy()
        mostrar_datos_api()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrecta")

# ------------------ DATOS DE API SI LOGIN ES CORRECTO ------------------
def mostrar_datos_api():
    ventana_datos = tk.Tk()
    ventana_datos.title("Rick and Morty - Personajes")
    ventana_datos.geometry("600x400")

    try:
        response = requests.get("https://rickandmortyapi.com/api/character")
        data = response.json()

        for i, personaje in enumerate(data['results'][:10]):  # Mostrar 10 personajes
            texto = f"{i+1}. {personaje['name']} - {personaje['status']} ({personaje['species']})"
            label = tk.Label(ventana_datos, text=texto, anchor="w")
            label.pack(fill="x", padx=10, pady=2)
    except Exception as e:
        tk.Label(ventana_datos, text="Error al obtener datos de la API").pack()

    ventana_datos.mainloop()

# ------------------ INTERFAZ LOGIN ------------------
crear_bd()

ventana_login = tk.Tk()
ventana_login.title("Login de Usuario")
ventana_login.geometry("300x200")

tk.Label(ventana_login, text="Usuario").pack(pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Contraseña").pack(pady=5)
entry_contraseña = tk.Entry(ventana_login, show="*")
entry_contraseña.pack()

tk.Button(ventana_login, text="Iniciar Sesión", command=validar_login).pack(pady=20)

ventana_login.mainloop()

# ------------------ para el usuario brayan , contraseña 1234------------------