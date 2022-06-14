FROM python:3.7
# install system dependencies
RUN apt-get -y update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*s

RUN apt-get install -yqq wget curl unzip

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN mkdir -p "chromedriver/stable"
RUN unzip /tmp/chromedriver.zip chromedriver -d /chromedriver/stable/ && chmod +x "chromedriver/stable/chromedriver"

ENV DRIVERFOLDER=/app

RUN python3 --version
RUN pip3 --version
RUN pip install --no-cache-dir --upgrade pip
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8080
ENTRYPOINT ["python", "./main.py"]