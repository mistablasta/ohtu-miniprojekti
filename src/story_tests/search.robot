*** Settings ***
Resource  resource.robot
Suite Setup      Setup And Reset
Suite Teardown   Close Browser

*** Test Cases ***
Searching a valid entry by title works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=book
    Click Button  Next
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

Searching by tags works
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Input Text  tags  tag1
    Click Button  Add entry
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Input Text  tags  tag2
    Click Button  Add entry
    Input Text  name=query  tag1
    Click Button  Search
    Wait Until Page Contains  tag1
    Page Should Not Contain  tag2