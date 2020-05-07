FROM      nginx
COPY      nginx.conf /etc/nginx/nginx.conf
COPY      static_collected /usr/share/nginx/html/static
RUN       rm -f /usr/share/nginx/html/*.html