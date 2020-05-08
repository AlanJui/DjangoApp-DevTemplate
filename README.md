# 使用 Docker Compose 建置 Django App

【參考文件】：

http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html

https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

# 系統架構

Django App 上線時之系統架構：

![docker1](http://pawamoy.github.io/assets/docker1.png)

結合「網路層」之系統架構：

![docker3](http://pawamoy.github.io/assets/docker3.png)

結合「Docker Compose」後之系統架構：

![docker4](http://pawamoy.github.io/assets/docker4.png)

# 專案資料結構

```
    《ProjectDir》
    ├── code
    │   ├── .venv
    │   ├── log_msg
    │   ├── static_collected
    │   ├── web_app
    │   ├── .python-version
    │   ├── manage.py
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   └── requirements.txt
    ├── config
    │   └── nginx
    │       ├── Dockerfile
    │       └── nginx.conf
    ├── .gitignore
    ├── docker-compose.yml
    ├── Dockerfile
    └── README.md

```

# Django App 資料夾結構

## 高階資料夾結構

```
    code
    ├── Pipfile
    ├── Pipfile.lock
    ├── log_msg
    ├── manage.py
    ├── requirements.txt
    ├── static_collected
    └── web_app
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

## 重要檔案

```
    code
    ├── Pipfile
    ├── Pipfile.lock
    ├── log_msg
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── ⋯⋯
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── static
    │   │   └── hello
    │   │       └── site.css
    │   ├── templates
    │   │   └── log_msg
    │   │       ├── about.html
    │   │       ├── contact.html
    │   │       ├── hello_there.html
    │   │       ├── home.html
    │   │       ├── layout.html
    │   │       └── log_message.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── requirements.txt
    ├── static_collected
    │   ├── admin
    │   │   ├── css
    │   │   │   ├── ⋯⋯
    │   │   │   └── ⋯⋯
    │   │   ├── fonts
    │   │   │   ├── ⋯⋯
    │   │   │   └── ⋯⋯
    │   │   ├── img
    │   │   │   ├── ⋯⋯
    │   │   │   └── ⋯⋯
    │   │   └── js
    │   │       ├── ⋯⋯
    │   │       └── ⋯⋯
    │   └── log_msg
    │       └── site.css
    └── web_app
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

# docker-compose 開發環境基本操作

## 建置開發環境

### （1）啟動開發環境

    $ docker-compose up -d --build

### （2）確認每個 Docker 容器均已啟動

    $ docker-compose ps
              Name                          Command               State           Ports
    ---------------------------------------------------------------------------------------------
    docker-compose-02_adminer_1   entrypoint.sh docker-php-e ...   Up      0.0.0.0:8080->8080/tcp
    docker-compose-02_db_1        docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
    docker-compose-02_proxy_1     nginx -g daemon off;             Up      0.0.0.0:5000->80/tcp
    docker-compose-02_web_1       gunicorn --bind 0.0.0.0:80 ...   Up      0.0.0.0:8000->8000/tcp

### （3）初始化資料庫

    $ docker-compose exec web python manage.py migrate
    Operations to perform:
      Apply all migrations: admin, auth, contenttypes, log_msg, sessions
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying auth.0010_alter_group_name_max_length... OK
      Applying auth.0011_update_proxy_permissions... OK
      Applying log_msg.0001_initial... OK
      Applying sessions.0001_initial... OK

### （4）建立後台管理員帳號

      $ docker-compose exec web python manage.py createsuperuser
      Username (leave blank to use 'root'): admin
      Email address:
      Password:
      Password (again):
      Superuser created successfully.

### （5）搜集「靜態檔案」

      $ docker-compose exec web python manage.py collectstatic --clear --no-input

      You have requested to collect static files at the destination
      location as specified in your settings:

          /app/static_collected

      This will DELETE ALL FILES in this location!
      Are you sure you want to do this?

      Type 'yes' to continue, or 'no' to cancel: yes
      Deleting 'admin/fonts/LICENSE.txt'
      ......
      Deleting 'admin/img/gis/move_vertex_on.svg'
      Deleting 'log_msg/test.png'
      Deleting 'log_msg/log_msg.css'

      132 static files copied to '/app/static_collected'.

### （6）瀏覽網頁驗證 Web App 已能正常運作

    http://localhost:5000/

# 各種疑難雜症排解

## PostgreSQL 基本操作

### 自 postgres 影象檔產生 docker 容器

    $ docker run --name postgres-12 -e POSTGRES_PASSWORD=Passw0rd -d postgres

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
    1349636c5389        postgres            "docker-entrypoint.s…"   4 seconds ago       Up 3 seconds        5432/tcp            postgres-12

### 要求 docker 容器執行 bash 指令

    $ docker exec -it postgres-12 /bin/bash

    root@ed337d648dea:/# su - postgres

    postgres@ed337d648dea:/# psql -h localhost -U postgres -W -d postgres

## 檢視 docker volume 容器中存放的檔案

    $ docker run --rm -i -v=docker-compose-02_staticfiles_volume:/tmp/myvolume busybox find /tmp/myvolume
    /tmp/myvolume
    /tmp/myvolume/admin
    /tmp/myvolume/admin/fonts
    /tmp/myvolume/admin/fonts/LICENSE.txt
    /tmp/myvolume/admin/fonts/Roboto-Regular-webfont.woff
    /tmp/myvolume/admin/fonts/Roboto-Bold-webfont.woff
    /tmp/myvolume/admin/fonts/Roboto-Light-webfont.woff
    /tmp/myvolume/admin/fonts/README.txt
    /tmp/myvolume/admin/css
    /tmp/myvolume/admin/css/login.css
    /tmp/myvolume/admin/css/autocomplete.css
    /tmp/myvolume/admin/css/vendor
    /tmp/myvolume/admin/css/vendor/select2
    /tmp/myvolume/admin/css/vendor/select2/select2.min.css
    /tmp/myvolume/admin/css/vendor/select2/LICENSE-SELECT2.md
    /tmp/myvolume/admin/css/vendor/select2/select2.css
    /tmp/myvolume/admin/css/dashboard.css
    /tmp/myvolume/admin/css/rtl.css
    /tmp/myvolume/admin/css/changelists.css
    /tmp/myvolume/admin/css/responsive_rtl.css
    /tmp/myvolume/admin/css/responsive.css
    /tmp/myvolume/admin/css/base.css
    /tmp/myvolume/admin/css/fonts.css
    /tmp/myvolume/admin/css/forms.css
    /tmp/myvolume/admin/css/widgets.css
    /tmp/myvolume/admin/js
    /tmp/myvolume/admin/js/admin
    /tmp/myvolume/admin/js/admin/DateTimeShortcuts.js
    /tmp/myvolume/admin/js/admin/RelatedObjectLookups.js
    /tmp/myvolume/admin/js/actions.min.js
    /tmp/myvolume/admin/js/SelectBox.js
    /tmp/myvolume/admin/js/popup_response.js
    /tmp/myvolume/admin/js/prepopulate.min.js
    /tmp/myvolume/admin/js/prepopulate_init.js
    /tmp/myvolume/admin/js/inlines.min.js
    /tmp/myvolume/admin/js/SelectFilter2.js
    /tmp/myvolume/admin/js/vendor
    /tmp/myvolume/admin/js/vendor/jquery
    /tmp/myvolume/admin/js/vendor/jquery/jquery.js
    /tmp/myvolume/admin/js/vendor/jquery/LICENSE.txt
    /tmp/myvolume/admin/js/vendor/jquery/jquery.min.js
    /tmp/myvolume/admin/js/vendor/xregexp
    /tmp/myvolume/admin/js/vendor/xregexp/xregexp.js
    /tmp/myvolume/admin/js/vendor/xregexp/xregexp.min.js
    /tmp/myvolume/admin/js/vendor/xregexp/LICENSE.txt
    /tmp/myvolume/admin/js/vendor/select2
    /tmp/myvolume/admin/js/vendor/select2/i18n
    /tmp/myvolume/admin/js/vendor/select2/i18n/cs.js
    ⋯⋯
    /tmp/myvolume/admin/js/vendor/select2/i18n/zh-TW.js
    ⋯⋯
    /tmp/myvolume/admin/js/vendor/select2/select2.full.js
    /tmp/myvolume/admin/js/vendor/select2/select2.full.min.js
    /tmp/myvolume/admin/js/vendor/select2/LICENSE.md
    /tmp/myvolume/admin/js/prepopulate.js
    /tmp/myvolume/admin/js/calendar.js
    /tmp/myvolume/admin/js/urlify.js
    /tmp/myvolume/admin/js/autocomplete.js
    /tmp/myvolume/admin/js/inlines.js
    /tmp/myvolume/admin/js/collapse.js
    /tmp/myvolume/admin/js/actions.js
    /tmp/myvolume/admin/js/change_form.js
    /tmp/myvolume/admin/js/jquery.init.js
    /tmp/myvolume/admin/js/cancel.js
    /tmp/myvolume/admin/js/collapse.min.js
    /tmp/myvolume/admin/js/core.js
    /tmp/myvolume/admin/img
    /tmp/myvolume/admin/img/icon-deletelink.svg
    /tmp/myvolume/admin/img/icon-addlink.svg
    /tmp/myvolume/admin/img/icon-no.svg
    /tmp/myvolume/admin/img/icon-unknown-alt.svg
    /tmp/myvolume/admin/img/tooltag-arrowright.svg
    /tmp/myvolume/admin/img/gis
    /tmp/myvolume/admin/img/gis/move_vertex_off.svg
    /tmp/myvolume/admin/img/gis/move_vertex_on.svg
    /tmp/myvolume/admin/img/tooltag-add.svg
    /tmp/myvolume/admin/img/selector-icons.svg
    /tmp/myvolume/admin/img/icon-clock.svg
    /tmp/myvolume/admin/img/icon-changelink.svg
    /tmp/myvolume/admin/img/calendar-icons.svg
    /tmp/myvolume/admin/img/icon-unknown.svg
    /tmp/myvolume/admin/img/inline-delete.svg
    /tmp/myvolume/admin/img/LICENSE
    /tmp/myvolume/admin/img/icon-calendar.svg
    /tmp/myvolume/admin/img/icon-yes.svg
    /tmp/myvolume/admin/img/README.txt
    /tmp/myvolume/admin/img/icon-viewlink.svg
    /tmp/myvolume/admin/img/search.svg
    /tmp/myvolume/admin/img/sorting-icons.svg
    /tmp/myvolume/admin/img/icon-alert.svg
    /tmp/myvolume/log_msg
    /tmp/myvolume/log_msg/test.png
    /tmp/myvolume/log_msg/log_msg.css


    $ docker volume inspect docker-compose-02_staticfiles_volume
    [
        {
            "CreatedAt": "2020-05-04T02:15:36Z",
            "Driver": "local",
            "Labels": {
                "com.docker.compose.project": "docker-compose-02",
                "com.docker.compose.version": "1.25.4",
                "com.docker.compose.volume": "staticfiles_volume"
            },
            "Mountpoint": "/var/lib/docker/volumes/docker-compose-02_staticfiles_volume/_data",
            "Name": "docker-compose-02_staticfiles_volume",
            "Options": null,
            "Scope": "local"
        }
    ]

# 各種設定檔參考資料

### nginx 預設的 default.conf

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;
        #access_log  /var/log/nginx/host.access.log  main;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;                                                                                                 [14/1631]
        location = /50x.html {
            root   /usr/share/nginx/html;
        }

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }

### ./docker-compose.yml

    version: '3'

    services:

      db:
        image: postgres
        restart: always
        ports:
          - 5432:5432
        environment:
          - POSTGRES_DB=web_app_dev_db
          - POSTGRES_USER=web_app_user
          - POSTGRES_PASSWORD=Passw0rd
        volumes:
          - postgres_data_volume:/var/lib/postgresql/data/

      adminer:
        image: adminer
        restart: always
        ports:
          - 8080:8080

      web:
        build: .
        ports:
          - 8000:8000
        volumes:
          - ./code:/app
          - static_files_volume:/app/static_collected/
        depends_on:
          - db

      proxy:
        build: ./config/nginx
        volumes:
          - static_files_volume:/usr/share/nginx/html/static/
        ports:
          - 5000:80
        depends_on:
          - web

    volumes:
      static_files_volume:
      postgres_data_volume:

### ./code/web_app/settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'web_app_dev_db',
            'USER': 'web_app_user',
            'PASSWORD': 'Passw0rd',
            'HOST': 'db',
            'PORT': 5432,
        }
    }

### ./Dockerfile

    FROM      python:3.8.2
    ENV       PYTHONUNBUFFERED 1

    RUN       mkdir /app
    WORKDIR   /app
    COPY      ./code /app/
    RUN       pip install -r requirements.txt

    # define the default command to run when starting the container
    CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_app.wsgi:application"]

### ./config/nginx/Dockerfile

    FROM      nginx
    COPY      nginx.conf /etc/nginx/nginx.conf
    COPY      static_collected /usr/share/nginx/html/static
    RUN       rm -f /usr/share/nginx/html/*.html

### ./config/nginx/nginx.conf

    user  nginx;
    worker_processes  1;

    error_log  /var/log/nginx/error.log warn;
    pid        /var/run/nginx.pid;


    events {
        worker_connections  1024;
    }


    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /var/log/nginx/access.log  main;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;


        upstream web_server {
            # docker will automatically resolve this to the correct address
            # because we use the same name as the service: "django_app"
            server web:8000;
        }

        #include /etc/nginx/conf.d/*.conf;
        server {
            listen       80;
            server_name  localhost;

            #charset koi8-r;
            charset utf-8;
            client_max_body_size 75M;
            access_log /var/log/nginx/host.access.log  main;

            # location / {
            #     root   /usr/share/nginx/html;
            #     index  index.html index.htm;
            # }

            location / {
                # everything is passed to Gunicorn
                proxy_pass http://web_server;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $host;
                proxy_redirect off;
            }

            location /static {
                alias /usr/share/nginx/html/static;
            }

            location /media {
                alias /usr/share/nginx/html/media;
            }


            #error_page  404              /404.html;

            # redirect server error pages to the static page /50x.html
            #
            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   /usr/share/nginx/html;
            }
        }
    }
