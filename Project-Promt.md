# API Endpoint Testing Application

## 1. Project Aim

The aim of this project is to develop a robust and user-friendly application for testing API endpoints thoroughly. This application will allow developers to define comprehensive test scenarios in a structured JSON format, execute these scenarios via a command-line interface (CLI), and generate detailed reports in both JSON and HTML formats to facilitate easy analysis of test results. The goal is to empower API developers to ensure the reliability, functionality, and performance of their endpoints efficiently.

## 2. Components and Features

The application will consist of the following key components:

### 2.1. Test Scenario Definition (JSON)

* **Structure:** Test scenarios are defined using a hierarchical JSON structure: `Collection` -> `TestGroup` -> `TestScenario`.
* **Test Scenario Details:** Each `TestScenario` will include:
    * `name`: A unique name for the test scenario.
    * `tag`: Optional tags for categorizing and filtering tests.
    * `DataGenerationSteps`: An array of steps to generate or manipulate data for the request. This can reference outputs from previous test scenarios within the same execution and perform data mapping (updates and removals of properties).
    * `Execution`: Defines how to execute the API endpoint, including:
        * `URL`: The endpoint URL, supporting dynamic values from previous steps and environment variables (using `{}`).
        * `method`: The HTTP method (GET, POST, PUT, DELETE, etc.).
        * `headers`: Custom headers for the request.
        * `queryParams`: Query parameters for the request, supporting dynamic values.
        * `body`: The request body (can be static or generated via `DataGenerationSteps`).
    * `Assertions`: An array of assertions to validate the API response, with each assertion having:
        * `name`: A descriptive name for the assertion.
        * `property`: The property to assert on (e.g., `statusCode`, `data.id`, `headers.Content-Type`, `responseTime`).
        * `operator`: The comparison operator (e.g., `equals`, `notEquals`, `contains`, `lessThan`, `isArrayOfLength`).
        * `value`: The expected value for the assertion (can reference dynamic values).

### 2.2. Environment Configuration (JSON)

* Environment-specific details such as base URLs, authentication tokens, and other configuration values will be stored in separate JSON files.
* These values can be referenced within the test scenario definitions using the `{env.key}` syntax.

### 2.3. Command-Line Interface (CLI)

* A CLI tool (`your_cli_name`) to interact with the test execution engine.
* **Features:**
    * **Execute Tests:** Run test scenarios defined in collection files.
    * **Specify Collection:** Use the `-c` option to provide the path to the collection JSON file.
    * **Specify Environment:** Use the `-e` option to provide the path to the environment JSON file.
    * **Execute Specific Scenarios:** Use the `-s` option to specify a comma-separated list of test scenario names to execute.
    * **Filter by Tags:** Use the `-t` option to execute only scenarios with specified tags.
    * **Verbose Output:** Use the `-v` flag for more detailed console output during execution.
    * **Report Generation:** Use the `-o` option to specify the output format (`json` or `html`) and the output file path.
    * **Parallel Execution:** Use the `-p` option to enable parallel execution with a specified number of workers.

### 2.4. Report Generation (JSON & HTML)

* **JSON Report:** A structured JSON file containing a summary of the test run (total, passed, failed, environment, timestamp, total execution time, parallel requests) and an array of detailed results for each test scenario, including status, execution time, assertion results (with failure details), and request/response details for failed tests.
* **HTML Report:** A user-friendly HTML report with:
    * A summary section at the top (total, passed, failed, environment, timestamp, total execution time, parallel requests).
    * A two-level accordion structure:
        * **Outer Accordion:** Represents the path to the test scenario (Collection / TestGroup(s)).
        * **Inner Accordion:** Represents each individual `TestScenario`, displaying its status, request details, response details, and a list of assertions with their pass/fail status and failure information.

## 3. Example JSON Structures

### 3.1. Example Collection JSON (`my_collection.json`)

```json
{
  "Collection": {
    "name": "User Management Tests",
    "description": "Tests for the user management API endpoints",
    "TestGroup": [
      {
        "name": "Create User",
        "description": "Tests for the user creation endpoint",
        "TestScenario": [
          {
            "name": "Create a new user successfully",
            "tag": "smoke",
            "Execution": {
              "URL": "{env.baseUrl}/users",
              "method": "POST",
              "headers": {
                "Content-Type": "application/json"
              },
              "body": {
                "username": "testuser",
                "email": "test@example.com"
              }
            },
            "Assertions": [
              {
                "name": "Check status code is 201",
                "property": "statusCode",
                "operator": "equals",
                "value": 201
              },
              {
                "name": "Verify user ID is present in response",
                "property": "data.id",
                "operator": "isNotNull",
                "value": null
              }
            ]
          }
        ]
      },
      {
        "name": "Get User Details",
        "description": "Tests for retrieving user details",
        "TestScenario": [
          {
            "name": "Get existing user details",
            "tag": "regression",
            "DataGenerationSteps": [
              {
                "referenceScenario": "Create User / Create a new user successfully",
                "DataMapping": {
                  "outputProperty": "data.id",
                  "updates": {}
                }
              }
            ],
            "Execution": {
              "URL": "{env.baseUrl}/users/{Create User / Create a new user successfully.data.id}",
              "method": "GET",
              "headers": {
                "Authorization": "Bearer {env.authToken}"
              }
            },
            "Assertions": [
              {
                "name": "Check status code is 200",
                "property": "statusCode",
                "operator": "equals",
                "value": 200
              },
              {
                "name": "Verify username in response",
                "property": "data.username",
                "operator": "equals",
                "value": "testuser"
              }
            ]
          }
        ]
      }
    ]
  }
}