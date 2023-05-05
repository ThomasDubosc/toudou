FROM python:3.10.10-slim-buster

WORKDIR /app
COPY dist/Toudou-*-py3-none-any.whl /app/
RUN pip install *.whl gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0", "toudou.wsgi:app"]
