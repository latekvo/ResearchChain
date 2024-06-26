FROM node:22-bookworm-slim

WORKDIR /app

COPY /webui/frontend /app

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]




