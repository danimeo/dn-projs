---
title: rhasspy省力脚本
---

```bash
git clone --recursive https://github.com/rhasspy/rhasspy
cd rhasspy/
./configure --enable-in-place
make
make install
```


```bash
docker run -d -p 12101:12101       --name rhasspy       --restart unless-stopped       -v "$HOME/.config/rhasspy/profiles:/profiles"       -v "/etc/localtime:/etc/localtime:ro"       --device /dev/snd:/dev/snd       rhasspy/rhasspy       --user-profiles /profiles       --profile zh
```

```yaml
  default:
    mic:
      name: arecord
    wake:
      name: porcupine1
    vad:
      name: silero
    asr:
      name: faster-whisper
    # intent:
    #   name: regex
    handle:
      name: repeat
    tts:
      name: piper
    snd:
      name: aplay

```

```bash

# pip install webrtcvad
mkdir -p config/programs/vad/
cp -R programs/vad/webrtcvad config/programs/vad/
config/programs/vad/webrtcvad/script/setup

```

```bash
script/run bin/server_run.py asr faster-whisper
```

