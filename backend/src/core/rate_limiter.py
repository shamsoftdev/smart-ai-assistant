from fastapi import HTTPException
import time

request_log = {}

def rate_limiter(user: str):
    username = user   
    
    now = time.time()

    if username not in request_log:
        request_log[username] = []

    request_log[username].append(now)

    # keep last 60 seconds
    request_log[username ] = [
        t for t in request_log[username] if now - t < 60
        ]
    
    print("User:", username) 
    print("Requests:", request_log[username])

    if len(request_log[username]) >= 3:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    