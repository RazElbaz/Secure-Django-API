USER_ROLES = {
    "b4d3658f-8c48-4e63-9f77": ["admin"],
    "f2d9e912-df15-4d5e-9c7d": ["user"],
    "92d9e13e-9d4d-4a91-8e3d": ["superuser"],
    "e1c4b3f7-9a8c-4d8b-99f0": ["editor"],
    "9f6e72c3-40c8-42cb-bf2a": ["viewer"],
    "5e86355d-9e89-4a67-9f28": ["admin", "user"],
    "21d7f3c8-b9ae-485e-964e": ["editor", "viewer"]
}

def get_user_roles(user_id):
    return USER_ROLES.get(user_id, [])