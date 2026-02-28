import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="AI Image Upscaler", page_icon="🖼️")

st.title("🖼️ Reescalador de Imágenes con Streamlit")
st.write("Sube una imagen y aumentaremos su resolución al doble (2x) usando el filtro Lanczos.")

# Widget para subir archivos
uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostrar imagen original
    img = Image.open(uploaded_file)
    st.subheader("Imagen Original")
    st.image(img, caption=f"Tamaño original: {img.width}x{img.height}", use_container_width=True)

    # Botón para procesar
    if st.button("🚀 Reescalar ahora"):
        with st.spinner('Procesando...'):
            # Lógica de reescalado
            new_size = (img.width * 2, img.height * 2)
            upscaled_img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Preparar la imagen para descargar (en memoria)
            buf = io.BytesIO()
            upscaled_img.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.success(True)
            st.subheader("Resultado (2x)")
            st.image(upscaled_img, caption=f"Nuevo tamaño: {new_size[0]}x{new_size[1]}", use_container_width=True)

            # Botón de descarga interactivo
            st.download_button(
                label="📥 Descargar imagen reescalada",
                data=byte_im,
                file_name="upscaled_image.png",
                mime="image/png"
            )
