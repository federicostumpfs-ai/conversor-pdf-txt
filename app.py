import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# Asegúrate de que NO haya espacios antes o después de la clave
API_KEY = "AIzaSyD1KQ72ZKxTIY3JoUPcaGRGBtIDfq3C43E".strip() 

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Centro de Cómputos - Generador", layout="centered")

st.title("📄 Generador de TXT para Sorteos")
st.write("Herramienta interna de procesamiento de extractos oficiales.")

uploaded_file = st.file_uploader("Cargue un PDF individual", type="pdf")
if uploaded_file:
    with st.spinner('Procesando PDF y extrayendo datos con Inteligencia Artificial...'):
        try:
            # 1. Leer el texto completo del PDF cargado
            reader = PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages:
                text_page = page.extract_text()
                if text_page:
                    full_text += text_page + "\n"

            # 2. Configurar el modelo
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 3. Instrucción
            prompt = f"Transforma este extracto de lotería al formato TXT de centro de cómputos. Usa bordes de '+==+' para Quini y '*==*' para Loto. Si no hay ganadores, pon 'VACANTE'. Texto: {full_text}"

            # 4. Generar el contenido
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                txt_final = response.text
                st.success("¡Archivo transformado con éxito!")
                st.text_area("Vista previa:", txt_final, height=450)
                
                nombre_salida = uploaded_file.name.replace(".pdf", ".txt").replace(".PDF", ".txt")
                
                st.download_button(
                    label="⬇️ Descargar archivo .txt",
                    data=txt_final,
                    file_name=nombre_salida,
                    mime="text/plain"
                )
            else:
                st.error("La IA no devolvió texto. Reintenta subir el archivo.")

        except Exception as e:
            st.error(f"Hubo un problema técnico: {e}")
