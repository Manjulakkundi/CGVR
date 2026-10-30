// EXPERIMENT 8 - Basic Vertex and Fragment Shader (Unity, Built-in pipeline)
//
// Pipeline:  mesh vertices -> VERTEX shader (position) -> rasterizer -> FRAGMENT shader (color) -> pixels
//
// The vertex shader builds 4x4 homogeneous matrices (Scale, Rotation, Translation)
// and applies  M = T * R * S  to every vertex, exactly like Experiments 4 and 10.
Shader "Lab/Exp8_VertexFragment"
{
    Properties
    {
        _Color     ("Tint Color", Color) = (1, 1, 1, 1)
        _Angle     ("Rotation Angle (degrees)", Float) = 0
        _Scale     ("Uniform Scale", Float) = 1
        _Translate ("Translate (x, y)", Vector) = (0, 0, 0, 0)
        _Animate   ("Animate rotation (0/1)", Float) = 1
    }

    SubShader
    {
        Tags { "RenderType" = "Opaque" }

        Pass
        {
            Cull Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            fixed4 _Color;
            float  _Angle;
            float  _Scale;
            float4 _Translate;
            float  _Animate;

            // data coming from the mesh, per vertex
            struct appdata
            {
                float4 vertex : POSITION;
                fixed4 color  : COLOR;
            };

            // data passed from the vertex shader to the fragment shader
            struct v2f
            {
                float4 pos   : SV_POSITION;
                fixed4 color : COLOR0;
            };

            // ---------------- VERTEX SHADER: runs once per vertex ----------------
            v2f vert (appdata v)
            {
                v2f o;

                float a = radians(_Angle + _Animate * _Time.y * 60.0);
                float c = cos(a);
                float s = sin(a);

                // Scaling matrix S
                float4x4 S = float4x4(
                    _Scale, 0,      0, 0,
                    0,      _Scale, 0, 0,
                    0,      0,      1, 0,
                    0,      0,      0, 1);

                // Rotation matrix R (about Z axis, counter-clockwise)
                float4x4 R = float4x4(
                    c, -s, 0, 0,
                    s,  c, 0, 0,
                    0,  0, 1, 0,
                    0,  0, 0, 1);

                // Translation matrix T
                float4x4 T = float4x4(
                    1, 0, 0, _Translate.x,
                    0, 1, 0, _Translate.y,
                    0, 0, 1, 0,
                    0, 0, 0, 1);

                // Composite matrix: scale first, then rotate, then translate
                float4x4 M = mul(T, mul(R, S));

                float4 transformed = mul(M, v.vertex);   // homogeneous coords (x, y, z, 1)

                o.pos   = UnityObjectToClipPos(transformed);  // model -> view -> projection
                o.color = v.color;
                return o;
            }

            // ---------------- FRAGMENT SHADER: runs once per pixel ----------------
            fixed4 frag (v2f i) : SV_Target
            {
                // vertex colors are interpolated across the triangle by the rasterizer
                return i.color * _Color;
            }
            ENDCG
        }
    }
}
