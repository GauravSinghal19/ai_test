## ADDED Requirements

### Requirement: Multi-Agent Orchestration Flow
The system SHALL coordinate specialized agents using the `AgentTool` pattern to ensure sequential data processing.

#### Scenario: Sequential agent execution
- **WHEN** user requests a report
- **THEN** the root agent calls `DateRangeAgent` (tool), then `SqlAgent` (tool), then `AnalyticsAgent` (tool), and finally `ResponseAgent` (tool) before responding.

### Requirement: Google Cloud SQL Data Retrieval
The system SHALL execute analytical queries against the production Google Cloud SQL instance to fetch raw onboarding metrics.

#### Scenario: Query execution with system filters
- **WHEN** the system queries Affinity onboarding counts
- **THEN** it joins `ep_messages` and `epc_create_auto_pdf` where status is SUCCESS and file name matches "create"

### Requirement: Metrics Calculation and Summarization
The system SHALL calculate total onboarded UPCs and provide a summarized response including percentages or growth trends if requested.

#### Scenario: Daily aggregation requested
- **WHEN** user asks for "daily onboarding report for last week"
- **THEN** the system returns counts grouped by day for each system
