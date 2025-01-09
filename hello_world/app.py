import json
import logging
import time
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Extract the timestamp from the event
        event_time_str = event.get('time', '1970-01-01T00:00:00Z')  
        event_time = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))  
        event_time_ms = event_time.timestamp() * 1000

        current_time_ms = time.time() * 1000  
        latency = current_time_ms - event_time_ms

        # Log latency
        logger.info(f"Event Latency: {latency} ms")
        
        # Log full event
        logger.info(f"Event received: {json.dumps(event)}")
        
        # Simulate failure for certain statuses
        status = event.get('detail', {}).get('status', '')
        if status != "success":
            raise ValueError(f"Unexpected status: {status}")
        
        return {"statusCode": 200, "body": "Messages processed successfully"}
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise
