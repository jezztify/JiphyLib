**JiphyLib**
=====================
--------------

The main intention of this project is to create a connector between robotframework test results to JIRA. It parses the output.xml that robotframework produces after it executes the tests, takes the test case names and their status, then posts it to Zephyr-for-Jira

--------------
**Installation**
--------------
1. Python 2.7.x
2. Python PIP module
3. Python modules

	cd /path/to/Jiphy
	
	pip install -r requirements

--------------
**How To Use**
--------------
1. Create your own python script (or use the example)
2. Run your test case via robot

    python PostToZ4J.py

NOTE: Make sure that you are running the script in the same directory where output.xml is

--------------
**ToDo**
--------------
1. Multithreaded posting of results for faster processing
