Last updated: 1 May 2022

# Credits
Discord user @Firefly#7113.
Check the [Discord server](https://discord.gg/VZYKBptWFJ)!


# Issues and Future Updates
- Grey out admin commands for non-admins (if supported by pycord)


# Invite
[Invite to your server](https://discord.com/api/oauth2/authorize?client_id=517165856933937153&permissions=275146435600&scope=bot%20applications.commands)


# Dependencies
Built and tested on Ubuntu 20.04 (WSL) with 
- python 3.8.10
- py-cord 2.0.0b5
- aiocron 1.8
- d20 1.1.2

Linted with pylint 2.13.5


# Setting up your server
1. Admin commands will not work for non-admins, but will not be greyed out by default. To grey out commands for non-players and admins, moderators should consider using the Integration settings in your server settings like so:
![ex 1](./images/perms_example1.PNG)
![ex 2](./images/perms_example2.PNG)
![ex 3](./images/perms_example3.PNG)

2. Each player and character in your game will need to be registered with `/profile_admin new`. Players can have multiple registered characters each, but only one active character at a time.

3. It is recommended to give each player their own channel to receive messages generated by `/msg whisper` and `/msg anon`. Do this with `/profile_admin edit channel`.


# Hosting
1. Set up python [virtual environment](https://docs.python.org/3.8/library/venv.html)
2. Start your virtual environment with `source /path/to/venv`.
3. Install dependencies with `pip install -r requirements.txt`.
4. In the top directory, create a file called `TOKEN.txt` and paste your bot's token as a single line.
5. Add any testing servers to `config.py`. Commands can take up to an hour to register to other servers.
6. Run with `python main.py`


## Cloning and Forking
Follow the license and don't be evil. That is all.


# Support the Developer
Github contributions are always welcome! Buy the developer a [coffee](https://ko-fi.com/firefly42), or [commission](https://docs.google.com/document/d/1kM7qFBWqGsHktgrQHdCSf0HYJCfrTAa9MVsGPE8xF6A/edit?usp=sharing) them.

# References
https://docs.pycord.dev/en/master/index.html