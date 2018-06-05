# Jiphy Library (JiphyLib)
A library to update your JIRA Tests

--------------
The main intention of this project is to create a connector between robotframework test results to JIRA to improve visibility and help in resolving CI/CD issues. It parses the output.xml that robotframework produces after it executes the tests, takes the test case names and their status, then posts it to JIRA Test. This can also be used for xunit tests xml files.

--------------
**Installation**
--------------
1. Python 2.7.x/3.x.x
2. Python PIP module
3. Python modules

	cd /path/to/Jiphy
	
	pip install -r requirements
--------------
**How To Use**
--------------
1. Create your own python script (or use the example)
2. Run your test case via robot and make sure that it creates an output.xml file
3. python PostToZ4J.py

NOTE: Make sure that you are running the script in the same directory where output.xml is

--------------
**ToDo**
--------------
1. Unit tests
2. Exception handling
3. Multithreaded posting of results for faster processing
