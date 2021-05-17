FROM python:3.6.9
RUN apt-get -y update && apt-get -y upgrade

# Install wget.
RUN apt-get install -y wget
# Download chrome installer
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Install Chrome.
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb && apt-get -y autoremove && apt-get -y clean

WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
ENV PORT 8080
CMD ["gunicorn", "app:app", "--config=config.py"]