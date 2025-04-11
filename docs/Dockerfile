
FROM nginx:alpine

# Copy prebuilt Sphinx docs from syntax_folder/ into NGINX web root
COPY docs/syntax_folder /usr/share/nginx/html

# Custom NGINX config
COPY docs/nginx/default.conf /etc/nginx/templates/default.conf.template