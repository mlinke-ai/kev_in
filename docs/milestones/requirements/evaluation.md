# Evaluation System

## Functional requirements

| Field | Value |
|---|---|
| Requirement # | 4.1 |
| Requirement Type | functional |
| Event/BUC/PUC # | evaluation |
| Description | the user receives an evaluation after submitting a solution |
| Rationale | the user needs to see an evaluation to understand the scoring |
| Originator | customer |
| Fit Criterion | validation with test data |
| Customer Satisfaction | 1 |
| Customer Dissatisfaction | 5 |
| Priority | 5 |
| Dependencies |  |
| Conflicts |  |
| Support Materials |  |
| History | created 05.11.2022 |

| Field | Value |
|---|---|
| Requirement # | 4.2 |
| Requirement Type | functional |
| Event/BUC/PUC # | evaluation |
| Description | the evaluation system saves results to the database |
| Rationale | learning process is evident and comparison the previous solutions is possible |
| Originator | customer |
| Fit Criterion | validation with test data |
| Customer Satisfaction | 2 |
| Customer Dissatisfaction | 4 |
| Priority | 2 |
| Dependencies |  |
| Conflicts |  |
| Support Materials |  |
| History | created 05.11.2022 |

| Field | Value |
|---|---|
| Requirement # | 4.3 |
| Requirement Type | functional |
| Event/BUC/PUC # | evaluation |
| Description | the evaluation system shall provide a sample solution |
| Rationale | user needs to see a correct solution for education effect |
| Originator | user, customer |
| Fit Criterion | validation with wrong solutions |
| Customer Satisfaction | 5 |
| Customer Dissatisfaction | 4 |
| Priority | 3 |
| Dependencies |  |
| Conflicts |  |
| Support Materials |  |
| History | created 05.11.2022 |

## Non-functional requirements

| Field | Value |
|---|---|
| Requirement # | 4.4 |
| Requirement Type | non-functional |
| Event/BUC/PUC # | evaluation |
| Description | the evaluation system handles malicious user input |
| Rationale | the evaluation system is available most of the time |
| Originator | customer, administrator |
| Fit Criterion | the evaluation system crashes only at 1% of cases when presented with specially crafted or randomly generated user input |
| Customer Satisfaction | 2 |
| Customer Dissatisfaction | 4 |
| Priority | 3 |
| Dependencies |  |
| Conflicts |  |
| Support Materials |  |
| History | created 05.11.2022 |

| Field | Value |
|---|---|
| Requirement # | 4.5 |
| Requirement Type | non-functional |
| Event/BUC/PUC # | evaluation |
| Description | the evaluation system shall perform task with low latency |
| Rationale | high user experience and satisfaction is ensured |
| Originator | user, customer |
| Fit Criterion | in tests the evaluation system returns after at least 1 second |
| Customer Satisfaction | 1 |
| Customer Dissatisfaction | 4 |
| Priority | 2 |
| Dependencies |  |
| Conflicts |  |
| Support Materials | https://www.selenium.dev/ |
| History | created 05.11.2022 |
