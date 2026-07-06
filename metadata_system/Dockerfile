FROM python:3.12-slim

WORKDIR /metadata_system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "-m", "orchestrator.orchestrator" ]