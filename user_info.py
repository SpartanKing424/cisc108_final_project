from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str


user_database = [
    User("user1", "1")
]