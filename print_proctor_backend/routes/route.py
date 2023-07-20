from fastapi import APIRouter,Depends,HTTPException
from models.users import User
from config.database import collection_name
from schemas.schemas import list_serial
from bson import ObjectId
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import timedelta,datetime
from jose import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

SECRET_KEY = '6c4af5dcbb3b06a3deac8813556f8867de907b455ac0fb8399e54aba02003567'
ALGORITHM = 'HS256'

def get_password_hash(password):
    return pwd_context.hash(password)

def check_user_exists(username : str):
    user_exist = collection_name.find_one({"username": username})

    return user_exist is not None

def authenticate_user(username,password):
    
    if check_user_exists(username):
        user_details = collection_name.find_one({"username": username})
        
        password_check = pwd_context.verify(password,user_details["password"])
        return password_check
    return False

def create_access_token(data:dict,expires_delta:timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

@router.post('/api/register')
async def sign_up(new_user:User):
    
    collection_name.insert_one({"username": new_user.username, "password": get_password_hash(new_user.password) })
    return {"message": "User registered successfully","status":True}

@router.post('/api/login')
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if authenticate_user(username,password):
        access_token = create_access_token(data={"sub":username},expires_delta=timedelta(minutes=60))
        return {"access_token":access_token,"token_type": "bearer"}
    else:
        raise HTTPException(status_code = 400,detail="Incorrect credentials provided!")


@router.get('/api/health_check')
async def health_check(token: str=Depends(oauth2_scheme)):
    return {"access_token": token}

