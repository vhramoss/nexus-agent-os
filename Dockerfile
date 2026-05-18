# ---------- STAGE 1 ----------
FROM python:3.11-slim

WORKDIR /app

# instalar dependências do sistema
RUN pip install --no-cache-dir --upgrade pip

# copiar código
COPY . .

# instalar dependências
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    pydantic_settings \
    python-dotenv \
    redis \
    sentence-transformers \
    faiss-cpu \
    langgraph \
    langchain \
    crewai

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "nexus_os.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
