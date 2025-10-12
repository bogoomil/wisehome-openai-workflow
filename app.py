from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import asyncio
from agent import run_workflow, WorkflowInput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            "helyiség": "nappali",
            "eszköz": "lámpa",
            "parancs": "bekapcsol"
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
        
        # Create workflow input
        workflow_input = WorkflowInput(input_as_text=input_text)
        
        # Run the workflow asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_workflow(workflow_input))
        loop.close()
        
        logger.info(f"Workflow result: {result}")
        
        # Return the parsed result
        return jsonify({
            "success": True,
            "result": result['output_parsed']
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
            "example": "curl -X POST http://localhost:5000/analyze -H 'Content-Type: application/json' -d '{\"text\":\"kapcsold be a lámpát\"}'"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting OpenAI Agent API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

