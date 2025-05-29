FROM rasa/rasa-sdk:3.6.0

WORKDIR /app

COPY actions /app/actions
COPY requirements-actions.txt ./

RUN pip install --no-cache-dir -r requirements-actions.txt

CMD ["run", "actions", "--port", "5055", "--debug"]
