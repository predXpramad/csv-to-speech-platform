FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --no-fund --no-audit

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
