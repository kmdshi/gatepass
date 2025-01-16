from pydantic import EmailStr
import time


def create_qr_link(orgHash: str):
    time = time.time().round()
    orgHashTime = f'{orgHash}-{time}'
