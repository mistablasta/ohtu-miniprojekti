*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
Searching a valid entry by title works
    Reset Entries
    Go To  ${ADD_ENTRY_URL}
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Go To  ${HOME_URL}
    Input Text  name=query  Book
    Click Button  Search
    Wait Until Page Contains  Book
    Wait Until Page Contains  Author

Searching a valid entry by year works
    Go To  ${HOME_URL}
    Input Text  name=query  2000
    Click Button  Search
    Wait Until Page Contains  2000
    Wait Until Page Contains  Author

Searching a valid entry by author works
    Go To  ${HOME_URL}
    Input Text  name=query  Author
    Click Button  Search
    Wait Until Page Contains  Author
    Wait Until Page Contains  2000

Searching a valid entry by publisher works
    Go To  ${HOME_URL}
    Input Text  name=query  Publisher
    Click Button  Search
    Wait Until Page Contains  Publisher
    Wait Until Page Contains  2000

Searching a valid entry partially works
    Go To  ${HOME_URL}
    Input Text  name=query  Auth
    Click Button  Search
    Wait Until Page Contains  Book
    Wait Until Page Contains  Author

Searching a valid entry without proper capitalization works
    Go To  ${HOME_URL}
    Input Text  name=query  auth
    Click Button  Search
    Wait Until Page Contains  Book
    Wait Until Page Contains  Author

Searching an invalid entry works
    Go To  ${HOME_URL}
    Input Text  name=query  INVALID
    Click Button  Search
    Page Should Contain  No entries found

Deleting a searched entry works
    Go To  ${HOME_URL}
    Input Text  name=query  2000
    Click Button  Search
    Wait Until Page Contains  2000
    Wait Until Page Contains  Author
    Click Button  Delete
    Handle Alert  action=ACCEPT
    Page Should Contain  No entries found
    Reset Entries