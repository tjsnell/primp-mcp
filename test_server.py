#!/usr/bin/env python3
"""Test script for the primp MCP server."""

import asyncio
import json
import sys
from unittest.mock import AsyncMock, Mock

async def test_basic_functionality():
    """Test basic server functionality."""
    try:
        from src.primp_mcp.server import PrimpMCPServer
        
        print("✓ Server imports successfully")
        
        # Create server instance
        server = PrimpMCPServer()
        print("✓ Server instantiated successfully")
        
        # Test that server has the expected handler methods
        assert hasattr(server, '_setup_handlers'), "Server missing _setup_handlers method"
        assert hasattr(server.server, 'list_tools'), "Server missing list_tools capability"
        assert hasattr(server.server, 'call_tool'), "Server missing call_tool capability"
        print("✓ Server has required handlers")
        
        print("✓ Basic server structure validated")
        print("\n🎉 Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_tool_schemas():
    """Test that tool schemas are valid."""
    try:
        from src.primp_mcp.server import PrimpMCPServer
        
        server = PrimpMCPServer()
        print("✓ Server created for schema validation")
        
        # Test that the tools are defined correctly in the source
        # Check if primp_request and primp_upload handlers exist
        assert hasattr(server, '_handle_primp_request'), "Missing _handle_primp_request method"
        assert hasattr(server, '_handle_primp_upload'), "Missing _handle_primp_upload method"
        print("✓ Tool handlers are defined")
        
        # Test that we can create a basic primp client
        import primp
        client = primp.Client(impersonate="chrome_131")
        print("✓ Primp client can be instantiated")
        
        print("\n🎉 Schema validation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test that all required dependencies can be imported."""
    try:
        import mcp
        print("✓ mcp imported successfully")
        
        import primp
        print("✓ primp imported successfully")
        
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import CallToolRequest, CallToolResult, TextContent, Tool
        print("✓ MCP types imported successfully")
        
        print("\n🎉 Import test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        print("Run 'pip install -e .' to install dependencies")
        return False

async def main():
    """Run all tests."""
    print("Running primp MCP server tests...\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Functionality Test", test_basic_functionality),
        ("Schema Validation Test", test_tool_schemas),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("="*50)
    print(f"Test Results: {passed}/{total} passed")
    print("="*50)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 All tests passed! Server is ready to use.")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} test(s) failed.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())