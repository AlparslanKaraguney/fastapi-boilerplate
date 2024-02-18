# Use a smaller base image
FROM python:3.11-alpine as requirements-stage

# Install system dependencies and build tools
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev build-base

# Set working directory
WORKDIR /tmp

# Install Poetry
RUN pip install poetry

# Copy only the necessary files for dependency resolution
# COPY pyproject.toml poetry.lock* run.sh .env alembic.ini /tmp/
COPY pyproject.toml poetry.lock* run.sh alembic.ini /tmp/

# Install dependencies without dev dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Final production image
FROM python:3.11-alpine

# Set working directory
WORKDIR /code

RUN pip install --upgrade pip
# RUN export GRPC_PYTHON_DISABLE_LIBC_COMPATIBILITY=1

# Install necessary system libraries for grpcio
RUN apk add linux-headers
RUN apk add --no-cache libstdc++ protobuf-dev


# Copy only the necessary files from the previous stage
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app
COPY --from=requirements-stage /tmp/run.sh /code/run.sh
# COPY --from=requirements-stage /tmp/.env /code/.env
COPY --from=requirements-stage /tmp/alembic.ini /code/alembic.ini

# Run the application
CMD [ "sh", "run.sh" ]
