# Use Node for the frontend
FROM node:22

# Set work directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project
COPY . .

# Expose the port Vue runs on
EXPOSE 5173

# Start the development server
CMD ["npm", "run", "dev", "--", "--host"]