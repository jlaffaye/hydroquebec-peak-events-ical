# hydroquebec-peak-events-ical

Provides iCal calendar files for HydroQuebec peak events

## How to use

First, get the offer code corresponding to your hydroquebec contract: https://donnees.hydroquebec.com/explore/dataset/evenements-pointe/information/

In my case, Winter Credit is `CPC-D`. The file is then located at
```
https://raw.githubusercontent.com/jlaffaye/hydroquebec-peak-events-ical/refs/heads/main/data/${OFFER}/${YEAR}.ics
```

### In HomeAssistant

I use the [ICS Calendar](https://github.com/franc6/ics_calendar) integration to synchronize the calendar into HomeAssistant.

This integration provides some variables for the year, so the final URL is
```
https://raw.githubusercontent.com/jlaffaye/hydroquebec-peak-events-ical/refs/heads/main/data/CPC-D/{year}.ics
```
