# Chronos Discord Bot

Chronos was created to streamline the program delivery process. Chronos currently features a variety of functions, including taking attendance, scheduling messages, merging channgels, and more. These features can be accessed by sending a text message featuring a **"$" prefix followed by a command** to a Discord text channel

## Who Can Access Chronos' Commands?
Chronos' commands are split into two categories: **admin & participant**. Users will fall into one of these two categories based on their roles. Please see Chronos documentation for more details

## Run Chronos 
python chronos.py OR python3 chronos.py

## Imports
`python3 -m pip install -U discord.py`

`pip3 install python-dotenv`


## Discord Bot Configuration
1. [Initial Discord bot setup](https://www.youtube.com/watch?v=SPTfmiYiuok)
2. Ensure bot has Administrator scope
2. Enable 'Privileged Gateway Intents' In the Discord Developer Portal on your Bot application (follow tutorial above). This makes it so Bot can read messages, see user voice status, etc. Required for proper bot functionality


## Troubleshooting
```bash
Error:
Cannot connect to host discord.com:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')]
```
Solution
 1. Go to MacintoshHD -> Applications -> Python3.x Folder
 2. Double click on the "Install Certificates.command"

```bash
Error:
Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page. If this is not possible, then consider disabling the privileged intents instead.
```

Solution
1. Go to Discord Developer Portal and enable 'Privileged Gateway Intents'


## Documentation
[Chronos User Manual](https://drive.google.com/file/d/15zjj3i4cJWsmNxVTiidDzou63tSeHDqm/view?usp=sharing)
