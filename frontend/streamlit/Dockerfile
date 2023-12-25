FROM python:3.9

WORKDIR /app

COPY requirement.txt ./requirement.txt

RUN pip install -r requirement.txt

Expose 8080

COPY . /app1

CMD streamlit run --server.port 8080 --server.enableCORS false streamlit_app.py