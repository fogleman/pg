#version 120

uniform mat4 matrix;

attribute vec4 position;
attribute vec2 uv;

varying vec2 frag_uv;

void main() {
    gl_Position = matrix * position;
    frag_uv = uv;
}
