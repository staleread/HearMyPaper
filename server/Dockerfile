FROM python:3.13-slim

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade .

COPY ./app /code/app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
