FROM python:3.8.9-slim-buster

# Flask demo application
WORKDIR /usr/src/home

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# System packages installation
RUN apt-get update && apt-get install -y nginx supervisor

# Nginx configuration
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "--loglevel=debug"]