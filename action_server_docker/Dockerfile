FROM rasa/rasa-sdk:3.6.0
WORKDIR /app
USER root
RUN groupadd -r rasa && useradd -r -g rasa rasa
RUN pip install --upgrade pip
COPY requirements-actions.txt .
RUN pip install --no-cache-dir -r requirements-actions.txt
COPY actions /app/actions
RUN chown -R rasa:rasa /app
USER rasa
EXPOSE 5055
CMD ["start", "--actions", "actions.actions", "--port", "5055", "--debug"]
