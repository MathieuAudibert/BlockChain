FROM python:3.12
WORKDIR /app

RUN pip install uv
COPY src/requirements.txt ./src/requirements.txt
RUN uv pip install --system -r src/requirements.txt
COPY . .

CMD ["python", "src/main.py"]