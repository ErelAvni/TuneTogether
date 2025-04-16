from datetime import datetime

# Ensure the timestamp has only date and time (no microseconds)
def get_current_time():
    """Get the current time without seconds and microseconds."""
    now = datetime.now()
    return now.replace(second=0, microsecond=0)


class Comment:
    def __init__(self, username: str, content: str, timestamp: datetime = None):
        self.username = username
        self.content = content
        self.timestamp = timestamp or get_current_time()


    @classmethod
    def from_dict(cls, data: dict):
        """Create a Comment object from a dictionary representation, ignoring seconds."""
        username = data['username']
        content = data['content']
        timestamp_str = data['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None
        if timestamp:
            timestamp = timestamp.replace(second=0, microsecond=0)
        return cls(username=username, content=content, timestamp=timestamp)


    def to_dict(self):
        """Convert the Comment object to a dictionary representation."""
        return {
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    

    def to_json(self):
        """Convert the Comment object to a JSON string."""
        import json
        return json.dumps(self.to_dict())


    def __repr__(self):
        '''Return a string representation of the Comment object.
        The representation includes the username, content, and timestamp, and is formatted for readability
        within the page itself.'''

        return f"{self.username}: \n{self.content} \n Commented at: {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    

if __name__ == "__main__":
    # Example usage
    comment = Comment(username="user123", content="This is a test comment.")
    print(comment.to_dict())
    print(comment.to_json())
    print(Comment.from_dict(comment.to_dict()))
    print(comment)