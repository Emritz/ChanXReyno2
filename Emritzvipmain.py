#!/usr/bin/python

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from Emritzvip import Emritz



def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)


def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != " ":
                color_index = int(
                    (
                        (x / (width - 1 if width > 1 else 1))
                        + (y / (height - 1 if height > 1 else 1))
                    )
                    * 0.5
                    * (len(colors) - 1)
                )
                color_index = min(
                    max(color_index, 0), len(colors) - 1
                )  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text


def banner(console):
    os.system("cls" if os.name == "nt" else "clear")
    brand_name = "Please Join Our Channel 𝙀𝙢𝙧𝙞𝙩𝙯 𝙋𝙧𝙞𝙫𝙖𝙩𝙚 𝙏𝙤𝙤𝙡 𝘾𝙝𝙖𝙣𝙣𝙚𝙡"

    text = Text(brand_name, style="bold black")

    console.print(text)
    console.print(
        "[bold white] ============================================================[/bold white]"
    )
    console.print(
        "[bold red]      𝗣𝗟𝗘𝗔𝗦𝗘 𝗟𝗢𝗚 𝗢𝗨𝗧 𝗙𝗥𝗢𝗠 𝗖𝗣𝗠 𝗕𝗘𝗙𝗢𝗥𝗘 𝗨𝗦𝗜𝗡𝗚 𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟[/bold red]"
    )
    console.print("[bold red]      𝗦𝗛𝗔𝗥𝗜𝗡𝗚 𝗧𝗛𝗘 𝗔𝗖𝗖𝗘𝗦 𝗞𝗘𝗬 𝗜𝗦 𝗡𝗢𝗧 𝗔𝗟𝗟𝗢𝗪𝗘𝗗[/bold red]")
    console.print(
        "[bold white] ============================================================[/bold white]"
    )


def load_player_data(cpm):
    response = cpm.get_player_data()

    if response.get("ok"):
        data = response.get("data")

        if all(key in data for key in ["floats", "localID", "money"]):

            console.print(
                "[bold][red]========[/red][ ᴘʟᴀʏᴇʀ ᴅᴇᴛᴀɪʟꜱ ][red]========[/red][/bold]"
            )

            console.print(
                f"[bold white]   >> Name        : {data.get('Name', 'UNDEFINED')}[/bold white]"
            )
            console.print(
                f"[bold white]   >> LocalID     : {data.get('localID', 'UNDEFINED')}[/bold white]"
            )
            console.print(
                f"[bold white]   >> Moneys      : {data.get('money', 'UNDEFINED')}[/bold white]"
            )
            console.print(
                f"[bold white]   >> Coins       : {data.get('coin', 'UNDEFINED')}[/bold white]"
            )
        else:
            console.print(
                "[bold red] '! ERROR: new accounts must be signed-in to the game at least once (✘)[/bold red]"
            )
            exit(1)
    else:
        console.print(
            "[bold red] '! ERROR: seems like your login is not properly set (✘)[/bold red]"
        )
        exit(1)


def load_key_data(cpm):

    data = cpm.get_key_data()

    console.print(
        "[bold][red]========[/red][ 𝘼𝘾𝘾𝙀𝙎𝙎 𝙆𝙀𝙔 𝘿𝙀𝙏𝘼𝙄𝙇𝙎 ][red]========[/red][/bold]"
    )

    console.print(
        f"[bold white]   >> Access Key  [/bold white]: [black]{data.get('access_key')}[/black]"
    )

    console.print(
        f"[bold white]   >> Telegram ID : {data.get('telegram_id')}[/bold white]"
    )

    console.print(
        f"[bold white]   >> Balance     : {data.get('coins') if not data.get('is_unlimited') else 'Unlimited'}[/bold white]"
    )


def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            console.print(
                f"[bold red]{tag} cannot be empty or just spaces. Please try again (✘)[/bold red]"
            )
        else:
            return value


def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    console.print(
        "[bold red] =============[bold white][ 𝙇𝙊𝘾𝘼𝙏𝙄𝙊𝙉 ][/bold white]=============[/bold red]"
    )
    console.print(
        f"[bold white]    >> Country    : {data.get('country')} {data.get('zip')}[/bold white]"
    )
    console.print(
        "[bold red] ===============[bold white][ ＭＥＮＵ ][/bold white]===========[/bold red]"
    )


def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i : i + 2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i : i + 2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(
        int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb)
    )
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)


def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f"[{interpolated_color}]{char}"
    return modified_string


if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value(
            "[bold][?] Account Email[/bold]", "Email", password=False
        )
        acc_password = prompt_valid_value(
            "[bold][?] Account Password[/bold]", "Password", password=False
        )
        acc_access_key = prompt_valid_value(
            "[bold][?] Access Key[/bold]", "Access Key", password=False
        )
        console.print("[bold red][%] Trying to Login[/bold red]: ", end=None)
        cpm = Emritz(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]ACCOUNT NOT FOUND (✘)[/bold red]")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold red]WRONG PASSWORD (✘)[/bold red]")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold red]INVALID ACCESS KEY (✘)[/bold red]")
                sleep(2)
                continue
            else:
                console.print("[bold red]TRY AGAIN[/bold red]")
                console.print(
                    "[bold red] '! Note: make sure you filled out the fields ![/bold red]"
                )
                sleep(2)
                continue
        else:
            console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
            sleep(1)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = [
                "00",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
            ]
            console.print(
                "[bold red][bold white](01)[/bold white]: King Rank                      [bold red]8K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](02)[/bold white]: Change Name                    [bold red]100[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](03)[/bold white]: Number Plates                  [bold red]2K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](04)[/bold white]: Account Delete                 [bold red]Free[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](05)[/bold white]: Account Register               [bold red]Free[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](06)[/bold white]: Delete Friends                 [bold red]500[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](07)[/bold white]: Unlock All Cars Siren          [bold red]3.5K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](08)[/bold white]: Unlock W16 Engine              [bold red]4K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](09)[/bold white]: Unlock All Horns               [bold red]3K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](10)[/bold white]: Unlock Disable Damage          [bold red]3K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](11)[/bold white]: Unlock Unlimited Fuel          [bold red]3K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](12)[/bold white]: Unlock Home 3                  [bold red]4K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](13)[/bold white]: Unlock Smoke                   [bold red]4K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](14)[/bold white]: Unlock Wheels                  [bold red]4K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](15)[/bold white]: Unlock Animations              [bold red]2K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](16)[/bold white]: Unlock Equipaments M           [bold red]3K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](17)[/bold white]: Unlock Equipaments F           [bold red]3K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](18)[/bold white]: Change Race Wins               [bold red]1K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](19)[/bold white]: Change Race Loses              [bold red]1K[/bold red][/bold red]"
            )
            console.print(
                "[bold red][bold white](0) [/bold white]: Exit From Tool [/bold red]"
            )

            console.print(
                "[bold red]===============[bold white][ VIPEMRITZ ][/bold white]===============[/bold red]"
            )

            service = IntPrompt.ask(
                f"[bold][?] Select a Service [red][1-{choices[-1]} or 0][/red][/bold]",
                choices=choices,
                show_choices=False,
            )

            console.print(
                "[bold red]===============[bold white][ VIPEMRITZ ][/bold white]===============[/bold red]"
            )

            if service == 0:  # Exit
                console.print("[bold white] Thank You for using my tool[/bold white]")
            elif service == 1:  # King Rank
                console.print(
                    "[bold red][!] Note:[/bold red]: if the king rank doesn't appear in game, close it and open few times.",
                    end=None,
                )
                console.print(
                    "[bold red][!] Note:[/bold red]: please don't do King Rank on same account twice.",
                    end=None,
                )
                sleep(2)
                console.print("[%] Giving you a King Rank: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold red] 'SUCCESSFUL[/bold red]")
                    console.print(
                        "[bold red] '======================================[/bold red]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
elif service == 2:  # Change Name
    console.print("[bold red][?] Enter your new Name[/bold red]")
    new_name = Prompt.ask("[?] Name")

    if 1 <= len(new_name) <= 64:  # Reasonable length limit for a name
        console.print("[bold green][%] Saving your data...[/bold green]")

        if cpm.set_player_name(new_name):
            console.print("[bold green]✔ SUCCESSFUL[/bold green]")
            console.print("[bold green]======================================[/bold green]")

            answ = Prompt.ask(
                "[?] Do you want to exit?", choices=["y", "n"], default="n"
            )
            if answ == "y":
                console.print("[bold white]Thank you for using my tool[/bold white]")
                break  # Exit the loop
            else:
                continue
        else:
            console.print("[bold red]✖ FAILED[/bold red]")
            console.print("[bold red]Please try again[/bold red]")
            sleep(2)
            continue
    else:
        console.print("[bold red]✖ FAILED[/bold red]")
        console.print("[bold red]Please enter a valid name (1-64 characters)[/bold red]")
        sleep(2)
        continue
            elif service == 3:  # Number Plates
                console.print("[%] Giving you a Number Plates: ", end=None)
                if cpm.set_player_plates():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 4:  # Account Delete
                console.print(
                    "[bold red] '[!] After deleting your account there is no going back !![/bold red]"
                )
                answ = Prompt.ask(
                    "[?] Do You want to Delete this Account ?!",
                    choices=["y", "n"],
                    default="n",
                )
                if answ == "y":
                    cpm.delete()
                    console.print("[bold red] 'SUCCESSFUL[/bold red]")
                    console.print(
                        "[bold red] '======================================[/bold red]"
                    )
                    console.print(
                        "[bold red] f'Thank You for using our tool, please join our telegram channe: @𝙀𝙢𝙧𝙞𝙩𝙯 𝙋𝙧𝙞𝙫𝙖𝙩𝙚 𝙏𝙤𝙤𝙡 𝘾𝙝𝙖𝙣𝙣𝙚𝙡[/bold red]"
                    )
                else:
                    continue
            elif service == 5:  # Account Register
                console.print("[bold red] '[!] Registring new Account[/bold red]")
                acc2_email = prompt_valid_value(
                    "[?] Account Email", "Email", password=False
                )
                acc2_password = prompt_valid_value(
                    "[?] Account Password", "Password", password=False
                )
                console.print("[%] Creating new Account: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold red] 'SUCCESSFUL[/bold red]")
                    console.print(
                        "[bold red] '======================================[/bold red]"
                    )
                    console.print(
                        "[bold red] f'INFO: In order to tweak this account with Telmun[/bold red]"
                    )
                    console.print(
                        "[bold red] 'you most sign-in to the game using this account[/bold red]"
                    )
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold red] 'This email is already exists ![/bold red]"
                    )
                    sleep(2)
                    continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 6:  # Delete Friends
                console.print("[%] Deleting your Friends: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 7:  # Unlock All Cars Siren
                console.print("[%] Unlocking All Cars Siren: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 8:  # Unlock w16 Engine
                console.print("[%] Unlocking w16 Engine: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 9:  # Unlock All Horns
                console.print("[%] Unlocking All Horns: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 10:  # Disable Engine Damage
                console.print("[%] Unlocking Disable Damage: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 11:  # Unlimited Fuel
                console.print("[%] Unlocking Unlimited Fuel: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 12:  # Unlock House 3
                console.print("[%] Unlocking House 3: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 13:  # Unlock Smoke
                console.print("[%] Unlocking Smoke: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 14:  # Unlock Smoke
                console.print("[%] Unlocking Wheels: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(8)
                    continue
            elif service == 15:  # Unlock Smoke
                console.print("[%] Unlocking Animations: ", end=None)
                if cpm.unlock_animations():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 16:  # Unlock Smoke
                console.print("[%] Unlocking Equipaments Male: ", end=None)
                if cpm.unlock_equipments_male():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 17:  # Unlock Smoke
                console.print("[%] Unlocking Equipaments Female: ", end=None)
                if cpm.unlock_equipments_female():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Thank You for using my tool[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print("[bold red]Please Try Again[/bold red]")
                    sleep(2)
                    continue
            elif service == 18:  # Change Races Wins
                console.print(
                    "[bold red] '[!] Insert how much races you win[/bold red]"
                )
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if (
                    amount > 0
                    and amount
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                ):
                    if cpm.set_player_wins(amount):
                        console.print("[bold red] 'SUCCESSFUL[/bold red]")
                        console.print(
                            "[bold red] '======================================[/bold red]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print("[bold red]Please Try Again[/bold red]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold red] '[!] Please use valid values[/bold red]"
                    )
                    sleep(2)
                    continue
            elif service == 19:  # Change Races Loses
                console.print(
                    "[bold red] '[!] Insert how much races you lose[/bold red]"
                )
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if (
                    amount > 0
                    and amount
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                ):
                    if cpm.set_player_loses(amount):
                        console.print("[bold red] 'SUCCESSFUL[/bold red]")
                        console.print(
                            "[bold red] '======================================[/bold red]"
                        )
                        answ = Prompt.ask(
                            "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Thank You for using my tool[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold red]FAILED[/bold red]")
                        console.print(
                            "[bold red] '[!] Please use valid values[/bold red]"
                        )
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED[/bold red]")
                    console.print(
                        "[bold red] '[!] Please use valid values[/bold red]"
                    )
                    sleep(2)
                    continue
            else:
                continue
            break
        break
