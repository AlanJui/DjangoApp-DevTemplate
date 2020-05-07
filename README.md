# 使用 Docker Compose 建置 Django App

【參考文件】：

http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html

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
    ├── Dockerfile
    ├── Vagrantfile
    ├── bootstrap.sh
    ├── code
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── hello
    │   ├── manage.py
    │   ├── requirements.txt
    │   ├── static_collected
    │   ├── uwsgi.ini
    │   └── web_project
    ├── config
    └── install-python.sh

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

## 啟動 DB 容器

啟動 Postgres 容器：

    $ docker run --name db -p 5433:5433 -e POSTGRES_PASSWORD=Passw0rd -d postgres


    $ docker ps

    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
    0c6e4509748a        postgres            "docker-entrypoint.s…"   6 seconds ago       Up 5 seconds        5432/tcp            db

## 啟動 Django App 容器

### 產生 Python 套件安裝檔

自 Django App 專案產生「套件安裝檔（requirements.txt）」。

```
    cd code
    pipenv shell
    pipenv lock --requirements > requirements.txt
```

## 製作 Dockerfile

Dockerfile 容器設定：

```
    FROM      python:3.8.2
    ENV       PYTHONUNBUFFERED 1
    RUN       mkdir /app
    WORKDIR   /app
    COPY      ./code/requirements.txt /app/
    RUN       pip install -r requirements.txt
    COPY      ./code /app/

    # define the default command to run when starting the container
    CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_app.wsgi:application"]
```

## 建置 Docker 容器

進入《專案根目錄》，透過指令建置 Django App 的 Docker 容器：

    docker build -t my_app .

驗證 Django App 的 Docker 容器已能正常運作：

（1）啟動 web 容器：

    $ docker run --name web -p 8000:8000 -d my_app
    $ docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
3e8e15b72d58 my_app "gunicorn --bind 0.0…" 4 seconds ago Up 3 seconds 0.0.0.0:8000->8000/tcp web
0c6e4509748a postgres "docker-entrypoint.s…" 5 minutes ago Up 5 minutes 5432/tcp db

（2）自 web 容器，執行 django 指令：

    $ docker exec -it web python manage.py migrate
    Operations to perform:
      Apply all migrations: admin, auth, contenttypes, hello, sessions
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
      Applying hello.0001_initial... OK
      Applying sessions.0001_initial... OK

    $ docker exec -it web python manage.py createsuperuser
    Username (leave blank to use 'root'): admin
    Email address:
    Password:
    Password (again):
    Superuser created successfully.

    $ docker exec -it web python manage.py collectstatic

    You have requested to collect static files at the destination
    location as specified in your settings:

        /opt/services/django_app/src/static_collected

    This will overwrite existing files!
    Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: yes

    130 static files copied to '/opt/services/django_app/src/static_collected', 1 unmodified.

（3）瀏覽 http://localhost:8000

（4）回到 Terminal（2）視窗，終止 Docker 容器運作

    $ docker stop my_app
    my_app

    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS               NAMES
    e6d79945d14e        my_django_img       "gunicorn --chdir . …"   16 minutes ago      Exited (0) 32 seconds ago                        my_app

    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    my_django_img       latest              bfeccafa4be7        20 minutes ago      985MB

（5）重新啟動 Docker 容器（my_app）

    $ docker start my_app
    my_app

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
    e6d79945d14e        my_django_img       "gunicorn --chdir . …"   22 minutes ago      Up 6 seconds        0.0.0.0:8000->8000/tcp   my_app

（6）瀏覽 http://localhost:8000

（7）再次終止 Docker 容器

    $ docker stop my_app

# docker-compose

    $ docker-compose build

    $ docker-compose run --rm app /bin/bash
    root@44f2a65aa0fe:/opt/services/django_app/src# psql -h localhost -U postgres
    psql: error: could not connect to server: could not connect to server: Connection refused
            Is the server running on host "localhost" (127.0.0.1) and accepting
            TCP/IP connections on port 5432?
    could not connect to server: Cannot assign requested address
            Is the server running on host "localhost" (::1) and accepting
            TCP/IP connections on port 5432?
    root@8d35d83ebf04:/#





    $ docker-compose build

    $ docker-compose run --rm db1 /bin/bash
    root@8d35d83ebf04:/# which psql
    /usr/bin/psql
    root@8d35d83ebf04:/#







    $ docker-compose build

    $ docker-compose up

    $ docker-compose ps
         Name                   Command               State     Ports
    -------------------------------------------------------------------
    test-101_app_1   gunicorn --chdir . --bind  ...   Up       8000/tcp
    test-101_db1_1   docker-entrypoint.sh postgres    Up       5432/tcp
    test-101_web_1   nginx -g daemon off;             Exit 1

    $ docker-compose run app bash
    Starting test-101_db1_1 ... done
    root@adcabbb9cb0f:/opt/services/django_app/src# python manage.py migrate




    alanjui@MBP-2018:~/workspace/vagrant/test-101 (master)
    $ docker-compose run app python manage.py shell
    Starting test-101_db1_1 ... done
    Python 3.8.2 (default, Apr 23 2020, 14:22:33)
    [GCC 8.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>>
    now exiting InteractiveConsole...

    alanjui@MBP-2018:~/workspace/vagrant/test-101 (master)
    $




    docker-compose run --rm app python manage.py db1 upgrade



    alanjui@MBP-2018:~/workspace/vagrant/test-101 (master)
    $ docker-compose run db1 psql -h localhost -U postgres
    psql: could not connect to server: Connection refused
    Is the server running on host "localhost" (127.0.0.1) and accepting
    TCP/IP connections on port 5432?
    could not connect to server: Cannot assign requested address
    Is the server running on host "localhost" (::1) and accepting
    TCP/IP connections on port 5432?

## PostgreSQL Service

    $ docker run --name postgres-12 -e POSTGRES_PASSWORD=Passw0rd -d postgres

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
    1349636c5389        postgres            "docker-entrypoint.s…"   4 seconds ago       Up 3 seconds        5432/tcp            postgres-12




    docker run --name postgres_bash --rm -i -t postgres bash
    docker exec -d postgres_bash touch /tmp/execWorks


    docker exec -it postgres_bash bash





    root@ed337d648dea:/# service postgresql start
    [warn] No PostgreSQL clusters exist; see "man pg_createcluster" ... (warning).



    root@ed337d648dea:/# /etc/init.d/postgresql start
    [warn] No PostgreSQL clusters exist; see "man pg_createcluster" ... (warning).




    $ service postgresql status

# 各種疑難雜症排解

檢視 docker volume 容器中存放的檔案

    docker run --rm -i -v=docker-compose-02_staticfiles_volume:/tmp/myvolume busybox find /tmp/myvolume
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

# nginx

## nginx 預設的 default.conf

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
