# Overkings Bot

This is a bot designed for the [Overkings](http://overkings.ru) game client. It automates various in-game tasks such as farming locations, managing inventory, selling items, and banking resources. The bot includes a graphical user interface (GUI) for configuration and monitoring.
![image](https://github.com/user-attachments/assets/c35ed6d2-32f5-42d1-a457-dd574556897f)

## Features

- **Automated Farming**: Farms resources across different regions and locations.
- **Inventory Management**: Repairs equipment, uses VIP chests and dark crystals, sells items, and banks resources.
- **Customizable GUI**: Configure farming sequences, skip specific location types (stun, slow, epic), and manage item handling preferences.
- **Hotkey Support**: Start/stop the bot with `Insert` and stop with `Escape`.
- **Statistics Tracking**: Monitors uptime, completed instances, and earnings (daily, monthly, total).
- **Error Handling**: Automatically recovers from game crashes and connection issues.

## Warning!

This bot is created for **educational purposes only**.  
Use it at your own risk. The author is not responsible for:  
- Account bans in the game (if the bot violates Overkings' rules).  
- Any damages or issues caused by this code.  
- Any unintended consequences from using this software.  

By using this software, you agree that you are solely responsible for any risks involved.

## Legal Notice

This project is not affiliated with, authorized, maintained, sponsored, or endorsed by Overkings or any of its affiliates.

## Fair Use

This bot is intended for educational and fair use purposes only. Any use of this software to gain an unfair advantage in the game may violate the game's Terms of Service.

## Prerequisites

- Python 3.x
- Overkings game client installed at `C:\Program Files (x86)\Overkings\Overkings\Overkings.exe`
- Required Python libraries (see `requirements.txt`)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/overkings-bot.git
   cd overkings-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Image Templates**:
   - Ensure the `patterns` directory exists in the project root and contains all necessary `.png` image templates required for image recognition.

4. **Launch the Game**:
   - Start the Overkings game client from `C:\Program Files (x86)\Overkings\Overkings\Overkings.exe`.
   - Log in to your account and ensure the game window is visible and not minimized.

5. **Run the Bot**:
   ```bash
   python bot.py
   ```

Upon running the bot, the GUI will launch, allowing you to configure farming sequences, adjust parameters, and monitor the bot’s activity via the Journal and Statistics tabs.

**Note**: The bot relies on image recognition to interact with the game. Keep the game window visible and unobstructed during operation.

## Usage

### GUI Overview

The bot’s graphical user interface includes the following tabs:

- **Farm Tab**: Set up the sequence of regions to farm and adjust parameters, such as skipping specific location types (stun, slow, epic) or managing inventory actions (e.g., using VIP chests or selling resource chests).
- **Skills Tab**: (Under development) Will enable setting skill priorities for automated combat.
- **Journal Tab**: Shows real-time logs of the bot’s actions and events.
- **Statistics Tab**: Tracks performance metrics like uptime, completed instances, and earnings (daily, monthly, total).

### Controls

- **Start/Stop the Bot**:
  - Press `Insert` to toggle the bot’s operation.
  - Alternatively, click the "СТАРТ (Insert)" button in the GUI.
- **Emergency Stop**:
  - Press `Escape` to immediately halt the bot if it’s running.

### Configuration

- **Location Sequence**:
  - In the Farm Tab, use dropdown menus to select up to 8 regions to farm sequentially.
- **Parameters**:
  - Use checkboxes to enable options like "Minimize after start," "Skip stun locations," or "Sell resource chests."
- **Settings**:
  - Configuration settings are saved in `settings.json` and loaded automatically when the bot starts.

