FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

#COPY front.py /app/front.py

RUN pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir

EXPOSE 8501

CMD ["streamlit", "run", "front.py"]