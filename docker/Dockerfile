FROM python:latest

RUN pip install gunicorn
RUN pip install metastock

COPY start.sh /start.sh

RUN chmod +x /start.sh

ENTRYPOINT ["/bin/bash", "-c", "/start.sh"]