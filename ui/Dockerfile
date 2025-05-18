# Stage 1: Install dependencies
FROM node:22.15.1 AS dependencies
WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn install

# Stage 2: Build the application
FROM node:22.15.1 AS builder
WORKDIR /usr/src/app
COPY --from=dependencies /usr/src/app/node_modules ./node_modules
COPY . .
RUN yarn build

# Stage 3: Run the application
FROM node:22.15.1 AS runner
WORKDIR /usr/src/app
ENV NODE_ENV=production
COPY --from=builder /usr/src/app ./
EXPOSE 3000
CMD ["yarn", "start"]