# Use OpenJDK base image
FROM openjdk:17-jdk-slim

# Set working directory inside the container
WORKDIR /app

# Copy WebGoat 8.2 JAR file into the container
COPY webgoat-server-8.2.2.jar /app/WebGoat.jar

# Expose WebGoat default port
EXPOSE 8080

# Run WebGoat when the container starts
#CMD ["java", "-jar", "/app/WebGoat.jar"]

CMD ["sh", "-c", "java -jar /app/WebGoat.jar & sleep infinity","--server.port=8080","--server.address=0.0.0.0"]

