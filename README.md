# lei-ihm_video_mapping
Our lei IHM to config mapping

## Init
    git submodule update --init --recursive
    pip install -r requirements.txt

## END POINTS

    [GET]: /
    > show index page for manage mapping
    
    [POST]: /sendPoints
    > post all image points with screen size
    > EXAMPLE REQUEST
    {'width': 1166, 'heigth': 706, 'points': [[[865, 190], [1143, 225], [1123, 382], [831, 333]], [[431, 154], [864, 190], [832, 332], [456, 326]], [[137, 169], [420, 164], [441, 327], [136, 331]]]}
    
    [GET]: /test
    > It is a test page