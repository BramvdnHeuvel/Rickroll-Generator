FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py ./
RUN python3 setup.py -y

COPY . .

CMD ["python3", "main.py", "0.0.0.0", "80"]
