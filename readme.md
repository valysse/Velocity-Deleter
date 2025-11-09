# ⚡ Velocity Deleter

<div align="center">

![Velocity Deleter](https://img.shields.io/badge/Velocity-Deleter-9b59b6?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**The fastest Discord message deletion tool for Windows**

*Delete your Discord messages at lightning speed* ⚡

</div>

---

## 🌟 Features

- 🎯 **Specific Channel Deletion** - Delete all your messages in a single channel
- 🏢 **Server-Wide Deletion** - Delete all your messages across all channels in a server
- 💬 **DM Support** - Delete messages in specific DMs or ALL DMs at once
- 🚀 **Nuclear Option** - Delete EVERYTHING - all messages in all servers and DMs
- ⚡ **Speed Modes** - Choose between Safe Mode (1.2s delay) or Fast Mode (0.35s delay)
- 🎨 **Beautiful Interface** - Violet-themed terminal with real-time progress tracking
- 🔒 **Rate Limit Protection** - Automatic handling of Discord API rate limits

## 📋 Requirements

- Python 3.7 or higher
- Windows OS
- Discord user account token

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/velocity-deleter.git
cd velocity-deleter
```

2. **Install dependencies**
```bash
pip install requests
```

3. **Run Velocity Deleter**
```bash
python velocity_deleter.py
```

## 🔑 Getting Your Discord Token

1. Open Discord in your web browser (Chrome/Firefox recommended)
2. Press `F12` to open Developer Tools
3. Go to the **Network** tab
4. Send any message in any channel
5. Look for requests to `discord.com/api`
6. In the request headers, find `authorization` - that's your token!

## 📖 How to Use

### Getting Channel/Server IDs

1. Enable Developer Mode in Discord:
   - Settings → Advanced → Developer Mode
2. Right-click on any channel/server → Copy ID

### Speed Modes

- **Safe Mode (Recommended)**: 1.2 second delay between deletions
  - Lower ban risk
  - Safer for large deletion operations
  
- **Fast Mode**: 0.35 second delay between deletions
  - ⚠️ Higher ban risk
  - Use for smaller operations or at your own risk

### Available Options

1. **Delete messages in a specific channel**
   - Deletes all YOUR messages in one channel
   
2. **Delete messages in all channels of a server**
   - Deletes all YOUR messages across an entire server
   
3. **Delete messages in a specific DM**
   - Deletes all YOUR messages in a single DM conversation
   
4. **Delete messages in ALL DMs**
   - Deletes all YOUR messages in every DM conversation
   
5. **Delete ALL messages EVERYWHERE** 🔥
   - Nuclear option: Deletes EVERYTHING across all servers and DMs
   - Requires typing `DELETE EVERYTHING` to confirm

## ⚠️ Important Warnings

### Terms of Service Violation
**Using this tool violates Discord's Terms of Service (self-botting).** Your account could be banned or suspended. Use at your own risk.

### What This Tool Does
- ✅ Deletes only YOUR messages
- ✅ Cannot delete other people's messages
- ✅ Works on user accounts only (not bots)
- ❌ Cannot bulk delete (Discord limitation)
- ❌ Deleted messages cannot be recovered

### Rate Limiting
- Discord has strict rate limits on message deletion
- The tool includes automatic rate limit handling
- Fast Mode increases ban risk but speeds up deletion
- Safe Mode is recommended for large operations

## 🛡️ Safety Tips

1. **Start Small**: Test with a channel that has few messages
2. **Use Safe Mode**: Especially for large deletion operations
3. **Take Breaks**: Don't run the tool continuously for hours
4. **Backup Important Messages**: Screenshot or save important conversations
5. **Be Patient**: Large operations can take time

## 🎨 Screenshots

```
    ╦  ╦┌─┐┬  ┌─┐┌─┐┬┌┬┐┬ ┬  ╔╦╗┌─┐┬  ┌─┐┌┬┐┌─┐┬─┐
    ╚╗╔╝├┤ │  │ ││  │ │ └┬┘   ║║├┤ │  ├┤  │ ├┤ ├┬┘
     ╚╝ └─┘┴─┘└─┘└─┘┴ ┴  ┴   ╩╩╝└─┘┴─┘└─┘ ┴ └─┘┴└─

    ⚡ The fastest Discord message deletion tool ⚡
    [!] WARNING: Self-botting violates Discord ToS
    ═══════════════════════════════════════════════
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

This tool is provided for educational purposes only. The developers are not responsible for any consequences resulting from the use of this tool, including but not limited to account suspension or termination. By using Velocity Deleter, you acknowledge that:

- You understand this violates Discord's Terms of Service
- You accept full responsibility for any consequences
- The developers assume no liability for your actions
- You will not hold the developers responsible for any account actions taken by Discord

## 🙏 Acknowledgments

- Built with Python and the Discord API
- Inspired by the need for efficient message management
- Thanks to the open-source community

---

<div align="center">

**Made with 💜 by the Velocity Team**

⚡ *Speed meets Power* ⚡

[Report Bug](https://github.com/yourusername/velocity-deleter/issues) · [Request Feature](https://github.com/yourusername/velocity-deleter/issues)

</div>