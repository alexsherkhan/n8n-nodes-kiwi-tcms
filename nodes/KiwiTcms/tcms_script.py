"""
Kiwi TCMS API Integration Script for n8n
Handles all TCMS operations through RPC calls with proper error handling
"""

import sys
import json
import logging
from tcms_api import TCMS
from functools import partial

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TCMSOperationError(Exception):
    """Custom exception for TCMS API failures"""
    pass

def initialize_tcms_client(url, username, password):
    """
    Initialize and verify TCMS connection
    Args:
        url: TCMS instance URL
        username: API username
        password: API password
    Returns:
        Authenticated TCMS client
    Raises:
        TCMSOperationError: If connection fails
    """
    try:
        logger.info("Initializing TCMS client")
        client = TCMS(url=url, username=username, password=password)
        
        # Verify connection works
        client.exec.Auth.whoami()
        logger.info("TCMS connection successful")
        return client
        
    except Exception as e:
        logger.error(f"TCMS connection failed: {str(e)}")
        raise TCMSOperationError(f"TCMS connection failed: {str(e)}")

def execute_tcms_action(client, action, params):
    """
    Execute TCMS RPC action with proper parameter handling
    Args:
        client: Authenticated TCMS client
        action: RPC method name (e.g., 'TestCase.filter')
        params: Dictionary of parameters
    Returns:
        RPC call result
    Raises:
        TCMSOperationError: If action fails
    """
    try:
        logger.info(f"Executing action: {action}")
        
        # Split object and method names
        obj_name, method_name = action.split('.', 1)
        rpc_obj = getattr(client.exec, obj_name)
        rpc_method = getattr(rpc_obj, method_name)
        
        # Special handlers for non-standard methods
        ACTION_HANDLERS = {
            # Test Plan actions
            'TestPlan.add_case': lambda: rpc_method(params['plan_id'], params['case_id']),
            'TestPlan.update_case_order': lambda: rpc_method(params['plan_id'], params['case_ids']),
            
            # Test Case actions  
            'TestCase.add_tag': lambda: rpc_method(params['case_id'], params['tag']),
            'TestCase.add_component': lambda: rpc_method(params['case_id'], params['component_id']),
            
            # Test Run actions
            'TestRun.add_case': lambda: rpc_method(params['run_id'], params['case_id']),
            'TestRun.add_cc': lambda: rpc_method(params['run_id'], params['email']),
        }
        
        # Execute with appropriate parameter format
        if action in ACTION_HANDLERS:
            return ACTION_HANDLERS[action]()
        elif isinstance(params, list):
            return rpc_method(*params)
        else:
            return rpc_method(params or {})
            
    except Exception as e:
        logger.error(f"Action {action} failed: {str(e)}")
        raise TCMSOperationError(f"{action} execution failed: {str(e)}")

def validate_input(input_data):
    """
    Validate input JSON structure
    Args:
        input_data: Parsed input dictionary
    Raises:
        ValueError: If required fields are missing
    """
    required_fields = {
        'url': str,
        'username': str,
        'password': str,
        'action': str
    }
    
    for field, field_type in required_fields.items():
        if field not in input_data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(input_data[field], field_type):
            raise ValueError(f"Field {field} must be {field_type.__name__}")

def format_error_response(error_type, message, context=None):
    """
    Create standardized error response
    Args:
        error_type: Error category
        message: Error description
        context: Additional context data
    Returns:
        Dictionary with error details
    """
    response = {
        'success': False,
        'error_type': error_type,
        'error': message,
        'timestamp': datetime.datetime.now().isoformat()
    }
    if context:
        response.update(context)
    return response

def main():
    """
    Main execution flow:
    1. Read input from stdin
    2. Validate input structure
    3. Initialize TCMS client
    4. Execute requested action
    5. Return formatted response
    """
    try:
        # Read and parse input
        raw_input = sys.stdin.read()
        logger.debug(f"Received input: {raw_input[:200]}...")
        
        try:
            input_data = json.loads(raw_input)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input")
            error = format_error_response(
                'INPUT_ERROR',
                'Invalid JSON format',
                {'json_error': str(e), 'input_sample': raw_input[:500]}
            )
            print(json.dumps(error), file=sys.stderr)
            sys.exit(1)
            
        # Input validation
        try:
            validate_input(input_data)
        except ValueError as e:
            logger.error(f"Input validation failed: {str(e)}")
            error = format_error_response(
                'INPUT_ERROR',
                str(e),
                {'required_fields': ['url', 'username', 'password', 'action']}
            )
            print(json.dumps(error), file=sys.stderr)
            sys.exit(1)
            
        # Execute TCMS operation
        client = initialize_tcms_client(
            input_data['url'],
            input_data['username'],
            input_data['password']
        )
        
        result = execute_tcms_action(
            client,
            input_data['action'],
            input_data.get('params', {})
        )
        
        # Prepare success response
        response = {
            'success': True,
            'action': input_data['action'],
            'result': result,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        print(json.dumps(response, default=str))
        
    except TCMSOperationError as e:
        error = format_error_response(
            'TCMS_ERROR',
            str(e),
            {'action': input_data.get('action')}
        )
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        error = format_error_response(
            'UNKNOWN_ERROR',
            'Unexpected error occurred',
            {
                'exception_type': type(e).__name__,
                'details': str(e)
            }
        )
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    import datetime  # For timestamp generation
    main()