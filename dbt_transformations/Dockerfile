FROM python:3.12-slim

WORKDIR /dbt_transformations

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dbt_project .

COPY packages.yml .

RUN dbt deps

COPY . .

ENTRYPOINT [ "/bin/bash", "-c" ]

CMD [ "dbt source freshness -s tag:observability,tag:prod --profiles-dir . && dbt test -s +exposure:*,tag:observability --profiles-dir . && dbt run -s +exposure:*,tag:observability --profiles-dir ." ]  