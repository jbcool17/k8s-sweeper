# Testing Sweeper

This project uses `kwok` to simulate a Kubernetes cluster for testing purposes. The test environment is managed via Docker.

## Running Tests

The following command will build the test Docker image, start a `kwok` cluster inside it, and run the test script.

```bash
make docker-test-run
```
