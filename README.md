### Purpose
This app autoupdates bitrix CRM currencies exchange rates (https://yourportal.bitrix24.ru/crm/configs/currency/) according to your base currency. Exchange rates is taken from cbr.ru (https://www.cbr.ru/scripts/XML_daily.asp).
### Usage
1. Add new bitrix app (api only) to your portal, specify handler path as `http://127.0.0.1:3000/`
2. Add `.env` file to the app directory with the following:
```
CLIENT_ID=###
CLIENT_SECRET=###
PORTAL_URL=https://###.bitrix24.ru/
OAUTH_URL=https://oauth.bitrix.info/oauth/token/
```
3. Build and run docker container
```
$ docker build -t bitrixcurrencies .
$ docker run -p 3000:3000 bitrixcurrencies
```
4. If you're using app for the first time, navigate to http://localhost:3000 and authorize through your bitrix portal