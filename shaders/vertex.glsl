#version 120

uniform mat4 matrix;

attribute vec4 position;
attribute vec3 color;

varying vec3 frag_color;

void main() {
    gl_Position = matrix * position;
    frag_color = color;
}
