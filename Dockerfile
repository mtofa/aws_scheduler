FROM python:3
RUN apt-get update && apt-get install -y sudo tzdata
RUN mkdir /code
ENV PYTHONUNBUFFERED 1
ENV DOCKERUP 1
ADD requirements.txt /code/
WORKDIR /code
ADD . /code/
ENV TZ=Australia/Adelaide
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Clean up
RUN apt-get remove -y --auto-remove
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache
RUN find . -name \*.pyc -delete

RUN pip install -r requirements.txt



