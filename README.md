# RPI-Server-v2
Framework for managing DIY IoT devices or other IoT devices

### First use

- Change values in "*__credentials.json__*"
    
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
    | / | __GET__, __POST__ | To check if server is up | JSON: { name, surname, username, email, password } |  |
    | /signup | __POST__ | To add new user |  |  |
    | /otp_request | __POST__ | To make otp request |  |  |
    | /login | __POST__ | To log in |  |  |
    | /change_password | __POST__ | To change user password |  |  |
    | /reset_password | __GET__ | To reset user password |  |  |
    | /device | __POST__ | To manage IoT devices |  |  |

### Supported devices

- [X] My Iot devices
- [ ] Philips Hue
- [ ] Sonoff BASICR3
- [ ] Sonoff RFR3
- [ ] Sonoff Mini