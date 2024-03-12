#########################################
# author: ashraf minhaj
# email : ashraf_minhaj@yahoo.com
# 
# date: 08-03-24
#########################################

# FROM --platform=linux/amd64 python:3.10 as builder
FROM python:3.10 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# runner stage
# FROM --platform=linux/amd64 python:3.10-slim as runner
FROM python:3.10-slim as runner

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY . .

# RUN useradd -m appmngr; chown appmngr:appmngr /app
# USER appmngr

EXPOSE 5001

CMD ["python", "main.py"]