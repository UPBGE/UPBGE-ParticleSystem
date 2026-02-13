bl_info = {
    "name": "UPBGE Particle System",
    "author": "Ghost DEV",
    "version": (0, 5, 0),
    "blender": (5, 0, 0),
    "location": "Properties > Physics Properties",
    "description": "Simple particle system for UPBGE using mesh instances (NO GPU)",
    "warning": "It is still an alpha version and it is not stable at all times",
    "wiki_url": "",
    "category": "Physics",
}

import bpy
from mathutils import Vector
import random

def update_game_prop(self, context):
    obj = context.object
    if not obj: return
    
    # Mapping between Addon props and Game props
    props_map = {
        'enabled': 'ps_enabled',
        'trigger_enabled': 'ps_trigger',
        'emission_mode': 'ps_emission_mode',
        'max_particles': 'ps_max_particles',
        'emission_rate': 'ps_emission_rate',
        'emission_delay': 'ps_emission_delay',
        'burst_count': 'ps_burst_count',
        'is_one_shot': 'ps_is_one_shot',
        'lifetime': 'ps_lifetime',
        'lifetime_random': 'ps_lifetime_random',
        'start_size': 'ps_start_size',
        'end_size': 'ps_end_size',
        'velocity_random': 'ps_velocity_random',
    }
    
    for addon_prop, game_prop in props_map.items():
        if game_prop in obj.game.properties:
            obj.game.properties[game_prop].value = getattr(self, addon_prop)

    # Vectors Handlers
    if 'ps_start_velocity_x' in obj.game.properties:
        obj.game.properties['ps_start_velocity_x'].value = self.start_velocity[0]
        obj.game.properties['ps_start_velocity_y'].value = self.start_velocity[1]
        obj.game.properties['ps_start_velocity_z'].value = self.start_velocity[2]

    if 'ps_gravity_x' in obj.game.properties:
        obj.game.properties['ps_gravity_x'].value = self.gravity[0]
        obj.game.properties['ps_gravity_y'].value = self.gravity[1]
        obj.game.properties['ps_gravity_z'].value = self.gravity[2]

    if 'ps_particle_mesh' in obj.game.properties:
        mesh_name = self.particle_mesh.name if self.particle_mesh else 'ParticleSphere'
        obj.game.properties['ps_particle_mesh'].value = mesh_name

# Particle System Properties
class ParticleSystemProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Enable Particles",
        description="Master switch for the system",
        default=False,
        update=update_game_prop
    )
    
    trigger_enabled: bpy.props.BoolProperty(
        name="Trigger",
        description="Control emission via Logic Bricks (True = Emit, False = Stop)",
        default=False,
        update=update_game_prop
    )
    
    emission_mode: bpy.props.EnumProperty(
        name="Emission Mode",
        items=[('CONTINUOUS', "Continuous", ""), ('BURST', "Burst", "")],
        default='CONTINUOUS',
        update=update_game_prop
    )
    
    max_particles: bpy.props.IntProperty(name="Max Particles", default=100, min=1, max=1000, update=update_game_prop)
    emission_rate: bpy.props.FloatProperty(name="Emission Rate", default=10.0, min=0.0, max=100.0, update=update_game_prop)
    
    # NEW: Delay for Burst Mode
    emission_delay: bpy.props.FloatProperty(name="Burst Delay", description="Time between bursts (seconds)", default=1.0, min=0.1, max=100.0, update=update_game_prop)
    
    burst_count: bpy.props.IntProperty(name="Burst Count", default=30, min=1, max=500, update=update_game_prop)
    is_one_shot: bpy.props.BoolProperty(name="One Shot", description="Fire once when triggered, reset when trigger stops", default=False, update=update_game_prop)
    
    lifetime: bpy.props.FloatProperty(name="Lifetime", default=3.0, min=0.1, max=100.0, update=update_game_prop)
    lifetime_random: bpy.props.FloatProperty(name="Random Lifetime", default=0.5, min=0.0, max=1.0, update=update_game_prop)
    start_size: bpy.props.FloatProperty(name="Start Size", default=0.1, min=0.001, max=10.0, update=update_game_prop)
    end_size: bpy.props.FloatProperty(name="End Size", default=0.05, min=0.001, max=10.0, update=update_game_prop)
    
    start_velocity: bpy.props.FloatVectorProperty(name="Start Velocity", default=(0.0, 0.0, 2.0), size=3, update=update_game_prop)
    velocity_random: bpy.props.FloatProperty(name="Random Velocity", default=0.5, min=0.0, max=7.0, update=update_game_prop)
    gravity: bpy.props.FloatVectorProperty(name="Gravity", default=(0.0, 0.0, -9.8), size=3, update=update_game_prop)
    
    particle_mesh: bpy.props.PointerProperty(name="Particle Mesh", type=bpy.types.Object, update=update_game_prop)


# Particle System Panel
class PARTICLE_PT_upbge_panel(bpy.types.Panel):
    bl_label = "UPBGE Particle System"
    bl_idname = "PARTICLE_PT_upbge_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        if obj is None: return
        
        box = layout.box()
        box.label(text="Setup:", icon='INFO')
        box.operator("particle.setup_logic", text="Initialize", icon='PLUS')
        
        layout.separator()
        ps = obj.particle_system_props
        
        layout.prop(ps, "enabled", text="Particle Emitter")
        
        if ps.enabled:
            box = layout.box()
            box.label(text="Emission:")
            
            box.prop(ps, "emission_mode", text="Mode")
            # MOVED DOWN: Trigger is now below Mode
            layout.prop(ps, "trigger_enabled", text="Emission Trigger")
            
            box.prop(ps, "max_particles")
            
            if ps.emission_mode == 'CONTINUOUS':
                box.prop(ps, "emission_rate")
            else: # BURST MODE
                box.prop(ps, "burst_count")
                box.prop(ps, "is_one_shot")
                # HIDE DELAY IF ONE SHOT IS ACTIVE
                if not ps.is_one_shot:
                    box.prop(ps, "emission_delay")
            
            box.prop(ps, "lifetime")
            box.prop(ps, "lifetime_random")
            
            box = layout.box()
            box.label(text="Appearance:")
            box.prop(ps, "start_size")
            box.prop(ps, "end_size")
            box.prop(ps, "particle_mesh")
            
            box = layout.box()
            box.label(text="Physics:")
            box.prop(ps, "start_velocity")
            box.prop(ps, "velocity_random")
            box.prop(ps, "gravity")

class PARTICLE_OT_setup_logic(bpy.types.Operator):
    """Setup logic brick and Initialize Game Properties"""
    bl_idname = "particle.setup_logic"
    bl_label = "Setup Particle System"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        
        # Camera Check
        if not scene.camera:
            for obj in scene.objects:
                if obj.type == 'CAMERA':
                    scene.camera = obj
                    break
        
        init_obj = context.active_object
        if not init_obj:
            self.report({'ERROR'}, "Please select an object first")
            return {'CANCELLED'}
        
        # Logic Bricks
        has_sensor = any(s.name == "ParticleInit" for s in init_obj.game.sensors)
        if not has_sensor:
            bpy.ops.logic.sensor_add(type='ALWAYS', name="ParticleInit", object=init_obj.name)
            init_obj.game.sensors[-1].name = "ParticleInit"
            init_obj.game.sensors[-1].use_pulse_true_level = False
            
        for ctrl in list(init_obj.game.controllers):
            if "Particle" in ctrl.name:
                init_obj.game.controllers.remove(ctrl)
        
        bpy.ops.logic.controller_add(type='PYTHON', name="ParticleController", object=init_obj.name)
        controller = init_obj.game.controllers[-1]
        controller.name = "ParticleController"
        controller.mode = 'SCRIPT'
        
        # Runtime Script with NEW LOGIC
        script_text = """# UPBGE Particle System Runtime v0.5.1

import bge
from bge import logic
from mathutils import Vector
import random

class Particle:
    def __init__(self, pos, vel, lifetime, size):
        self.position = Vector(pos)
        self.velocity = Vector(vel)
        self.age = 0.0
        self.lifetime = lifetime
        self.size = size
        self.obj = None

class ParticleSystem:
    def __init__(self, emitter_obj):
        self.emitter = emitter_obj
        self.particles = []
        self.time_since_emit = 0.0
        self.particle_template = None
        self.burst_triggered = False # Flag for One Shot
        self.props = {}
        self.load_properties()
        self.create_particle_template()
        
    def load_properties(self):
        obj = self.emitter
        self.props = {
            'enabled': obj.get('ps_enabled', True),
            'trigger': obj.get('ps_trigger', True),
            'emission_mode': obj.get('ps_emission_mode', 'CONTINUOUS'),
            'max_particles': obj.get('ps_max_particles', 100),
            'emission_rate': obj.get('ps_emission_rate', 10.0),
            'emission_delay': obj.get('ps_emission_delay', 1.0), # NEW
            'burst_count': obj.get('ps_burst_count', 30),
            'is_one_shot': obj.get('ps_is_one_shot', False),
            'lifetime': obj.get('ps_lifetime', 3.0),
            'lifetime_random': obj.get('ps_lifetime_random', 0.5),
            'start_size': obj.get('ps_start_size', 0.1),
            'end_size': obj.get('ps_end_size', 0.05),
            'start_velocity': (obj.get('ps_start_velocity_x', 0.0), obj.get('ps_start_velocity_y', 0.0), obj.get('ps_start_velocity_z', 2.0)),
            'velocity_random': obj.get('ps_velocity_random', 0.5),
            'gravity': (obj.get('ps_gravity_x', 0.0), obj.get('ps_gravity_y', 0.0), obj.get('ps_gravity_z', -9.8)),
            'particle_mesh': obj.get('ps_particle_mesh', 'ParticleSphere')
        }
        
    def create_particle_template(self):
        scene = logic.getCurrentScene()
        mesh_name = self.props.get('particle_mesh', 'ParticleSphere')
        if mesh_name in scene.objectsInactive:
            self.particle_template = scene.objectsInactive[mesh_name]
        else:
            print(f"Warning: Mesh {mesh_name} not found in inactive objects")
            
    def emit_particle(self):
        if not self.particle_template: return
        if len(self.particles) >= self.props['max_particles']:
            old_p = self.particles.pop(0)
            if old_p.obj: old_p.obj.endObject()
        
        base_vel = Vector(self.props['start_velocity'])
        random_offset = Vector(((random.random()-0.5)*2*self.props['velocity_random'], (random.random()-0.5)*2*self.props['velocity_random'], (random.random()-0.5)*2*self.props['velocity_random']))
        lifetime = self.props['lifetime'] * (1.0 + (random.random()-0.5) * self.props['lifetime_random'])
        
        particle = Particle(self.emitter.worldPosition.copy(), base_vel + random_offset, lifetime, self.props['start_size'])
        try:
            particle.obj = logic.getCurrentScene().addObject(self.particle_template, self.emitter, 0)
            particle.obj.worldPosition = particle.position
            particle.obj.worldScale = [particle.size] * 3
            self.particles.append(particle)
        except: pass
    
    def emit_burst(self):
        for _ in range(self.props['burst_count']): self.emit_particle()
        
    def update(self, dt):
        self.load_properties()
        
        # --- SPAWN LOGIC ---
        if self.props['enabled']:
            mode = self.props['emission_mode']
            trigger = self.props['trigger']
            
            if mode == 'CONTINUOUS':
                if trigger:
                    self.time_since_emit += dt
                    rate = self.props['emission_rate']
                    interval = 1.0 / rate if rate > 0 else float('inf')
                    while self.time_since_emit >= interval:
                        self.emit_particle()
                        self.time_since_emit -= interval
            
            elif mode == 'BURST':
                if self.props['is_one_shot']:
                    # One Shot Logic: Fire once on Rising Edge
                    if trigger and not self.burst_triggered:
                        self.emit_burst()
                        self.burst_triggered = True # Lock it
                    elif not trigger:
                        self.burst_triggered = False # Unlock/Reset when trigger stops
                else:
                    # Repeating Burst Logic (While Trigger is Held)
                    if trigger:
                        self.time_since_emit += dt
                        if self.time_since_emit >= self.props['emission_delay']:
                            self.emit_burst()
                            self.time_since_emit = 0.0
        
        # --- PHYSICS LOGIC ---
        grav = Vector(self.props['gravity'])
        to_remove = []
        for i, p in enumerate(self.particles):
            p.age += dt
            if p.age >= p.lifetime:
                to_remove.append(i)
                if p.obj: p.obj.endObject()
                continue
            p.velocity += grav * dt
            p.position += p.velocity * dt
            if p.obj:
                p.obj.worldPosition = p.position
                life_ratio = p.age / p.lifetime
                p.size = self.props['start_size'] + (self.props['end_size'] - self.props['start_size']) * life_ratio
                p.obj.worldScale = [p.size] * 3
        for i in reversed(to_remove): self.particles.pop(i)

class ParticleManager:
    def __init__(self):
        self.systems = {}
        self.last_time = 0.0
    def scan(self):
        scene = logic.getCurrentScene()
        for obj in scene.objects:
            if 'ps_enabled' in obj:
                if obj.name not in self.systems: self.systems[obj.name] = ParticleSystem(obj)
            elif obj.name in self.systems:
                for p in self.systems[obj.name].particles:
                    if p.obj: p.obj.endObject()
                del self.systems[obj.name]
    def update(self):
        cur = logic.getClockTime()
        dt = cur - self.last_time if self.last_time > 0 else 0.016
        self.last_time = cur
        dt = min(dt, 0.1)
        for sys in self.systems.values(): sys.update(dt)

def init():
    if not hasattr(logic, '_pm'):
        logic._pm = ParticleManager()
        logic.getCurrentScene().pre_draw.append(lambda c: logic._pm.update())
        logic._pm.scan()
init()
"""
        
        # Script Refresh Logic
        import time
        script_name = f"ParticleSys_Runtime_{int(time.time())}.py"
        for t in bpy.data.texts:
            if "ParticleSys_Runtime" in t.name: bpy.data.texts.remove(t)
            
        text_block = bpy.data.texts.new(script_name)
        text_block.write(script_text)
        controller.text = text_block
        
        sensor = next((s for s in init_obj.game.sensors if s.name == "ParticleInit"), None)
        if sensor: controller.link(sensor=sensor)
        
        # Property Creation
        def ensure_prop(name, type, value):
            if name not in init_obj.game.properties:
                bpy.ops.object.game_property_new(type=type, name=name)
            init_obj.game.properties[name].value = value

        props = init_obj.particle_system_props
        
        ensure_prop('ps_enabled', 'BOOL', props.enabled)
        ensure_prop('ps_trigger', 'BOOL', props.trigger_enabled)
        ensure_prop('ps_emission_mode', 'STRING', props.emission_mode)
        ensure_prop('ps_max_particles', 'INT', props.max_particles)
        ensure_prop('ps_emission_rate', 'FLOAT', props.emission_rate)
        ensure_prop('ps_emission_delay', 'FLOAT', props.emission_delay) # NEW
        ensure_prop('ps_burst_count', 'INT', props.burst_count)
        ensure_prop('ps_is_one_shot', 'BOOL', props.is_one_shot)
        ensure_prop('ps_lifetime', 'FLOAT', props.lifetime)
        ensure_prop('ps_lifetime_random', 'FLOAT', props.lifetime_random)
        ensure_prop('ps_start_size', 'FLOAT', props.start_size)
        ensure_prop('ps_end_size', 'FLOAT', props.end_size)
        ensure_prop('ps_velocity_random', 'FLOAT', props.velocity_random)
        
        ensure_prop('ps_start_velocity_x', 'FLOAT', props.start_velocity[0])
        ensure_prop('ps_start_velocity_y', 'FLOAT', props.start_velocity[1])
        ensure_prop('ps_start_velocity_z', 'FLOAT', props.start_velocity[2])
        ensure_prop('ps_gravity_x', 'FLOAT', props.gravity[0])
        ensure_prop('ps_gravity_y', 'FLOAT', props.gravity[1])
        ensure_prop('ps_gravity_z', 'FLOAT', props.gravity[2])
        
        mesh_name = props.particle_mesh.name if props.particle_mesh else 'ParticleSphere'
        ensure_prop('ps_particle_mesh', 'STRING', mesh_name)
        
        self.report({'INFO'}, "System Initialized!")
        return {'FINISHED'}

# Registration
classes = (
    ParticleSystemProperties,
    PARTICLE_PT_upbge_panel,
    PARTICLE_OT_setup_logic,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.particle_system_props = bpy.props.PointerProperty(type=ParticleSystemProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.particle_system_props

if __name__ == "__main__":
    register()
