# 0001. Use MongoDB for primary storage

- **Status:** Accepted
- **Date:** [TODO: add date]
- **Deciders:** [TODO: add team or individuals]

## Context

Our domain data is highly variable and evolves rapidly across releases. Product catalogs, user activity streams, and configuration documents frequently contain nested structures and optional fields that differ significantly between tenants. The schema changes from one release to the next, making rigid table structures difficult to maintain. We need strong query capabilities for both analytics and real-time features, and we expect growth patterns that will require horizontal scaling. The team needs to maintain development velocity while managing data that does not naturally fit relational patterns.

## Decision

We will use MongoDB as the primary datastore for our core services.

## Consequences

**Easier:**
- Nested and variable structures can be stored naturally without forcing denormalization or creating sparse tables with many optional columns.
- Schema changes no longer require expensive migrations or coordinated deployments; new fields can be added organically.
- Developer velocity increases because the document model matches the domain objects directly.
- Horizontal scaling through sharding maps cleanly to our expected growth, allowing us to add capacity as needed.
- The aggregation pipeline provides the query power needed for analytics and real-time features without complex join logic.

**Harder:**
- Strongly relational queries (such as complex multi-document joins) will be more difficult to express and may require denormalization or application-level joins.
- Data integrity constraints that relational databases enforce at the schema level (foreign keys, strict types) must now be handled in application code or through careful validation.
- The team will need to develop expertise in MongoDB-specific concepts like sharding strategies, replica set management, and index optimization.
- Migration back to a relational database in the future would be costly if requirements change.

## Alternatives considered

- **PostgreSQL** — Excellent for strongly relational workloads with mature tooling and strict consistency guarantees. Rejected because our data is not primarily relational, and the highly variable schemas would force us into expensive migration workflows or sparse table designs. Managing horizontal write-scaling through manual partitioning and read replicas would add operational complexity at the scale we expect.
