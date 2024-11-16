# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /home/ubuntu/asklepios/Backend/create_Database_part
#WORKDIR /app

#set envs
# e.g.
# docker build --build-arg CHROMA_PATH="../data/guidelines" --build-arg DATA_PATH="../data/guidelines" -t asklepios-db .
ARG CHROMA_PATH
ARG DATA_PATH
ENV CHROMA_PATH=${CHROMA_PATH}
ENV DATA_PATH=${DATA_PATH}

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Command to run the FlaskAPI app
CMD ["python3", "populate_database.py"]