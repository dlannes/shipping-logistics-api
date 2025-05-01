# Shipping Logistics API
An API for managing a logistics company that ships general goods via vessels.

## Setup Instructions

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
The dev dependencies `requirements-dev.txt` contain the formatters, linters and test related packages, ignore it outside of development environments.
    - Using pip:
        ```bash
        pip install -r requirements.txt
        pip install -r requirements-dev.txt  # For development dependencies
        ```

    - Using pip-tools:
        ```bash
        pip install pip-tools
        pip-sync requirements.txt and requirements-dev.txt
        ```

    - Using poetry:
        ```bash
        poetry install --with dev
        ```
