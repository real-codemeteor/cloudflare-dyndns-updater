FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /opt/app-root/
RUN adduser default -D
COPY pyproject.toml uv.lock /opt/app-root/
RUN chown -R default /opt/app-root
USER default
RUN uv sync && uv build
COPY /src/. /opt/app-root/
WORKDIR /opt/app-root/cloudflare_dyndns_updater
ENV SETTINGS_FILE=/config.toml 
CMD ["uv", "run", "python", "main.py"]
