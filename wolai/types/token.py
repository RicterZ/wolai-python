
class AppToken:
    app_token: str = None
    app_id: str = None
    created_time: int = 0
    expired_time: int = -1
    updated_time: int = 0

    def __init__(self, app_token: str, app_id: str, create_time: int, expire_time: int, update_time: int):
        self.app_token = app_token
        self.app_id = app_id
        self.created_time = create_time
        self.expired_time = expire_time
        self.updated_time = update_time

    def __str__(self):
        return self.app_token

    def __repr__(self):
        return f'<WolaiToken: {self.app_token}, app id: {self.app_id}, expired at: {self.expired_time}>'

