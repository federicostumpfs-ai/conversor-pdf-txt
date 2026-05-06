API_KEY = "AIzaSyDUCyGsLBiYVlJJGp1mGMLlSgd3rRASk1Q"

genai.configure(api_key=API_KEY)



st.set_page_config(page_title="Centro de Cómputos - Generador", layout="centered")



st.title("📄 Generador de TXT para Sorteos")

st.write("Herramienta interna de procesamiento de extractos oficiales.")



uploaded_file = st.file_uploader("Cargue un PDF individual", type="pdf")
if uploaded_file:

    with st.spinner('Procesando PDF y extrayendo datos...'):

        # 1. Leer el PDF

        reader = PdfReader(uploaded_file)

        full_text = ""

        for page in reader.pages:

            full_text += page.extract_text()



        # 2. Instrucción de Inteligencia Artificial

        model = genai.GenerativeModel('gemini-1.5-flash')

        

        prompt = f"""

        Actúa como un experto en extracción de datos para un centro de cómputos de lotería.

        Tu tarea es leer el siguiente texto de un PDF y transformarlo al formato TXT exacto de la empresa.



        REGLAS DE FORMATO:

        1. Si es QUINI 6: Usa bordes con '+' y '-' y el encabezado exacto que viste en los ejemplos.

        2. Si es LOTO: Usa bordes con '*' y '='. 

        3. Identifica: Número de Sorteo, Fecha, Números Ganadores, Pozo, Cantidad de Ganadores y Premio por Cupón.

        4. Si el premio dice 'VACANTE', respeta esa palabra en el TXT.

        5. Mantén la alineación de las columnas para que se vea ordenado.



        TEXTO DEL PDF:

        {full_text}

        """



        response = model.generate_content(prompt)

        txt_final = response.text



        # 3. Mostrar resultado y permitir descarga

        st.success("Archivo procesado correctamente")

        st.text_area("Vista previa del TXT:", txt_final, height=400)

        

        nombre_salida = uploaded_file.name.replace(".pdf", ".txt")

        st.download_button(

            label="⬇️ Descargar archivo .txt",

            data=txt_final,

            file_name=nombre_salida,

            mime="text/plain"

        )
