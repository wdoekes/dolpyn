#!/usr/bin/env python3
"""
Create signal.ir file for the Flipper Zero from "csv" data

The values are hardcoded below. They are taken from the "MAIN ZONE" from
the marantz-2014-ir excel sheet [1].

[1] https://www.marantz.com/-/media/files/documentmaster/marantzna/\
us/marantz-2014-ir-command-sheet.xls and turn it into:
"""
from dolpyn_ir_signals import Rc5IrSignal, Rc5MarantzIrSignal

MAIN_ZONE = '''\
POWER ON/OFF;16;12;---
POWER ON;16;12;01
POWER OFF;16;12;02
SYSTEM POWER OFF;16;12;13
VOL +;16;16;---
VOL -;16;17;---
Direct VOLUME 25%;16;111;16
Direct VOLUME 50%;16;111;32
Direct VOLUME 75%;16;111;48
Audio MUTE ON;16;13;00
Audio MUTE OFF;16;13;01
Audio MUTE (Toggle);16;13;---
SPEAKER Sel.;16;29;---
SPEAKER-A ON/OFF;16;35;---
SPEAKER-A ON;16;35;00
SPEAKER-A OFF;16;35;01
SPEAKER-B ON/OFF;16;39;---
SPEAKER-B ON;16;39;00
SPEAKER-B OFF;16;39;01
OSD Menu On;16;82;---
MENU;16;82;60
OPTION;16;82;11
Source Select Menu;16;82;20
EXIT MENU;16;83;---
ENTER (OK);16;87;---
Return;16;87;04
CURSOR Up;16;80;---
CURSOR Down;16;81;---
CURSOR Left;16;85;---
CURSOR Right;16;86;---
Shift;16;32;00
Soft keyboard/Search;16;82;61
Insert;16;77;01
Delete;16;78;01
Dimmer(Display);16;15;00
Dimmer;16;71;---
Info.;16;15;08
OSD Info.;16;15;---
Status;16;15;07
InstaPreview ON/OFF;16;15;20
InstaPreview ON;16;15;21
InstaPreview OFF;16;15;22
Video Select;16;15;50
VIDEO OFF (V.OFF);16;13;02
INPUT NEXT;16;00;13
INPUT BACK;16;00;14
TUNER (TUNER,FM);17;63;---
Blu-ray(BD)(Code1);07;63;00
Blu-ray(BD)(Code2);28;63;00
Blu-ray/DVD;16;02;04
CD;20;63;---
TV AUDIO(TV);00;63;---
DVD;16;00;10
MEDIAPLAYER(VCR1);05;63;---
CBL/SAT(SAT,VCR2);06;63;---
AUX1(AUX);16;00;06
AUX2;16;00;07
AUX3(Additional Source);16;00;08
AUX4(Additional Source);16;02;00
AUX5(Additional Source);16;02;01
AUX6(Additional Source);16;02;02
AUX7(Additional Source);16;02;03
Bluetooth;16;02;16
GAME;16;00;62
GAME2;16;00;08
PHONO;21;63;---
USB(iPod/USB);24;63;01
USB(iPod/USB)2;24;63;11
Online Music(NETWORK);24;63;10
Internet Radio Select;27;63;20
Spotify (*6);27;63;28
SIRIUSXM (*4);27;63;29
Rhapsody Select (*4);27;63;21
Napstar Select (*6);27;63;22
Flickr Select;27;63;23
Media Server Select;27;63;24
Pandora Select (*4);27;63;26
Last.fm Select (*5);27;63;27
Online Music(NETWORK);27;63;10
Online Music(NET);27;63;11
M-XPort;29;63;01
BALANCED;16;00;20
7.1 (6.1) CH. Input ON/OFF;16;01;03
7.1 (6.1) CH. Input ON;16;01;12
7.1 (6.1) CH. Input OFF;16;01;13
Smart Select1;16;02;21
Smart Select2;16;02;22
Smart Select3;16;02;23
Smart Select4;16;02;24
Smart Select5;16;02;25
Input Mode Select;16;01;01
INPUT MODE:AUTO;16;01;15
INPUT MODE:HDMI;16;01;16
INPUT MODE:DIGITAL;16;01;17
INPUT MODE:ANALOG;16;01;18
Bilingual (Audio Channel);16;01;14
LIP SYNC.(Audio Delay);16;10;01
Resolution(Analog);16;15;10
Resolution(HDMI);16;15;11
Vertical Stretch ON;16;15;12
Vertical Stretch OFF;16;15;13
HDMI Audio Output Select (Toggle);16;84;00
HDMI Audio Output: Enable (Decode by AVR);16;84;01
HDMI Audio Output: Through (Decode by TV);16;84;02
HDMI AUTO LIP SYNC.: ENABLE;16;84;11
HDMI AUTO LIP SYNC.: DISABLE;16;84;12
I/P CONVERT: ENABLE;16;84;21
I/P CONVERT: DISABLE;16;84;22
COMPONENT-2 for MAIN;16;84;31
COMPONENT-2 for MULTI-A;16;84;32
Video Mode (Toggle);16;84;50
Video Mode: Auto;16;84;51
Video Mode: Movie;16;84;52
Video Mode: Game;16;84;53
HDMI In-1;16;84;41
HDMI In-2;16;84;42
HDMI In-3;16;84;43
HDMI In-4;16;84;44
HDMI Output Select (Toggle);16;120;00
HDMI Out-1;16;120;01
HDMI Out-2;16;120;02
HDMI Out-Auto(Dual);16;120;03
SURROUND MODE (Toggle/NEXT);16;37;---
SURROUND MODE (Back);16;64;15
MOVIE SURROUND;16;37;29
MUSIC SURROUND;16;37;53
GAME SURROUND;16;64;18
AUTO;16;37;45
STEREO;16;37;30
MONO;16;37;37
MULTI-CH Stereo/ Select;16;37;57
MULTI-CH MOVIE;16;64;20
MULTI-CH MUSIC (Stereo);16;64;21
THX;16;64;13
THX CINEMA;16;37;36
THX SURRUND EX;16;37;58
THX ULTRA 2;16;64;07
THX 5.1 MUSIC;16;64;04
THX GAMES;16;64;14
NEURAL;16;64;16
DOLBY;16;37;41
PRO LOGIC;16;37;00
PL IIx(z) Movie / PL II Movie;16;64;00
PL IIx(z) Music / PL II Music;16;64;01
PL IIx Game;16;64;12
PL IIz;16;64;17
Dolby Atomos ON/OFF;16;64;25
DOLBY HEADPHONE;16;37;60
EX/ES;16;37;61
DTS Mode;16;64;08
DTS;16;37;46
DTS ES;16;64;03
DTS Neo6 Cinema;16;64;05
DTS Neo6 Music;16;64;06
DTS NEO:X ON/OFF;16;64;22
CS-II (SRS) (Toggle);16;64;09
CS-II (SRS) Mono;16;64;10
CS-II Cinema (CS 5.1 Cinema);16;64;02
CS-II Music (CS 5.1 Music);16;37;62
HALL;16;37;01
STADIUM;16;37;02
MATRIX;16;37;09
MOVIE;16;37;29
VIRTUAL;16;37;51
Decoder Mode;16;01;20
DSP MODE;16;37;63
SOURCE(Pure) DIRECT (Toggle);16;34;---
PURE DIRECT (Toggle);16;34;01
Direct Mode;16;34;02
Pure Direct;16;34;03
All Zone Stereo ON/OFF;16;100;00
All Zone Stereo ON;16;100;01
All Zone Stereo OFF;16;100;02
NIGHT (Toggle);16;37;42
Re-EQ (Toggle);16;37;44
Cinema EQ (HT-EQ)(Toggle);16;64;11
Loudness Management ON/OFF(Toggle);16;64;19
M-DAX;16;22;04
M-DAX OFF;16;22;06
M-DAX HIGH;16;22;07
M-DAX LOW;16;22;08
M-DAX MID;16;22;09
Bass Sync UP;16;22;12
Bass Sync DOWN;16;22;22
TONE CONTROL ON/OFF (Toggle);16;22;01
TONE CONTROL OFF;16;22;10
TONE CONTROL ON;16;22;11
BASS +;16;22;---
BASS -;16;23;---
TREBLE +;16;24;---
TREBLE -;16;25;---
TEST TONE;16;37;21
Volume Reset;16;37;31
CH. SELECT;16;37;33
CH. LEVEL +;16;37;34
CH. LEVEL -;16;37;35
BALANCE RIGHT;16;26;---
BALANCE LEFT;16;27;---
Front L (A-TRIM) + (Up);16;26;01
Front L (A-TRIM) - (Down);16;26;02
Front R (B-TRIM) + (Up);16;26;03
Front R (B-TRIM) - (Down);16;26;04
Surround L + (Up);16;26;05
Surround L - (Down);16;26;06
Surround R + (Up);16;26;07
Surround R - (Down);16;26;08
Surround Back L + (Up);16;26;09
Surround Back L - (Down);16;26;10
Surround Back R + (Up);16;26;11
Surround Back R - (Down);16;26;12
Front Wide L + (Up);16;26;13
Front Wide L - (Down);16;26;14
Front Wide R + (Up);16;26;15
Front Wide R - (Down);16;26;16
Front Height L + (Up);16;26;17
Front Height L - (Down);16;26;18
Front Height R + (Up);16;26;19
Front Height R - (Down);16;26;20
Center + (Up);16;37;11
Center - (Down);16;37;12
Subwoofer + (Up);16;37;49
Subwoofer - (Down);16;37;50
Subwoofer 2 + (Up);16;64;23
Subwoofer 2 - (Down);16;64;24
Top Front L + (Up);16;26;21
Top Front L - (Down);16;26;22
Top Front R + (Up);16;26;23
Top Front R - (Down);16;26;24
Top Middle L + (Up);16;26;25
Top Middle L - (Down);16;26;26
Top Middle R + (Up);16;26;27
Top Middle R - (Down);16;26;28
Top Rear L + (Up);16;26;29
Top Rear L - (Down);16;26;30
Top Rear R + (Up);16;26;31
Top Rear R - (Down);16;26;32
Rear Height L + (Up);16;26;33
Rear Height L - (Down);16;26;34
Rear Height R + (Up);16;26;35
Rear Height R - (Down);16;26;36
Front Dolby L + (Up);16;26;37
Front Dolby L - (Down);16;26;38
Front Dolby R + (Up);16;26;39
Front Dolby R - (Down);16;26;40
Surround Dolby L + (Up);16;26;41
Surround Dolby L - (Down);16;26;42
Surround Dolby R + (Up);16;26;43
Surround Dolby R - (Down);16;26;44
Back Dolby L + (Up);16;26;45
Back Dolby L - (Down);16;26;46
Back Dolby R + (Up);16;26;47
Back Dolby R - (Down);16;26;48
Audyssey MultEQ: OFF;16;28;00
Audyssey MultEQ MODE (Toggle);16;28;02
Audyssey MultEQ MODE: UP;16;28;03
Audyssey MultEQ MODE: DOWN;16;28;04
Audyssey MultEQ: MODE-1;16;28;05
Audyssey MultEQ: MODE-3;16;28;07
Audyssey MultEQ: MODE-4;16;28;08
Audyssey MultEQ: MODE-5;16;28;09
Audyssey Dynamic EQ/VOL;16;28;40
Audyssey Dynamic EQ Mode;16;28;20
Audyssey Dynamic EQ Mode Off;16;28;21
Audyssey Dynamic EQ Mode On;16;28;22
Audyssey Dynamic Volume Mode;16;28;30
Audyssey Dynamic Volume Mode Off;16;28;31
Audyssey Dynamic Volume Mode L;16;28;32
Audyssey Dynamic Volume Mode M;16;28;33
Audyssey Dynamic Volume Mode H;16;28;34
Audyssey Dynamic EQ Offset;16;28;50
Audyssey Dynamic EQ Offset Off;16;28;51
Audyssey Dynamic EQ Offset -5dB;16;28;52
Audyssey Dynamic EQ Offset -10dB;16;28;53
Audyssey Dynamic EQ Offset -15dB;16;28;54
Audyssey LFC ON/OFF;16;64;40
Audyssey LFC ON;16;64;41
Audyssey LFC OFF;16;64;42
Audyssey DSX ON/OFF;16;64;50
Audyssey DSX OFF;16;64;51
Audyssey DSX ON(Height);16;64;52
Audyssey DSX ON(Wide);16;64;53
Audyssey DSX ON(Wide/Height);16;64;54
Graphic EQ ON/OFF;16;28;10
Graphic EQ ON;16;28;12
Graphic EQ OFF;16;28;11
ECO Mode;16;58;10
ECO Mode ON;16;58;12
ECO Mode OFF;16;58;11
ECO Mode AUTO;16;58;13
SLEEP;16;38;---
SLEEP OFF;16;38;00
DC Trgger-1 ON;16;125;01
DC Trgger-1 OFF;16;125;02
DC-Trgger-2 ON;16;125;03
DC-Trgger-2 OFF;16;125;04
DC Trgger-3 ON;16;125;05
DC Trgger-3 OFF;16;125;06
DC-Trgger-4 ON;16;125;07
DC-Trgger-4 OFF;16;125;08
BAND;17;63;---
;17;47;01
FM;17;45;---
AM;17;46;---
DISPLAY MODE;17;15;---
T-MODE;17;37;---
MEMO (MEMORY);17;41;---
CLEAR;17;58;---
FREQ. Direct;17;11;---
FREQ.(tuning) Up +;17;30;---
FREQ.(tuning) Down -;17;31;---
PRESET Up +;17;32;---
PRESET Down -;17;33;---
PRESET SCAN;17;43;---
PRESET INFO;17;82;---
PRESET Direct 1;17;64;01
PRESET Direct 2;17;64;02
PRESET Direct 5;17;64;05
PRESET Direct 25;17;64;25
0 (PRESET 0);17;00;---
1 (PRESET 1);17;01;---
2 (PRESET 2);17;02;---
3 (PRESET 3);17;03;---
4 (PRESET 4);17;04;---
5 (PRESET 5);17;05;---
6 (PRESET 6);17;06;---
7 (PRESET 7);17;07;---
8 (PRESET 8);17;08;---
9 (PRESET 9);17;09;---
PRESET SHIFT;17;32;00
SHIFT A;17;32;30
SHIFT B;17;32;31
SHIFT C;17;32;32
SHIFT D;17;32;33
SHIFT E;17;32;34
SHIFT F;17;32;35
SHIFT G;17;32;36
Cursor Up;17;80;01
Cursor Down;17;81;01
Cursor Left;17;85;01
Cursor Right;17;86;01
Cursor Enter;17;87;01
RETURN;17;83;01
HD-RADIO SEEK UP;17;30;10
HD-RADIO SEEK DOWN;17;31;10
PTY　(For Europe Model);17;120;---
RT　(For Europe Model);17;120;40
RDS/SEARCH;17;120;60
iPod Mode Select (Toggle);16;82;07
Cursor Up;24;80;01
Cursor Down;24;81;01
Back;24;83;01
Cursor Left;24;85;01
Cursor Right;24;86;01
Enter;24;87;01
Return;24;87;21
Page Search/Character Search;24;80;04
Page Previous;24;32;20
Page Next;24;33;20
Top;24;82;02
Info.;24;82;05
Play/Pause;24;53;00
Play;24;53;01
iPod Play;24;53;31
Pause;24;48;01
Stop;24;54;01
Next;24;32;01
Previous;24;33;01
REW (Toggle);24;50;01
REW 1 (x2 speed);24;50;05
REW 2 (x4 speed);24;50;06
REW 3 (x8 speed);24;50;07
FF (Toggle);24;52;01
FF 1 (x2 speed);24;52;05
FF 2 (x4 speed);24;52;06
FF 3 (x8 speed);24;52;07
Random(Toggle);24;28;01
Random Off;24;28;02
Random On(Songs);24;28;03
Random (Album);24;28;04
Repeat(Toggle);24;29;01
Repeat Off;24;29;02
Repeat One;24;29;03
Repeat All;24;29;04
Repeat Folder;24;29;05
Screen Saver On/Off (Toggle);24;110;01
SHIFT;24;32;00
MEMORY;24;41;50
PRESET CH UP;24;32;20
PRESET CH DOWN;24;33;20
PRESET 1;24;01;01
PRESET 2;24;02;01
PRESET 3;24;03;01
PRESET 4;24;04;01
PRESET 5;24;05;01
PRESET 6;24;06;01
PRESET 7;24;07;01
PRESET 8;24;08;01
[Network(Digital Media Player)] 0;27;00;01
[Network(Digital Media Player)] 1;27;01;01
[Network(Digital Media Player)] 2;27;02;01
[Network(Digital Media Player)] 3;27;03;01
[Network(Digital Media Player)] 4;27;04;01
[Network(Digital Media Player)] 5;27;05;01
[Network(Digital Media Player)] 6;27;06;01
[Network(Digital Media Player)] 7;27;07;01
[Network(Digital Media Player)] 8;27;08;01
[Network(Digital Media Player)] 9;27;09;01
SHIFT A;27;01;60
SHIFT B;27;02;60
SHIFT C;27;03;60
SHIFT D;27;04;60
SHIFT E;27;05;60
SHIFT F;27;06;60
SHIFT G;27;07;60
Network(DMP): Information;27;15;01
Network(DMP): Random (toggle);27;28;01
Network(DMP): Random Off;27;28;02
Network(DMP): Random On;27;28;03
Network(DMP): Repeat (toggle);27;29;01
Network(DMP): Repeat Off;27;29;02
Network(DMP): Repeat 1;27;29;03
Network(DMP): Repeat All;27;29;04
USB: Repeat Folder;27;29;05
SHIFT;27;32;00
PRESET CH UP;27;32;20
PRESET CH DOWN;27;33;20
Internet Radio Preset 1/FAVORITE STATION 1;27;34;11
Internet Radio Preset 2/FAVORITE STATION 2;27;34;12
Internet Radio Preset 3/FAVORITE STATION 3;27;34;13
Internet Radio Preset 4/FAVORITE STATION 4;27;34;14
Network(DMP)/USB: Next;27;32;01
Network(DMP)/USB: Previous;27;33;01
Network(DMP)/USB: Pause;27;48;01
Network(DMP)/USB: REW;27;50;01
Network(DMP)/USB: FF;27;52;01
Network(DMP): Play(/Pause);27;53;01
One Touch Play;27;53;04
iPod Play;27;53;31
Party mode (Toggle);27;53;41
Internet Radio - Recent Played Station;27;53;50
Favorite Direct Play;27;53;61
Network(DMP): Stop;27;54;01
JPEG Skip + (NEXT);27;32;10
JPEG Skip - (PREVIOUS);27;33;10
MEMORY;27;41;50
Network(DMP): Cursor Up;27;80;01
Network(DMP): Cursor Down;27;81;01
Network(DMP): Cursor Left;27;85;01
Network(DMP): Cursor Right;27;86;01
Network(DMP): Enter;27;87;01
Network(DMP): Page Next;27;80;04
Network(DMP): Page Previous;27;81;04
Network(DMP): Back;27;83;01
Network(DMP): Return;27;87;21
Network(DMP):HOME;27;82;02
'''

print('Filetype: IR signals file')
print('Version: 1')
print('#')
print('# Marantz 2014 IR Command Sheet / MAIN ZONE')
print('# converted by dolpyn_ir_signals.py / wdoekes')
print('# NOTE: The flipper does NOT cope with this many entries!')
print('# As of writing this (sept 2022), the flipper will show')
print('# about 19 entries only.')
for line in MAIN_ZONE.strip().split('\n'):
    try:
        name, address, command, extension = line.rsplit(';', 3)
        address, command = int(address), int(command)
        if extension == '---':
            signal = Rc5IrSignal(
                name, address, command,
                comment=f'{name} [{address} {command}]')
        else:
            extension = int(extension)
            signal = Rc5MarantzIrSignal(name, address, command, extension)
            signal = signal.as_raw()
            assert signal.name.endswith(' (raw)')
            signal.name = signal.name[:-6]
        signal.name = signal.name.lower()
    except Exception as exc:
        raise ValueError(line) from exc
    print('#')
    print(signal)
