# Chronos Discord Bot

Chronos was created to streamline the Discord <> program delivery process. Chronos makes your channel management a breeze through functions like taking attendance, scheduling messages, merging channels, and more. These features can be accessed by sending a text message featuring a **"$" prefix followed by a command** to a Discord text channel. 

## Commands

https://github.com/user-attachments/assets/db1d6054-7c6a-48bb-91e9-c02f2089b5a7

### $attendance

https://github.com/user-attachments/assets/74aeef7d-f88b-40ce-abdc-d1c7f89bf572

### $schedule

https://github.com/user-attachments/assets/486c133e-d150-42ee-b5d4-a267c82900c5

### $reminders

https://github.com/user-attachments/assets/fcfb2ae3-ebc0-4ce2-ade5-0f6669d907d1

### $delete

https://github.com/user-attachments/assets/8eca0e17-4432-4d7f-8cbe-11f414c73aec

### $merge

https://github.com/user-attachments/assets/5e035874-3dc4-4edb-865c-f97aeb34e372

### $zoom

https://github.com/user-attachments/assets/424cddd2-273a-4a32-8480-286ef4d5eb8e

### $background

https://github.com/user-attachments/assets/50e1ab4d-5658-4cd8-bd38-92ac2a955570

### $program

https://github.com/user-attachments/assets/44b5450a-48a0-4f20-b0e8-32efa1576272

### $help, $command, $commands

https://github.com/user-attachments/assets/930ae57d-561a-40b7-bfdb-ffc99a0682da



## Who Can Access Chronos' Commands?
Chronos' commands are split into two categories: **admin & participant**. Users will fall into one of these two categories based on their roles. Please see Chronos documentation for more details

## Run Chronos 
python chronos.py OR python3 chronos.py

## Dependencies
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
