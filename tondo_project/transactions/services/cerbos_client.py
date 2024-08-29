import uuid
import requests
import logging
from .user_roles import get_user_roles

logger = logging.getLogger(__name__)
CERBOS_URL = 'http://cerbos:3592/api/check'

def check_user_role(user_id, action):
    """Check if the user is authorized to perform the given action."""
    #https://docs.cerbos.dev/cerbos/latest/policies/scoped_policies
    roles = get_user_roles(user_id)
    payload = {
        "request_id": str(uuid.uuid4()), 
        "actions": [action],
        "principal": {
            "id": user_id,
            "roles": roles
        },
        "resource": {
            "kind": "transaction",  
            "instances": {
                "resource_id": {}
            }
        }
    }
    
    logger.info(payload)
    try:
        response = requests.post(CERBOS_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        # Check if the action is allowed, https://docs.cerbos.dev/cerbos/latest/tutorial/03_calling-cerbos.html
        actions = result.get("resourceInstances", {}).get("resource_id", {}).get('actions', {})
        action_effect = actions.get(action, 'EFFECT_DENY')

        if action_effect  == 'EFFECT_ALLOW':
            return True
    except requests.RequestException as e:
        logger.error(f"Error contacting Cerbos: {e}")
    
    return False
    