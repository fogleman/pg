#version 120

uniform sampler2D sampler;

varying float diffuse;
varying vec2 frag_uv;

const vec3 light_color = vec3(0.8);
const vec3 ambient = vec3(0.2);

void main() {
    vec3 color = vec3(texture2D(sampler, frag_uv));
    vec3 light = ambient + light_color * diffuse;
    color = clamp(color * light, vec3(0.0), vec3(1.0));
    gl_FragColor = vec4(color, 1.0);
}
