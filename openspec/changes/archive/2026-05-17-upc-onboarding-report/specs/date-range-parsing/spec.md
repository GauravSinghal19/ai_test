## ADDED Requirements

### Requirement: Natural Language Date Understanding
The system SHALL parse natural language expressions into standardized start and end timestamps.

#### Scenario: Relative date range parsing
- **WHEN** user says "last week"
- **THEN** system calculates the date range from 7 days ago until today

#### Scenario: Specific month parsing
- **WHEN** user says "March 2026"
- **THEN** system sets range from 2026-03-01 00:00:00 to 2026-03-31 23:59:59

### Requirement: Date Range Normalization
The system SHALL normalize all date ranges to a consistent format (e.g., ISO-8601) for use in SQL queries.

#### Scenario: Normalization for SQL injection prevention
- **WHEN** a date range is parsed
- **THEN** the timestamps are formatted as strings compatible with Cloud SQL timestamp fields
