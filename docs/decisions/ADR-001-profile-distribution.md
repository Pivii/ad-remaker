# ADR-001 - Distribute Ad Remaker as a Hermes profile

## Status

Accepted.

## Context

Ad Remaker needs an identity, Skills, connections, memory, and sessions isolated from Pierre's main Hermes profile. The project must remain versioned, installable, and updatable from a private repository.

## Decision

The `Pivii/ad-remaker` repository is an official Hermes profile distribution. It contains the identity, credential-free configuration, Skills, declarative MCP connections, and any distributed scheduled jobs.

Secrets, brand data, memories, sessions, and work outputs remain specific to each installation.

## Consequences

- The profile can be installed and updated with the dedicated Hermes commands.
- The main profile is not cloned, so its Skills and memories do not contaminate Ad Remaker.
- Integrations must be declared without secrets and verified in the installed profile.
- The repository must remain compatible with the Hermes distribution format.
