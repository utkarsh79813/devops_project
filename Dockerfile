FROM python:3-slim
WORKDIR /myapp
COPY app/ .
RUN pip install -r requirements.txt
CMD [ "python3", "app2tier.py" ]
EXPOSE 5000
