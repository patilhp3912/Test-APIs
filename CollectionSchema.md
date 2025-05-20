# API Endpoint Testing Application Requirements

## 1. Test Scenario Definition (JSON Format)

Test scenarios will be defined using JSON files with the following hierarchical structure:

```json
{
  "Collection": {
    "name": "Collection Name",
    "description": "Optional description of the collection",
    "TestGroup": [
      {
        "name": "Group Name 1",
        "description": "Optional description of the group",
        "TestScenario": [
          {
            "name": "Scenario Name 1",
            "tag": "optional_tag",
            "DataGenerationSteps": [
              // Steps to generate data, can reference previous TestScenario outputs
              // and include DataMapping operations
              {
                "referenceScenario": "PreviousScenarioName",
                "DataMapping": {
                  "outputProperty": "GetTest.Output",
                  "updates": {
                    "prop1": "updatedValue",
                    "newProp": "newValue"
                  },
                  "removals": ["oldProp"]
                }
              }
            ],
            "Execution": {
              "URL": "{env.baseUrl}/some/endpoint/{dynamicId}",
              "method": "GET",
              "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer {env.authToken}"
              },
              "queryParams": {
                "filter": "value",
                "sort": "{PreviousScenario.Output.sortField}"
              },
              "body": {
                // Request body, can be static or constructed via DataGenerationSteps
              }
            },
            "Assertions": [
              {
                "name": "Check successful status code",
                "property": "statusCode",
                "operator": "equals",
                "value": 200
              },
              {
                "name": "Verify ID in response",
                "property": "data.id",
                "operator": "equals",
                "value": "{PreviousScenario.Output.id}"
              },
              {
                "name": "Check content type",
                "property": "headers.Content-Type",
                "operator": "contains",
                "value": "application/json"
              },
              {
                "name": "Response time within limit",
                "property": "responseTime",
                "operator": "lessThan",
                "value": 1000
              }
              // ... more assertions
            ]
          },
          // ... more TestScenarios in Group Name 1
        ]
      },
      // ... more TestGroups
    ]
  }
  // ... more Collections (potentially in separate files)
}