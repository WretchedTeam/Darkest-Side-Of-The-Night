define config.gl2 = True

init python:
    renpy.register_shader("dsotn.crt", variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform vec2 res0;
        uniform float u_time;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;

        uniform mat4 u_transform;
        attribute vec4 a_position;
    """, vertex_100="""
        gl_Position = u_transform * a_position;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        #define BLUR_RADIUS 2

        #define BLUR
        //#define CHROMATIC
        #define SATURATION
        #define CONTRAST
        #define SCANLINES
        #define FLICKER
        #define VIGNETTE
        #define STATIC

        const float RADIUS = 0.95;
        const float SOFTNESS = 0.5;

        float vignette(vec2 uv) {
            vec2 center = vec2(0.5);
            float dist = distance(center, uv);
            return smoothstep(RADIUS, RADIUS - SOFTNESS, dist);
        }

        vec3 saturation(vec3 rgb, float adjustment)
        {
            const vec3 W = vec3(0.2125, 0.7154, 0.0721);
            vec3 intensity = vec3(dot(rgb, W));
            return mix(intensity, rgb, adjustment);
        }

        vec3 brightnessContrast(vec3 value, float brightness, float contrast)
        {
            return (value - 0.5) * contrast + 0.5 + brightness;
        }

        float rand(vec2 n) { 
            return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
        }
    """, fragment_200="""
        vec2 st = v_tex_coord;

        vec4 color = texture2D(tex0, st);

        #ifdef BLUR
        for (int i = 1; i <= BLUR_RADIUS; i++) {
            color += texture2D(tex0, st + vec2(float(i) / res0.x, 0.0));
            color += texture2D(tex0, st - vec2(float(i) / res0.x, 0.0));
        }

        color /= float(BLUR_RADIUS) * 2.0 + 1.0;
        #endif

        #ifdef CHROMATIC
        color.r = texture2D(tex0, st + vec2(1.0 / res0.x, 0.0)).r;
        color.g = texture2D(tex0, st - vec2(1.0 / res0.x, 0.0)).g;
        #endif

        #ifdef SCANLINES
        float count = res0.y * 2.0;

        vec2 scanlineCoords = vec2(sin((st.y + u_time * 0.005) * count), 0);
        vec3 scanlines = vec3(scanlineCoords.x, scanlineCoords.y, scanlineCoords.x);
        color.rgb -= color.rgb * scanlines * 0.5 * color.a;
        #endif

        #ifdef SATURATION
        // saturation(<color>, <saturation_value>)
        color.rgb = saturation(color.rgb, 0.6) * color.a;
        #endif

        #ifdef CONTRAST
        // brightnessContrast(<color>, <brightness>, <contrast>)
        color.rgb = brightnessContrast(color.rgb, -0.05, 0.8) * color.a;
        #endif


        #ifdef FLICKER
        color.rgb -= color.rgb * sin(120.0 * u_time) * 0.02 * color.a;
        #endif

        #ifdef VIGNETTE
        color.rgb *= vignette(st) * color.a;
        #endif

        #ifdef STATIC
        float staticMult = 0.15; // Change this to adjust the opacity
        color.rgb -= rand(st * u_time) * color.a * staticMult;
        #endif

        gl_FragColor = color;
    """)

transform old_tv:
    mesh True
    shader "dsotn.crt"