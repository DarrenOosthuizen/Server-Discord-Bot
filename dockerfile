# Stage 1
FROM python:3.6.1-alpine
RUN pip install --upgrade pip
RUN pip install wakeonlan
RUN apt-get install arping
RUN apk update
RUN apk add --no-cache gcc musl-dev linux-headers
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python","main.py"]
