![SonarQube](https://github.com/dj-d/DJD-IoT-Framework/workflows/SonarQube/badge.svg)

# RPI-Server-v2
Framework for managing IoT devices

### First use

- Insert data in "*__credentials.json__*"
    
    ```json
    {
      "server": {
        "domain": "YOUR_DDNS",
        "port": 5000
      },
      "db": {
        "host": "YOUR_DB_HOST",
        "db_name": "YOUR_DB_NAME",
        "root_password": "YOUR_DB_ROOT_PASSWORD",
        "user": "YOUR_DB_USER",
        "user_password": "YOUR_DB_USER_PASSWORD",
        "port": 3307
      },
      "phpmyadmin": {
        "port": 9081
      },
      "email": {
        "address": "YOUR_EMAIL_ADDRESS",
        "password": "YOUR_EMAIL_PASSWORD!",
        "host": "smtp.gmail.com",
        "port": 465
      }
    }
    ```
  
  **You can change ports without problems there are no constraints*
  
- Now run "*__start.sh__*" script

**This script delete old containers, install dependencies, create .env file and build and run the docker-compose*

### Update Server
- To update the server run "*__build_and_run_dockerfile.sh__*" script that stop and remove old container, delete old image and build and run the new image

**The DataBase and PhpMyAdmin will not be changed*

### Using

- API

    | Endpoint | Method | Description | Request body | Response body | 
    | --- | --- | --- | --- | --- |
    | / | __GET__, __POST__ | To check if server is up |  |  |
    | /signup | __POST__ | To add new user | JSON: { name: str, surname: str, username: str, email: str, password: str } | JSON: { valid: bool, info: { api_key: str } } |
    | /otp_request | __POST__ | To make otp request |  |  |
    | /login | __POST__ | To log in |  |  |
    | /change_password | __POST__ | To change user password |  |  |
    | /reset_password | __GET__ | To reset user password |  |  |
    | /device | __POST__ | To manage IoT devices |  |  |

- Device action

    | Action | Description | Request body | Response body |
    | --- | --- | --- | --- |
    | create | To add new device |  |  |
    | delete | To delete a device |  |  |
    | change_ps_name | To change name of a power strip (if exist) |  |  |
    | change_switch_name | To change name of a switch of a power strip (if exist) |  |  |
    | send | To send the action that the device will have to perform |  |  |
    | get | To get the status of component of device |  |  |

### Supported devices

- [X] DIY NodeMCU
    - [X] [SmartPowerStrip](https://github.com/dj-d/NodeMCU-SmartPowerStrip-v2)
    - [X] [RemoteController](https://github.com/dj-d/NodeMCU-RemoteController-v2)
    - [X] [LedStripController](https://github.com/dj-d/NodeMCU-LedStripController-v2)
- [ ] Philips Hue
- [ ] Sonoff BASICR3
- [ ] Sonoff RFR3
- [ ] Sonoff Mini
