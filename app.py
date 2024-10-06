import streamlit as st
from PIL import Image
import io

def cargar_imagen():
    """Permite al usuario cargar una imagen."""
    uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png", "bmp", "gif"])
    if uploaded_file is not None:
        imagen = Image.open(uploaded_file)
        st.image(imagen, caption='Imagen Cargada', use_column_width=True)
        return imagen, uploaded_file.name
    return None, None

def convertir_imagen(imagen, formato):
    """Convierte la imagen al formato seleccionado."""
    with io.BytesIO() as buffer:
        imagen.save(buffer, format=formato)
        return buffer.getvalue()

def main():
    st.title("🔄 Conversor de Imágenes")
    st.write("Carga una imagen, selecciona el formato de destino y descarga la imagen convertida.")

    imagen, nombre_archivo = cargar_imagen()

    if imagen:
        formatos_disponibles = {
            "JPEG": "JPEG",
            "PNG": "PNG",
            "BMP": "BMP",
            "GIF": "GIF",
            "TIFF": "TIFF"
        }

        formato_seleccionado = st.selectbox("Selecciona el formato de conversión:", list(formatos_disponibles.keys()))

        if st.button("Convertir"):
            imagen_convertida = convertir_imagen(imagen, formatos_disponibles[formato_seleccionado])
            st.success(f"Imagen convertida a {formato_seleccionado} exitosamente.")

            nombre_nuevo = nombre_archivo.rsplit(".", 1)[0] + f".{formato_seleccionado.lower()}"
            st.download_button(
                label="Descargar Imagen Convertida",
                data=imagen_convertida,
                file_name=nombre_nuevo,
                mime=f"image/{formatos_disponibles[formato_seleccionado].lower()}"
            )

if __name__ == "__main__":
    main()