FROM python
FROM node

WORKDIR /app

COPY frontend/package.json ./
COPY frontend/package-log.json ./
COPY requirements.txt ./

RUN npm install
RUN npm run build
RUN python -m pip install -r requirements.txt

COPY . .

ENV port=8000

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
