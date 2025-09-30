# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code Adapter built with FastAPI that converts Claude Code tool definitions into system prompts, allowing non-native tool models to understand and use tools. The adapter acts as a proxy between Anthropic-style API requests and OpenAI-compatible endpoints.

## Development Commands

### Basic Commands
- `make run` - Start development server with hot reload
- `make run-prod` - Run production server
- `make test` - Run tests
- `make lint` - Run code linting (flake8 + mypy)
- `make format` - Format code (black + isort)

### Environment Setup
- `make setup` - Create virtual environment
- `make install` - Install production dependencies
- `make install-dev` - Install development dependencies
- `make check-env` - Check environment configuration

### Docker Commands
- `make docker-build` - Build Docker image
- `make docker-run` - Run Docker container
- `make docker-compose-up` - Start with docker-compose

## Architecture

### Core Components
- **app.py** - FastAPI application with main endpoints (`/health`, `/v1/messages`)
- **services.py** - Business logic layer (message conversion, OpenAI client, response processing)
- **models.py** - Pydantic data models for API requests/responses
- **config.py** - Configuration management with YAML and environment variable support
- **utils.py** - Utility functions for tool parsing and content processing

### Key Features
- **Tool Prompt Adaptation**: Converts tool definitions into system prompts for non-native models
- **Message Format Conversion**: Translates between Anthropic and OpenAI message formats
- **Tool Selection**: Dynamic tool selection based on conversation context
- **Streaming Support**: Full support for streaming responses
- **Flexible Configuration**: YAML config files with environment variable overrides

### Project Structure
```
src/claude_code_adapter/
├── app.py          # FastAPI application and endpoints
├── config.py       # Configuration management
├── models.py       # Pydantic data models
├── services.py     # Business logic services
└── utils.py        # Utility functions
```

## Configuration

Configuration is managed through `config.yaml` with environment variable overrides. Key settings include:
- `target_base_url` - Target OpenAI-compatible API endpoint
- `enable_tool_selection` - Enable dynamic tool selection
- `tool_use_prompt` - Template for tool usage instructions

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /v1/messages` - Main proxy endpoint for message processing

## Development Notes

- The project uses Python 3.9+ with modern async/await patterns
- Configuration supports both YAML files and environment variables
- Tool selection uses a separate model to intelligently choose relevant tools
- Response processing handles both text responses and tool call extraction
- Error handling includes comprehensive logging and graceful degradation
