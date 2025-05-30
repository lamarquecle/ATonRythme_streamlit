FROM python:3.11

EXPOSE 8080
WORKDIR /streamlit

COPY . ./

ENV API_URL="https://atonrythme-fastapi-800884171084.europe-west1.run.app"
ENV DASHBOARD_URL="https://app.powerbi.com/reportEmbed?reportId=4b114b9d-e044-4285-8754-dbc666af346d&autoAuth=true&ctid=64394016-0de7-4462-aeaa-f7aac3e7bcf9"

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "connexion.py", "--server.port=8080", "--server.address=0.0.0.0"]
