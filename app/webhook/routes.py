from flask import Blueprint, json, request
from app.extensions import mongo
from app.webhook.github_event_schema import github_event_schema #MongoDB schema
from datetime import datetime, timezone

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def format_github_timestamp(ts_str):
    """Convert GitHub ISO 8601 timestamp to 'Dth Month Year - HH:MM AM/PM UTC' format"""
    try:
        # Parse ISO 8601 timestamp (e.g., "2026-01-30T12:09:38+05:30")
        dt = datetime.fromisoformat(ts_str)
        # Convert to UTC
        dt_utc = dt.astimezone(timezone.utc)
        # Extract components
        day = dt_utc.day
        month = dt_utc.strftime('%B')
        year = dt_utc.year
        time = dt_utc.strftime('%I:%M %p')
        
        # Add ordinal suffix to day (1st, 2nd, 3rd, 4th, etc.)
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        
        return f"{day}{suffix} {month} {year} - {time} UTC"
    except:
        return datetime.now(timezone.utc).strftime('%d %B %Y - %I:%M %p UTC')

@webhook.route('/', methods=["GET"]) # Health Check Route
def index():
    return {"success": True, "status": "Server is up"}, 200

@webhook.route('/receiver', methods=["POST"]) # Webhook Receiver Route
def receiver():
    try:
        payload = request.json
        event_data = {}

        #for push action
        if(payload.get("pusher") is not None):
            event_data = {
                "request_id": payload.get('head_commit', {}).get('id', 'N/A'),
                "author": payload.get('pusher', {}).get('name'),
                "action": payload.get('action','push'), #push
                "from_branch": "", #Push events do not have a from_branch
                "to_branch": payload.get('ref','').replace('refs/heads/',''),
                "timestamp": format_github_timestamp(payload.get('head_commit', {}).get('timestamp', datetime.now(timezone.utc).isoformat())),
                "created_at": datetime.now(timezone.utc)
            }

        #for pull_request action
        if(payload.get("pull_request") is not None):
            #if pull request is created
            if(payload.get('action') == 'opened'):
                event_data = {
                    "request_id": str(payload.get('pull_request', {}).get('id')),
                    "author": payload.get('pull_request', {}).get('user', {}).get('login'),
                    "action": payload.get('action','pull_request'), #opened or pull_request
                    "from_branch": payload.get('pull_request', {}).get('head', {}).get('ref'),
                    "to_branch": payload.get('pull_request', {}).get('base', {}).get('ref'),
                    "timestamp": format_github_timestamp(payload.get('pull_request', {}).get('created_at', datetime.now(timezone.utc).isoformat())),
                    "created_at": datetime.now(timezone.utc)
                }
            #if pull request is closed - merged only and not rejected ones
            elif (payload.get('action') == 'closed' and payload.get('pull_request', {}).get('merged') == True):
                event_data = {
                    "request_id": str(payload.get('pull_request', {}).get('id')),
                    "author": payload.get('pull_request', {}).get('merged_by',{}).get('login',"N/A"),
                    "action": payload.get('action','merge'), #closed or merge
                    "from_branch": payload.get('pull_request', {}).get('head', {}).get('ref'),
                    "to_branch": payload.get('pull_request', {}).get('base', {}).get('ref'),
                    "timestamp": format_github_timestamp(payload.get('pull_request', {}).get('merged_at', datetime.now(timezone.utc).isoformat())),
                    "created_at": datetime.now(timezone.utc)
                }
        
        if(event_data == {}):
            return {
                "success": False,
                "error": "Unsupported event type or missing data"
            }, 400

        result = mongo.db.webhook_events.insert_one(event_data)

        return {
            "success": True, 
            "record_id": str(result.inserted_id)
        }, 201

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }, 500

@webhook.route('/data', methods=["GET"]) # Data Retrieval Route with Pagination
def data():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 15))
        skip = (page - 1) * per_page
        records = list(mongo.db.webhook_events.find().sort("created_at", -1).skip(skip).limit(per_page))
        total_records = mongo.db.webhook_events.count_documents({})
        return json.dumps({
            'success': True, 
            'records': records,
            'total_records': total_records,
            'page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to fetch data: {str(e)}"
        }, 500