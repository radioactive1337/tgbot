FROM python:3.10
LABEL admin="radioactive"
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
ENTRYPOINT [ "python" ]
CMD [ "./main.py" ]