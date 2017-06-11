 ____        _          _____                          _       
|  _ \  __ _| |_ __ _  |  ___|__  _ __ _ __ ___   __ _| |_ ___ 
| | | |/ _` | __/ _` | | |_ / _ \| '__| '_ ` _ \ / _` | __/ __|
| |_| | (_| | || (_| | |  _| (_) | |  | | | | | | (_| | |_\__ \
|____/ \__,_|\__\__,_| |_|  \___/|_|  |_| |_| |_|\__,_|\__|___/
                                                               

--------------
 STREAM_*.txt 
--------------
  + Every new line in the file represents a single time frame in a Processing 
  animation assuming a framerate of [15 FPS] for refresh. 
      - Note that 0 denotes an unwillingness to meet again and that 1 represents
        a willingness to meet with the other party.
  + The party's specific gender is not noted in the stream, 
  but points at which the conversation turns to the other speaker are denoted by the token "switch"
  + This special "switch" sentinel value does NOT represent a frame advancement and the new line
    when switch is read should not be counted as a frame in the Processing animation