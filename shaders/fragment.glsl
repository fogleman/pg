#version 120

varying vec3 frag_color;
varying float frag_dist;

void main() {
    float p = (frag_dist - 1.2) / 0.4;
    gl_FragColor = mix(vec4(frag_color, 1.0), vec4(0), pow(p, 0.8));
}
