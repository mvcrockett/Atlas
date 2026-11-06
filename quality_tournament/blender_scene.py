"""Original benchmark character: stylized lavender-jacket woman, waving one hand.
Actual Blender EEVEE scene; 40 frames at 8fps; CPU-only GitHub runner.
"""
import bpy,math
from mathutils import Vector
from pathlib import Path
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE" if bpy.app.version<(4,2,0) else "BLENDER_EEVEE_NEXT"
scene.render.resolution_x=480;scene.render.resolution_y=270;scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG";scene.render.film_transparent=False
scene.world.color=(0.09,0.10,0.19)
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 n=m.node_tree.nodes;n.clear();o=n.new("ShaderNodeOutputMaterial");e=n.new("ShaderNodeEmission");e.inputs["Color"].default_value=(*color,1);m.node_tree.links.new(e.outputs[0],o.inputs["Surface"]);return m
skin=mat("warm skin",(0.89,0.62,0.54));hair=mat("dark plum hair",(0.15,0.08,0.21));coat=mat("lavender jacket",(0.52,0.37,0.78));eyes=mat("deep brown eyes",(0.08,0.05,0.12))
def sphere(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=loc);obj=bpy.context.object;obj.name=name;obj.scale=scale;obj.data.materials.append(material);return obj
def segment(name,start,end,radius,material):
 a,b=Vector(start),Vector(end);mid=(a+b)*.5
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=radius,depth=(b-a).length,location=mid)
 obj=bpy.context.object;obj.name=name;obj.rotation_euler=(b-a).to_track_quat("Z","Y").to_euler();obj.data.materials.append(material)
 return obj
sphere("head",(0,0,1.75),(.43,.25,.50),skin)
sphere("hair cap",(0,.07,2.07),(.47,.29,.28),hair)
sphere("torso",(0,0,.75),(.58,.28,.86),coat)
sphere("left eye",(-.17,-.248,1.80),(.045,.025,.07),eyes)
sphere("right eye",(.17,-.248,1.80),(.045,.025,.07),eyes)
segment("resting arm",(-.53,0,1.32),(-.72,0,.50),.14,skin)
# animated separate upper arm and forearm, use geometry parenting to pivot empties
bpy.ops.object.empty_add(location=(.50,0,1.28));shoulder=bpy.context.object;shoulder.name="right shoulder pivot"
upper=segment("upper arm",(.50,0,1.28),(.94,0,1.43),.145,skin)
upper.parent=shoulder;upper.matrix_parent_inverse=shoulder.matrix_world.inverted()
bpy.ops.object.empty_add(location=(.94,0,1.43));elbow=bpy.context.object;elbow.name="right elbow pivot";elbow.parent=shoulder;elbow.matrix_parent_inverse=shoulder.matrix_world.inverted()
forearm=segment("forearm",(.94,0,1.43),(1.04,0,2.05),.115,skin)
forearm.parent=elbow;forearm.matrix_parent_inverse=elbow.matrix_world.inverted()
hand=sphere("palm",(1.04,0,2.13),(.13,.10,.19),skin)
hand.parent=elbow;hand.matrix_parent_inverse=elbow.matrix_world.inverted()
for f in range(1,41):
 t=(f-1)/39
 shoulder.rotation_euler[1]=0
 shoulder.rotation_euler[0]=0
 shoulder.rotation_euler[2]=.15*math.sin(t*math.pi*2)
 elbow.rotation_euler[1]=.12*math.sin(t*math.pi*4)
 shoulder.keyframe_insert(data_path="rotation_euler",frame=f)
 elbow.keyframe_insert(data_path="rotation_euler",frame=f)
bpy.ops.object.camera_add(location=(0,-7,2));cam=bpy.context.object
direction=Vector((0,0,1.2))-cam.location;cam.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()
cam.data.type="ORTHO";cam.data.ortho_scale=4.9;scene.camera=cam
scene.render.image_settings.color_mode="RGB"
scene.render.film_transparent=False
folder=Path("output/quality_tournament/blender_frames");folder.mkdir(parents=True,exist_ok=True)
for i in range(40):
 scene.frame_set(i+1)
 scene.render.filepath=str(folder/f"frame_{i:04d}.png")
 bpy.ops.render.render(write_still=True)
print("RENDERED 40 ACTUAL BLENDER FRAMES")
