# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Spring Boot 3.5.4 web application (RestSvcPrometheus) configured as a WAR deployment using Java 17. The project appears to be a minimal Spring Boot starter focused on REST services with potential Prometheus integration (indicated by the name).

## Build System & Commands

### Maven Commands
- **Build project**: `./mvnw clean compile`
- **Run application**: `./mvnw spring-boot:run`
- **Run tests**: `./mvnw test`
- **Run tests with coverage**: `./mvnw clean test` (generates JaCoCo report)
- **Package WAR**: `./mvnw clean package`
- **Run specific test**: `./mvnw test -Dtest=RestSvcPrometheusApplicationTests`

### Code Coverage
- **JaCoCo Plugin**: Version 0.8.13 (Java 24 compatible) with 80% line coverage threshold
- **Coverage Report**: Available at `target/site/jacoco/index.html` after running tests
- **Coverage Data**: Raw execution data in `target/jacoco.exec`

### Development Server
The application runs on the default Spring Boot port (8080) and can be started with `./mvnw spring-boot:run`.

### Load Testing Tools
Two CLI tools are provided for load testing the math API endpoint:

**Bash CLI (`math-cli.sh`)**:
- Simple bash script for basic load testing
- Usage: `./math-cli.sh <iterations> [base_url] [delay_seconds]`
- Default: 100 iterations, localhost:8080, 0.1s delay
- Examples:
  ```bash
  ./math-cli.sh 50                                    # 50 requests
  ./math-cli.sh 100 http://localhost:8080 0.2        # Custom URL and delay
  ```

**Python CLI (`math-cli.py`)**:
- Advanced Python script with detailed statistics and concurrent testing
- Usage: `./math-cli.py <iterations> [options]`
- Features: Custom formulas, concurrent requests, detailed metrics
- Examples:
  ```bash
  ./math-cli.py 10                                    # 10 requests, default formulas
  ./math-cli.py 50 --concurrent 5                    # 50 requests, 5 workers
  ./math-cli.py 20 --a-formula 'i*3' --b-formula 'i+5' # Custom formulas
  ./math-cli.py 100 --verbose                        # Show individual request details
  ```

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
- Micrometer Prometheus registry for metrics
- Spring Boot Actuator for metrics endpoints

### Configuration
- Application configuration in `application.properties`
- Application name: `RestSvcPrometheus`
- WAR packaging for deployment to external servlet containers

### Prometheus Metrics Integration
- **Metrics Endpoint**: `http://localhost:8080/actuator/prometheus`
- **Exposed Endpoints**: health, info, prometheus
- **Available Metrics**:
  - System metrics: `system_cpu_usage`, `system_load_average_1m`, `disk_free_bytes`
  - JVM metrics: `jvm_memory_used_bytes`, `jvm_gc_*`
  - HTTP metrics: `http_server_requests_seconds_count`, response times per endpoint
  - Custom business metrics for the math API endpoint

### API Endpoints
- **Math Addition**: `GET /api/math/add?a={int}&b={int}`
  - Returns the sum of parameters a and b
  - Automatically tracked in Prometheus metrics
  - Example: `curl "http://localhost:8080/api/math/add?a=5&b=3"` returns `8`

## Development Notes

### Current State
This is a Spring Boot project with:
- Spring Web dependency for REST API endpoints
- WAR packaging for external servlet container deployment
- Prometheus metrics integration with Micrometer
- JaCoCo code coverage reporting
- Comprehensive test structure with 100% coverage on business logic

### Key Files
- `pom.xml`: Maven configuration with Spring Boot parent, web, actuator, and Prometheus dependencies
- `RestSvcPrometheusApplication.java`: Main Spring Boot application class
- `ServletInitializer.java`: WAR deployment configuration
- `MathController.java`: REST controller with math addition endpoint
- `MathControllerTest.java`: Comprehensive tests for the math endpoint
- `math-cli.sh` / `math-cli.py`: CLI tools for load testing the API
- `application.properties`: Actuator and Prometheus configuration