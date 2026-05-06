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

            # 2. Configurar el modelo correcto según la última documentación oficial
            # Usamos 'gemini-1.5-flash' directamente
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 3. Darle instrucciones ultra-precisas con ejemplos reales del Centro de Cómputos
            prompt = f"""
            Actúas como un operador experto del centro de cómputos de una lotería nacional.
            Tu tarea es tomar el texto crudo extraído de un PDF oficial de sorteo y estructurarlo exactamente en el formato TXT plano que requiere nuestro sistema operativo interno.

            REGLAS ESTRICTAS DE FORMATO SEGÚN EL JUEGO DETECTADO:

            --- EJEMPLO 1: SI EL TEXTO CORRESPONDE A UN QUINI 6 ---
            Debes estructurarlo usando bordes '+=======================================+' y mayúsculas, respetando las columnas POZO, CANTIDAD GANADORES y PREMIO POR CUPÓN:
            +=======================================+
            |QUINI 6 # [NÚMERO] - [FECHA] [PREMIOS]  |
            +=======================================+
            |     POZO     CANTIDAD      PREMIO     |
            |      $       GANADORES     POR CUPON  |
            +=======================================+
            |PRIMER SORTEO    [NÚMEROS GANADORES]   |
            |                                       |
            |1P  [POZO]  [CANTIDAD]   [PREMIO CUPÓN]|
            |2P  [POZO]  [CANTIDAD]   [PREMIO CUPÓN]|
            |3P  [POZO]  [CANTIDAD]   [PREMIO CUPÓN]|
            |ES  [POZO]  [GANADORES]  [PREMIO CUPÓN]|
            +=======================================+
            [Y continuar así con LA SEGUNDA, REVANCHA, SIEMPRE SALE, PREMIO EXTRA y al final colocar el PROXIMO SORTEO con su POZO ESTIMADO]

            --- EJEMPLO 2: SI EL TEXTO CORRESPONDE A LOTO PLUS o LOTO 5 ---
            Debes estructurarlo usando bordes de asteriscos '*======================================*' y barras verticales:
            *======================================*
            | LOTO PLUS # [NÚMERO] - [FECHA] [PREMIOS]|
            *======================================*
            |TRADICIONAL  [NÚMEROS GANADORES]      |
            *======================================*
            |6 AC       [CANTIDAD/VACANTE]  [MONTO] |
            |5 AC       [CANTIDAD/VACANTE]  [MONTO] |
            |4 AC       [CANTIDAD/VACANTE]  [MONTO] |
            *======================================*

            REQUISITOS ADICIONALES:
            - Si el premio quedó sin ganadores, escribe obligatoriamente la palabra 'VACANTE'.
            - Alinea los números de manera prolija para mantener las columnas verticales rectas.
            - Devuelve ÚNICAMENTE el texto que irá dentro del archivo .txt, sin introducciones ni formatos markdown adicionales (no pongas ```text al inicio).

            TEXTO EXTRAÍDO DEL PDF ORIGINAL A TRANSFORMAR:
            {full_text}
            """

           # 4. Generar el contenido
            response = model.generate_content(prompt)
            txt_final = response.text

            # 5. Mostrar resultado en la interfaz web y habilitar descarga
            st.success("¡Archivo transformado con éxito!")
            st.text_area("Vista previa del formato generado:", txt_final, height=450)
            
            # Cambiar extensión para la descarga (.pdf -> .txt)
            nombre_salida = uploaded_file.name.replace(".pdf", ".txt").replace(".PDF", ".txt")
            
            st.download_button(
                label="⬇️ Descargar archivo .txt listo",
                data=txt_final,
                file_name=nombre_salida,
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Hubo un problema al procesar el archivo: {e}")
            st.info("Tip técnico: Si dice NotFound, asegúrese de que el archivo requirements.txt tenga cargada la última versión de google-generativeai.")
