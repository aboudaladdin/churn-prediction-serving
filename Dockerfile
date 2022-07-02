FROM python:3.10.5-slim

ENV PYTHONUNBUFFERED=TRUE

RUN pip install --no-cache-dir install pipenv

WORKDIR /app

COPY ["Pipfile","Pipfile.lock","./"]

RUN pipenv install --deploy --system && rm -rf /root/.cache

COPY ["*.py", "churn-model.bin", "./"]


ENTRYPOINT ["gunicorn", "churn_flask:app"] 