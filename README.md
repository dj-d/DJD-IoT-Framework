# RPI-Server-v2
Framework for managing DIY IoT devices or other IoT devices

### Startup

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
  
- If it is your first use of this framework run "*__start.sh__*" script
- If you just want to update the server run "*__build_and_run_dockerfile.sh__*"

### Supported devices

- [X] My Iot devices
- [ ] Philips Hue
- [ ] Sonoff BASICR3
- [ ] Sonoff RFR3
- [ ] Sonoff Mini