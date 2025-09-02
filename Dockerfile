FROM  maven:3.9.6-eclipse-temurin-17  as build
WORKDIR /app
COPY pom.xml .
COPY src ./src
COPY settings.xml .
COPY userdata ./userdata
##RUN mvn clean package -DskipTests
RUN mvn -s settings.xml clean package -DskipTests install

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.war vprofile-v2.war
EXPOSE 8080
ENTRYPOINT [ "java", "-jar", "vprofile-v2.war" ]
