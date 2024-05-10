
#!/bin/sh -v
dir="/home/inunekoippiki/hatoba_eyes/"
echo $dir
(
    cd $dir
    ./.venv/bin/python3 ./pygame_renderer.py --fullscreen True
)