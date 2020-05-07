FROM      python:3.8.2
ENV       PYTHONUNBUFFERED 1

RUN       mkdir /app
WORKDIR   /app
COPY      ./code/requirements.txt /app/
RUN       pip install -r requirements.txt
COPY      ./code /app/

# define the default command to run when starting the container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_app.wsgi:application"]
