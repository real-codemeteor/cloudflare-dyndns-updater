FROM python:3.8-slim-buster


COPY requirements.txt requirements.txt

RUN apt update && apt install cron busybox rsyslog -y
RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/app/config", "/app/logs"]
HEALTHCHECK NONE
COPY crontab /etc/cron.d/crontab

COPY . .
RUN chmod +x /app/main.py
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
#CMD busybox syslogd && cron 