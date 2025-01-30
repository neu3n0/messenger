FROM node:22

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 5173

# CMD ["npm", "start", "--", "--host", "0.0.0.0", "--disable-host-check"]
CMD ["npm", "run", "dev", "--", "--host"]