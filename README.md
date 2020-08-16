# PanoCap
Panopto Capture is for downloading offline lectures and other video streams combining the difference video streams into one file.

# Prerequisites
1. Install python
1. Install certifi using PIP, `PIP install certifi`.

# First use
1. Log into your Panopto account on a web browser, copy the ASPXAUTH cookie, a very long Hex string (512 characters), eg:
`B819C52C60946E84A14C8356DC55B480684CDC323945997DEA2B77B2101A2048B0AE738ECFFD0EE147314A93501271DC634B09D239937BBC2DE172C419327BA2AF02B80AE0CFD318B912F545ED55A3553328B73CA418488F77E37DF5CE523021B0DE7E11A6322AB276EC9910A0048BC10946C671434AD6E37E0A5FE445670783E306824F286E07F1D3A3E20D5FEA6BF0FBEB64BAACE00E3A9281F34BCFAEFD3E1141C63286027C9C10F449CB63D743C523ED1EC770F337B36A18D9A31510A57B302D41188AA832208A672C0600E49174B11A77427E6CB8668EF73423323C871FAE367150C7D13FAB191E9AF2D03E9C12119F62CD140BFA5F52B939F6669B3258`
1. Enter your ASPXAUTH cookie and ID and your off! 

# Settings
All settings can be accessed in the settings.ini that is generated on first run.
This includes:

* Directories
  * basedir - Where the videos will be downloaded to
  * netloc - No implemented yet
  * seshfile - Where the raw data for each video and group is stored
  * csvfile - Where meta data for each video can be edited, i.e. group and video names
  * logfile - Where the log data is stored

* Cookies
  * aspxauth - your unique key that allows logging into the server, never share this with anyone
  * sandboxcookie - unused, no longer needed
  * csrftoken - unused, no longer needed
  * yourid - your log in ID

* Modifiers
  * group_regex - The regex that generates the group names, default: ^.*?\:\s(\d{2})\/(\d{2})\-(.*)
  * excluded_groups - Groups that you do not want to download videos from
  * only_groups- Groups that you only want to download videos from
  * excluded_session_ids - Video ID's you dont want to download

* Settings
  * istest - True to run in test mode
  * num_treads - number of simultaneous threads that will preform actions e.g. get data from server, download from server and transcode video files, set to 1+, be aware, more threads dosen't mean quicker.
  * queuelength - Max number of tasks each thread can have queued.

* StreamTypes - For renaming stream types to something more useful, it is shown when switching video streams.

# To Do
1. remove uneeded cookie options
1. remove compress sessions unless better/more efficient encoding is found - help would be appricated in this
1. fix resizing/layout
1. edit names in program rather than via CSV
1. exclude groups and sessions in program rather than in settings

 

