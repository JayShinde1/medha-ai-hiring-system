from passlib.context import CryptContext
# pure hashing logic


bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def hash_password(password: str):
    return bcrypt_context.hash(password)

def verify_password(actual_password, hashed_password):
    return bcrypt_context.verify(actual_password, hashed_password)