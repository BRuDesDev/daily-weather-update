# ☁ Daily Weather Update ☂
A CLI script that will send a daily text to your phone.  The message contains the temp (high and low) and whether to expect rain.

For this script to work. You will have to install dependencies: <code>pip install -r requirements.txt</code> and open and edit the main.py file. There are some variables at the top of the program that need specific information.
It is very simple to see where the info is to be placed. The info you will need to have is this:

  1. The Lattitude and Longitude of where you live.<br>
  2. The phone number you wish to recieve daily text<br><br>

Sign up for a free twilio.com account. After signing up you can get last 3 things you need:<br>
  3. Twilio Account SID<br>
  4. Twilio Auth Token<br>
  5. Your Twilio Phone number they give you<br><br>

Simply plug in those 5 values into the variables in the file. You can then have this script run on a server, or a task scheduling service such as 
pythonanywhere.com so the script is executed everyday.
