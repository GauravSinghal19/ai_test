## Why

The current system lacks a consolidated view of UPC onboarding metrics across different systems (Affinity, STEP, Stella). Users need to manually track or query different databases to get a report on how many UPCs were onboarded in a given time range. This feature provides a conversational interface to generate these reports quickly, supporting both tabular and graphical representations for better insights.

## What Changes

- **New Backend Sub-Agents**: Introduction of `sql_agent`, `analytics_agent`, and `date_range_agent` to handle database interactions, metric calculations, and natural language date parsing.
- **Google Cloud SQL Integration**: Implementation of secure connections and analytical queries against `ep_messages`, `epc_create_auto_pdf`, and `epc_create_auto_stella` tables.
- **Frontend Visualization**: Enhancement of the chat interface to render analytical data in tabular and graphical formats (e.g., bar charts for system-wise onboarding).
- **Onboarding Metrics**: New capability to aggregate UPC counts by system (Affinity, STEP, Stella) over daily, weekly, or monthly intervals.

## Capabilities

### New Capabilities
- `upc-onboarding-analytics`: Query and aggregate UPC onboarding data from Affinity, STEP, and Stella systems via Google Cloud SQL.
- `date-range-parsing`: Parse and normalize natural language date ranges (e.g., "last week", "previous month", "March 2026") into absolute timestamps.
- `report-visualization`: Format analytical response data for tabular and graphical display in the frontend.

### Modified Capabilities
<!-- No existing capabilities to modify. -->

## Impact

- **Backend**: New agent logic and database connection utilities in `/agents`.
- **Frontend**: New UI components for data visualization (tables, charts) in `/app/src`.
- **Data**: New analytical queries against Google Cloud SQL production tables.
- **Dependencies**: Potential addition of a charting library (e.g., Recharts or Chart.js) to the frontend.
