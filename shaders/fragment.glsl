#version 120

uniform sampler2D sampler;

varying vec2 frag_uv;

void main() {
    gl_FragColor = texture2D(sampler, frag_uv);
}
