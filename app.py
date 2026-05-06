import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# 1. Configuración de Seguridad
API_KEY = "AIzaSyD1KQ72ZKxTIY3JoUPcaGRGBtIDfq3C43E"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Centro de Cómputos - Generador", layout="centered")

# 2. Interfaz de Usuario
st.title("📄 Generador de TXT para Sorteos")
st.write("Herramienta interna de procesamiento de extractos oficiales.")

uploaded_file = st.file_uploader("Cargue un PDF individual", type="pdf")

# 3. Procesamiento del Archivo
if uploaded_file:
    with st.spinner('Procesando PDF con IA...'):
        try:
            # Extraer texto del PDF
            reader = PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages:
                text_page = page.extract_text()
                if text_page:
                    full_text += text_page + "\n"

            # Configurar el modelo (Usamos gemini-pro por estabilidad)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Transforma este extracto de lotería al formato TXT de centro de cómputos. Usa bordes de '+==+' para Quini y '*==*' para Loto. Si no hay ganadores, pon 'VACANTE'. Texto: {full_text}"

            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                txt_final = response.text
                st.success("¡Archivo transformado!")
                st.text_area("Vista previa:", txt_final, height=450)
                
                # Botón de descarga
                nombre_salida = uploaded_file.name.replace(".pdf", ".txt").replace(".PDF", ".txt")
                st.download_button(
                    label="⬇️ Descargar archivo .txt",
                    data=txt_final,
                    file_name=nombre_salida,
                    mime="text/plain"
                )
            else:
                st.error("La IA no pudo generar el texto. Intenta de nuevo.")

        except Exception as e:
            st.error(f"Error técnico: {e}")
