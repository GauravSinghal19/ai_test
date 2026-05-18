# UPC Onboarding Report Architecture

This diagram illustrates the flow of a user's analytical query through the multi-agent system and the retrieval of data from Google Cloud SQL.

```mermaid
graph TD
    %% Frontend Components
    subgraph Frontend [Next.js Web App]
        UI[Chat Interface]
        Viz[AnalyticalTable / OnboardingChart]
    end

    %% Backend Orchestration
    subgraph Backend [Google ADK Backend]
        Root[Root Agent]
        
        subgraph SubAgents [Sub-Agents]
            DRA[Date Range Agent]
            SQA[SQL Agent]
            ANA[Analytics Agent]
            RSA[Response Agent]
        end
    end

    %% Data Layer
    subgraph Data [Data Layer]
        GCSQL[(Google Cloud SQL)]
        T1[ep_messages]
        T2[epc_create_auto_pdf]
        T3[epc_create_auto_stella]
    end

    %% Interaction Flow
    UI -->|1. NL Query| Root
    Root -->|2. Delegate Date Parsing| DRA
    DRA -->|3. Standardized Range| SQA
    SQA -->|4. Analytical Query| GCSQL
    GCSQL -->|5. Raw Metrics| ANA
    ANA -->|6. Aggregated Data| RSA
    RSA -->|7. Structured JSON| Root
    Root -->|8. Final Response| UI
    UI -->|9. Render Data| Viz

    %% External Systems Mapping
    GCSQL --- T1
    GCSQL --- T2
    GCSQL --- T3
```

### Flow Description
1. **NL Query**: The user asks a question like "Show me weekly onboarding for last month".
2. **Date Parsing**: The `Date Range Agent` parses "last month" into absolute start/end timestamps.
3. **SQL Generation**: The `SQL Agent` constructs and executes queries against the `ep_messages`, `epc_create_auto_pdf`, and `epc_create_auto_stella` tables.
4. **Aggregation**: The `Analytics Agent` computes totals and trends (e.g., daily counts, system distribution).
5. **Formatting**: The `Response Agent` packages the results into a structured JSON format suitable for chart rendering.
6. **Visualization**: The Next.js frontend detects the data structure and renders either an `AnalyticalTable` or an `OnboardingChart` using Recharts.
