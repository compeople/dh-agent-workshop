FROM python:3.12

# Set working directory to /app
WORKDIR /app
COPY main.py /app
COPY pyproject.toml /app
COPY poetry.lock /app
RUN pip install poetry
RUN poetry install
EXPOSE 8080
CMD ["poetry", "run", "python", "main.py"]