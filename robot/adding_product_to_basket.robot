*** Settings ***
Documentation  HepsiBuradaTest
Library  Selenium2Library
Library  DebugLibrary
Library  Collections
Library  String
Library  OperatingSystem
Library  String

Test Setup      Begin Web Test
Test Teardown   End Web Test

*** Variables ***
${BROWSER}                  chrome

${BASE_URL}                 https://www.hepsiburada.com
${USER_EMAIL}               test.hepsiburada@yopmail.com
${USER_PASSWORD}            Burada
${USER_NAME}                Hepsi Burada
# Login Page
${LOC_EMAIL}                id=email
${LOC_PASSWORD}             id=password
${LOC_LOGIN_BUTTON}         css=.btn-login-submit
# Header: MyAccount
${LOC_MYACCOUNT}            css=#myAccount.icon-view-account
${LOC_LOGIN_USERNAME}       id=login
${LOC_LOGOUT}               css=.logout
${LOC_USERNAME}             css=.usersProsess .login.user-name
# Header: Basket
${LOC_BASKET_BUTTON}        css=.icon-view-basket
# Header: Product Search
${LOC_SEARCH}               id=productSearch
${LOC_SEARCH_BUTTON}        id=buttonProductSearch
# Search Results Page
${LOC_PRODUCT_LIST}         css=.box.product
# Product Details Page
${LOC_OTHER_SELLERS_ADD_BASKET}     css=.add-to-basket.button.small
# Basket Page
${LOC_BASKET_CONTAINER}     css=.box.umbrella
${LOC_PRODUCT_NAME}         css=.box.umbrella .product-name .hbus
${LOC_SELLERS}              css=.box.umbrella .merchant .hbus
${LOC_DELETE_BUTTON}        css=.btn-delete.hbus


*** Keywords ***
Begin Web Test
    Open Browser    about:blank     ${BROWSER}
    maximize browser window

End Web Test
    Close Browser

Open Home Page
    go to           ${BASE_URL}
    Sleep       3

Navigate To Login Page
    Mouse Up        ${LOC_MYACCOUNT}
    Sleep   1
    Click Element   ${LOC_LOGIN_USERNAME}
    Sleep   2

Login With Crendentials
    [Arguments]     ${usr_mail}=${USER_EMAIL}   ${usr_pass}=${USER_PASSWORD}
    Input Text      ${LOC_EMAIL}        ${usr_mail}
    Sleep   1
    Input Password  ${LOC_PASSWORD}     ${usr_pass}
    Click Element   ${LOC_LOGIN_BUTTON}
    Sleep   3

Validate that Login is successful
    Wait Until Element Is Visible       ${LOC_USERNAME}
    ${elm}    Get WebElement            ${LOC_USERNAME}
    ${att}    Get Element Attribute     ${elm}   text
    Should Be Equal     ${att}          ${USER_NAME}
    log to console  ${att}

Search A Product
    [Arguments]     ${term}
    Input Text      ${LOC_SEARCH}    ${term}
    Click Element   ${LOC_SEARCH_BUTTON}

Click first Product in Search Results
    ${elms}         Get WebElements     ${LOC_PRODUCT_LIST}
    Click Element   ${elms[0]}
    Sleep   2

Add Product to Basket from two different Sellers
    Wait Until Element Is Visible       ${LOC_OTHER_SELLERS_ADD_BASKET}
    ${elms}         Get WebElements     ${LOC_OTHER_SELLERS_ADD_BASKET}
    Click Element   ${elms[1]}
    Sleep   4
    Click Element   ${elms[0]}
    Sleep   4

Navigate To Basket Page
    Wait Until Element Is Enabled   ${LOC_BASKET_BUTTON}
    Click Element   ${LOC_BASKET_BUTTON}
    Sleep   2

Validate that Selected Product added correctly
    Wait Until Element Is Visible       ${LOC_PRODUCT_NAME}
    ${elms}    Get WebElements          ${LOC_PRODUCT_NAME}
    ${att1}    Get Element Attribute    ${elms[0]}   text
    ${att2}    Get Element Attribute    ${elms[1]}   text
    Should Be Equal     ${att1}     ${att2}
    log to console  ${att1}
    log to console  ${att2}

Validate that Sellers are different
    Wait Until Element Is Visible       ${LOC_SELLERS}
    ${elms}    Get WebElements          ${LOC_SELLERS}
    ${att1}    Get Element Attribute    ${elms[0]}   text
    ${att2}    Get Element Attribute    ${elms[1]}   text
    log to console  ${att1}
    log to console  ${att2}

Empty the Basket
    Wait Until Element Is Visible   ${LOC_DELETE_BUTTON}
    : FOR    ${i}    IN RANGE    999999
    \   ${elements}=    Get WebElements     ${LOC_DELETE_BUTTON}
    \   ${elm_len}=     get length          ${elements}
    \   Exit For Loop If    ${elm_len} == 0
    \   Click Element       ${elements[0]}
    \   Sleep   2

Validate that Basket is emptied
    Page Should Not Contain Element      ${LOC_PRODUCT_NAME}

Logout
    Mouse Up        ${LOC_MYACCOUNT}
    Sleep   1
    Click Element   ${LOC_LOGOUT}
    Sleep   2

Validate that Logout is successful
    Log to console      Validate that Logout is successful
    Element Should Not Be Visible       ${LOC_USERNAME}
    ${elm}    Get WebElement            ${LOC_USERNAME}
    ${att}    Get Element Attribute     ${elm}   text
    log to console          ${att}
    Should Not Be Equal     ${att}      ${USER_NAME}

Add Product ${product} to the Basket without User Login
    Open Home Page
    Search A Product    ${product}
    Click first Product in Search Results
    Add Product to Basket from two different Sellers
    Navigate To Basket Page
    Validate that Selected Product added correctly
    Validate that Sellers are different
    Empty the Basket
    Validate that Basket is emptied

Add Product ${product} to the Basket by User Login
    Open Home Page
    Navigate To Login Page
    Login With Crendentials
    Search A Product    ${product}
    Click first Product in Search Results
    Add Product to Basket from two different Sellers
    Navigate To Basket Page
    Validate that Selected Product added correctly
    Validate that Sellers are different
    Empty the Basket
    Validate that Basket is emptied
    Logout
    Validate that Logout is successful


*** Test Cases ***
Adding Products to the Basket by User Login
    [Template]  Add Product ${product} to the Basket by User Login
    # Examples:
    # Product
    Fifa 20
    Sony Kulaklık

Adding Products to the Basket without User Login
    [Template]  Add Product ${product} to the Basket without User Login
    # Examples:
    # Product
    Walkman
    God Of War

