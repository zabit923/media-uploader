from pydantic import BaseModel


class AudioRead(BaseModel):
    download_url: str
