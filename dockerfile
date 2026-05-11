FROM python:3.13.13-trixie

WORKDIR /opt/app-root/
RUN adduser default --disabled-password
COPY pyproject.toml uv.lock /opt/app-root/
RUN chown -R default /opt/app-root
USER default
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH=/home/default/.local/bin:${PATH}
RUN uv sync && uv build
COPY /src/. /opt/app-root/
WORKDIR /opt/app-root/cloudflare_dyndns_updater
ENV SETTINGS_FILE=/config.toml 
CMD ["uv", "run", "python", "main.py"]
