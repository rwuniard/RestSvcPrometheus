# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Spring Boot 3.5.4 web application (RestSvcPrometheus) configured as a WAR deployment using Java 17. The project appears to be a minimal Spring Boot starter focused on REST services with potential Prometheus integration (indicated by the name).

## Build System & Commands

### Maven Commands
- **Build project**: `./mvnw clean compile`
- **Run application**: `./mvnw spring-boot:run`
- **Run tests**: `./mvnw test`
- **Package WAR**: `./mvnw clean package`
- **Run specific test**: `./mvnw test -Dtest=RestSvcPrometheusApplicationTests`

### Development Server
The application runs on the default Spring Boot port (8080) and can be started with `./mvnw spring-boot:run`.

## Architecture

### Project Structure
- **Main application class**: `RestSvcPrometheusApplication.java` - Standard Spring Boot entry point
- **WAR deployment**: Configured with `ServletInitializer.java` for traditional servlet container deployment
- **Package structure**: `org.rw.restsvcprometheus`
- **Build artifacts**: Packaged as WAR file for servlet container deployment

### Technology Stack
- Spring Boot 3.5.4 (web starter)
- Java 17
- Maven build system
- JUnit 5 for testing
- Tomcat (provided scope for WAR deployment)

### Configuration
- Application configuration in `application.properties`
- Application name: `RestSvcPrometheus`
- WAR packaging for deployment to external servlet containers

## Development Notes

### Current State
This is a minimal Spring Boot project generated from Spring Initializr with:
- Spring Web dependency
- WAR packaging
- Basic test structure in place

### Key Files
- `pom.xml`: Maven configuration with Spring Boot parent and web dependencies
- `RestSvcPrometheusApplication.java`: Main Spring Boot application class
- `ServletInitializer.java`: WAR deployment configuration
- `RestSvcPrometheusApplicationTests.java`: Basic context loading test

The project name suggests Prometheus integration but no Prometheus dependencies are currently configured.