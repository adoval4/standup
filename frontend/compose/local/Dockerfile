FROM node:lts-alpine

WORKDIR /code

COPY ./frontend/package*.json ./

RUN npm install

COPY ./frontend/ .

EXPOSE 8080
CMD ["npm", "run", "dev"]