from json import load, dump


class Shop(object):
    def __init__(self, server_name: str, server_id: int, channel_id: int, interval: int, can_ping: bool, can_embed: str, custom_ping: str) -> None:
        self.server_name =  server_name
        self.server_id   =  server_id
        self.channel_id  =  channel_id
        self.interval    =  interval
        self.can_ping    =  can_ping
        self.can_embed   =  can_embed
        self.custom_ping =  custom_ping


class Config(object):

    CONFIG_DATA = {"discordToken": "None", "embed": False, "messages": {}, "shops": []}

    def __init__(self) -> None:
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        try:
            return load(open("config.json", "r"))
        except:
            self.create_config()
            return load(open("config.json", "r"))
    
    def create_config(self) -> dict:
        dump(self.CONFIG_DATA, open("config.json", "w+"))
    
    def update_config(self) -> None:
        dump(self.config, open("config.json", "w+"), sort_keys=True, indent=4)
    
    def add_shop(self, shop: Shop) -> None:
        new_shop = shop.__dict__
        new_shop["lastPing"] = "None"
        self.config["shops"].append(new_shop)
        self.update_config()
