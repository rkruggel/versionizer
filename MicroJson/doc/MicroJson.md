# MicroJson

MicroJson

Es können Daten schemafrei in form einer Key-Value nosql gespeichert werden.
Es wird zwischen eine Dict und einer List unterschieden. Die Dict ist ein 
Dictionary welches unter einem Key gespeichert wird. Es hat folgenden Aufbau

**Python**

    datadict = {
        'id': '4711',
        'vorname': 'roland',
        'name': 'kruggel',
        'alter': 54
    }

nach dem Speicher sieht der Json-File der DB dan so aus:

**MicoJson**

    {
        "4711": {
            "id": "4711", 
            "vorname": "roland", 
            "name": "kruggel", 
            "alter": 54
        }
    }

### Die Id

Jeder Datensatz bekommt eine eindeuige ID. Die ID ist immer vom type String. Die Form und
das Format ist unabhängig und wahlfrei. Wenn keine Id vergeben wird, erstellt MicroJason 
eine eigene ID. Die besteht aus einem Timestamp mit 6 Nachkommastellen im format String.

Bei dem Befehl `set()` kann optional eine ID mit angegeben werden. Wenn diese Id mit 
angegeben wird, wird sie verwendet. Die eventuell vorhandenen ID in dem Python Dict wird 
dann überschrieben.

## Die Befehle

### Init

Die Datenbank initialisieren.

    tb = JsonDictDb('../jsondb/t_dict.json', False)

Jede Collection bekommt eine eigene Datei. Es werden sowohl dict's als auch list's gespeichert.
Eine Unterscheidung ist beim Init nicht notwendig. dict und list können auch zusammen in eine Datei
gespeichert werden.

### Set

Daten speichern, updaten uns/oder hinzufügen. 

    datadict = {
    	'id': '4711',
        'vorname': 'roland',
        'name': 'roland',
        'alter': 54
    }
    nid = tb.set(datadict, xid='kl99')

