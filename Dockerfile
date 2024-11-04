FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime

WORKDIR /medical-image-segmentation

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh .
COPY src/ ./src/

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]
