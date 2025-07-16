/#!/usr/bin/python

import os
import sys
import time
import signal
import random
import requests
from time import sleep
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.live import Live
from rich.align import Align
from rich.spinner import Spinner
from chanxreyno2 import Emritz  # Your game logic class

__CHANNEL_USERNAME__ = "𝐂𝐡𝐚𝐧 𝐗 𝐑𝐞𝐲𝐧𝐨 𝐂𝐏𝐌𝟐 𝐓𝐨𝐨𝐥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥"
__GROUP_USERNAME__   = "𝐂𝐡𝐚𝐧 𝐗 𝐑𝐞𝐲𝐧𝐨 𝐂𝐏𝐌𝟐 𝐓𝐨𝐨𝐥 𝐂𝐡𝐚𝐭"

console = Console()

# Signal handler with style
def signal_handler(sig, frame):
    console.print("\n[bold red]✖ Exit triggered. Shutting down...[/bold red]")
    time.sleep(0.5)
    console.print("[bold yellow]👋 Goodbye, Hacker.[/bold yellow]")
    sys.exit(0)

# Gradient text rendering
def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

# Cool animated banner with cycling effect
def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')

    brand_name = "ChanXReyno2"
    padding = 6
    box_width = len(brand_name) + padding
    box_top = "╭" + "─" * box_width + "╮"
    box_mid = f"│{' ' * (padding // 2)}{brand_name}{' ' * (padding // 2)}│"
    box_bot = "╰" + "─" * box_width + "╯"
    box_lines = f"{box_top}\n{box_mid}\n{box_bot}"

    gradient_colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#8A2BE2"]

    # Animate the box with blink effect
    with Live(console=console, refresh_per_second=4, transient=True) as live:
        for _ in range(6):  # blink a few times
            colorful_box = gradient_text(box_lines, gradient_colors)
            live.update(Align.center(colorful_box))
            time.sleep(0.2)
            live.update(Align.center(Text("")))
            time.sleep(0.1)

    # Static Display After Animation
    console.print("\n")
    console.print(gradient_text(box_lines, gradient_colors), justify="center")
    console.print("[bold green]♕ ChanXReyno2[/bold green]: Car Parking Multiplayer 2 Hacking Tool.", justify="center")
    console.print(f"[bold green]♕ Telegram[/bold green]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue] | [bold blue]@{__GROUP_USERNAME__}[/bold blue]", justify="center")
    console.print("[bold red]==================================================[/bold red]", justify="center")
    console.print("[bold yellow]! Note[/bold yellow]: Logout from the game before using this tool!", justify="center")
    console.print("[bold red]==================================================[/bold red]\n", justify="center")
    
# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        WalletData = data.get('WalletData')
        PlayerStorage = data.get('PlayerStorage')

        if 'Money' in WalletData and 'LocalID' in PlayerStorage and 'Brakes' in PlayerStorage:
            name = PlayerStorage.get('Name', 'UNDEFINED')
            local_id = PlayerStorage.get('LocalID', 'UNDEFINED')
            money = WalletData.get('Money', 'UNDEFINED')
            coins = WalletData.get('Coins', 'UNDEFINED')

            table = Table(title="🚗 Player Profile", box=box.SQUARE, border_style="bold cyan")
            table.add_column("Field", style="bold yellow")
            table.add_column("Value", style="bold white")

            table.add_row("👤 Name", str(name))
            table.add_row("🆔 ID", str(local_id))
            table.add_row("💸 Money", str(money))
            table.add_row("🪙 Coins", str(coins))

            console.print(Panel.fit(table, title="[bold green]✓ Player Details Loaded", subtitle="CPM2 Data Viewer", border_style="green"))
    
def load_key_data(cpm):
    data = cpm.get_key_data()

    table = Table(box=box.ROUNDED, border_style="bold green", show_header=False)
    table.add_row("🔑 [bold yellow]Access Key[/bold yellow]", f"{data.get('access_key')}")
    table.add_row("🆔 [bold yellow]Telegram ID[/bold yellow]", f"{data.get('telegram_id')}")
    
    balance = data.get('coins') if not data.get('is_unlimited') else 'Unlimited'
    table.add_row("💰 [bold yellow]Balance[/bold yellow]", str(balance))

    panel = Panel(table, title="🔐 Access Info", border_style="green", padding=(1, 2))
    console.print(panel)

def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()

    table = Table(box=box.SQUARE, border_style="cyan", show_header=False)
    location = f"{data.get('city')}, {data.get('regionName')}, {data.get('countryCode')}"
    table.add_row("📍 [bold yellow]Location[/bold yellow]", location)
    table.add_row("🌐 [bold yellow]ISP[/bold yellow]", data.get('isp'))

    panel = Panel(table, title="🌍 Client Details", subtitle="Fetched via IP", border_style="cyan", padding=(1, 2))
    console.print(panel)

    console.print(Panel("[bold magenta]🛠️ Services Loaded Successfully[/bold magenta]", border_style="magenta"))

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(f"[bold cyan]{content}[/bold cyan]", password=password)
        if not value or value.isspace():
            warning = Text(f"⚠️  {tag} cannot be empty or just spaces. Please try again.", style="bold red")
            console.print(warning)
        else:
            return value

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

# Cool animated banner splash
def animated_intro(console):
    title = "[bold cyan]🚀 CXR Tool[/bold cyan]"
    subtitles = [
        "🔒 Secure. ⚙️ Powerful. 🎮 Game-On!",
        "👑 Powered by Emritz",
        f"📡 Connecting to servers..."
    ]
    with Live(console=console, refresh_per_second=10) as live:
        for subtitle in subtitles:
            panel = Panel(Align.center(Text(subtitle, style="bold white"), vertical="middle"),
                          title=title,
                          border_style="green")
            live.update(panel)
            sleep(1)

# Cool loading spinner text
def loading_spinner(console, message="Processing..."):
    with console.status(f"[bold cyan]{message}[/bold cyan]", spinner="dots"):
        sleep(random.uniform(1.2, 2.2))

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        animated_intro(console)
        banner(console)

        acc_email = prompt_valid_value("[bold][?] Account Email[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] Account Password[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] Access Key[/bold]", "Access Key", password=False)

        loading_spinner(console, "🔐 Attempting Login")
        cpm = Emritz(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)

        if login_response != 0:
            if login_response == 100:
                console.print("[bold red]✖ ACCOUNT NOT FOUND[/bold red]")
            elif login_response == 101:
                console.print("[bold red]✖ WRONG PASSWORD[/bold red]")
            elif login_response == 103:
                console.print("[bold red]✖ INVALID ACCESS KEY[/bold red]")
            else:
                console.print("[bold red]✖ UNKNOWN ERROR[/bold red]")
                console.print("[bold yellow]! Note[/bold yellow]: Make sure all fields are correctly filled.")
            sleep(2)
            continue
        else:
            console.print("[bold green]✅ LOGIN SUCCESSFUL[/bold green]")
            sleep(1.5)

        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()

            console.rule("[bold cyan]💻 Select a Service[/bold cyan]")

            menu_items = [
                "Exit",  # 0
                "Change Email ~ 10K",
                "Change Password ~ 5K",
                "Increase Money ~ 4K",
                "Change Name ~ 1K",
                "Delete Friends ~ 2K",
                "King Rank ~ 6K",
                "Maximize Drag Wins ~ 6K",
                "Unlock All Home ~ 10K",
                "Unlock All Brakes ~ 5K",
                "Unlock All Wheels ~ 6K",
                "Unlock All Male Equipment ~ 9K",
                "Unlock All Calipers ~ 5K",
                "Unlock All Paints ~ 7K",
                "Unlock All Animation ~ 5K",
                "Unlock All Female Equipment ~ 9K",
                "Unlock All Cars Siren ~ 5K",
                "Unlock 20 Slots ~ 7K",  # 17
                "Unlock 20 Slots + 20 Cars Maintenance ~ 10K"       # 18
]

            choices = [str(i) for i in range(len(menu_items))]

            for index, item in enumerate(menu_items):
                color = "green" if item != "Exit" else "red"
                console.print(f"[bold cyan]({index:02}):[/bold cyan] [{color}]{item}[/{color}]")

            console.print()  # Add spacing
            service = IntPrompt.ask(
                f"[bold][?] Select a Service [red][0-{choices[-1]}][/red][/bold]",
                choices=choices,
                show_choices=False
            )

            if service == 0:
                console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                break
            elif service == 1: # Change Email
                console.print("[bold cyan][!] You are about to change your account's email address.[/bold cyan]")
                new_email = Prompt.ask("[bold cyan][?] Enter New Email[/bold cyan]", default="")

                # Basic email format validation (can be more robust)
                if "@" not in new_email or "." not in new_email:
                    console.print("[bold red][!] Invalid email format. Please try again.[/bold red]")
                    sleep(2)
                    continue

                    console.print(f"[bold cyan][%] Changing Email to {new_email}[/bold cyan]: ", end="")
                if cpm.change_email(new_email):
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold yellow][!] Your email has been updated.[/bold yellow]")
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold red][!] The email you entered is already registered to another account or an error occurred.[/bold red]")
                sleep(2)
                continue
            elif service == 2: # Change Password
                console.print("[bold cyan][!] You are about to change your account's password.[/bold cyan]")
                new_password = Prompt.ask("[bold cyan][?] Enter New Password[/bold cyan]", password=True)

                # Add password strength validation (e.g., minimum length, complexity)
                if len(new_password) < 6:
                    console.print("[bold red][!] Password must be at least 8 characters long. Please try again.[/bold red]")
                    sleep(2)
                    continue

                console.print(f"[bold cyan][%] Changing Password[/bold cyan]: ", end="")
                if cpm.change_password(new_password):
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    console.print(f"[bold yellow][!] Your password has been updated.[/bold yellow]")
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold red][!] An error occurred while changing your password. Please try again.[/bold red]")
                    sleep(2)
                    continue 
            elif service == 3: # Increase Money
                console.print("[bold cyan][!] Insert how much money do you want.[/bold cyan]")
                amount = IntPrompt.ask("[bold][?] Amount[/bold]")
                console.print("[bold cyan][%] Saving your data[/bold cyan]: ", end=None)
                if amount > 0 and amount <= 5000000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]SUCCESSFUL.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]FAILED.[/bold red]")
                        console.print("[bold yellow][!] Please try again.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please use valid values.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4: # Change Name
                console.print("[bold cyan][!] Enter your new Name.[/bold cyan]")
                new_name = Prompt.ask("[bold][?] Name[/bold]")
                console.print("[bold cyan][%] Saving your data[/bold cyan]: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 30:
                    if cpm.set_player_name(new_name):
                        console.print("[bold green]SUCCESSFUL.[/bold green]")
                        console.print("==================================")
                        answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                        if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                        else: continue
                    else:
                        console.print("[bold red]FAILED.[/bold red]")
                        console.print("[bold yellow][!] Please try again.[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please use valid values.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5: # Delete Friends
                console.print("[bold cyan][%] Deleting Friends[/bold cyan]: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 6: # King Rank
                console.print("[bold red][!] Note:[/bold red]: if the king rank doesn't appear in game, logout and login few times.")
                console.print("[bold red][!] Note:[/bold red]: please don't do King Rank on same account twice !!.", end="\n\n")
                sleep(2)
                console.print("[bold cyan][%] Upgrading Rank[/bold cyan]: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 7: # Maximize Drag Wins
                console.print("[bold cyan][%] Maximizing drag wins[/bold cyan]: ", end=None)
                if cpm.maximize_drag_wins():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 8: # Unlock Apartments
                console.print("[bold cyan][%] Unlocking All apartments[/bold cyan]: ", end=None)
                if cpm.unlock_apartments():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 9: # Unlock Brakes
                console.print("[bold cyan][%] Unlocking Brakes[/bold cyan]: ", end=None)
                if cpm.unlock_brakes():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10: # Unlock Wheels
                console.print("[bold cyan][%] Unlocking Wheels[/bold cyan]: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11: # Unlock Clothes
                console.print("[bold cyan][%] Unlocking Clothes[/bold cyan]: ", end=None)
                if cpm.unlock_clothes():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 12: # Unlock Calipers
                console.print("[bold cyan][%] Unlocking Caliper[/bold cyan]: ", end=None)
                if cpm.unlock_calipers():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue       
            elif service == 13: # Unlock Paint
                console.print("[bold cyan][%] Unlocking Paints[/bold cyan]: ", end=None)
                if cpm.unlock_paints():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue                     
            elif service == 14: # Unlock animation
                console.print("[bold cyan][%] Unlocking All Animation[/bold cyan]: ", end=None)
                if cpm.unlock_animation():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue 
            elif service == 15: # Unlock female
                console.print("[bold cyan][%] Unlocking All Female Equipment[/bold cyan]: ", end=None)
                if cpm.unlock_clothess():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16:  # Unlock All Cars Siren
                console.print("[bold cyan][%] Unlocking All Cars Siren[/bold            cyan]: ", end=None)
                if cpm.unlock_all_cars_siren():            
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17: # Unlock Slots
                console.print("[bold cyan][%] Unlocking all slots[/bold cyan]: ", end=None)
                if cpm.unlock_slots():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18: # Unlock 
                console.print("[bold cyan][%] Maintenance [/bold cyan]: ", end=None)
                if cpm.unlock_slotss():
                    console.print("[bold green]SUCCESSFUL.[/bold green]")
                    console.print("==================================")
                    answ = Prompt.ask("[bold cyan][?] Do You want to Exit ?[/bold cyan]", choices=["y", "n"], default="n")
                    if answ == "y": console.print(f"[bold yellow][!] Thank You for using our tool, please join our telegram channel[/bold yellow]: [bold blue]@{__CHANNEL_USERNAME__}[/bold blue].")
                    else: continue
                else:
                    console.print("[bold red]FAILED.[/bold red]")
                    console.print("[bold yellow][!] Please try again.[/bold yellow]")
                    sleep(2)
                    continue                    
            else: continue
            break
        break