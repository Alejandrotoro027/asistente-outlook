# ✉️ Asistente Virtual para Limpieza de Correos Outlook

Este proyecto es un asistente virtual inteligente que se conecta a tu cuenta de Outlook.com para ayudarte a **clasificar, mover o eliminar automáticamente correos no deseados**, con una interfaz web intuitiva que permite también el entrenamiento continuo del sistema.

---

## 🚀 Características

- 🔒 Inicio de sesión seguro con OAuth 2.0 (Microsoft Outlook)
- 🧠 Clasificación automática de correos (spam, trabajos, importante, eliminar, etc.)
- 👀 Revisión manual de clasificaciones con opción de corrección
- 📚 Entrenamiento supervisado continuo desde la interfaz
- 📊 Historial con filtros, búsqueda, paginación y exportación a CSV
- 💡 Aprendizaje constante de tus decisiones

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10+**
- **Flask** – Framework web
- **SQLite** – Base de datos local para almacenamiento y entrenamiento
- **Microsoft Graph API** – Conexión con Outlook
- **OAuth 2.0 Authorization Code Flow** – Inicio de sesión seguro
- **HTML + CSS** – Interfaz moderna y adaptable

---

## 🧑‍💻 Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/Alejandrotoro027/asistente-outlook.git
cd asistente-outlook```
```
---

2. **Crea un entorno virtual (opcional pero recomendado)**

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```
---

3. **Instala las dependencias del proyecto**

```bash
pip install -r requirements.txt
```
---

4. **Configura tus credenciales de Outlook (requerido)**

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
REDIRECT_URI=http://localhost:5000/callback
```
🔐 Reemplaza tu_client_id y tu_client_secret con las credenciales reales de tu aplicación registrada en el Azure Portal, y asegúrate de que REDIRECT_URI coincida con la que configuraste (por ejemplo, http://localhost:5000/callback).

Este archivo es ignorado automáticamente por Git (gracias al .gitignore) y no se subirá al repositorio

---

5. **Ejecuta el asistente virtual**

Desde la raíz del proyecto, ejecuta el siguiente comando en tu terminal:

```bash
python run_web.py
```
Esto iniciará la aplicación web en [http://localhost:5000/](http://localhost:5000/).

** Acciones disponibles en la interfaz:**

- 🔑 **Iniciar sesión** con tu cuenta de Outlook  
- 🧹 **Ejecutar limpieza** de correos no deseados (basado en clasificación automática o manual)  
- 🧠 **Entrenar el modelo de aprendizaje** con correos revisados  
- 📊 **Revisar clasificaciones anteriores** y corregirlas manualmente  
- 📂 **Ver historial** de correos procesados con filtros, búsqueda por remitente y exportación a CSV

Una vez logueado, podrás navegar entre las distintas funcionalidades desde el **menú principal** de la interfaz.

---

📁 **Estructura del proyecto**

asistente_outlook/
│
├── core/ # Lógica del asistente (API, limpieza, ML, base de datos)
│ ├── auth.py
│ ├── db.py
│ ├── eliminador.py
│ └── modelo.py
│
├── web/ # Interfaz Flask
│ ├── app.py
│ ├── templates/
│ └── static/
│ └── styles.css
│
├── run_web.py # Archivo principal para ejecutar la app
├── requirements.txt # Dependencias del proyecto
└── .gitignore # Exclusiones para seguridad

---

🛡️ **Seguridad: `.gitignore` recomendado**

Este es un ejemplo de `.gitignore` ya incluido en el repositorio para proteger tus credenciales y archivos sensibles:

```bash
# Archivos confidenciales
token.txt
client_secret.txt
client_id.txt
.env

# Archivos de entrenamiento
whitelist.txt
eliminados.txt
recuperados.txt

# Python
__pycache__/
*.pyc

# Entorno virtual
venv/
.env/
```
---

📈 Próximas mejoras
🌐 Despliegue en la nube (Render, Heroku, Azure)

📅 Clasificación basada en fechas, frecuencia y prioridades

🧠 Entrenamiento automático por lote

🔔 Notificaciones por correo o Telegram

📊 Panel de analíticas con gráficos

🤝 Contribuciones
¡Las contribuciones son bienvenidas! Puedes:

Abrir un issue con sugerencias o errores

Hacer un fork y enviar un pull request

Proponer ideas para mejorar el aprendizaje automático o la interfaz

📄 Licencia
Este proyecto está bajo la licencia MIT.

💬 Contacto
Si tienes dudas o deseas colaborar:

✉️ Email: [tu-email@ejemplo.com]

🐙 GitHub: https://github.com/tu-usuario
