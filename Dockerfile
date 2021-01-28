FROM python:3.8-buster

# Set our working directory
WORKDIR /usr/src/app

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt ./

RUN apt update && \
    apt install python3-dev -y && apt autoremove -y
# pip install python deps from requirements.txt on the resin.io build server
RUN pip install --no-cache-dir -r requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY . ./

CMD ["bash","start.sh"]