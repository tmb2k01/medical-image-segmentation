FROM python:3.10

WORKDIR /medical-image-segmentation

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh ./entrypoint.sh
COPY src/ ./src/

# Expose port 7860 to allow external access to the Gradio application
EXPOSE 7860

# Disable Python output buffering to ensure logs are displayed in real-time
ENV PYTHONUNBUFFERED=1

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]
