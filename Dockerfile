FROM continuumio/anaconda3

# Set the working directory to /root
WORKDIR /root/

# Copy the current directory contents into the container at /root
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80


CMD ["bash", "startsystem.sh"]




