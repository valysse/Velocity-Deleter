import requests
import time
import json
import os
from datetime import datetime

class Colors:
    VIOLET = '\033[38;5;141m'
    PURPLE = '\033[38;5;135m'
    PINK = '\033[38;5;213m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{Colors.VIOLET}{Colors.BOLD}
    ╦  ╦┌─┐┬  ┌─┐┌─┐┬┌┬┐┬ ┬  ╔╦╗┌─┐┬  ┌─┐┌┬┐┌─┐┬─┐
    ╚╗╔╝├┤ │  │ ││  │ │ └┬┘   ║║├┤ │  ├┤  │ ├┤ ├┬┘
     ╚╝ └─┘┴─┘└─┘└─┘┴ ┴  ┴   ╩╩╝└─┘┴─┘└─┘ ┴ └─┘┴└─
{Colors.ENDC}"""
    print(banner)
    print(f"{Colors.PINK}    ⚡ The fastest Discord message deletion tool ⚡{Colors.ENDC}")
    print(f"{Colors.YELLOW}    [!] WARNING: Self-botting violates Discord ToS{Colors.ENDC}")
    print(f"{Colors.VIOLET}    ═══════════════════════════════════════════════{Colors.ENDC}\n")

class DiscordMessageDeleter:
    def __init__(self, token, fast_mode=False):
        self.token = token
        self.fast_mode = fast_mode
        self.delay = 0.35 if fast_mode else 1.2
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = 'https://discord.com/api/v9'
    
    def get_user_info(self):
        """Get information about the authenticated user"""
        r = requests.get(f'{self.base_url}/users/@me', headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"{Colors.RED}[✗] Error getting user info: {r.status_code}{Colors.ENDC}")
            return None
    
    def get_channels(self, guild_id):
        """Get all channels in a guild"""
        r = requests.get(f'{self.base_url}/guilds/{guild_id}/channels', headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return []
    
    def get_guilds(self):
        """Get all guilds the user is in"""
        r = requests.get(f'{self.base_url}/users/@me/guilds', headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return []
    
    def get_dms(self):
        """Get all DM channels"""
        r = requests.get(f'{self.base_url}/users/@me/channels', headers=self.headers)
        if r.status_code == 200:
            return r.json()
        return []
    
    def get_messages_directly(self, channel_id, limit=100):
        """Get messages directly from channel"""
        messages = []
        before = None
        
        print(f"{Colors.VIOLET}[→] Fetching messages...{Colors.ENDC}")
        
        while True:
            params = {'limit': limit}
            if before:
                params['before'] = before
            
            r = requests.get(
                f'{self.base_url}/channels/{channel_id}/messages',
                headers=self.headers,
                params=params
            )
            
            if r.status_code != 200:
                if r.status_code == 429:  # Rate limited
                    retry_after = r.json().get('retry_after', 5)
                    print(f"{Colors.YELLOW}[!] Rate limited. Waiting {retry_after}s...{Colors.ENDC}")
                    time.sleep(retry_after)
                    continue
                print(f"{Colors.RED}[✗] Fetch error: {r.status_code}{Colors.ENDC}")
                break
            
            batch = r.json()
            
            if not batch:
                break
            
            messages.extend(batch)
            before = batch[-1]['id']
            
            print(f"{Colors.PURPLE}[→] Loaded {len(messages)} messages...{Colors.ENDC}", end='\r')
            time.sleep(0.3)
            
            if len(batch) < limit:
                break
        
        print()
        return messages
    
    def delete_message(self, channel_id, message_id):
        """Delete a single message"""
        r = requests.delete(
            f'{self.base_url}/channels/{channel_id}/messages/{message_id}',
            headers=self.headers
        )
        
        if r.status_code == 429:  # Rate limited
            retry_after = r.json().get('retry_after', 5)
            print(f"\n{Colors.YELLOW}[!] Rate limited. Waiting {retry_after}s...{Colors.ENDC}")
            time.sleep(retry_after)
            return self.delete_message(channel_id, message_id)
        
        return r.status_code == 204
    
    def delete_messages_in_channel(self, channel_id, channel_name="Unknown"):
        """Delete all user messages in a channel"""
        user = self.get_user_info()
        if not user:
            return 0, 0
        
        user_id = user['id']
        all_messages = self.get_messages_directly(channel_id)
        user_messages = [msg for msg in all_messages if msg['author']['id'] == user_id]
        
        if not user_messages:
            print(f"{Colors.YELLOW}[!] No messages in {channel_name}{Colors.ENDC}")
            return 0, 0
        
        print(f"{Colors.GREEN}[✓] Found {len(user_messages)} messages in {channel_name}{Colors.ENDC}")
        
        deleted = 0
        failed = 0
        
        for i, msg in enumerate(user_messages, 1):
            msg_id = msg['id']
            content_preview = msg.get('content', '')[:40] if msg.get('content') else '[Attachment/Embed]'
            
            if self.delete_message(channel_id, msg_id):
                deleted += 1
                print(f"{Colors.GREEN}[{i}/{len(user_messages)}] ✓ {content_preview}...{Colors.ENDC}")
            else:
                failed += 1
                print(f"{Colors.RED}[{i}/{len(user_messages)}] ✗ Failed{Colors.ENDC}")
            
            time.sleep(self.delay)
        
        return deleted, failed
    
    def delete_all_in_channel(self, channel_id):
        """Delete all user messages in a specific channel"""
        print(f"\n{Colors.VIOLET}[→] Authenticating...{Colors.ENDC}")
        user = self.get_user_info()
        if not user:
            return False
        
        username = user['username']
        print(f"{Colors.GREEN}[✓] Authenticated as: {Colors.BOLD}{username}{Colors.ENDC}")
        
        deleted, failed = self.delete_messages_in_channel(channel_id, f"Channel {channel_id}")
        
        print(f"\n{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.GREEN}[✓] Completed!{Colors.ENDC}")
        print(f"{Colors.PURPLE}    Deleted: {deleted}{Colors.ENDC}")
        if failed > 0:
            print(f"{Colors.RED}    Failed: {failed}{Colors.ENDC}")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        return self.post_operation_menu()
    
    def delete_all_in_guild(self, guild_id):
        """Delete all user messages in all channels of a guild"""
        print(f"\n{Colors.VIOLET}[→] Authenticating...{Colors.ENDC}")
        user = self.get_user_info()
        if not user:
            return False
        
        username = user['username']
        print(f"{Colors.GREEN}[✓] Authenticated as: {Colors.BOLD}{username}{Colors.ENDC}")
        
        print(f"{Colors.VIOLET}[→] Getting channels...{Colors.ENDC}")
        channels = self.get_channels(guild_id)
        text_channels = [c for c in channels if c['type'] == 0]
        
        print(f"{Colors.GREEN}[✓] Found {len(text_channels)} text channels{Colors.ENDC}\n")
        
        total_deleted = 0
        total_failed = 0
        
        for idx, channel in enumerate(text_channels, 1):
            channel_id = channel['id']
            channel_name = channel.get('name', 'Unknown')
            
            print(f"{Colors.PURPLE}{'─' * 50}{Colors.ENDC}")
            print(f"{Colors.BOLD}[{idx}/{len(text_channels)}] #{channel_name}{Colors.ENDC}")
            print(f"{Colors.PURPLE}{'─' * 50}{Colors.ENDC}")
            
            deleted, failed = self.delete_messages_in_channel(channel_id, f"#{channel_name}")
            total_deleted += deleted
            total_failed += failed
            print()
        
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] ALL COMPLETE!{Colors.ENDC}")
        print(f"{Colors.PURPLE}    Total Deleted: {total_deleted}{Colors.ENDC}")
        if total_failed > 0:
            print(f"{Colors.RED}    Total Failed: {total_failed}{Colors.ENDC}")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        return self.post_operation_menu()
    
    def delete_in_dm(self, dm_channel_id):
        """Delete messages in a specific DM"""
        print(f"\n{Colors.VIOLET}[→] Authenticating...{Colors.ENDC}")
        user = self.get_user_info()
        if not user:
            return False
        
        username = user['username']
        print(f"{Colors.GREEN}[✓] Authenticated as: {Colors.BOLD}{username}{Colors.ENDC}")
        
        deleted, failed = self.delete_messages_in_channel(dm_channel_id, "DM")
        
        print(f"\n{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.GREEN}[✓] Completed!{Colors.ENDC}")
        print(f"{Colors.PURPLE}    Deleted: {deleted}{Colors.ENDC}")
        if failed > 0:
            print(f"{Colors.RED}    Failed: {failed}{Colors.ENDC}")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        return self.post_operation_menu()
    
    def delete_all_dms(self):
        """Delete messages in all DMs"""
        print(f"\n{Colors.VIOLET}[→] Authenticating...{Colors.ENDC}")
        user = self.get_user_info()
        if not user:
            return False
        
        username = user['username']
        print(f"{Colors.GREEN}[✓] Authenticated as: {Colors.BOLD}{username}{Colors.ENDC}")
        
        print(f"{Colors.VIOLET}[→] Getting DM channels...{Colors.ENDC}")
        dms = self.get_dms()
        
        print(f"{Colors.GREEN}[✓] Found {len(dms)} DM channels{Colors.ENDC}\n")
        
        total_deleted = 0
        total_failed = 0
        
        for idx, dm in enumerate(dms, 1):
            dm_id = dm['id']
            recipient_name = "Unknown"
            
            if dm.get('recipients'):
                recipient_name = dm['recipients'][0].get('username', 'Unknown')
            elif dm.get('name'):
                recipient_name = dm['name']
            
            print(f"{Colors.PURPLE}{'─' * 50}{Colors.ENDC}")
            print(f"{Colors.BOLD}[{idx}/{len(dms)}] DM with {recipient_name}{Colors.ENDC}")
            print(f"{Colors.PURPLE}{'─' * 50}{Colors.ENDC}")
            
            deleted, failed = self.delete_messages_in_channel(dm_id, f"DM with {recipient_name}")
            total_deleted += deleted
            total_failed += failed
            print()
        
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] ALL DMS COMPLETE!{Colors.ENDC}")
        print(f"{Colors.PURPLE}    Total Deleted: {total_deleted}{Colors.ENDC}")
        if total_failed > 0:
            print(f"{Colors.RED}    Total Failed: {total_failed}{Colors.ENDC}")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        return self.post_operation_menu()
    
    def delete_everything(self):
        """Delete ALL messages in ALL servers and DMs"""
        print(f"\n{Colors.VIOLET}[→] Authenticating...{Colors.ENDC}")
        user = self.get_user_info()
        if not user:
            return False
        
        username = user['username']
        print(f"{Colors.GREEN}[✓] Authenticated as: {Colors.BOLD}{username}{Colors.ENDC}")
        
        total_deleted = 0
        total_failed = 0
        
        # Delete in all guilds
        print(f"\n{Colors.PINK}{Colors.BOLD}[→] Processing ALL Servers...{Colors.ENDC}")
        guilds = self.get_guilds()
        print(f"{Colors.GREEN}[✓] Found {len(guilds)} servers{Colors.ENDC}\n")
        
        for guild_idx, guild in enumerate(guilds, 1):
            guild_id = guild['id']
            guild_name = guild.get('name', 'Unknown')
            
            print(f"\n{Colors.PINK}{'═' * 50}{Colors.ENDC}")
            print(f"{Colors.PINK}{Colors.BOLD}SERVER [{guild_idx}/{len(guilds)}]: {guild_name}{Colors.ENDC}")
            print(f"{Colors.PINK}{'═' * 50}{Colors.ENDC}\n")
            
            channels = self.get_channels(guild_id)
            text_channels = [c for c in channels if c['type'] == 0]
            
            for ch_idx, channel in enumerate(text_channels, 1):
                channel_id = channel['id']
                channel_name = channel.get('name', 'Unknown')
                
                print(f"{Colors.PURPLE}[{ch_idx}/{len(text_channels)}] #{channel_name}{Colors.ENDC}")
                deleted, failed = self.delete_messages_in_channel(channel_id, f"#{channel_name}")
                total_deleted += deleted
                total_failed += failed
        
        # Delete in all DMs
        print(f"\n{Colors.PINK}{Colors.BOLD}[→] Processing ALL DMs...{Colors.ENDC}")
        dms = self.get_dms()
        print(f"{Colors.GREEN}[✓] Found {len(dms)} DM channels{Colors.ENDC}\n")
        
        for dm_idx, dm in enumerate(dms, 1):
            dm_id = dm['id']
            recipient_name = "Unknown"
            
            if dm.get('recipients'):
                recipient_name = dm['recipients'][0].get('username', 'Unknown')
            elif dm.get('name'):
                recipient_name = dm['name']
            
            print(f"{Colors.PURPLE}[{dm_idx}/{len(dms)}] DM: {recipient_name}{Colors.ENDC}")
            deleted, failed = self.delete_messages_in_channel(dm_id, f"DM with {recipient_name}")
            total_deleted += deleted
            total_failed += failed
        
        print(f"\n{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] EVERYTHING COMPLETE!{Colors.ENDC}")
        print(f"{Colors.PURPLE}    Total Deleted: {total_deleted}{Colors.ENDC}")
        if total_failed > 0:
            print(f"{Colors.RED}    Total Failed: {total_failed}{Colors.ENDC}")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        return self.post_operation_menu()
    
    def post_operation_menu(self):
        """Show menu after operation completes"""
        print(f"\n{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.BOLD}What would you like to do?{Colors.ENDC}")
        print(f"{Colors.GREEN}  [M]{Colors.ENDC} Return to Main Menu")
        print(f"{Colors.RED}  [Q]{Colors.ENDC} Quit")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        
        while True:
            choice = input(f"\n{Colors.BOLD}Press M or Q: {Colors.ENDC}").strip().upper()
            
            if choice == 'M':
                return True
            elif choice == 'Q':
                return False
            else:
                print(f"{Colors.RED}[✗] Invalid option. Press M or Q{Colors.ENDC}")


def main():
    try:
        clear_screen()
        print_banner()
        
        token = input(f"{Colors.BOLD}Enter your Discord token: {Colors.ENDC}").strip()
        
        if not token:
            print(f"{Colors.RED}[✗] Token cannot be empty{Colors.ENDC}")
            input(f"\n{Colors.DIM}Press Enter to exit...{Colors.ENDC}")
            return
        
        # Ask for speed mode
        print(f"\n{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        print(f"{Colors.BOLD}Speed Mode:{Colors.ENDC}")
        print(f"{Colors.GREEN}  [1]{Colors.ENDC} Safe Mode (1.2s delay) - {Colors.DIM}Recommended{Colors.ENDC}")
        print(f"{Colors.YELLOW}  [2]{Colors.ENDC} Fast Mode (0.35s delay) - {Colors.DIM}Higher ban risk{Colors.ENDC}")
        print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
        
        speed_choice = input(f"\n{Colors.BOLD}Select mode (1-2): {Colors.ENDC}").strip()
        fast_mode = speed_choice == '2'
        
        if fast_mode:
            print(f"{Colors.YELLOW}[!] Fast mode enabled. Use at your own risk!{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}[✓] Safe mode enabled{Colors.ENDC}")
        
        time.sleep(1)
        deleter = DiscordMessageDeleter(token, fast_mode)
        
        while True:
            clear_screen()
            print_banner()
            
            print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
            print(f"{Colors.BOLD}Options:{Colors.ENDC}")
            print(f"{Colors.PURPLE}  [1]{Colors.ENDC} Delete messages in a specific channel")
            print(f"{Colors.PURPLE}  [2]{Colors.ENDC} Delete messages in all channels of a server")
            print(f"{Colors.PURPLE}  [3]{Colors.ENDC} Delete messages in a specific DM")
            print(f"{Colors.PURPLE}  [4]{Colors.ENDC} Delete messages in ALL DMs")
            print(f"{Colors.PINK}  [5]{Colors.ENDC} Delete ALL messages EVERYWHERE {Colors.DIM}(Nuclear option){Colors.ENDC}")
            print(f"{Colors.RED}  [6]{Colors.ENDC} Exit")
            print(f"{Colors.VIOLET}{'═' * 50}{Colors.ENDC}")
            
            choice = input(f"\n{Colors.BOLD}Select option (1-6): {Colors.ENDC}").strip()
            
            continue_running = True
            
            if choice == '1':
                channel_id = input(f"{Colors.BOLD}Enter channel ID: {Colors.ENDC}").strip()
                confirm = input(f"{Colors.YELLOW}Delete all YOUR messages in this channel? (yes/no): {Colors.ENDC}").strip()
                if confirm.lower() == 'yes':
                    continue_running = deleter.delete_all_in_channel(channel_id)
                else:
                    print(f"{Colors.YELLOW}[!] Cancelled{Colors.ENDC}")
                    time.sleep(1)
            
            elif choice == '2':
                guild_id = input(f"{Colors.BOLD}Enter server/guild ID: {Colors.ENDC}").strip()
                confirm = input(f"{Colors.YELLOW}Delete all YOUR messages in ALL channels? (yes/no): {Colors.ENDC}").strip()
                if confirm.lower() == 'yes':
                    continue_running = deleter.delete_all_in_guild(guild_id)
                else:
                    print(f"{Colors.YELLOW}[!] Cancelled{Colors.ENDC}")
                    time.sleep(1)
            
            elif choice == '3':
                dm_id = input(f"{Colors.BOLD}Enter DM channel ID: {Colors.ENDC}").strip()
                confirm = input(f"{Colors.YELLOW}Delete all YOUR messages in this DM? (yes/no): {Colors.ENDC}").strip()
                if confirm.lower() == 'yes':
                    continue_running = deleter.delete_in_dm(dm_id)
                else:
                    print(f"{Colors.YELLOW}[!] Cancelled{Colors.ENDC}")
                    time.sleep(1)
            
            elif choice == '4':
                confirm = input(f"{Colors.RED}Delete all YOUR messages in ALL DMs? (yes/no): {Colors.ENDC}").strip()
                if confirm.lower() == 'yes':
                    continue_running = deleter.delete_all_dms()
                else:
                    print(f"{Colors.YELLOW}[!] Cancelled{Colors.ENDC}")
                    time.sleep(1)
            
            elif choice == '5':
                print(f"\n{Colors.RED}{Colors.BOLD}[!!!] NUCLEAR OPTION [!!!]{Colors.ENDC}")
                print(f"{Colors.RED}This will delete ALL your messages in EVERY server and DM!{Colors.ENDC}")
                confirm = input(f"{Colors.RED}Type 'DELETE EVERYTHING' to confirm: {Colors.ENDC}").strip()
                if confirm == 'DELETE EVERYTHING':
                    continue_running = deleter.delete_everything()
                else:
                    print(f"{Colors.YELLOW}[!] Cancelled{Colors.ENDC}")
                    time.sleep(1)
            
            elif choice == '6':
                clear_screen()
                print(f"\n{Colors.VIOLET}[→] Thanks for using Velocity Deleter!{Colors.ENDC}\n")
                break
            
            else:
                print(f"{Colors.RED}[✗] Invalid option{Colors.ENDC}")
                time.sleep(1)
            
            if not continue_running:
                clear_screen()
                print(f"\n{Colors.VIOLET}[→] Thanks for using Velocity Deleter!{Colors.ENDC}\n")
                break
    
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.YELLOW}[!] Operation cancelled by user{Colors.ENDC}")
        print(f"{Colors.VIOLET}[→] Thanks for using Velocity Deleter!{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Error: {str(e)}{Colors.ENDC}")
        input(f"\n{Colors.DIM}Press Enter to exit...{Colors.ENDC}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Fatal Error: {str(e)}{Colors.ENDC}")
        input(f"\n{Colors.DIM}Press Enter to exit...{Colors.ENDC}")