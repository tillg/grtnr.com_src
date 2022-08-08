---
layout: post
title: Named volumes with docker-compose
slug: named-volumes-with-docker-compose
date_published: 2021-09-04T12:51:55.000Z
date_updated: 2021-09-04T19:24:42.000Z
tags: Tech
excerpt: How to create a volume within docker-compose, used by many containers and within a specific location on the host.
---

While working on a side project that uses **docker-compose**, I stumbled over a problem. One that I had encountered before but had never properly investigated or solved.

Here is what I want to do:

- Have a bunch of services running within a docker-compose setup
- Have those services use mounted shares - one share, used by more than one container.
- The problematic thing: I want **multiple containers** to use the **same volume**!

Make a long story short, here is how it works smoothly:

    version: '3'
    services:
      service1:
        image: nginx
        container_name: service1
        ports:
          - '81:80'
        volumes:
          - content:/usr/share/nginx/html
    
      service2:
        image: nginx
        container_name: service2
        ports:
          - '82:80'
        volumes:
          - content:/usr/share/nginx/html
    
    volumes:
      content:
         driver_opts:
               type: none
               device: ./data/content 
               o: bind

That's what's going on:

- We have 2 services of the same type: plain nginx containers for demo purposes.
- They both expose their (internal) port 80 to port 81 resp. 82 to the outside world.
- They both use a volume called **content** that is defined in the volumes section. 

The detail that I missed for so long was the **volumes** section with the **driver_opts**. And while I ran a couple of tests and everything behaved exactly the way I hoped, I couldn't find any proper documentation. Here's what the [docker documentation](https://docs.docker.com/compose/compose-file/compose-file-v3/#driver_opts) says about **driver_opts**:

> Specify a list of options as key-value pairs to pass to the driver for this volume. Those options are driver-dependent - consult the driver’s documentation for more information.

When investigating how things are working, docker's inspect tools give some insights: This is the **Mounts** part of **docker inspect service1**

     "Mounts": [
                {
                    "Type": "volume",
                    "Name": "docker-playground_content",
                    "Source": "/var/lib/docker/volumes/docker-playground_content/_data",
                    "Destination": "/usr/share/nginx/html",
                    "Driver": "local",
                    "Mode": "rw",
                    "RW": true,
                    "Propagation": ""
                }
            ]
     

At first I was sceptic because of this line:

    "Source": "/var/lib/docker/volumes/docker-playground_content/_data"

But it turns out my data is **not** in this docker-managed directory, but where I wanted it. In my case that's in** ./data/content**. Also the relative path works fine.

### Sources

Here are the original sources that helped me most

- Docker documentation - strange enough, it dodn't help at all...
- This was the most helpful [Stackoverflow article](https://stackoverflow.com/questions/35841241/docker-compose-named-mounted-volume).

### Versions

Since these kind of setups might be version sensitive, here is my setup:

    docker-compose version 1.29.2, build 5becea4c
    docker-py version: 5.0.0
    CPython version: 3.9.0
    OpenSSL version: OpenSSL 1.1.1h  22 Sep 2020

And it runs on my Mac with Big Sur Version 11.5.2 (wit h Intel CPU 😜).

The code can be found [on Github](https://github.com/tillg/docker-compose-volumes-playground/).
