# My Ringtone App (v1.0)

A custom Android ringtone manager built with **Python** and **Kivy**. Import audio files from your device, preview them with built-in playback controls, and set them directly as your phone's default ringtone.

## Features
- **Import Audio Files:** Browse and add audio tracks directly from local storage.
- **Built-in Audio Player:** Play, pause, and switch between saved tracks before setting them.
- **Direct Ringtone Setup:** Set any saved track as your default Android ringtone using native Android APIs (`RingtoneManager`).
- **Local Database:** Automatically saves your ringtone library using SQLite.
- **Adaptive Layout:** Opens in a mobile preview window on PC and scales to full screen on Android.

## Tech Stack
- **Language:** Python
- **UI Framework:** Kivy
- **Database:** SQLite3
- **Android Bridge:** Pyjnius
- **Build Tool:** Buildozer (WSL / Ubuntu)

## Android Permissions Used
- Storage / Media Audio access (to pick and play local audio files)
- Modify System Settings (`WRITE_SETTINGS`) (to update the default ringtone)

## Author
Made by **Spell-0608**
