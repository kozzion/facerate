FROM continuumio/anaconda3

RUN apt-get update
RUN apt-get install build-essential cmake -y
RUN apt-get install libopenblas-dev liblapack-dev -y

RUN pip install --upgrade pip
# this next can one take about 8 minutes on t2.medium instance
RUN pip install dlib
RUN pip install face_recognition

# Set the working directory to /root
WORKDIR /root/

# Copy the current directory contents into the container at /root
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["bash", "startsystem.sh"]
