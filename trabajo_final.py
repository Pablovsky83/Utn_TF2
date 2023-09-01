import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


def crear_tabla():
    conn = sqlite3.connect("BD_neumatron.db")
    c = conn.cursor()

    # Crear la tabla mediciones si no existe
    c.execute(
        """CREATE TABLE IF NOT EXISTS mediciones (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Muestra TEXT,
                    Especie TEXT,
                    Pplant REAL,
                    Pconfig REAL,
                    Pini REAL,
                    Pfin REAL
                )"""
    )

    conn.commit()
    conn.close()


def mostrar_registros():
    # Limpiar la tabla
    tabla.delete(*tabla.get_children())

    conn = sqlite3.connect("BD_neumatron.db")
    c = conn.cursor()

    # Obtener los registros de la tabla mediciones
    c.execute("SELECT * FROM mediciones")
    registros = c.fetchall()

    # Mostrar los registros en la tabla
    for registro in registros:
        tabla.insert("", "end", values=registro)

    conn.close()


def agregar_registro():
    def guardar_registro():
        muestra = entrada_muestra.get()
        especie = entrada_especie.get()
        pplant = entrada_pplant.get()
        pconfig = entrada_pconfig.get()
        pini = entrada_pini.get()
        pfin = entrada_pfin.get()

        # Validar que los campos no estén vacíos
        if muestra and especie and pplant and pconfig and pini and pfin:
            conn = sqlite3.connect("BD_neumatron.db")
            c = conn.cursor()

            # Insertar el nuevo registro en la tabla mediciones
            c.execute(
                "INSERT INTO mediciones (Muestra, Especie, Pplant, Pconfig, Pini, Pfin) VALUES (?, ?, ?, ?, ?, ?)",
                (muestra, especie, pplant, pconfig, pini, pfin),
            )

            conn.commit()
            conn.close()

            # Actualizar la tabla y cerrar la ventana de formulario
            mostrar_registros()
            ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Registro")

    etiqueta_muestra = ttk.Label(ventana_agregar, text="Muestra:")
    etiqueta_muestra.pack()
    entrada_muestra = ttk.Entry(ventana_agregar)
    entrada_muestra.pack()

    etiqueta_especie = ttk.Label(ventana_agregar, text="Especie:")
    etiqueta_especie.pack()
    entrada_especie = ttk.Entry(ventana_agregar)
    entrada_especie.pack()

    etiqueta_pplant = ttk.Label(ventana_agregar, text="Pplant:")
    etiqueta_pplant.pack()
    entrada_pplant = ttk.Entry(ventana_agregar)
    entrada_pplant.pack()

    etiqueta_pconfig = ttk.Label(ventana_agregar, text="Pconfig:")
    etiqueta_pconfig.pack()
    entrada_pconfig = ttk.Entry(ventana_agregar)
    entrada_pconfig.pack()

    etiqueta_pini = ttk.Label(ventana_agregar, text="Pini:")
    etiqueta_pini.pack()
    entrada_pini = ttk.Entry(ventana_agregar)
    entrada_pini.pack()

    etiqueta_pfin = ttk.Label(ventana_agregar, text="Pfin:")
    etiqueta_pfin.pack()
    entrada_pfin = ttk.Entry(ventana_agregar)
    entrada_pfin.pack()

    boton_guardar = ttk.Button(
        ventana_agregar, text="Guardar", command=guardar_registro
    )
    boton_guardar.pack()


def modificar_registro():
    seleccionado = tabla.focus()

    if seleccionado:
        datos = tabla.item(seleccionado)["values"]

        def guardar_modificacion():
            muestra = entrada_muestra.get()
            especie = entrada_especie.get()
            pplant = entrada_pplant.get()
            pconfig = entrada_pconfig.get()
            pini = entrada_pini.get()
            pfin = entrada_pfin.get()

            if muestra and especie and pplant and pconfig and pini and pfin:
                conn = sqlite3.connect("BD_neumatron.db")
                c = conn.cursor()

                c.execute(
                    """UPDATE mediciones SET
                                Muestra = ?,
                                Especie = ?,
                                Pplant = ?,
                                Pconfig = ?,
                                Pini = ?,
                                Pfin = ?
                            WHERE ID = ?""",
                    (muestra, especie, pplant, pconfig, pini, pfin, datos[0]),
                )

                conn.commit()
                conn.close()

                mostrar_registros()
                ventana_modificar.destroy()
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")

        ventana_modificar = tk.Toplevel(root)
        ventana_modificar.title("Modificar Registro")

        etiqueta_muestra = ttk.Label(ventana_modificar, text="Muestra:")
        etiqueta_muestra.pack()
        entrada_muestra = ttk.Entry(ventana_modificar)
        entrada_muestra.pack()
        entrada_muestra.insert(0, datos[1])

        etiqueta_especie = ttk.Label(ventana_modificar, text="Especie:")
        etiqueta_especie.pack()
        entrada_especie = ttk.Entry(ventana_modificar)
        entrada_especie.pack()
        entrada_especie.insert(0, datos[2])

        etiqueta_pplant = ttk.Label(ventana_modificar, text="Pplant:")
        etiqueta_pplant.pack()
        entrada_pplant = ttk.Entry(ventana_modificar)
        entrada_pplant.pack()
        entrada_pplant.insert(0, datos[3])

        etiqueta_pconfig = ttk.Label(ventana_modificar, text="Pconfig:")
        etiqueta_pconfig.pack()
        entrada_pconfig = ttk.Entry(ventana_modificar)
        entrada_pconfig.pack()
        entrada_pconfig.insert(0, datos[4])

        etiqueta_pini = ttk.Label(ventana_modificar, text="Pini:")
        etiqueta_pini.pack()
        entrada_pini = ttk.Entry(ventana_modificar)
        entrada_pini.pack()
        entrada_pini.insert(0, datos[5])

        etiqueta_pfin = ttk.Label(ventana_modificar, text="Pfin:")
        etiqueta_pfin.pack()
        entrada_pfin = ttk.Entry(ventana_modificar)
        entrada_pfin.pack()
        entrada_pfin.insert(0, datos[6])

        boton_guardar = ttk.Button(
            ventana_modificar, text="Guardar", command=guardar_modificacion
        )
        boton_guardar.pack()

    else:
        messagebox.showwarning("Advertencia", "Seleccione un registro para modificar.")


def eliminar_registro():
    seleccionado = tabla.focus()

    if seleccionado:
        if messagebox.askyesno(
            "Confirmar", "¿Está seguro que quiere eliminar este registro?"
        ):
            datos = tabla.item(seleccionado)["values"]
            id_registro = datos[0]

            conn = sqlite3.connect("BD_neumatron.db")
            c = conn.cursor()

            c.execute("DELETE FROM mediciones WHERE ID = ?", (id_registro,))

            conn.commit()
            conn.close()

            mostrar_registros()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")


# Crear la base de datos y la tabla si no existen
crear_tabla()

# Crear la ventana principal
root = tk.Tk()
root.title("Registro de Mediciones")

# Crear la tabla
tabla = ttk.Treeview(
    root,
    columns=("ID", "Muestra", "Especie", "Pplant", "Pconfig", "Pini", "Pfin"),
    show="headings",
)
tabla.pack()

# Configurar las columnas de la tabla
tabla.heading("ID", text="ID")
tabla.heading("Muestra", text="Código de muestra")
tabla.heading("Especie", text="Especie")
tabla.heading("Pplant", text="Presión de la planta")
tabla.heading("Pconfig", text="Presión de configuración")
tabla.heading("Pini", text="Presión inicial")
tabla.heading("Pfin", text="Presión final")

# Configurar el scroll para la tabla
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tabla.yview)
scrollbar.pack(side="right", fill="y")
tabla.configure(yscrollcommand=scrollbar.set)

# Mostrar los registros en la tabla
mostrar_registros()

# Crear los botones
boton_agregar = ttk.Button(root, text="AGREGAR", command=agregar_registro)
boton_agregar.pack()

boton_modificar = ttk.Button(root, text="MODIFICAR", command=modificar_registro)
boton_modificar.pack()

boton_eliminar = ttk.Button(root, text="ELIMINAR", command=eliminar_registro)
boton_eliminar.pack()

# Iniciar la aplicación
root.mainloop()
