# Project Architecture Overview

This document provides a high-level overview of the architecture and directory responsibilities for the **agridatahub** FastAPI backend.

## Directory Responsibilities

- **app/configuration/**  
  Handles application configuration, environment variables, and settings management. Centralizes all configuration logic for easy access and modification.

- **app/controllers/**  
  (Optional) Contains controller logic for orchestrating complex request flows. Useful for larger or more complex applications.

- **app/dal/**  
  Data Access Layer. Responsible for interacting with external data sources (APIs, databases, etc.).  
  - **api_clients/**: Contains client classes for communicating with external APIs.

- **app/endpoints/**  
  Defines FastAPI routers and API endpoints. Responsible for exposing application functionality to clients and delegating business logic to services.

- **app/exceptions/**  
  Contains custom exception classes and global exception handlers for consistent error management across the application.

- **app/helpers/**  
  Houses helper functions and utilities that provide reusable logic (e.g., date parsing, formatting).

- **app/models/**  
  Defines core business/domain models using Pydantic.  
  - **models.py**: Main data structures representing entities (e.g., Crop, Farmer, Field).
  - **schema/request/**: Pydantic schemas for request validation.
  - **schema/response/**: Pydantic schemas for response serialization.

- **app/repositories/**  
  Implements repository classes for database operations (CRUD). Abstracts data persistence and retrieval logic for each entity.

- **app/services/**  
  Contains business logic and orchestration services. Coordinates data fetching, processing, and storage by utilizing API clients, repositories, and models.

- **app/setup/**  
  Handles application initialization code, such as startup events and dependency injection setup.

- **app/static/**  
  Stores static files (images, CSS, JS, etc.) for serving with the application.

- **app/templates/**  
  Contains HTML templates for server-side rendering, if needed.

- **app/tests/**  
  Organizes all tests for the application.
  - **unit/**: Unit tests for individual components.
  - **integration/**: Integration tests covering interactions between components and end-to-end flows.

- **app/utils/**  
  General utility modules and shared functions that are used across the application.

- **app/main.py**  
  The FastAPI application entrypoint.

- **builds/**  
  Contains deployment and build scripts (e.g., Dockerfiles, Kubernetes manifests).

- **.env**  
  Environment variable definitions (never commit secrets to version control).

---

## Typical Data Flow Example

**Scenario:** Fetch data from an external API, store it in the local database, and expose it via an API endpoint.

1. **API Client (`app/dal/api_clients/`)**  
   - Implements logic to connect to the external API and fetch raw data.

2. **Service (`app/services/`)**  
   - Calls the API client to fetch data.
   - Processes and validates the data using Pydantic models.
   - Calls the repository to store the data in the local database.

3. **Repository (`app/repositories/`)**  
   - Handles CRUD operations for storing and retrieving data from the database.

4. **Endpoint (`app/endpoints/`)**  
   - Defines the API route for clients to trigger the process or retrieve stored data.
   - Uses request/response schemas for input validation and output serialization.

5. **Models & Schemas (`app/models/`)**  
   - Used throughout the process for data validation, serialization, and type safety.

---

## Summary Table

| Directory                      | Responsibility                                              |
|---------------------------------|------------------------------------------------------------|
| configuration/                  | App settings and environment management                    |
| controllers/                    | (Optional) Request orchestration                           |
| dal/                            | Data access and external API clients                       |
| endpoints/                      | FastAPI routers and API endpoints                          |
| exceptions/                     | Custom exceptions and error handlers                       |
| helpers/                        | Helper functions and utilities                             |
| models/                         | Business/domain models and Pydantic schemas                |
| repositories/                   | Database CRUD operations                                   |
| services/                       | Business logic and orchestration                           |
| setup/                          | App initialization and dependency injection                |
| static/                         | Static files                                               |
| templates/                      | HTML templates                                             |
| tests/                          | Unit and integration tests                                 |
| utils/                          | General utilities                                          |
| main.py                         | FastAPI app entrypoint                                     |
| builds/                         | Deployment/build scripts                                   |
| .env                            | Environment variables                                      |

---

## Best Practices

- Maintain clear separation of concerns between layers.
- Use Pydantic models and schemas for all data validation and serialization.
- Keep business logic in services, not in endpoints or repositories.
- Use repositories to abstract all database interactions.
- Write unit and integration tests for all critical components.
- Document each directory’s purpose in its `__init__.py` and in this architecture file.

---