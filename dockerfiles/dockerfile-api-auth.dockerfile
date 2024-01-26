FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./api /app

EXPOSE 8080

RUN pip install asyncpg mysql-connector-python psycopg2-binary

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]