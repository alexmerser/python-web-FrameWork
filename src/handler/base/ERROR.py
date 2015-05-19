"""
API ERROR_CODE Constants

"""

NORMAL = 0
COOKIE_EXPIRED = 1
API_INTERNAL_ERROR = 2
ACCESS_RIGHT_ERROR = 3
UNKNOWN_ERROR = 10
PARAMETERS_INVALID = 11
IP_NOT_IN_SETTING_LIST = 12

# account
INVALID_ACCOUNT_OR_PASSWORD = 1002
USER_ON_TRIAL = 1003
USER_FORBIDDEN = 1004
NO_AUTH_INFO = 1004
AGENT_NOT_FOUND = 1005
INVALID_VIDEO_PASSWORD = 1006
INVALID_MAIL = 1007
ACTIVE_CODE_EXPIRE = 1008
USER_NOT_EXISTS = 1009
USER_DOMAIN_ERROR = 1010
CANNOT_CREATE_SUB_ADMIN = 1011
REACH_STAFF_LIMIT = 1012
USER_USERNAME_EXISTS = 1013

# sub account
SUB_ID_REQUIRE = 8001
DELETE_USER_FAILED = 8002
SUB_USERNAME_EXISTS = 8003

# group
GROUP_ID_REQUIRE = 12001
GROUP_NAME_EXIST = 12002
DELETE_GROUP_FAILED = 12003
GROUP_NOT_FOUND = 12004
GROUP_NAME_REQUIRE = 12005
GROUP_USER_LIST_INVALID = 12006
GROUP_WORK_TABLES_INVALID = 12007