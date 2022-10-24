from models import *
import datetime
import auth

def login(session, username, password):
    user = session.query(User).filter_by(username=username).first()
    if user:
        if not auth.verify_password(password, user.password):
            return {"msg": "Incorrect Password"}
        else:
            data =  {
                "username": f"{user.username}",
                "user_id": f"{user.user_id}",
                "user_name": f"{user.user_name}",
                "role_id": user.role_id
            }
            return auth.create_access_token(data, datetime.timedelta(hours= 48))
    elif user == None:
        return {"msg": "User Not Found"}