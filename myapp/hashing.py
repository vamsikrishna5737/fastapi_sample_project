from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class hash():
    def bcrypt(password: str):
        
        hashedpassword= pwd_cxt.hash(password)
        return hashedpassword

    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)
