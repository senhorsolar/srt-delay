## Subtitle file (.srt) synchronizer

Simple python script to delay or speed up a .srt subtitle file. 

### Usage:
```
python srt_delay.py <file.srt> <delay in sec> [--from <starting sec>]
```

This script creates a new file with the time values modified according to some given delay. The optional --from parameter allows you to apply the delay from some initial starting point.

### Background
I was watching a movie with subtitles, and the subtitles were about 40s too early. The built-in synchronizer in VLC player wasn't sufficient, as everytime I'd pause I'd have to wait 40s in order to see the subtitles again. I took a look at the subtitle file, and realized it was just a plain text file. Very easy to modify yourself. 


