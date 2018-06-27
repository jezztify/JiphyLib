*** Settings ***
Library    ../lib/jiphyLibrary.py     https://this.jira.url/rest/zapi/latest    TEST USER    TEST PASSWORD
Library    Collections

*** Variables ***
${projectID}
${cycleID}

*** Test Cases ***
Push Results To JIRA
    ${projectID} =    get projectID    TEST PROJECT NAME
    ${cycleName} =    TEST CYCLE NAME
    ${versionID} =    123456789
    ${cycleID} =    get test cycleID    ${projectID}    ${cycleName}   ${versionID}
    ${projectCode} =    TEST PROJECT CODE
    @{issueIDs} =    get all issueID    ${projectCode}
    &{parseOutput} =    parse xml    /full/path/to/output.xml
    ${outputLength} =    Get Length    &{parseOutput}
    :FOR   ${result}    IN RANGE    0   ${outputLength} 
    \    Push Results    &{parseOutput}[${result}]    @{issueIDs}    ${projectID}    ${cycleID}

*** Keywords ***
Push Results
    [Arguments]    &{result}   @{issueIDs}    ${projectID}    ${cycleID}
    ${resultLength} =    Get Length    &{result}
    :FOR    ${testName}    IN RANGE    0    ${resultLength}
    \    ${tcName} =    &{result}[${testname}]['name']
    \    ${status} =    &{result}[${testname}]['status']
    \    ${issueID} =    Get IssueID    @{issueIDs}    ${tcName}
    \    ${executionID} =    create executionID    ${projectID}    ${cycleID}    ${issueID}
    \    update test case execution status    ${executionID}    ${status}
