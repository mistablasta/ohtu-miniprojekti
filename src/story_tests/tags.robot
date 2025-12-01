*** Settings ***
Resource         resource.robot
Suite Setup      Setup And Reset
Suite Teardown   Close Browser
Test Setup       Reset Entries

*** Test Cases ***
Adding a single tag works
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Input Text  tags  tag1
    Click Button  Add entry
    Page Should Contain  tag1

Adding two tags works
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Input Text  tags  tag1, tag2
    Click Button  Add entry
    Page Should Contain  tag1
    Page Should Contain  tag2

Editing tags works
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Input Text  tags  tag1, tag2
    Click Button  Add entry
    Page Should Contain  tag1
    Page Should Contain  tag2
    Click Button  Edit
    Input Text  tags  tag1
    Click Button  Save
    Page Should Contain  tag1
    Page Should Not Contain  tag2

Existing tags correct
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Input Text  tags  tag1, tag2
    Click Button  Add entry
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Page Should Contain  tag1
    Page Should Contain  tag2
