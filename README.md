# UPBGE Particle System
It's an addon design for UPBGE 0.5+ to create particle effects for your game without doing it from scratch, and it create with help of AI
## Features
+ Integrated directly into **The physics properties** for easy access
+ Two emission modes **continuous** and **burst**
+ Customization settings to create wide style options
+ Any object mesh can be a particle, allowing for total creative freedom
+ Easy to setup particles on any object you want
+ Controlling the system with an emission trigger for smart use by toggle **ps_tigger** bool property

## Installation guide
1. Download the addon 
2. Go to **Edit** -> **preferences** -> **Add-on** -> **Add-on settings** -> **Install from disk**
3. Locate the zip <sub>Particle system</sub> file
4. Click on the checkbox to activate the Add-on

## Quick setup
1. Add empty
2. Go to physics
3. Enable the option "Particle Emitter."
4. Go to particle mesh and select any object you want
5. Hide the object by selecting it and pressing H or clicking on the eye in the outliner
6. Click on "Initialize"
7. Press P and enjoy!

> [!TIP]
You can control the particle spawning with *Logic Brick* or *Logic nodes* by using **ps_tigger** bool property

> [!WARNING]
The performance is not great since the Add-on uses CPU, but to deliver the best performance, follow these steps:
1. Select the object you want to use as a  particle
2. Go to **object properties** and enable ***UPBGE Dupli Base***
3. Change the physics properties to **No Collision** and uncheck **Sound Occluder**
4. If you want to use textures i highly recommend to use *DDS* format
5. The Add-on still does not use billboard for particle try using simple objects geometry or reduce the **Emission Rate**

## Discord Server
If you want to join the community, go to the Discord server https://discord.gg/842uWxchu7

## Report bugs
If you face any bug plaese report it in GitHub

Enjoy!
