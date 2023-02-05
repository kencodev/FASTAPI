from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This function hashes a password
def hash(password: str):
    return pwd_context.hash(password)


# This function hashes plain password and verifies if it is the same as hashed password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
