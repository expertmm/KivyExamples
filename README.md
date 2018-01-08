# KivyExamplesPy3
UtahPythonKivyExamples (python3 fork by expertmm)

## Changes
(2018-01-07)
* added pointrenderer3d.py and pointshader3d.glsl (animated particles with 3d position)
(2018-01-06)
* expertmm fork
* ran `2to3 -w KivyExamplesPy3`
* changed vertex_format from string,value,string to bytestring,value,string (changed `('` to `(b'` on each vertext format element) in:
  * Drawing_Multiple_Shapes_Shaders/main.py
  * Drawing_Multiple_Shapes_Shaders/pointrender.py
  * Drawing_Nice_Lines/glslline.py
  * Drawing_With_Point_Sprites/main.py
* cProfiling_On_Android/main.py: changed `if platform() == 'android'` to `if platform == 'android'` (not sure why it was assumed to be a method--this change was not tested on android)

## Kovak version:
This repo contains code snippets to be used in my presentation at the August 8, 2013 Utah Python Meeting

You can find the presentation that accompanied these examples at the Utah Python August 2013 meeting on youtube here: http://www.youtube.com/watch?v=3gzZbsKlFMs
