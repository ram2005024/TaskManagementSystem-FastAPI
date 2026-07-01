FROM python:3.13-slim
WORKDIR /code
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODES=1
COPY pyproject.toml .
COPY uv.lock .
RUN pip install uv
RUN uv sync
COPY . .
CMD [ "uv","run","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload" ]
