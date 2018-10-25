#!/bin/bash

domains="${DOMAIN},www.${DOMAIN}"

cert_dir="/etc/letsencrypt/live/${DOMAIN}"
echo "$cert_dir"

mkdir -p /var/nginx
ln -s "${cert_dir}" /var/nginx/certificates

/opt/certbot certonly \
    --standalone \
    --non-interactive \
    --domains "${domains}" \
    --config config/letsencrypt/config.ini \
    --agree-tos \
    --pre-hook "supervisorctl stop nginx" \
    --post-hook "supervisorctl start nginx"
