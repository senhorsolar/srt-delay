## Subtitle file (.srt) synchronizer

Simple python script to delay or speed up a .srt subtitle file. Usage:
```
python srt_delay.py <file.srt> <delay in sec> [--from <starting sec>]
```

The optional --from parameter allows you to apply the delay from some initial starting point.

I was watching a movie with subtitles, and the subtitles were about 40s too soon. The built-in synchronizer in VLC player wasn't sufficient, as everytime you pause it would wait 40s in order to see the subtitles again. This script creates a new file with the time values modified according to some given delay.


