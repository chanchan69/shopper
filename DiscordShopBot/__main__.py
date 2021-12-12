import asyncio
from DiscordShopBot import *
from DiscordShopBot.config import Shop
from DiscordShopBot.utils import epic_file_dialog
from DiscordShopBot.discord import Discord

from os import system
from json import load
from aiohttp import ClientSession
from time import sleep
from datetime import datetime, timedelta


class Main:
    def __init__(self) -> None:
        while True:
            system("cls")
            i = input(main_menu)
            
            if i == "1":
                asyncio.run(self.send_messages())
            elif i == "2":
                self.new_shop()
            elif i == "3":
                asyncio.run(self.get_invites())
            elif i == "4":
                self.settings()
            elif i == "5":
                asyncio.run(self.test_embed())
            elif i == "x":
                break
    
    def new_shop(self) -> None:
        system("cls")
        print(title)
        server_name = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}0{fg('#564787')}] {fg('#B392AC')}Server Name: ")
        server_id = int(input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}1{fg('#564787')}] {fg('#B392AC')}Server ID: "))
        channel_id = int(input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}2{fg('#564787')}] {fg('#B392AC')}Channel ID: "))
        interval = int(input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}3{fg('#564787')}] {fg('#B392AC')}Ping Interval (in days): "))
        can_ping = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}4{fg('#564787')}] {fg('#B392AC')}Can Ping (y/n): ") == "y"
        can_embed = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}5{fg('#564787')}] {fg('#B392AC')}Can Embed (y/n): ") == "y"
        if input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}6{fg('#564787')}] {fg('#B392AC')}Use Custom Ping (y/n): ") == "y":
            custom_ping = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}7{fg('#564787')}] {fg('#B392AC')} Custom Ping Message: ")
        else:
            custom_ping = "None"

        shop = Shop(server_name, server_id, channel_id, interval, can_ping, can_embed, custom_ping)
        Config.add_shop(shop)
    
    def settings(self) -> None:
        system("cls")
        while True:
            settings_menu = f"{fg('#16F4D0')}{title} \n\n      {fg('#564787')}[{fg('#F2D0A9')}Select an Value to Edit{fg('#564787')}]\n\n      {fg('#564787')}[{fg('#F2D0A9')}1{fg('#564787')}] {fg('#B392AC')}Discord Token: {Config.config['discordToken']}\n      {fg('#564787')}[{fg('#F2D0A9')}2{fg('#564787')}] {fg('#B392AC')}Embed Messages: {Config.config['embed']}\n      {fg('#564787')}[{fg('#F2D0A9')}3{fg('#564787')}] {fg('#B392AC')}Messages: [{', '.join(list(Config.config['messages'].keys()))}]\n      {fg('#564787')}[{fg('#F2D0A9')}x{fg('#564787')}] {fg('#B392AC')}Return to Main Menu\n\n      {fg('#564787')}~> {fg('#16F4D0')}"

            i = input(settings_menu)

            if i == "x":
                return
            elif i == "3":
                self.new_message()
                system("cls")
                continue

            system("cls")
            print(title)
            new_value = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}0{fg('#564787')}] {fg('#B392AC')}New Value: ")

            system("cls")
            if i == "1":
                Config.config["discordToken"] = new_value
                Config.update_config()
            elif i == "2":
                Config.config["embed"] = eval(new_value)
                Config.update_config()
            else:
                return
    
    def new_message(self) -> None:
        system("cls")
        print(title)

        message_name = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}0{fg('#564787')}] {fg('#B392AC')}Message Name: ")
        message_text = open(epic_file_dialog("Select your text message"), "r").read()
        if input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}1{fg('#564787')}] {fg('#B392AC')}Include Embed (y/n): ") == "y":
            message_embed = load(open(epic_file_dialog("Select your embed file"), "r"))
        else:
            message_embed = {}
        
        Config.config["messages"][message_name] = {"embed": message_embed, "text": message_text}
        Config.update_config()

        return

    async def send_messages(self) -> None:
        system("cls")
        print(title)

        print(f"\n\n      {fg('#564787')}[{fg('#F2D0A9')}{', '.join(list(Config.config['messages'].keys()))}{fg('#564787')}]")
        message = input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}0{fg('#564787')}] {fg('#B392AC')}Select a Message: ")
        message = Config.config["messages"][message]

        system("cls")
        print(title)

        print(f"\n\n      {fg('#564787')}[{fg('#F2D0A9')}Press Ctrl+C to Exit{fg('#564787')}]")
        async with ClientSession() as session:
            d = Discord(Config.config["discordToken"], session)
            while True:
                try:
                    for shop in Config.config["shops"]:
                        try:
                            last_ping = datetime.strptime(shop["lastPing"], "%Y-%m-%d %H:%M:%S.%f")
                            can_ping = (datetime.now() - last_ping).days >= shop["interval"]
                        except:
                            can_ping = True
                        
                        if not can_ping:
                            continue

                        if shop["can_embed"] and message["embed"] != {} and Config.config["embed"]:
                            await d.send_message(message["embed"], True, shop["can_ping"], shop["channel_id"])
                        else:
                            await d.send_message(message["text"], False, shop["can_ping"], shop["channel_id"])
                        
                        if shop["custom_ping"] != "None":
                            await d.send_message(shop["custom_ping"], False, False, shop["channel_id"])
                        
                        for x in range(0, len(Config.config["shops"])):
                            if Config.config["shops"][x]["channel_id"] == shop["channel_id"]:
                                Config.config["shops"][x]["lastPing"] = str(datetime.now())
                                Config.update_config()
                        print(f"\n      {shop['server_name']}: {fg('#564787')}[{fg('#F2D0A9')}Next Ping {datetime.now() + timedelta(days=shop['interval'])}{fg('#564787')}]")
                        sleep(1)
                    sleep(10)
                except Exception as ex:
                    break

    async def get_invites(self) -> None:
        system("cls")
        print(title)

        async with ClientSession() as session:
            d = Discord(Config.config["discordToken"], session)
            for shop in Config.config["shops"]:
                try:
                    code = "https://discord.gg/"+ await d.get_invite(shop["channel_id"])
                except:
                    code = "failed"
                
                print(f"\n      {shop['server_name']}: {fg('#564787')}[{fg('#F2D0A9')}{code}{fg('#564787')}]")
        
        input()

    async def test_embed(self) -> None:
        system("cls")
        print(title)

        chanel_id = int(input(f"\n      {fg('#564787')}[{fg('#F2D0A9')}0{fg('#564787')}] {fg('#B392AC')}Channel ID: "))

        async with ClientSession() as session:
            d = Discord(Config.config["discordToken"], session)
            await d.send_message([
    {
      "title": "Test Embed",
      "description": "Does this server allow embeds?",
      "color": None,
      "author": {
        "name": "Shopper"
      },
      "footer": {
        "text": "made by sirchanchan",
        "icon_url": "https://cdn.discordapp.com/avatars/892098730499653662/a_514e6d245c39664fedd65380c47a1449.gif?size=256"
      }
    }
  ], True, False, chanel_id)


if __name__ == "__main__":
    Main()
