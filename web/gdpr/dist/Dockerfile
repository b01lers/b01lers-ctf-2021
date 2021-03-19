FROM node:alpine3.10

RUN mkdir server_files

WORKDIR /server_files
COPY package-lock.json package.json ./
RUN npm install

COPY index.js index.html comic_sans.woff comic_sans.woff2 ./

#CMD ["/bin/node /server_files/index.js"]
CMD ["/bin/sh"]
