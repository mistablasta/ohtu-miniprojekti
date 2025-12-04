*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Entries

*** Test Cases ***
User Can Edit An Entry
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Original Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Original Book
    Click Button  Edit
    Wait Until Page Contains  Edit Entry
    Input Text  title  Updated Book
    Click Button  Save
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Updated Book
    Page Should Not Contain  Original Book

User Can Cancel Editing An Entry
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Original Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Original Book
    Click Button  Edit
    Wait Until Page Contains  Edit Entry
    Input Text  title  Changed Book
    Click Button  Cancel
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Original Book
    Page Should Not Contain  Changed Book
