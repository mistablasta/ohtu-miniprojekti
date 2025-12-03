*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Keywords ***
Create Book Entry With Tag
    [Arguments]  ${title}  ${year}  ${author}  ${publisher}  ${tag}
    Go To  ${ADD_ENTRY_FORM_URL}?type=book
    Input Text  title  ${title}
    Input Text  year  ${year}
    Input Text  author  ${author}
    Input Text  publisher  ${publisher}
    Input Text  tags  ${tag}
    Click Button  Add entry

*** Test Cases ***
Filter by Year Range
    Reset Entries
    Create Book Entry With Tag  Old Book  1990  Author1  Pub1  history
    Create Book Entry With Tag  Mid Book  2000  Author2  Pub2  science
    Create Book Entry With Tag  New Book  2020  Author3  Pub3  fiction
    
    Go To  ${HOME_URL}
    
    Click Button  Show Filters
    
    Input Text  name=year_min  1995
    Input Text  name=year_max  2005
    
    Click Button  Search with Filters
    
    Page Should Contain  Mid Book
    Page Should Not Contain  Old Book
    Page Should Not Contain  New Book

Filter by Tags
    Reset Entries
    Create Book Entry With Tag  SciFi Book  2021  AuthorA  PubA  scifi
    Create Book Entry With Tag  Romance Book  2021  AuthorB  PubB  romance
    Create Book Entry With Tag  Another SciFi  2021  AuthorC  PubC  scifi
    
    Go To  ${HOME_URL}
    
    Click Button  Show Filters
    
    Select Checkbox  xpath=//input[@value='scifi']
    Click Button  Search with Filters
    
    Page Should Contain  SciFi Book
    Page Should Contain  Another SciFi
    Page Should Not Contain  Romance Book

Sort by Title Ascending
    Reset Entries
    Create Book Entry With Tag  C Book  2000  Author  Pub  tag
    Create Book Entry With Tag  A Book  2000  Author  Pub  tag
    Create Book Entry With Tag  B Book  2000  Author  Pub  tag
    
    Go To  ${HOME_URL}
    Click Button  Show Filters
    
    Select From List By Value  name=sort  title_asc
    Click Button  Search with Filters
    
    ${t1}=  Get Text  xpath=(//div[@class='entry-card']//p[strong[text()='Title:']])[1]
    ${t2}=  Get Text  xpath=(//div[@class='entry-card']//p[strong[text()='Title:']])[2]
    ${t3}=  Get Text  xpath=(//div[@class='entry-card']//p[strong[text()='Title:']])[3]
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
    
    Should Contain  ${t1}  A Book
    Should Contain  ${t2}  B Book
    Should Contain  ${t3}  C Book

Sort by Year Descending
    Reset Entries
    Create Book Entry With Tag  Old  1900  Author  Pub  tag
    Create Book Entry With Tag  New  2020  Author  Pub  tag
    Create Book Entry With Tag  Mid  1950  Author  Pub  tag
    
    Go To  ${HOME_URL}
    Click Button  Show Filters
    
    Select From List By Value  name=sort  year_desc
    Click Button  Search with Filters
    
    ${y1}=  Get Text  xpath=(//div[@class='entry-card']//p[strong[text()='Year:']])[1]
    ${y2}=  Get Text  xpath=(//div[@class='entry-card']//p[strong[text()='Year:']])[2]
    ${y3}=  Get Text  xpath=(//div[@class='entry-card']//p[strong[text()='Year:']])[3]
    
    Should Contain  ${y1}  2020
    Should Contain  ${y2}  1950
    Should Contain  ${y3}  1900
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
