FROM python:3.12.2

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libsasl2-dev \
    libldap2-dev

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "main.py"]
