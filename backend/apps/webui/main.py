from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from apps.webui.routers import (
    auths,
    users,
    chats,
    documents,
    tools,
    models,
    prompts,
    configs,
    memories,
    utils,
)
from config import (
    WEBUI_BUILD_HASH,
    SHOW_ADMIN_DETAILS,
    ADMIN_EMAIL,
    WEBUI_AUTH,
    DEFAULT_MODELS,
    DEFAULT_PROMPT_SUGGESTIONS,
    DEFAULT_USER_ROLE,
    ENABLE_SIGNUP,
    MASK_LOCATION,
    MASK_COMPANY,
    MASK_NAME,
    MASK_CREDIT_CARD,
    MASK_CRYPTO,
    MASK_EMAIL_ADDRESS,
    MASK_IBAN_CODE,
    MASK_IP_ADDRESS,
    MASK_PERSON,
    MASK_PHONE_NUMBER,
    MASK_US_SSN,
    MASK_US_BANK_NUMBER,
    MASK_CREDIT_CARD_RE,
    MASK_UUID,
    MASK_EMAIL_ADDRESS_RE,
    MASK_US_SSN_RE,
    MASK_URL,
    USER_PERMISSIONS,
    WEBHOOK_URL,
    WEBUI_AUTH_TRUSTED_EMAIL_HEADER,
    JWT_EXPIRES_IN,
    WEBUI_BANNERS,
    ENABLE_COMMUNITY_SHARING,
    AppConfig,
)

app = FastAPI()

origins = ["*"]

app.state.config = AppConfig()

app.state.config.MASK_COMPANY = MASK_COMPANY
app.state.config.MASK_NAME = MASK_NAME
app.state.config.MASK_LOCATION = MASK_LOCATION
app.state.config.MASK_CREDIT_CARD = MASK_CREDIT_CARD
app.state.config.MASK_CRYPTO = MASK_CRYPTO
app.state.config.MASK_EMAIL_ADDRESS = MASK_EMAIL_ADDRESS
app.state.config.MASK_IBAN_CODE = MASK_IBAN_CODE
app.state.config.MASK_IP_ADDRESS = MASK_IP_ADDRESS
app.state.config.MASK_PERSON = MASK_PERSON
app.state.config.MASK_PHONE_NUMBER = MASK_PHONE_NUMBER
app.state.config.MASK_US_SSN = MASK_US_SSN
app.state.config.MASK_US_BANK_NUMBER = MASK_US_BANK_NUMBER
app.state.config.MASK_CREDIT_CARD_RE = MASK_CREDIT_CARD_RE
app.state.config.MASK_UUID = MASK_UUID
app.state.config.MASK_EMAIL_ADDRESS_RE = MASK_EMAIL_ADDRESS_RE
app.state.config.MASK_US_SSN_RE = MASK_US_SSN_RE
app.state.config.MASK_URL = MASK_URL

app.state.config.ENABLE_SIGNUP = ENABLE_SIGNUP
app.state.config.JWT_EXPIRES_IN = JWT_EXPIRES_IN
app.state.AUTH_TRUSTED_EMAIL_HEADER = WEBUI_AUTH_TRUSTED_EMAIL_HEADER


app.state.config.SHOW_ADMIN_DETAILS = SHOW_ADMIN_DETAILS
app.state.config.ADMIN_EMAIL = ADMIN_EMAIL


app.state.config.DEFAULT_MODELS = DEFAULT_MODELS
app.state.config.DEFAULT_PROMPT_SUGGESTIONS = DEFAULT_PROMPT_SUGGESTIONS
app.state.config.DEFAULT_USER_ROLE = DEFAULT_USER_ROLE
app.state.config.USER_PERMISSIONS = USER_PERMISSIONS
app.state.config.WEBHOOK_URL = WEBHOOK_URL
app.state.config.BANNERS = WEBUI_BANNERS

app.state.config.ENABLE_COMMUNITY_SHARING = ENABLE_COMMUNITY_SHARING

app.state.MODELS = {}
app.state.TOOLS = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auths.router, prefix="/auths", tags=["auths"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(models.router, prefix="/models", tags=["models"])
app.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
app.include_router(memories.router, prefix="/memories", tags=["memories"])

app.include_router(configs.router, prefix="/configs", tags=["configs"])
app.include_router(utils.router, prefix="/utils", tags=["utils"])


@app.get("/")
async def get_status():
    return {
        "status": True,
        "auth": WEBUI_AUTH,
        "default_models": app.state.config.DEFAULT_MODELS,
        "default_prompt_suggestions": app.state.config.DEFAULT_PROMPT_SUGGESTIONS,
    }
