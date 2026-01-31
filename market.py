import streamlit as st
import pandas as pd

st.set_page_config(page_title="Supermercado El más barato", layout="centered")
st.title("Supermercado El más barato")

# --- Tabla en session_state ---
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        columns=["Producto", "Precio", "Cantidad", "Subtotal", "Imp 18%", "Imp 15%", "Total"]
    )

# --- Control de formulario ---
if "form_version" not in st.session_state:
    st.session_state.form_version = 0

def nuevo_formulario():
    # Limpia formulario
    st.session_state.form_version += 1
    # Limpia tabla COMPLETA
    st.session_state.table_data = pd.DataFrame(
        columns=["Producto", "Precio", "Cantidad", "Subtotal", "Imp 18%", "Imp 15%", "Total"]
    )

v = st.session_state.form_version

# --- Botón Nuevo (borra TODO lo anterior) ---
st.button("Nuevo", on_click=nuevo_formulario)

# --- Formulario ---
with st.form(f"producto_form_{v}"):
    producto_nombre = st.text_input(
        "Ingrese el nombre del producto",
        key=f"producto_nombre_{v}"
    )
    producto_precio = st.number_input(
        "Ingrese el precio del producto",
        min_value=0.0,
        step=1.0,
        key=f"producto_precio_{v}"
    )
    producto_cantidad = st.number_input(
        "Ingrese la cantidad",
        min_value=1,
        step=1,
        key=f"producto_cantidad_{v}"
    )

    comprar = st.form_submit_button("Comprar producto")

# --- Comprar producto ---
if comprar:
    if producto_nombre.strip() == "":
        st.warning("Ingrese el nombre del producto.")
    else:
        subtotal = producto_precio * producto_cantidad
        imp15 = subtotal * 0.15
        total = subtotal  + imp15

        nueva_fila = {
            "Producto": producto_nombre.strip(),
            "Precio": producto_precio,
            "Cantidad": producto_cantidad,
            "Subtotal": subtotal,
            "Imp 15%": imp15,
            "Total": total
        }

        st.session_state.table_data = pd.concat(
            [st.session_state.table_data, pd.DataFrame([nueva_fila])],
            ignore_index=True
        )

        # Limpia SOLO el formulario después de comprar
        st.session_state.form_version += 1

# --- Mostrar tabla ---
st.dataframe(st.session_state.table_data, use_container_width=True)

# --- Total a pagar ---
if st.button("Calcular Total a Pagar"):
    if st.session_state.table_data.empty:
        st.info("Todavía no hay productos en la lista.")
    else:
        total_pagar = st.session_state.table_data["Total"].sum()
        st.subheader("Total a Pagar")
        st.write(f"Lempiras {total_pagar:.2f}")

"""
===========================
ENTENDER EL FLUJO DEL PROGRAMA
===========================

¿Qué hace st.session_state?
st.session_state se utiliza para mantener la información entre las interacciones
del usuario. Como Streamlit vuelve a ejecutar todo el programa en cada acción,
esta estructura permite que la tabla de compras no se pierda y se mantenga
durante el uso de la aplicación.

¿Qué hace el cálculo del subtotal?
El programa calcula el subtotal multiplicando el precio por la cantidad.
Luego calcula el impuesto del 15% y obtiene el total. Esa información se guarda
en una nueva fila que se agrega al DataFrame almacenado en la sesión.

¿Por qué se usa st.form()?
st.form() permite enviar los datos del producto en un solo evento al presionar
el botón "Comprar producto", evitando que el programa se ejecute cada vez que
se cambia un campo del formulario.

¿Qué se muestra con st.dataframe()?
Se muestra la tabla actual de compras guardada en la sesión, la cual se va
actualizando cada vez que se agrega un nuevo producto.

-
"""
