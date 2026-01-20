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
