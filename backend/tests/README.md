# Backend Tests

This directory contains comprehensive tests for all Python files in the backend application.

## Structure

Tests are organized following the layered architecture of the application:

```
tests/
├── infrastructure/       # Infrastructure layer tests
├── domain/              # Domain layer tests
│   ├── model/          # Domain model tests
│   └── service/        # Domain service tests
├── application/         # Application layer tests
│   └── exception/      # Application exception tests
├── api/                # API layer tests
│   └── routes/         # API routes tests
└── test_main.py        # Main application tests
```

## Running Tests

### Install Test Dependencies

```bash
pip install -e ".[test]"
```

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Verbose Output

```bash
pytest tests/ -v
```

### Run Tests for a Specific Layer

```bash
# Infrastructure layer
pytest tests/infrastructure/

# Domain layer
pytest tests/domain/

# Application layer
pytest tests/application/

# API layer
pytest tests/api/
```

### Run a Specific Test File

```bash
pytest tests/infrastructure/test_csv_dataframe_loader.py -v
```

## Test Pattern

All tests follow the **Given-When-Then** pattern, explicitly documented via comments:

```python
def test_example(self):
    # Given
    # Setup test data and preconditions
    
    # When
    # Execute the functionality being tested
    
    # Then
    # Assert the expected outcomes
```

This pattern ensures tests are:
- Easy to read and understand
- Clear in their intent
- Consistent across the codebase

## Test Coverage

The test suite covers:

1. **Infrastructure Layer**
   - CSV data loading functionality
   - Dependency injection

2. **Domain Layer**
   - Fixed effects result model immutability
   - Fixed effects analysis service logic
   
3. **Application Layer**
   - Exception handling
   - Application service orchestration
   - Data validation and normalization
   
4. **API Layer**
   - Route handlers
   - Exception handlers
   - Request/response validation
   - Application initialization

## Layered Architecture Compliance

Tests respect the layered architecture:
- Infrastructure layer tests do not depend on higher layers
- Domain layer tests are independent and use pure domain logic
- Application layer tests use mocks for infrastructure dependencies
- API layer tests verify integration behavior

No unnecessary cross-layer coupling exists in tests.
