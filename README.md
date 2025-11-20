## Team 222 | Ohjelmistotuotanto Miniproject

[![CI](https://github.com/mistablasta/ohtu-miniprojekti/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/mistablasta/ohtu-miniprojekti/actions/workflows/ci.yaml)  |   [Backlog](https://docs.google.com/spreadsheets/d/1Wal9lf7m1hLwKvrNIfiCST6wdOhEhACKW7qlMtfY_5g/edit?usp=sharing)

## Definition of Done
These are the requirements for each feature branch before merging into the **main** branch.

- Appropriate tests are done and passing
- The feature is fully documented
- Correctly integrated into the rest of the project

## Standards

These are standards to be applied when working on this project

- Commits have to be small enough
- Commits have to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format

## Production
This project is deployed at https://olisipa.beer/ on a personal VPS using Docker Compose (process described below).
Works by rebuilding on commits to the main branch.

## Docker
You can spin this project up using Docker Compose.

### Setup
1. Make sure you have Docker installed and Docker Engine running.
2. *(Optional)* If you wish to modify the default environment variables defined in `docker-compose.yml`, then create a `.env` file in the root of the project with the following contents:
    
   ```dotenv
    POSTGRES_PASSWORD=test
    POSTGRES_USER=test
    POSTGRES_DB=test
    DATABASE_URL=postgresql://test:test@database:5432/test
    SECRET_KEY=very secret
   ```

3. In the root of the project, run

    ```bash
    docker-compose up -d --build
    ```

4. Both a PostgreSQL database and the application should now be running.

    The app will be available at http://127.0.0.1:5001/

### Possible Issues

* Docker Compose may not have access to `src/schema.sql`. Fixed by making it readable by everyone:

    ```bash
    sudo chmod 644 ./src/schema.sql
    ```

* Docker Compose may not work with a non-root user on Linux on a fresh installation. Follow this guide to fix:

  https://docs.docker.com/engine/install/linux-postinstall

### Usage
| Command                      | Description                                                                     |
|------------------------------|---------------------------------------------------------------------------------|
| docker-compose up            | Start all services                                                              |
| docker-compose up -d --build | Rebuild and start all services in the background (useful when code has changed) |
| docker-compose down          | Stop all services                                                               |
| docker-compose down -v       | Stop all services and delete their volume data (useful for clearing the db)     |
| docker-compose logs          | See the logs of both services                                                   |