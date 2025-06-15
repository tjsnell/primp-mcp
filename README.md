# Primp MCP Server

A Model Context Protocol (MCP) server that provides access to the [primp](https://github.com/deedy5/primp) HTTP client library with browser impersonation capabilities.

## Features

- **Browser Impersonation**: Impersonate various browsers (Chrome, Firefox, Safari, Edge) and operating systems
- **HTTP Methods**: Support for GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- **Authentication**: Basic auth and Bearer token support
- **Proxy Support**: HTTP/HTTPS proxy support
- **File Uploads**: Multipart form data file uploads
- **Response Formats**: Return responses as text, JSON, markdown, plain text, or rich text
- **Advanced Options**: Configurable timeouts, redirect handling, SSL verification

## Installation

```bash
pip install -e .
```

## Usage

The server provides two main tools:

### 1. `primp_request`

Make HTTP requests with browser impersonation:

```python
# Example usage in MCP client
{
    "name": "primp_request",
    "arguments": {
        "url": "https://httpbin.org/get",
        "method": "GET",
        "impersonate": "chrome_131",
        "impersonate_os": "windows",
        "headers": {
            "User-Agent": "My-App/1.0"
        },
        "return_format": "json"
    }
}
```

### 2. `primp_upload`

Upload files using multipart form data:

```python
# Example usage in MCP client
{
    "name": "primp_upload",
    "arguments": {
        "url": "https://httpbin.org/post",
        "files": [
            {
                "name": "file",
                "filename": "example.txt",
                "content": "SGVsbG8gV29ybGQ=",  # base64 encoded
                "content_type": "text/plain"
            }
        ],
        "data": {
            "description": "Test upload"
        }
    }
}
```

## Configuration

Add to your MCP settings:

```json
{
  "mcpServers": {
    "primp": {
      "command": "primp-mcp"
    }
  }
}
```

## Supported Browsers

- Chrome (versions 99-131)
- Firefox (versions 99-133)
- Safari (versions 12-18, including iPad/iPhone)
- Edge (versions 99-131)
- OkHttp (versions 3.14.9-5.0.0)

## Supported Operating Systems

- Windows
- macOS
- Linux
- Android
- iOS

## License

MIT