FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./auth_service/requirements.txt
RUN pip install --no-cache-dir -r auth_service/requirements.txt

COPY . ./auth_service

EXPOSE 8000

CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]