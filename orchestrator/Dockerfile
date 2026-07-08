FROM python:3.12-slim

WORKDIR /orchestrator

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python" , "-u", "-m"]

CMD ["orchestrator.orchestrator"]