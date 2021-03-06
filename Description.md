# Initial Preamble

LDAP is a tree-based database. It consists of:
 * Organisational units (OU) that form the nodes of the tree
 * Objects for the leaves, that are distinguised by their Common Name (CN)
 * Each CN has multiple properties associated with them that form a list. Each entry is representable as a string, but may be underlying a construction of one of:
 1. Numeric
 2. String
 3. Boolean ('FALSE' or 'TRUE')
 4. Binary data
 5. A reference to a DN
 * There is no known formal type binding for each object.
The top OU is called a Domain Component (DC), which typically has multiple fields, e.g.
    dc=nurdspace,dc=nl
All objects can be uniquely identified by their Distinguished Name (DN).

At the present time there are no 'good' Window-based LDAP browsers available for Linux. The aim of this project is to provide a simple, robust browser and editor.

# Window description

The main display should be split into two sides - the left side as a tree browser, whilst the right side is an information panel about the selected object.

The tree browser should show each OU as a folder. Initially, only the DC is visible, but this can be expanded out into a tree of top-level OUs, which can each be expanded to display the child objects (OUs or CNs).

When selecting an OU or CN, the information panel should display a list of properties in tabular format related to the selected object. In the background, this should make a request for LDAP information at the moment of selection. Selecting a different object should update this window. If the data represented is of binary type, then this should be shown as a base64 endoded string.

It should be possible to edit the properties of an object in the information panel by double-clicking on them and bringing up a separate edit window. This window should consist of:
 * The original data pre-selected for replacement
 * The type of data as a radio-button selection (binary or text/integer)
When data is entered in binary mode, the string entered should be base64 encoded, and should be written to the server as the corresponding binary. As soon as data is entered, the server should be updated with the new information and the information panel refreshed to reflect this change. Whilst editing a field, the main window should be unable to be updated.

# Menu Description

Initially the application starts in an unconnected state. Connection should be made through a Connect field in the menu structure. This should bring up a new window which the following fields are required, filled from default.conf is it exists:
* Bind DN (username) - Text box, default
* Password - Text box, Secret
* LDAP URI - Text box, defaultly 'ldap://'
* SASL - radiobutton, forced off (cannot enable)
* Force Protocol 2 - radiobutton, default off
* Force Protocol 3 - radiobutton, default off
(It should be possible to get the DC somehow, otherwise this will need a field...)
A 'Load' button
A 'Save as...' button
A 'Connect' button
This information should be locally cached, and written to an external config file. The password may not be saved. Saving the information to the default config file (default.conf) will mean it is automatically read on startup. If there is no password set when Connect is pressed, a new prompt must ask for this in a secret fashion.

There should be a disconnect button. This immediately returns the application to the unconnected state where no DC is shown on the tree viewer and the information panel is blank.

There should be a refresh button. This refreshes the currently selected object's information panel (if any), and the tree viewer's OU's up to the DC from the current object. If the selected object is an OU, that should be updated in the tree viewer as well. This may be hotkeyed to F5.
