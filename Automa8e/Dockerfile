FROM ghcr.io/railwayapp/nixpacks:ubuntu-1707782610

# Install Python 3.8
RUN apt-get update && apt-get install -y python3.8

WORKDIR /app/

COPY . /app/.

# Install dependencies using the full path to pip
RUN /usr/bin/python3.8 -m pip install -r requirements.txt

# Start your application (replace with your command)
CMD ["gunicorn", "Chatbot:app"]
