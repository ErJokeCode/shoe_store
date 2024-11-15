FROM node:16-alpine

ADD . /opt/client
WORKDIR /opt/client
RUN npm install

EXPOSE 3010

CMD ["npm", "start"]

