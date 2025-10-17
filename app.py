from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import asyncio
import json
from agent import run_workflow, WorkflowInput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load available values from JSON file
with open('available_values.json', 'r') as f:
    AVAILABLE_VALUES = json.load(f)
    logger.info(f"Loaded available values: {len(AVAILABLE_VALUES.get('rooms', []))} rooms")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "openai-agent-api"
    }), 200

@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    """
    Analyze smart home command
    
    Request body:
    {
        "text": "kapcsold be a nappaliban a lámpát"
    }
    
    Response:
    {
        "success": true,
        "result": {
            "room": "living room",
            "device": "lamp",
            "command": "turn on",
            "missing_information": []
        }
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field in request body"
            }), 400
        
        input_text = data['text'].strip()
        
        if not input_text:
            return jsonify({
                "success": False,
                "error": "Text field cannot be empty"
            }), 400
        
        logger.info(f"Analyzing command: {input_text}")
        
        # Create workflow input with available values
        workflow_input = WorkflowInput(
            input_as_text=input_text,
            available_values=AVAILABLE_VALUES
        )
        
        # Run the workflow asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_workflow(workflow_input))
        loop.close()
        
        logger.info(f"Workflow result: {result}")
        
        # Check for missing information
        parsed_result = result['output_parsed']
        missing_info = parsed_result.get('missing_information', [])
        
        if missing_info:
            logger.warning(f"Missing information detected: {missing_info}")
        
        # Return the parsed result
        return jsonify({
            "success": True,
            "result": parsed_result,
            "has_missing_info": len(missing_info) > 0
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API documentation"""
    return jsonify({
        "service": "OpenAI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API documentation",
            "GET /health": "Health check",
            "POST /analyze": "Analyze smart home command"
        },
        "usage": {
            "endpoint": "/analyze",
            "method": "POST",
            "body": {
                "text": "kapcsold be a nappaliban a lámpát"
            },
            "response_fields": {
                "room": "Room/location",
                "device": "Device type",
                "command": "Command to execute",
                "missing_information": "List of missing/unclear fields"
            },
            "example": "curl -X POST http://localhost:5000/analyze -H 'Content-Type: application/json' -d '{\"text\":\"kapcsold be a lámpát\"}'"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting OpenAI Agent API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

