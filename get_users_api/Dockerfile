# Use the Python Alpine image.
FROM python:3.8-alpine

# Install the application's dependencies.
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Add and run the application.
COPY . /app
EXPOSE 3000
CMD ["python3", "app.py"]
