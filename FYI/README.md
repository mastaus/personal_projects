## For Your Information (FYI)

**Problem Statement:**  Keeping up with all the birthdays, weddings, anniversaries, mother's and father's days and all the other important events in one's busy life can be challenging. Having forgotten some of these events in the past, I know how it feels :fearful:  
**Goal:**  Create a system that will never let us forget important events and upset our loved ones   
**MVP:**  A program that reminds us (by email) about events recorded in a pre-populated database. Including a webpage to enter new events  

**Approach:**   
1. Create a postgreSQL database
	* #People :family:
	* #Events :gift: :wedding: :mortar_board:
	* #Reminders :envelope:
	* #Solutions (nice to have)
2. Write a python code that would check if any reminders about events are due on the day, and if so, send it out
3. Design the webpage
4. Connect the python code to the webpage
5. Test test test
6. Deploy the product on Heroku-like service (nice to have)


**Plan of action:**
1. Create a function to add a record to **people** database
2. Create a function to add a record to **events** database
	* Make sure to remove white-space from the input
3. Create a function to change a record in **people** db
4. Create a function to change a record in **events** db
	* Make sure to remove white-space from the input
5. Create a function to delete a record in **people** db
6. Create a function to delete a record in **events** db
7. Write a function that will send email reminders
8. Write a function that will send message reminders
9. Create the interface app
10. Create an API for calling the functions
	* Test Test Test
11. Dockerize the code
	* Test Test Test
12. Make the app run every day
13. Host the app on external service (like AWS) to make sure the web-app works on any computer (not just local) (???)
