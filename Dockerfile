FROM python:3.12-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PORT 8080
EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app.py"]
