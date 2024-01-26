FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./api_auth /app

EXPOSE 8080

RUN pip install asyncpg mysql-connector-python psycopg2-binary python-jose

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]