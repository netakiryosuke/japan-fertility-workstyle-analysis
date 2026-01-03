from typing import Annotated, Any

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str]:
    if isinstance(v, str):
        return [i.strip().rstrip("/") for i in v.split(",") if i.strip()]
    if isinstance(v, list):
        return [str(i).rstrip("/") for i in v]
    raise ValueError(v)

class WebConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    BACKEND_CORS_ORIGINS: Annotated[
        list[str], BeforeValidator(parse_cors)
    ] = []

web_config = WebConfig()
