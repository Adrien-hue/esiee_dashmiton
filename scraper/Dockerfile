# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run scrapy command
CMD ["scrapy", "crawl", "marmiton_home", "-O", "/path/to/dashboard/recipes.json"]
