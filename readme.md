# My Game Upscaler Scripts

A collection of my scripts, notes, for game upscaling.
Ideally as I play games, I'd like to use AI scaling on the fly.

Two possible approaches
- single powerful gaming pc doing all the dumping, ai upscaling, and texture reloading.
- offloading ai upscaling to the cloud or another pc on the network
  - i'm probably not going to do.

**ideally you need to figure out how to install python yourself and run things via commandline**

# What is this ?
This repo is a place for my personal scripts and notes available to fellow modders to look at.

**This is just a fun time project during my off hours. I'm a student part-time with a part-time job. So I'm not planning on being very community active like using issues or doing pr's. if you want something just fork this repo, and do whatever you want.**

# Why ?

I was originally using https://github.com/WalkerMx/AutoCrispy to upscale some games as I played them.
- you should definitely check out https://github.com/WalkerMx/AutoCrispy/blob/master/GUIDES.md for tips on hot reloading textures in different emulators.

However I ran into some issues with upscaling and playing Devil Summoner 2, it had a lot of junk textures(?). Since I wanted the texture to generate as fast as possible since I was playing the game, I needed a way to filter out textures which AutoCrispy didnt' let me do. I imagine you'll have to write custom code per game to do easy filtering.

So I decided to write my own scripts.