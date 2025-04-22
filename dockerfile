FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /opt/app-root/
COPY pyproject.toml uv.lock /opt/app-root/
RUN uv sync
COPY /src/. /opt/app-root/

RUN adduser default -D
USER default
CMD ["uv", "run", "python", "main.py"]
