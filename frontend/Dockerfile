# Stage 1: Build the React application
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or npm-shrinkwrap.json)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the built application using a lightweight server
FROM node:18-alpine

WORKDIR /app

# Install 'serve' to serve static files
RUN npm install -g serve

# Copy the build output from the 'build' stage
COPY --from=build /app/dist /app/dist

# Expose port 3000 (or whatever port 'serve' will use by default or configured)
EXPOSE 3000

# Command to serve the 'dist' folder
# Adjust port if necessary, -l flag listens on a specific port
CMD ["serve", "-s", "dist", "-l", "3000"]
