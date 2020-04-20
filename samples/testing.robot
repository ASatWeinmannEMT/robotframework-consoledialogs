*** Settings ***
Library  ConsoleDialogs

*** Test Cases ***
Test Pause
    Pause Execution   Pause with message
    Pause Execution
    Pause Execution   Pause with exceeding long message that should get wrapped blah blah blah blah blah
    Pause Execution
    Pause Execution   Message de pause
    Pause Execution
    Pause Execution   Message de pause
    Pause Execution
