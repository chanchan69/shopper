from aiohttp import ClientSession
from random import randint
from json import dumps


class Discord(object):
    def __init__(self, token: str, session: ClientSession) -> None:
        self.token = token
        self.session = session
    
    async def send_message(self, body: any, embed: bool, ping: bool, channel_id: int) -> bool:
        payload = self.construct_payload(body, ping, embed)
        
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "authorization": self.token,
            "content-length": str(len(dumps(payload))),
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
            }
        
        async with self.session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload) as resp:
            return resp.status == 200
    
    async def get_invite(self, channel_id: int) -> str:
        payload = {
            "validate": None,
            "max_age": 604800,
            "max_uses": 0,
            "target_type": None,
            "temporary": False
        }

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "authorization": self.token,
            "content-length": str(len(dumps(payload))),
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
            }

        async with self.session.post(f"https://discord.com/api/v9/channels/{channel_id}/invites", headers=headers, json=payload) as resp:
            c = await resp.json()
            return c["code"]
    
    @staticmethod
    def nonce() -> str:
        return str(randint(pow(10, 17-1), pow(10, 17) - 1))
    
    def construct_payload(self, body: any, ping: bool, embed: bool = False) -> dict:
        if embed:
            payload = {
                "embeds": body,
                "nonce": self.nonce(), 
                "tts": False
                }
        
        else:
            payload = {
                "content": body, 
                "nonce": self.nonce(), 
                "tts": False
                }
                
        if ping and embed:
            payload["content"] = "||@everyone||"
        elif ping and not embed:
            payload["content"] += " \n||@everyone||"

        return payload
