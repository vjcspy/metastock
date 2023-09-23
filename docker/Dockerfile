FROM python:latest

RUN pip install gunicorn

COPY start.sh /start.sh

RUN chmod +x /start.sh

ENTRYPOINT ["/bin/bash", "-c", "/start.sh"]