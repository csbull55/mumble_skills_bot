# use official python as parent image
FROM python:3

# sets working directory
WORKDIR /usr/src/app

COPY requirements.txt ./

# installs requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# runs app when the container is launched
CMD [ "python", "./discord_bot.py" ]