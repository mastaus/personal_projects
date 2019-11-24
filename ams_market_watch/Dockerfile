FROM python:3
COPY requirements.txt /usr/src/market_watch_app/
ADD .py
WORKDIR
RUN pip install -r requirements.txt
CMD ["python", "./.py"]
