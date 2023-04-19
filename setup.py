from os import urandom
import sys

# Example invocation: python setup.py "my.domain.name.com"

# Domain name set by 1st argument
domain_name=sys.argv[1]
database_password=urandom(36).hex()

if(len(sys.argv)<2):
    print("Missing an argument for your domain name")
    exit()

def render_yaml():
    return f'''version: '3.1'

services:

  wordpress:
    image: wordpress
    restart: always
    ports:
      - 5000:80
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: '{database_password}'
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - ./wordpress:/var/www/html
    logging:
      options:
        max-size: "5m"
        max-file: "5"

  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: '{database_password}'
      MYSQL_ROOT_PASSWORD: '{database_password}'
    volumes:
      - ./db:/var/lib/mysql
    ports:
      - 3306:3306
    logging:
      options:
        max-size: "5m"
        max-file: "5"

  caddyproxy:
    network_mode: "host"
    image: "caddy"
    restart: "always"
    command:
      [
        "caddy",
        "reverse-proxy",
        "--from",
        "{domain_name}",
        "--to",
        "127.0.0.1:5000"
      ]
    ports:
      - "0.0.0.0:80:80"
      - "0.0.0.0:443:443"
    logging:
      options:
        max-size: "5m"
        max-file: "5"'''


with open("docker-compose.yaml","w") as compose_file:
    compose_file.write(render_yaml())