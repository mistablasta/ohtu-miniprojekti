FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

# Disable use of .venv (fixes some env and dependency issues)
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

# Copy pyproject and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root

# Copy only the source files
COPY src ./src

CMD ["python", "src/index.py"]
