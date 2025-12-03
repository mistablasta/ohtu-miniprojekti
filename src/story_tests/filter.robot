*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
Filter a valid entry by title
    Reset Entries
    Go To  ${HOME_URL}
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  Book
    Input Text  year  2000
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  ABook
    Input Text  year  2001
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  CBook
    Input Text  year  2002
    Input Text  author  Author
    Input Text  publisher  Publisher
    Click Button  Add entry
    Go To  ${HOME_URL}
    Select From List By Value  name=filter  title_asc
    Click Button  Search
    Wait Until Page Contains  ABook
    ${t1}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Title:']])[1]
    ${t2}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Title:']])[2]
    ${t3}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Title:']])[3]
    Should Contain  ${t1}  ABook
    Should Contain  ${t2}  Book
    Should Contain  ${t3}  CBook

    Select From List By Value  name=filter  title_desc
    Click Button  Search
    Wait Until Page Contains  CBook
    ${t1}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Title:']])[1]
    ${t2}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Title:']])[2]
    ${t3}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Title:']])[3]
    Should Contain  ${t1}  CBook
    Should Contain  ${t2}  Book
    Should Contain  ${t3}  ABook
    

    Select From List By Value  name=filter  year_asc
    Click Button  Search
    Wait Until Page Contains  2000
    ${y1}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Year:']])[1]
    ${y2}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Year:']])[2]
    ${y3}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Year:']])[3]
    Should Contain  ${y1}  2000
    Should Contain  ${y2}  2001
    Should Contain  ${y3}  2002
    

    Select From List By Value  name=filter  year_desc
    Click Button  Search
    Wait Until Page Contains  2002
    ${y1}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Year:']])[1]
    ${y2}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Year:']])[2]
    ${y3}=  Get Text  xpath=(//div[@class='entry-card']//div[@class='entry-content'][strong[text()='Year:']])[3]
    Should Contain  ${y1}  2002
    Should Contain  ${y2}  2001
    Should Contain  ${y3}  2000