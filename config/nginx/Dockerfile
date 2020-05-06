FROM      nginx
COPY      nginx.conf /etc/nginx/nginx.conf
COPY      static_collected /usr/share/nginx/html/static
RUN       rm -f /usr/share/nginx/html/*.html

# RUN       rm -f /etc/nginx/conf.d/default.conf
# COPY      conf.d/web_app.conf /etc/nginx/conf.d/web_app.conf
#
# COPY      static_collected /usr/share/nginx/html/static
#
# RUN       ls -l /etc/nginx/nginx.conf
# RUN       ls -l /etc/nginx/conf.d
# RUN       ls -l /usr/share/nginx/html/static
