---
title: Playing with JavaScript
tags: tech
date: 2015-12-06
---

I've been playing around with HTML & JavaScript. And Geometry is just it ;)

Unfortunatly the script won't render here, nso I just show you the code:

```html
<div id="c" onload="Draw()"></div>

<script>
  var c = document.getElementById("c")
  var ctx = c.getContext("2d")
  var cw = (c.width = 600),
    cx = cw / 2
  var ch = (c.height = 600),
    cy = ch / 2
  var rad = Math.PI / 180
  var phi = 0

  ctx.lineWidth = 0.2
  ctx.strokeStyle = "black"
  var num_circles = 200
  var frames = 0
  var flag = false

  var I = 50
  var a = 3 * I
  var b = 1 * I

  var outer_rad = cy
  var nVert = 3
  var angle_incr = (360 / nVert) * rad

  function Draw() {
    if (frames >= 7) {
      flag = true
    } else if (frames <= 0) {
      flag = false
    }
    if (flag == false) {
      frames += 0.005
    } else {
      frames -= 0.005
    }

    phi += 0.01 * Math.cos(50 * frames * rad)
    var step = Math.abs(Math.cos(frames * rad)) + 0.005
    ctx.clearRect(0, 0, cw, ch)
    ctx.beginPath()
    for (var i = 0; i <= num_circles; i += step) {
      var ratio = i / num_circles
      var angle = i * angle_incr * Math.cos(frames * rad)
      var spiral_rad = ratio * outer_rad
      var r = spiral_rad / nVert

      var h = a * Math.sin(i * rad)
      var x = cx + (a - b) * Math.cos(angle) + h * Math.cos(phi + ((a - b) / b) * angle)
      var y = cy + (a - b) * Math.sin(angle) - h * Math.sin(phi + ((a - b) / b) * angle)

      ctx.arc(x, y, 1, 0, 2 * Math.PI)
      //ctx.lineTo(x, y);
    }
    ctx.stroke()
    requestId = window.requestAnimationFrame(Draw)
  }

  function start() {
    requestId = window.requestAnimationFrame(Draw)
    stopped = false
  }

  function stopAnim() {
    if (requestId) {
      window.cancelAnimationFrame(requestId)
    }
    stopped = true
  }

  window.addEventListener("load", start(), false)

  c.addEventListener(
    "click",
    function () {
      stopped == true ? start() : stopAnim()
    },
    false
  )
</script>
```
