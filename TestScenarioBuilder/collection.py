class Collection:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.test_groups = []

    def add_test_group(self, test_group):
        self.test_groups.append(test_group)

    def update_properties(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Collection(name={self.name}, description={self.description}, test_groups={self.test_groups})"


class TestGroup:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.test_scenarios = []

    def add_test_scenario(self, test_scenario):
        self.test_scenarios.append(test_scenario)

    def update_properties(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"TestGroup(name={self.name}, description={self.description}, test_scenarios={self.test_scenarios})"


class TestScenario:
    def __init__(self, name, tag, data_generation_steps, execution, assertions):
        self.name = name
        self.tag = tag
        self.data_generation_steps = data_generation_steps
        self.execution = execution
        self.assertions = assertions

    def update_properties(self, name, tag):
        self.name = name
        self.tag = tag

    def __str__(self):
        return f"TestScenario(name={self.name}, tag={self.tag}, data_generation_steps={self.data_generation_steps}, execution={self.execution}, assertions={self.assertions})"


class DataGenerationStep:
    def __init__(self, reference_scenario, data_mapping):
        self.reference_scenario = reference_scenario
        self.data_mapping = data_mapping

    def __str__(self):
        return f"DataGenerationStep(reference_scenario={self.reference_scenario}, data_mapping={self.data_mapping})"


class Execution:
    def __init__(self, url, method, headers, query_params, body):
        self.url = url
        self.method = method
        self.headers = headers
        self.query_params = query_params
        self.body = body

    def __str__(self):
        return f"Execution(url={self.url}, method={self.method}, headers={self.headers}, query_params={self.query_params}, body={self.body})"


class Assertion:
    def __init__(self, name, property, operator, value):
        self.name = name
        self.property = property
        self.operator = operator
        self.value = value

    def __str__(self):
        return f"Assertion(name={self.name}, property={self.property}, operator={self.operator}, value={self.value})"
