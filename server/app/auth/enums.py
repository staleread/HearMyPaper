from enum import StrEnum, Enum


class UserRole(StrEnum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"


class UserPermission(StrEnum):
    CAN_READ_COURSE_INFO = "can_read_course_info"
    CAN_READ_USER_INFO = "can_read_user_info"
    CAN_READ_SUBMITION_INFO = "can_read_submition_info"
    CAN_READ_SUBMITION_CONTENT = "can_read_submition_content"
    CAN_JOIN_COURSE = "can_join_course"
    CAN_MODIFY_OWN_USER_INFO = "can_modify_own_user_info"
    CAN_CREATE_SUBMITION = "can_create_submition"
    CAN_CREATE_COURSE = "can_create_course"
    CAN_CONVERT_SUBMITION_TO_AUDIO = "can_convert_submition_to_audio"


class ConfidentialityLevel(Enum):
    PUBLIC = 1
    RESTRICTED = 2
    CONFIDENTIAL = 3
