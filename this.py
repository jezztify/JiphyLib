from JiphyLib import Jiphy

if __name__ == "__main__":
    this = Jiphy("https://jira.int.net.nokia.com/rest/zapi/latest","reg001","RegTest@001")
    print this.user
    print this.passwd
    print this.url
    projectID = this.Get_ProjectID("NPO Engine Testing")
    cycleID = this.Get_Test_CycleID(projectID, "JESS_ZAPI_PYTHONLIB_TEST")
    issueID = this.Get_IssueID("Add Operators to the Project", "NPOETT")
    executionID = this.Create_ExecutionID(projectID, cycleID, issueID)
    this.Update_Test_Case_Execution_Status(executionID, "PASS")