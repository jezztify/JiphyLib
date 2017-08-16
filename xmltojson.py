from Lib import JiphyLib
''' This example parses an output.xml file from robotframework
...	and displays the parsed xml file in json format
'''
## main function
if __name__ == "__main__":
	## variables
	this = JiphyLib.Jiphy("https://www.jira.com", "thisuser", "thispassword")
	print this.user
	print this.passwd
	print this.url
	outputjson = this.parse_xml("TestData/output.xml")
	print outputjson