# transform_loading.py
import arcade
from array import array
import math
import random
from arcade.gl import BufferDescription

class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        ctx = self.window.ctx

        self.points_program = ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_pos;
            out vec3 color;
            void main() {
                color = vec3(
                    mod(float(gl_VertexID*100 % 11) / 10.0, 1.0),
                    mod(float(gl_VertexID*100 % 27) / 10.0, 1.0),
                    mod(float(gl_VertexID*100 % 71) / 10.0, 1.0));
                gl_Position = vec4(in_pos, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            in vec3 color;
            out vec4 fragColor;
            void main() {
                fragColor = vec4(color, 1.0);
            }
            """
        )

        self.gravity_program = ctx.program(
            vertex_shader="""
            #version 330
            uniform float dt;
            uniform float force;
            uniform vec2 gravity_pos;
            in vec2 in_pos;
            in vec2 in_vel;
            out vec2 out_pos;
            out vec2 out_vel;
            void main() {
                vec2 dir = gravity_pos - in_pos;
                float dist = length(dir) + 0.001;
                dir = normalize(dir) * force;
                vec2 vel = in_vel + dir / dist * 0.01;
                out_vel = vel;
                out_pos = in_pos + vel * dt;
            }
            """
        )

        N = 20000
        self.buffer_1 = ctx.buffer(data=array("f", self._gen_points(N)))
        self.buffer_2 = ctx.buffer(reserve=self.buffer_1.size)

        self.vao_1 = ctx.geometry([BufferDescription(self.buffer_1, "2f 2x4", ["in_pos"])])
        self.vao_2 = ctx.geometry([BufferDescription(self.buffer_2, "2f 2x4", ["in_pos"])])
        self.gravity_1 = ctx.geometry([BufferDescription(self.buffer_1, "2f 2f", ["in_pos", "in_vel"])])
        self.gravity_2 = ctx.geometry([BufferDescription(self.buffer_2, "2f 2f", ["in_pos", "in_vel"])])

    def _gen_points(self, count):
        for _ in range(count):
            yield random.uniform(-1.2, 1.2)
            yield random.uniform(-1.2, 1.2)
            yield random.uniform(-0.3, 0.3)
            yield random.uniform(-0.3, 0.3)

    def on_draw(self):
        self.clear()
        self.window.ctx.point_size = 2 * self.window.get_pixel_ratio()
        self.gravity_program["dt"] = 1/60
        self.gravity_program["force"] = 0.25
        self.gravity_program["gravity_pos"] = (
            math.sin(self.window.time * 0.77) * 0.5,
            math.cos(self.window.time) * 0.5
        )

        self.gravity_1.transform(self.gravity_program, self.buffer_2)
        self.vao_2.render(self.points_program, mode=arcade.gl.POINTS)

        self.gravity_1, self.gravity_2 = self.gravity_2, self.gravity_1
        self.vao_1, self.vao_2 = self.vao_2, self.vao_1
        self.buffer_1, self.buffer_2 = self.buffer_2, self.buffer_1
