*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Entries

*** Test Cases ***
Export Without Selection Shows Error
    Go To  ${HOME_URL}
    Click Element  id=batch-bibtex
    Wait Until Element Contains  id=error  Make a selection first!

Export Selected Entries As BibTeX
    Create Book Entry  Selected One  2024  First Author  First Publisher
    Create Book Entry  Selected Two  2023  Second Author  Second Publisher
    Create Book Entry  Not Selected  2022  Third Author  Third Publisher

    Go To  ${HOME_URL}
    Page Should Contain  Selected One
    Page Should Contain  Selected Two
    Page Should Contain  Not Selected

    Execute Javascript  window.__downloadedContent = null; (function(){const orig = HTMLAnchorElement.prototype.click; HTMLAnchorElement.prototype.click = function(...args){const href = this.getAttribute('href'); if (href && href.startsWith('data:text/plain,')) { const encoded = href.slice('data:text/plain,'.length); window.__downloadedContent = decodeURIComponent(encoded); } return orig.apply(this, args);};})();

    Click Element  xpath=//div[@class='entry-card'][.//div[@class='entry-content'][strong[text()='Title:'] and contains(., 'Selected One')]]//input[@class='entry-checkbox']
    Click Element  xpath=//div[@class='entry-card'][.//div[@class='entry-content'][strong[text()='Title:'] and contains(., 'Selected Two')]]//input[@class='entry-checkbox']

    Click Element  id=batch-bibtex

    Wait For Condition  return window.__downloadedContent !== null;  timeout=5s
    ${bibtex}=  Execute Javascript  return window.__downloadedContent;

    Should Not Be Empty  ${bibtex}
    Should Contain  ${bibtex}  @book{first2024selected
    Should Contain  ${bibtex}  title     = "Selected One"
    Should Contain  ${bibtex}  author    = "First Author"
    Should Contain  ${bibtex}  year      = "2024"
    Should Contain  ${bibtex}  publisher = "First Publisher"
    Should Contain  ${bibtex}  @book{second2023selected
    Should Contain  ${bibtex}  title     = "Selected Two"
    Should Not Contain  ${bibtex}  @book{third2022not
