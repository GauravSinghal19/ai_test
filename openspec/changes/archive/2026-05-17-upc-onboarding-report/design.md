## Context

The current AI service agent platform uses a multi-agent architecture (Google ADK) to handle conversational tasks. To support UPC onboarding analytics, we need to extend the backend with specialized sub-agents and integrate with Google Cloud SQL. The frontend must also evolve to display complex analytical data through tables and charts.

## Goals / Non-Goals

**Goals:**
- **Modular Backend**: Implement `date_range_agent`, `sql_agent`, and `analytics_agent` as distinct sub-agents.
- **Secure SQL Access**: Establish a secure, performant connection to Google Cloud SQL using environment-based credentials.
- **Rich Visualization**: Enable the Next.js frontend to render tabular and graphical reports using Recharts. Ensure that data is presented in a way that is immediately actionable and visually appealing, moving away from raw JSON representations.
- **NL Date Parsing**: Provide robust support for natural language date ranges (relative and absolute).

**Non-Goals:**
- **Real-time Data Sync**: This feature focuses on point-in-time analytical queries, not real-time streaming updates.
- **Data Modification**: The agents will have read-only access to the production onboarding tables.
- **Cross-Database Joins**: All data retrieval is scoped to the primary Google Cloud SQL instance.

## Decisions

### 1. Orchestrator-Worker Pattern (AgentTool)
**Choice**: Sequential orchestration using `AgentTool` from the `root_agent`.
**Rationale**: Unlike standard delegation (`sub_agents`) which transfers control permanently, `AgentTool` allows the `root_agent` to invoke utility agents as tools and receive their output. This is essential for the sequential pipeline: Date Parsing -> SQL Retrieval -> Analytics Processing -> Response Formatting.
**Alternatives**: Standard `sub_agents` delegation (breaks the sequential chain) or a `SequentialAgent` workflow (less flexible for natural language mixed with analytics).

### 2. Frontend Visualization Library
**Choice**: `Recharts`.
**Rationale**: Highly compatible with React and Tailwind CSS, providing responsive and accessible SVG-based charts with minimal boilerplate.
**Alternatives**: `Chart.js` (requires more React wrapping) or `Victory` (steeper learning curve).

### 3. Backend Database Layer
**Choice**: `SQLAlchemy` with an async driver (`asyncpg` for PostgreSQL or equivalent for MySQL).
**Rationale**: Provides a robust connection pool and allows for safe, parameterized query execution.
**Alternatives**: Raw `psycopg2`/`mysql-connector` (lacks high-level pooling/abstractions).

### 4. Robust JSON Extraction
**Choice**: Client-side markdown stripping and robust JSON parsing.
**Rationale**: LLMs occasionally wrap structured output in markdown code blocks (e.g., \`\`\`json ... \`\`\`), which can break standard \`JSON.parse()\`. Implementing a pre-parsing cleanup step ensures that the UI consistently renders the expected visual components.
**Alternatives**: Stricter backend prompts (prone to failure) or manual string slicing (less robust than regex-based cleaning).

## Risks / Trade-offs

- **[Risk]**: Analytical queries against production tables may impact database performance.
  - **[Mitigation]**: Use read-only replicas if available; otherwise, implement strict query timeouts and ensure critical columns like `create_timestamp` are indexed.
- **[Risk]**: Ambiguous natural language date ranges (e.g., "next week" in a historical context).
  - **[Mitigation]**: The `date_range_agent` will default to the most logical past interval and provide a confirmation of the interpreted range in the response.
- **[Risk]**: Large data payloads crashing the frontend or exceeding token limits.
  - **[Mitigation]**: Implement pagination or aggregation at the SQL level to ensure the payload remains manageable.
