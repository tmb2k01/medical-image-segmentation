FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime

WORKDIR /usr/src/app
COPY requirements.txt .
COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main.py"]
