# ETL Facturas (Gemini + COP)

Este mini-proyecto procesa facturas en PDF usando Gemini (Google) para extraer campos en CSV, los convierte a DataFrame, transforma importes a COP y persiste en SQLite.

Requisitos
- Python 3.10+ (probado con 3.11/3.12)
- Virtualenv o Conda

Dependencias (pip)
- python-dotenv
- pandas
- PyMuPDF
- requests
- sqlalchemy
- google-cloud-aiplatform (que trae google.genai)

Instalación rápida (venv)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configuración de Git
```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/juanduque09/ETL-AI.git
git push -u origin main
```

Variables de entorno (`.env`)
- GOOGLE_API_KEY=tu_api_key
- MODEL_NAME=models/gemini-2.0-flash
- MAX_OUTPUT_TOKENS=512
- TEMPERATURE=0.0
- FALLBACK_RATE_USD_COP=4500
- FALLBACK_RATE_EUR_COP=4900
- FALLBACK_MODEL=models/gemini-2.5-flash  # modelo alterno si el principal está sobrecargado
- BACKOFF_BASE=1.0   # backoff exponencial base (segundos)
- BACKOFF_MAX=30.0   # backoff máximo (segundos)
- BACKOFF_JITTER=0.5 # jitter máximo añadido al backoff (segundos)
- LOG_LEVEL=INFO     # nivel de logging (INFO, DEBUG, WARNING)
- LLM_METRICS_CSV=llm_usage.csv  # archivo CSV donde se escriben métricas de uso del LLM
 - LLM_RETRIES=5     # número máximo de reintentos para llamadas LLM

Ejemplos de ejecución
- Probar LLM con un texto de ejemplo:
```bash
python3 test_gemini.py
```
- Ejecutar pipeline sobre `./facturas` y reemplazar la tabla:
```bash
python3 main.py --overwrite
```
- Ejecutar pipeline y anexar a la tabla existente:
```bash
python3 main.py
```

Inspeccionar la BD:
```bash
python3 - <<'PY'
import pandas as pd
from sqlalchemy import create_engine
e = create_engine('sqlite:///facturas.db')
print(pd.read_sql('facturas', e).head())
PY
```

Siguientes mejoras disponibles:
- Logging y reintentos (ya implementado)
- Mejor reconocimiento de monedas
- Tests unitarios
- Añadir control de costos/token limits
 
Notas sobre fallback y reintentos
- El sistema intentará 5 reintentos para llamadas a Gemini usando backoff exponencial con jitter. Si detecta errores de sobrecarga (503 / 'unavailable'), y `FALLBACK_MODEL` está definido en `.env`, cambiará temporalmente al modelo de fallback y seguirá reintentando.
- Las métricas de uso (tokens) se registran en el archivo indicado por `LLM_METRICS_CSV` si el SDK devuelve información de usage. Esto te permite auditar consumo de tokens y costes.

