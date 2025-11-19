*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Entries

*** Test Cases ***
At start there are no entries
    Go To  ${HOME_URL}
    Title Should Be  Bibliography App
    Page Should Contain  No entries found

Adding entry redirects to form
    Go To  ${HOME_URL}
    Click Link  Add entry
    Wait Until Location Contains  ${ADD_ENTRY_URL}
    Page Should Contain  Add entry

Adding valid entry works
    Go To  ${ADD_ENTRY_URl}
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Book
    Page Should Contain  2000

Adding invalid entry year fails
    Go To  ${ADD_ENTRY_URl}
    Input Text  title  Book
    Input Text  year  Book
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Page Should Contain  Year must be a number

Adding invalid entry title fails
    Go To  ${ADD_ENTRY_URl}
    Input Text  title  ${SPACE}
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Page Should Contain  Please input a valid title

Adding and removing valid entry works
    Go To  ${ADD_ENTRY_URl}
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Click Button  Delete
    Page Should Contain  No entries found