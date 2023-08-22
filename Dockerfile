FROM mcr.microsoft.com/devcontainers/python:0-3.10
WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
COPY __main__.py .
RUN apt update ; apt install -y ffmpeg ; pip install pipenv ; pipenv sync
ENTRYPOINT ["pipenv", "run", "python", "."]
