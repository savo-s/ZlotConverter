# Notice to some API features

API has xx parts, separated to directories:

- Database part in 'db' directory, with files that handles database and table features
- Http directory, where is code that comunicate NBP API. Idea was to create it in a way that allows easy to add new endpoints, and also easy to add wrappers to some different APIs, following same logic. Please notice that I couldn't find any weight limits for NBP API, but to demonstrate weights concept, it is defined max of 5 calls to NBP API per minute.
- Routers part for this API
- Services - that manipulate data from NBP api and a service for wallet data in SQLite database
- SQLite database is in data directory
- In a root directory of a project are docker files, environment vaeiables (.env) and main.py. 


# How to access the API

1. To get the code, type:
```
> git clone https://github.com/savo-s/ZlotConverter.git
```

3. After copied, in terminal type:
```
> docker-compose up --build
```

3. To get Swagger doc for an API, open browser, and for URL type:
```
http://localhost:8000/docs
```

4. Select **/register** route, then click 'Try it out' button. Define username and password values and click 'Execute' button

5. Click **/login** route, then click 'Try it out' button. Use previously defined username and password values and click 'Execute' button.

6. From section 'Responses' of /login route, from 'Response body' part, copy value of **access_token**

7. Get back to top of a page, click button '**Authorize**' in right-top corner. In form's text-box paste access_token previosly copied and click green 'Authorize' button, and then click 'Close'.

8. Choose some of /wallet endpoints:
   
**/wallet** - gives you list of all balances per currency and total balance in PNL

**/wallet/add/{currency}/{amount}** - add amount to current balance of selected currency

**/wallet/add/{currency}/{amount}** - substract amount from current balance of selected currency. Please have in mind that you can't take from balance more than you have.

**/wallet/add/{currency}/{amount}** - add amount to current balance of selected currency

DELETE **/wallet/{currency}** - deletes balance for that currency in your wallet (remove currency from your wallet)
