import streamlit as st
from PIL import Image
import io

def cargar_imagen():
    """Permite al usuario cargar una imagen."""
    uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png", "bmp", "gif", "webp"])
    if uploaded_file is not None:
        try:
            imagen = Image.open(uploaded_file).convert("RGBA")
            st.image(imagen, caption='Imagen Cargada', use_column_width=True)
            return imagen, uploaded_file.name
        except Exception as e:
            st.error(f"Error al cargar la imagen: {e}")
    return None, None

def convertir_imagen(imagen, formato):
    """Convierte la imagen al formato seleccionado."""
    with io.BytesIO() as buffer:
        if formato.upper() == "JPEG":
            # JPEG no soporta transparencias, convertir a RGB
            imagen = imagen.convert("RGB")
        elif formato.upper() == "WEBP":
            # Opcional: Puedes ajustar la calidad de WebP aquí si lo deseas
            imagen.save(buffer, format=formato, quality=80)
            return buffer.getvalue()
        imagen.save(buffer, format=formato)
        return buffer.getvalue()

def main():
    st.set_page_config(page_title="🔄 Conversor de Imágenes", page_icon="🔄")
    st.title("🔄 Conversor de Imágenes")
    st.write("Carga una imagen, selecciona el formato de destino y descarga la imagen convertida.")

    imagen, nombre_archivo = cargar_imagen()

    if imagen:
        formatos_disponibles = {
            "JPEG": "JPEG",
            "PNG": "PNG",
            "BMP": "BMP",
            "GIF": "GIF",
            "TIFF": "TIFF",
            "WEBP": "WEBP"  # Añadido WebP
        }

        formato_seleccionado = st.selectbox("Selecciona el formato de conversión:", list(formatos_disponibles.keys()))

        if st.button("Convertir"):
            try:
                imagen_convertida = convertir_imagen(imagen, formatos_disponibles[formato_seleccionado])
                st.success(f"Imagen convertida a {formato_seleccionado} exitosamente.")

                # Generar el nuevo nombre de archivo con la extensión correcta
                if '.' in nombre_archivo:
                    nombre_nuevo = nombre_archivo.rsplit(".", 1)[0] + f".{formatos_disponibles[formato_seleccionado].lower()}"
                else:
                    nombre_nuevo = f"imagen_convertida.{formatos_disponibles[formato_seleccionado].lower()}"

                # Determinar el tipo MIME correcto
                mime_types = {
                    "jpeg": "image/jpeg",
                    "png": "image/png",
                    "bmp": "image/bmp",
                    "gif": "image/gif",
                    "tiff": "image/tiff",
                    "webp": "image/webp"
                }

                mime_type = mime_types.get(formatos_disponibles[formato_seleccionado].lower(), "application/octet-stream")

                st.download_button(
                    label="Descargar Imagen Convertida",
                    data=imagen_convertida,
                    file_name=nombre_nuevo,
                    mime=mime_type
                )
            except Exception as e:
                st.error(f"Error al convertir la imagen: {e}")

if __name__ == "__main__":
    main()
