from datetime import datetime
from bson import ObjectId

github_event_schema = {
    "_id": ObjectId,
    "request_id": str,
    "author": str,
    "action": str,
    "from_branch": str,
    "to_branch": str,
    "timestamp": datetime,
    "created_at": datetime
}
