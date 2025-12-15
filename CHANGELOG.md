# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

## [0.1.0] - 2025-12-15

### Added
- **Core Features**
  - AI-powered API mocking server with zero configuration
  - Dynamic endpoint generation for any REST API path
  - Support for GET, POST, PUT, PATCH, DELETE, OPTIONS methods
  - Automatic realistic data generation based on resource types

- **AI Providers**
  - Demo mode with template-based responses (no API key required)
  - DeepSeek integration via OpenRouter
  - Groq integration for ultra-fast inference
  - Ollama support for local/offline operation

- **Smart Data Generation**
  - Automatic recognition of resource types (users, products, orders, etc.)
  - Realistic field generation (names, emails, dates, IDs, prices)
  - Context-aware responses that remember previous actions

- **Session Management**
  - `X-Session-ID` header support for maintaining context
  - Session-based caching for consistent responses
  - Independent data contexts per session

- **Chaos Engineering**
  - Configurable error rate simulation
  - Random latency injection
  - Customizable delay ranges for resilience testing

- **Infrastructure**
  - Redis caching with 24-hour TTL
  - Docker and Docker Compose support
  - Health check and status endpoints
  - FastAPI-based architecture

- **Documentation**
  - Comprehensive README with usage examples
  - API endpoint documentation
  - Configuration guide for all AI providers

### Technical Details
- Python 3.11+ required
- FastAPI 0.95.2
- Redis for caching and session storage
- AGPLv3 License

---

## Version History

### Versioning Scheme

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Links

- [Compare Unreleased](https://github.com/ashfromsky/Helix/compare/v0.1.0...HEAD)
- [Release v0.1.0](https://github.com/ashfromsky/Helix/releases/tag/v0.1.0)