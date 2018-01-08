#!/usr/bin/env python3
#this file was added by expertmm and based on pointrenderer.py
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Mesh, RenderContext
from random import random
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
import cProfile
from kivy.graphics.opengl import glEnable
from kivy.clock import Clock

class PointRendererOp:
    vertices = None
    indices = None

class PointRenderer(Widget):

    def __init__(self, **kwargs):
        self.this_op = None
        self.units_per_meter = 16.0
        self.gravity = 9.8
        self.fps = 60.0
        self.vertex_format = [
                              (b'vPosition', 3, 'float'),
                              (b'vSize', 1, 'float'),
                              (b'vRotation', 1, 'float'),
                              (b'vVelocity', 3, 'float'),
                             ]
        self.ROTATION_I = 4  # must match index of vRotation above
        self.VELOCITY_I = 5  # must match index of vVelocity above
        self.vertex_depth = 0
        for element in self.vertex_format:
            self.vertex_depth += element[1]
        self.star_list = []
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'pointshader3d.glsl'
        glEnable(0x8642) #GL_VERTEX_PROGRAM_POINT_SIZE
        glEnable(0x8861) #GL_POINT_SPRITE
        self.mesh = None
        super(PointRenderer, self).__init__(**kwargs)
        self.canvas["camera_eyespace_z"] = self.width / 2.0
        self.canvas["max_particle_size"] = self.width
        self.draw_mesh_points(60)
        #Clock.schedule_interval(self.test_mesh_remove, 1./60.)
        Clock.schedule_interval(self.test_mesh_move, 1./self.fps)

    def test_mesh_move(self, dt):
        this_star_list = self.star_list
        offset = 0
        #sl_len = len(this_star_list)
        #vertex_count = int(sl_len/self.vertex_depth)
        #v_i = 0
        v_len = len(self.this_op.vertices)
        while offset < v_len:
            if self.this_op.vertices[offset+1] > 0.0:
                self.this_op.vertices[offset] += self.this_op.vertices[offset+self.VELOCITY_I]
                self.this_op.vertices[offset+1] += self.this_op.vertices[offset+self.VELOCITY_I+1]  # +1 for y
                self.this_op.vertices[offset+2] += self.this_op.vertices[offset+self.VELOCITY_I+2]  # +2 for z
                if self.this_op.vertices[offset+1] < 0.0:
                    self.this_op.vertices[offset+1] = 0.0
                self.this_op.vertices[offset+self.VELOCITY_I+1] -= (self.gravity / self.units_per_meter) / self.fps  # +1 for y
                self.this_op.vertices[offset+self.ROTATION_I] += self.this_op.vertices[offset+self.VELOCITY_I+2] * 2  # +2 for z (spin according to speed and direction of z velocity)
            else:
                self.this_op.vertices[offset+self.VELOCITY_I] = 0.0
                self.this_op.vertices[offset+self.VELOCITY_I+1] = 0.0
                self.this_op.vertices[offset+self.VELOCITY_I+2] = 0.0
            offset += self.vertex_depth
        self.draw_mesh(None)

    def test_mesh_remove(self, dt):
        r = random()
        if r > .5:
            self.canvas.remove(self.mesh)
            self.mesh = None
        self.draw_mesh_points(60)

    def draw_mesh_points(self, number):
        self.star_list = []
        w, h = self.size
        sa = self.star_list.append
        for number in range(number):
            rand_x = random()*w
            rand_y = random()*h
            rand_z = random()*w
            rand_velocity = [random()*10.-5., random()*5.-2.5, random()*20.-5.]
            size = 29.0
            rotation = random()*360.0
            this_v = (rand_x, rand_y, rand_z, size, rotation, rand_velocity[0], rand_velocity[1], rand_velocity[2])
            if len(this_v) != self.vertex_depth:
                print("FATAL ERROR: tuple size does not match vertex depth (offset)")
                exit(1)
            sa(this_v)
        self.draw_mesh(self.star_list)

    def draw_mesh(self, this_star_list):
        if self.this_op is None:
            self.this_op = PointRendererOp()
            star_tex = Image('star1.png').texture
            self.this_op.indices = []
            ia = self.this_op.indices.append
            for star_number in range(len(this_star_list)):
                ia(star_number)
            self.this_op.vertices = []
            e = self.this_op.vertices.extend
            for star in this_star_list:
                this_star = [ star[0], star[1], star[2], star[3], \
                              star[4], star[5], star[6], star[7] ]
                if len(this_star) != self.vertex_depth:
                    print("FATAL ERROR: array size does not match " + \
                          "vertex depth (offset)")
                    exit(1)
                e(this_star)
        if self.mesh == None:
            with self.canvas:
                PushMatrix()
                self.mesh = Mesh(
                    indices=self.this_op.indices,
                    vertices=self.this_op.vertices,
                    fmt=self.vertex_format,
                    mode='points',
                    texture=star_tex)
                PopMatrix()
        else:
            #self.mesh.indices = self.this_op.indices
            self.mesh.vertices = self.this_op.vertices
            pass


class PointShaderApp(App):

    def build(self):
        root = FloatLayout()
        mq = PointRenderer(size=(800, 800))
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    PointShaderApp().run()
    #cProfile.run('PointShaderApp().run()', 'point_prof')
