FROM python:3.6
LABEL maintainer Max Lamberti <maximilien.lamberti@gmail.com>

# create workdir
RUN mkdir -p /src/
WORKDIR /src

# move scripts
COPY scraper.py /src
COPY requirements.txt /src
COPY utils.py /src
COPY config.py /src

# install google chrome and chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install python packages
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# run job
CMD [ "python", "scraper.py" ]
