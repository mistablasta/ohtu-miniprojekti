*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}         localhost:5001
${DELAY}          0.5 seconds
${HOME_URL}       http://${SERVER}
${SELECT_ENTRY_TYPE_URL}  http://${SERVER}/new_entry
${ADD_ENTRY_FORM_URL}  http://${SERVER}/add_entry_form
${RESET_URL}      http://${SERVER}/reset_db
${BROWSER}        firefox
${HEADLESS}       false

*** Keywords ***
Setup And Reset
    Open And Configure Browser
    Reset Entries

Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset Entries
    Go To  ${RESET_URL}

Create Book Entry
    [Arguments]  ${title}  ${year}  ${author}  ${publisher}
    Go To  ${SELECT_ENTRY_TYPE_URL}
    Click Element  id=book
    Click Button  Next
    Input Text  title  ${title}
    Input Text  year  ${year}
    Input Text  author  ${author}
    Input Text  publisher  ${publisher}
    Click Button  Add entry
    Wait Until Location Contains  ${HOME_URL}
