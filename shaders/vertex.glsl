#version 120

uniform mat4 matrix;

attribute vec4 position;
attribute vec3 color;

varying vec3 frag_color;
varying float frag_dist;

void main() {
    gl_Position = matrix * position;
    frag_color = color;
    frag_dist = distance(vec4(0), position);
}
