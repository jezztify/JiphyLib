__author__ = "Jessnar Sinues"
__copyright__ = "(c) 2017, Jessnar Sinues"
__license__ = "Creative Commons (Non-Commercial) CC BY-NC 3.0"
__version__ = "0.0.1"
__maintainer__ = "Jessnar Sinues"
__status__ = "alpha"

import requests
import json
import datetime
import xmltodict

class Jiphy(object):
	def __init__(self, url, user, passwd):
		self.url = url
		self.user = user
		self.passwd = passwd

	## Get Project ID (projectID)
	def Get_ProjectID(self, projectName):
		''' Gets the projectID of a project in JIRA
			params: projectName (string)
			usage: Get_ProjectID("This Project Name")
		'''
		endpoint = "/util/project-list"
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for index in range(0,len(results['options'])):
			if results['options'][index]['label'] == projectName:
				projectID = json.dumps(results['options'][index]['value'])
				projectID = projectID.strip('\"')
				break
		print "projectID: " + projectID
		return projectID

	## Get Test Cycle ID (cycleID)
	def Get_Test_CycleID(self, projectID, cycleName):
		''' Gets the test cycleID of a test cycle in JIRA
			params: projectID(int), cycleName(string)
			usage: Get_Test_CycleID(123, "This Test Cycle Name")
		'''
		cycleID = "0"
		endpoint = "/cycle?projectId=" + projectID
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for version in results:
			for index in range(0,len(results[version])):
				for thisID in results[version][index]:
					if thisID != 'recordsCount':
						if results[version][index][thisID]['name'] == cycleName:
							cycleID = json.dumps(thisID)
							cycleID = cycleID.strip('\"')
							break
	## Create A New Test Cycle ID
		if cycleID == "0" :
			endpoint = "/cycle"
			headers = {
					'content-type': "application/json"
			}
			today = datetime.datetime.today().strftime('%d/%b/%y')
			payload = {
				"name": cycleName,
				"build": "",
				"environment": "e2e_paas",
				"description": "Test Automation",
				"startDate": today,
				"endDate": today,
				"projectId": projectID,
				"versionId": "-1"
			}
			response = requests.post(self.url+endpoint, data=json.dumps(payload), headers=headers, auth=(self.user,self.passwd))
			results = json.loads(response.text)
			cycleID = json.dumps(results['id'])
			cycleID = cycleID.strip("\"")
		print "cycleID: " + cycleID
		return cycleID

	## Get Test Case ID (issueID)
	def Get_IssueID(self,tcName, projectCode):
		''' Gets the issueID of an in JIRA
			params: tcName(string), projectCode(string)
			usage: Get_IssueID("This Test Case Name", "PRJCODE")
		'''		
		endpoint = "/zql/executeSearch?zqlQuery=project='"+ projectCode +"'"
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for tc in range(0,len(results['executions'])):
			if results['executions'][tc]['issueSummary'] == tcName:
				issueID = json.dumps(results['executions'][tc]['issueId'])
				issueID = issueID.strip('\"')
				break
		print "issueID: " + issueID
		return issueID

	## Create New/Get Execution ID (executionID)
	def Create_ExecutionID(self, projectID, cycleID, issueID):
		''' Creates a new/Gets the existing executionID of a test case in JIRA
			params: projectID(int), cycleID(int), issueID(int)
			usage: Create_ExecutionID(123, 456, 789)
		'''		
		endpoint = "/execution"
		payload = {
			"projectId": projectID,
			"cycleId":  cycleID,
			"issueId": issueID,
			"assigneeType": "assignee",
			"assignee": self.user
		}
		headers = {
				'content-type': "application/json"
		}
		response = requests.post(self.url+endpoint, data=json.dumps(payload), headers=headers, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for id in results:
			executionID = json.dumps(id)
			executionID = executionID.strip("\"")
			break
		print "executionID: " + executionID
		return executionID
	
	## Get Available Test Execution Status IDs (execstatusID)
	def __Get_Exec_StatusID(self,status):
		''' Gets the execution status ID for a certain status
			params: status(string)
			usage: __Get_Exec_StatusID("PASS")
		'''		
		endpoint = "/util/testExecutionStatus"
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for item in range(0,len(results)):
			if results[item]['name'] == status:
				execstatusID = json.dumps(results[item]['id'])
				execstatusID = execstatusID.strip("\"")
				break
		print "execstatusID: " + execstatusID
		return execstatusID

	def Update_Test_Case_Execution_Status(self, executionID,status):
		''' Updates a test case's execution status in JIRA
			params: executionID(int), status(string)
			usage: Update_Test_Case_Execution_Status(123, "PASS")
		'''		
		## Update Test Case Execution Status
		endpoint = "/execution/" + executionID + "/execute"
		headers = {
				'content-type': "application/json"
		}
		payload = {
			"status": self.__Get_Exec_StatusID(status)
		}
		response = requests.put(self.url+endpoint, data=json.dumps(payload), headers=headers, auth=(self.user,self.passwd))
		print response.status_code
		return response.status_code

