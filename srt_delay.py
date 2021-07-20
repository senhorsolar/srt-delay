import argparse
from datetime import datetime, timedelta
import glob
from pathlib import Path
import re

# Regex patterns
HOURS = "[0-9]{2}"
MINUTES = "[0-5][0-9]"
SECONDS = "[0-5][0-9]"
MILLIS = "[0-9]{3}"


def convert_to_sec(hour, minute, sec, ms):
    return hour * 3600 + minute * 60 + sec + ms/1000


def split_seconds(sec):
    
    hours = int(sec // 3600)
    assert(hours < 100)
    sec %= 3600

    mins = int(sec // 60)
    sec %= 60

    secs = int(sec // 1)
    sec %= 1

    ms = int(sec * 1000)

    return hours, mins, secs, ms


def extract_time(time_str):
    pattern = f"({HOURS}):({MINUTES}):({SECONDS}),({MILLIS})"
    if m := re.match(pattern, time_str):
        hours, mins, secs, ms = map(int, m.groups())
    else:
        raise RuntimeError(f"Time is not in the valid format: arg = {time_str}")

    return convert_to_sec(hours, mins, secs, ms)


def secs_to_time_str(secs):
    hours, mins, secs, ms = split_seconds(secs)
    return f"{hours:0>2}:{mins:0>2}:{secs:0>2},{ms:0>3}"


def get_output_fname(filename):
    p = Path(filename)
    return f"{p.stem}_synched.{p.suffix}"


def main(filename, sec_to_add, from_sec=0):

    time_str = f"{HOURS}:{MINUTES}:{SECONDS},{MILLIS}"
    pattern = f"({time_str}) --> ({time_str})"
    
    output_filename = get_output_fname(filename)

    with open(filename, 'r', errors='replace') as f, open(output_filename, 'w') as output_f:
        for line in f.readlines():
            if m := re.match(pattern, line):
             
                beg, end = map(extract_time, m.groups())

                if beg < from_sec:
                    output_f.write(line)
                    continue

                beg_sec, end_sec = sec_to_add + beg, sec_to_add + end

                if beg_sec < 0:
                    raise RuntimeError("Shift results in negative time of {beg_sec}s")

                new_beg, new_end = map(secs_to_time_str, [beg_sec, end_sec])
                new_time = f"{new_beg} --> {new_end}\n"
            
                output_f.write(new_time)
            else:
                output_f.write(line)

    print(f"Output file: {output_filename}")


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Synchronize subtitle time")
    parser.add_argument('filename', type=str, help='<filename>.srt subtitle file')
    parser.add_argument('sec_to_add', type=float, help='Number of seconds to shift subtitle time')
    parser.add_argument('--from', dest='from_sec', type=float, default=0., help='Time from which to apply time shift')
    args = parser.parse_args()

    main(args.filename, args.sec_to_add, args.from_sec)

