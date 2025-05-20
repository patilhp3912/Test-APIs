{
  "summary": {
    "total": 10,
    "passed": 8,
    "failed": 2,
    "environment": "development",
    "timestamp": "2025-05-11T13:00:00Z",
    "totalExecutionTime": "15.5s",
    "parallelRequests": 4
  },
  "results": [
    {
      "name": "Scenario Name 1",
      "status": "pass",
      "executionTime": "1.2s",
      "assertions": [
        {
          "name": "Check successful status code",
          "status": "pass"
        },
        // ... more assertions
      ]
    },
    {
      "name": "Scenario Name 2",
      "status": "fail",
      "executionTime": "0.8s",
      "assertions": [
        {
          "name": "Check successful status code",
          "status": "pass"
        },
        {
          "name": "Verify ID in response",
          "status": "fail",
          "property": "data.id",
          "operator": "equals",
          "expectedValue": "123",
          "actualValue": "456"
        }
        // ... more assertions
      ],
      "request": {
        "method": "GET",
        "url": "[https://api.example.com/users/123](https://api.example.com/users/123)",
        "headers": { ... },
        "body": { ... }
      },
      "response": {
        "statusCode": 404,
        "headers": { ... },
        "body": { ... }
      }
    },
    // ... more test results
  ]
}