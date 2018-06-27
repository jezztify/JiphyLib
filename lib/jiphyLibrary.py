import requests
import json
import datetime
import xmltodict

class jiphyLibrary(object):
	def __init__(self, url, user, passwd):
		self.url = url
		self.user = user
		self.passwd = passwd

	## Get Project ID (projectID)
	def get_projectID(self, projectName):
		''' Gets the projectID of a project in JIRA
			params: projectName (string)
			usage: Get_ProjectID("This Project Name")
		'''
		endpoint = "/util/project-list"
		response = requests.Session()
		response.trust_env = False
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for index in range(0,len(results['options'])):
			if results['options'][index]['label'] == projectName:
				projectID = json.dumps(results['options'][index]['value'])
				projectID = projectID.strip('\"')
				break
		print("projectID: %s" %projectID)
		return projectID
		
	## Get Version ID (versionID)
	def get_versionID(self, projectID, versionName):
		''' Gets the versionID of a test cycle in JIRA
			params: cycleName (string)
			usage: Get_VersionID("This Cycle Name")
		'''
		endpoint="/util/versionBoard-list?projectId="+projectID
		response = requests.Session()
		response.trust_env = False
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		versionID = -1
		for releaseStatus in results:
			for version in range (0,len(results[releaseStatus])):
				if results[releaseStatus][version]['value'] == versionID:
					versionID = results[releaseStatus][version]['value']
		return versionID
	
	## Get Test Cycle ID (cycleID)
	def get_test_cycleID(self, projectID, cycleName, versionID):
		''' Gets the test cycleID of a test cycle in JIRA
			params: projectID(int), cycleName(string)
			usage: Get_Test_CycleID(123, "This Test Cycle Name")
		'''
		cycleID = "0"
		endpoint = "/cycle?projectId=" + projectID
		response = requests.Session()
		response.trust_env = False
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
		if cycleID == "0" :
			cycleID = create_test_cycle()
		print("cycleID: %s" %cycleID)
		return cycleID

	## Create A New Test Cycle ID
	def create_test_cycle(self):
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
			"versionId": versionID
		}
		response = requests.Session()
		response.trust_env = False
		response = requests.post(self.url+endpoint, data=json.dumps(payload), headers=headers, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		cycleID = json.dumps(results['id'])
		cycleID = cycleID.strip('\"')
		return cycleID
		
	## Get All Test Case IDs (issueID)
	def get_all_issueID(self, projectCode):
		''' Gets all the issueIDs of a of a project in JIRA
			params: projectCode(string)
			usage: Get_IssueID("PRJCODE")
		'''		
		endpoint = "/zql/executeSearch?zqlQuery=project='"+ projectCode +"'&maxRecords=1000"
		response = requests.Session()
		response.trust_env = False
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		issueIDs = []
		for tc in range(0,len(results['executions'])):
			tcName = json.dumps(results['executions'][tc]['issueSummary'])
			tcName = tcName.strip('\"')
			issueID = json.dumps(results['executions'][tc]['issueId'])
			issueID = issueID.strip('\"')
			thisdict = { "name": tcName, "issueID": issueID}
			issueIDs.append(thisdict)
		print("Total Issue IDs Fetched: %s" %(str(len(issueIDs))))
		return issueIDs
	## Get Issue IDs via Test Case Name(issueID)
	def get_issueID(issueIDs, tcName):
		''' Gets the issueID of an in JIRA
			params: issueIDs(dictionary)
			        tcName(string)
			usage: get_issueID(ListOfIssueIDs, TestCaseName))
		'''	
	    for index in range(0,len(issueIDs)):
		if tcName.lower() == issueIDs[index]['name'].lower():
		    return json.dumps(issueIDs[index]['issueID']).strip('\"')
	    for index in range(0,len(issueIDs)):
		if similar(tcName.lower(), issueIDs[index]['name'].lower()) >= 0.80:
		    return json.dumps(issueIDs[index]['issueID']).strip('\"')        
	    for index in range(0,len(issueIDs)):
		if tcName.lower() in issueIDs[index]['name'].lower():
		    return json.dumps(issueIDs[index]['issueID']).strip('\"')
	    for index in range(0,len(issueIDs)):
		if issueIDs[index]['name'].lower() in tcName.lower():
		    return json.dumps(issueIDs[index]['issueID']).strip('\"')        
	return 0

	## Create New/Get Execution ID (executionID)
	def create_executionID(self, projectID, cycleID, issueID):
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
		response = requests.Session()
		response.trust_env = False
		response = requests.post(self.url+endpoint, data=json.dumps(payload), headers=headers, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for id in results:
			executionID = json.dumps(id)
			executionID = executionID.strip('\"')
			break
		print("executionID: %s" %executionID)
		return executionID
	
	## Get Available Test Execution Status IDs (execstatusID)
	def __get_execution_statusID(self,status):
		''' Gets the execution status ID for a certain status
			params: status(string)
			usage: __Get_Exec_StatusID("PASS")
		'''		
		endpoint = "/util/testExecutionStatus"
		response = requests.Session()
		response.trust_env = False
		response = requests.get(self.url+endpoint, auth=(self.user,self.passwd))
		results = json.loads(response.text)
		for item in range(0,len(results)):
			if results[item]['name'] == status:
				execstatusID = json.dumps(results[item]['id'])
				execstatusID = execstatusID.strip('\"')
				break
		print("execstatusID: %s" %execstatusID)
		return execstatusID

	#Update Test Case Execution Status
	def update_test_case_execution_status(self, executionID,status):
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
		response = requests.Session()
		response.trust_env = False
		response = requests.put(self.url+endpoint, data=json.dumps(payload), headers=headers, auth=(self.user,self.passwd))
		print(response.status_code)
		return response.status_code

	#Parse an output.xml file (xunit format)
	def parse_xml(self, filename):
		''' Parses an xml to be a json object
			params: filename(string)
			usage: parse_xml('output.xml')
		'''
		with open(filename) as f:
			thisjson = xmltodict.parse(f, xml_attribs=True)
			f.close()
		## for logging and checking purposes only
		with open('output.json','w') as f:
			f.write(json.dumps(thisjson, indent=4))
			f.close()
		resultdict = []
		for suite in range(0,len(thisjson['robot']['suite']['suite'][0]['suite'])):
			for test in range(0,len(thisjson['robot']['suite']['suite'][0]['suite'][suite]['test'])):
				tcName = json.dumps(thisjson['robot']['suite']['suite'][0]['suite'][suite]['test'][test]['@name'])
				tcName = tcName.strip('\"').split(None,1)[1]
				status = json.dumps(thisjson['robot']['suite']['suite'][0]['suite'][suite]['test'][test]['status']['@status'])
				status = status.strip('\"')
				thisdict = [{ "name":tcName, "status": status}]
				resultdict.append(thisdict)
		for test in range(0,len(thisjson['robot']['suite']['suite'][1]['test'])):
			tcName = json.dumps(thisjson['robot']['suite']['suite'][1]['test'][test]['@name'])
			tcName = tcName.strip('\"').split(None,1)[1]
			status = json.dumps(thisjson['robot']['suite']['suite'][1]['test'][test]['status']['@status'])
			status = status.strip('\"')
			thisdict = [{ "name":tcName, "status": status}]
			resultdict.append(thisdict)
		return resultdict
