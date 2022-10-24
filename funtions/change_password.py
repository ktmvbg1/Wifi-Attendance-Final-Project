import auth
from models import *

def change_password(session, username, password, newpassword, confirmpassword):
    user = session.query(User).filter_by(username=username).first()
    if not auth.verify_password(password, user.password):
        return {"msg": "Incorrect Password"}
    elif password == newpassword:
        return {"msg": "New password must be different from current password"}
    elif newpassword != confirmpassword:
        return {"msg": "Incorrrect confirmation of new password"}
    else:
        newpasswordhash = auth.get_password_hash(newpassword)
        user.password = newpasswordhash
        session.commit()
        return {"msg": "Change Successful"}