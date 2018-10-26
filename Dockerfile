FROM continuumio/anaconda3

# Set the working directory to /root
WORKDIR /root/

# Copy the current directory contents into the container at /root
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

RUN apt-get update
RUN apt-get install build-essential cmake
RUN apt-get install libopenblas-dev liblapack-dev 
RUN pip install --upgrade pip

#RUN pip install dlib
#RUN pip install face_recognition

CMD ["bash", "startsystem.sh"]




