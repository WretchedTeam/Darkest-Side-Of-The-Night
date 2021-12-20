define config.gl2 = True

screen vhs_overlay(t="►PLAY"):
    style_prefix "vhs_overlay"

    vbox spacing 2 at old_tv:
        align (0.0, 0.0) offset (40, 40)
        text t
        text _("FEB 27 1999")

style vhs_overlay_text is empty

style vhs_overlay_text:
    font gui.interface_font
    size 36

init python:
    config.overlay_screens.append("vhs_overlay")

    renpy.register_shader("dsotn.vhs", variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform vec2 res0;
        uniform float u_time;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec4 u_random;

        uniform mat4 u_transform;
        attribute vec4 a_position;
    """, vertex_100="""
        gl_Position = u_transform * a_position;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        #define INTERLACING_SEVERITY 0.0001

        #define GET_LUMA(x) dot(x, vec3(0.212395, 0.701049, 0.086556))
        float vignette(vec2 uv, float r, float s) {
            vec2 center = vec2(0.5);
            float dist = distance(center, uv);
            return smoothstep(r, r - s, dist);
        }

        vec3 lerp3(float x, float y, vec3 color) { return x + (y - x) * color; }
        float rand(vec2 noise) { return fract(sin(dot(noise.xy,vec2(10.998,98.233)))*12433.14159265359); }

        //random hash
        vec4 hash42(vec2 p){
            
            vec4 p4 = fract(vec4(p.xyxy) * vec4(443.8975,397.2973, 491.1871, 470.7827));
            p4 += dot(p4.wzxy, p4+19.19);
            return fract(vec4(p4.x * p4.y, p4.x*p4.z, p4.y*p4.w, p4.x*p4.w));
        }


        float hash( float n ){
            return fract(sin(n)*43758.5453123);
        }

        // 3d noise function (iq's)
        float n( in vec3 x ){
            vec3 p = floor(x);
            vec3 f = fract(x);
            f = f*f*(3.0-2.0*f);
            float n = p.x + p.y*57.0 + 113.0*p.z;
            float res = mix(mix(mix( hash(n+  0.0), hash(n+  1.0),f.x),
                                mix( hash(n+ 57.0), hash(n+ 58.0),f.x),f.y),
                            mix(mix( hash(n+113.0), hash(n+114.0),f.x),
                                mix( hash(n+170.0), hash(n+171.0),f.x),f.y),f.z);
            return res;
        }

        //tape noise
        float nn(vec2 p, float t){


            float y = p.y;
            float s = t*2.;
            
            float v = (n( vec3(y*.01 +s, 			1., 1.0) ) + .0)
                    *(n( vec3(y*.011+1000.0+s, 	1., 1.0) ) + .0) 
                    *(n( vec3(y*.51+421.0+s, 	1., 1.0) ) + .0)   
                ;
            //v*= n( vec3( (fragCoord.xy + vec2(s,0.))*100.,1.0) );
            v*= hash42(   vec2(p.x +t*0.01, p.y) ).x +.3 ;

            
            v = pow(v+.3, 1.);
            if(v<.7) v = 0.;  //threshold
            return v;
        }
    """, fragment_200="""
        vec2 uv = v_tex_coord.xy;
        uv.x -= sin(uv.y * 500.0 + u_time) * INTERLACING_SEVERITY;

        vec4 buffer = vec4(0.0);

        if (texture2D(tex0, uv).a > 0.0) {
            buffer.b = texture2D(tex0, uv).b;

            float sum = 0.0;

            for (float i = 1.0; i <= 1.0; i++) {
                float weight = cos(1.0 - (i / 3.0));
                vec2 offset = vec2(i / res0.x, 0.0);
                buffer.r += texture2D(tex0, uv + offset).r * weight;
                buffer.g += texture2D(tex0, uv - offset).g * weight;
                sum += weight;
            }

            buffer.rg /= sum;

            buffer.a = GET_LUMA(texture2D(tex0, uv).rgb);
            float luma = GET_LUMA(texture2D(tex0, uv, 2.5).rgb);

            buffer.rgb = buffer.rgb - luma;
            buffer.rgb = buffer.rgb + buffer.a;
            buffer.rgb = lerp3(16.0 / 255.0, 235.0 / 255.0, buffer.rgb);
            buffer.a = texture2D(tex0, uv).a;

            // buffer.rgb *= vignette(uv, 0.95, 0.1) * buffer.a;

            vec2 uv2 = fract(uv * fract(sin(u_time * 10.0)));
            float strength = clamp(u_random.x, 0.125, 0.130);
            vec3 colour = vec3(rand(uv2.xy)) * strength;
            buffer.rgb += colour;

            float linesN = 240.; //fields per seconds
            float one_y = res0.y / linesN; //field line
            uv = floor(uv * res0.xy / one_y) * one_y;

            float col =  nn(uv, u_time);
            buffer.rgb += col * 0.1;
        } else {
            buffer = texture2D(tex0, uv);
        }

        gl_FragColor = buffer;
    """)

    renpy.register_shader("dsotn.chroma", variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform vec2 res0;
        uniform float u_time;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec4 u_random;
    """, vertex_300="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions="""
        #define color_resX 1.0
        #define bias 30.0

        vec3 rgb2yuv(vec3 rgb)
        {
            return vec3(0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b,
                        -0.147 * rgb.r - 0.289 * rgb.g + 0.436 * rgb.b,
                        0.615 * rgb.r - 0.515 * rgb.g - 0.100 * rgb.b);
        }

        vec3 yuv2rgb(vec3 yuv)
        {
            return vec3(yuv.r + 1.140 * yuv.b, yuv.r - 0.395*yuv.g - 0.581*yuv.b, yuv.r + 2.032*yuv.g);
        }
    """, fragment_300="""
        int color_res = int((sin(u_time + (v_tex_coord.y * res0.y) / 10.0) + 1.1) * color_resX + bias);
        // Normalized pixel coordinates (from 0 to 1)
        
        vec4 sampled = texture2D(tex0, v_tex_coord);

        float Y = 0.299 * sampled.r + 0.587 * sampled.g + 0.114 * sampled.b;
        
        vec2 colorData = vec2(0.0 , 0.0);
        int samples = 10;
        for (int i = 0; i < int(color_res); i++)
        {
            if (int((v_tex_coord.x * res0.x)) - i > 0)
            {
                vec2 uv2 = vec2((v_tex_coord.x * res0.x) - float(i), (v_tex_coord.y * res0.y)) / res0.xy;
                vec3 sampled = rgb2yuv(vec3(texture2D(tex0, uv2)));
                if (length(sampled.gb) > 0.02)
                {
                    colorData += sampled.gb;
                    samples++;
                }

            }
        }
        colorData = sin(colorData / float(samples) * 1.2);
                
        vec3 rgb = yuv2rgb(vec3(Y, colorData.x, colorData.y));
        gl_FragColor = vec4(rgb,1.0);
    """)

transform old_tv:
    mesh True
    shader [ "dsotn.vhs" ]
    pause 0.0
    repeat