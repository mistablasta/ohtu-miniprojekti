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
    Wait Until Location Contains  ${SELECT_ENTRY_TYPE_URL}
    Page Should Contain  Select Entry Type
    Click Element  id=book
    Click Button  Next
    Wait Until Location Contains  ${ADD_ENTRY_FORM_URL}
    Page Should Contain  Add Book

Adding valid book entry works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=book
    Click Button  Next
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Book
    Page Should Contain  2000

Adding invalid entry year fails
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=book
    Click Button  Next
    Input Text  title  Book
    Input Text  year  Book
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Page Should Contain  Year must be a number

Adding invalid entry title fails
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=book
    Click Button  Next
    Input Text  title  ${SPACE}
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Page Should Contain  Title is a required field.

Adding and removing valid entry works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=book
    Click Button  Next
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Click Button  Delete
    Handle Alert  action=ACCEPT
    Page Should Contain  No entries found

Adding valid article entry works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=article
    Click Button  Next
    Input Text  title  Article
    Input Text  year  2021
    Input Text  author  Writer
    Input Text  journal  Science Today
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Article
    Page Should Contain  2021

Adding valid misc entry works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=misc
    Click Button  Next
    Input Text  title  Miscellaneous
    Input Text  year  2000
    Input Text  author  Writer
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
    Page Should Contain  Miscellaneous
    Page Should Contain  2000
    Page Should Contain  Writer

Invalid DOI returns error message
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Input Text  doi  https://www.youtube.com/
    Click Button  Next
    Wait Until Page Contains  No BibTeX entry found for DOI https://www.youtube.com/  timeout=15s

Unreachable DOI returns error message
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Input Text  doi  https://thissimulatesnetworkshutdown.fi/notreal
    Click Button  Next
    Wait Until Page Contains  Failed to fetch DOI  timeout=15s

Adding a valid DOI number works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Input Text  doi  10.1126/science.aar3646
    Click Button  Next
    Wait Until Page Contains  Edit Entry  timeout=15s

Adding a valid DOI link works
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Input Text  doi  https://doi.org/10.1126/science.aar3646
    Click Button  Next
    Wait Until Page Contains  Edit Entry  timeout=15s
