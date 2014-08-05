#version 120

uniform mat4 matrix;
uniform mat4 normal_matrix;

attribute vec4 position;
attribute vec3 normal;
attribute vec2 uv;

varying float diffuse;
varying vec2 frag_uv;

const vec3 light_direction = normalize(vec3(-1.0, 0.5, 0.0));

void main() {
    gl_Position = matrix * position;
    diffuse = max(0.0, dot(mat3(normal_matrix) * normal, light_direction));
    frag_uv = uv;
}
