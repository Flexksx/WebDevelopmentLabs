# Scrapper Assignment Description

## Deadline
- **Due Date**: 18.10.2024 (2 weeks from the start date)

## Objectives
1. Understand web scraping.
2. Learn the fundamentals of HTTP/S protocol.
3. Gain insight into the TCP transport layer.
4. Practice serialization/deserialization techniques.
5. Explore Docker basics.

## Grade Conditions

1. **Existence**: Ensure all tasks are implemented.
2. **HTTP GET Request**:
   - Select an e-commerce website (e.g., 999.md, darwin.md, smart.md, asos.com).
   - Send an HTTP GET request and receive a valid HTML response.
3. **HTML Parsing**:
   - Extract product name (string) and price (int) using an HTML parser.
4. **Product Link Scraping**:
   - Extract product links and scrape additional details (e.g., color).
5. **Data Validation**:
   - Implement two validations (e.g., remove whitespace, ensure price is an integer).
6. **Functional Programming**:
   - Use `Map`, `Filter`, and `Reduce`:
     - Convert prices to EUR (or MDL if already in EUR).
     - Filter products within a specific price range.
     - Calculate the sum of filtered prices.
     - Attach the sum and a UTC timestamp to the new data model.
7. **TCP Socket Request**:
   - Use a TCP socket instead of an HTTP library to send requests and process the response.
8. **Custom Serialization**:
   - Serialize data models to JSON and XML manually (without libraries).
   - Log/print the serialized data.
9. **Custom Format Serialization**:
   - Create and implement a custom serialization and deserialization technique.
10. **Docker Integration**:
    - Install Docker and run a provided HTTP server using `docker-compose.yml`.

## Docker Steps
1. Ensure Docker is installed.
2. Create a `docker-compose.yml` file with the following:
   ```yaml
   version: '3.8'
   services:
     lab1-http-server:
       image: nicug/server-pr-lab1:latest
       ports:
         - "8000:8000"
       environment:
         - PORT=8000
