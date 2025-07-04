---
date: 2025-03-14
image: pools.png
excerpt: Me encantaría construir un pequeño sitio web que optimice mis horarios de natación en las piscinas públicas de Múnich.
Translation: es
Source-Language: en
Translator: gpt-4
Translate-Date: 2025-07-04T17:04:04.535105
Source-File: /Users/tgartner/git/grtnr.com_src/content/articles/2025-03-14-optimal-swimming-slot/2025-03-14-optimal-swimming-slot.md
Generated-By: automatic-translation-plugin
---

![Piscinas](pools.png)

Como la mayoría de vosotros probablemente sabéis, vivo en [Múnich/Alemania](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). Y desde que vivimos en Vietnam me he aficionado a la natación - quizás no realmente enganchado, pero me gusta. Aprendí a nadar a crol más de 1 km en el mar en Vietnam, y de vez en cuando trabajo en mantener viva esta habilidad aquí en Múnich.

El problema es que, en Múnich necesitas una piscina pública (porque no tengo una privada 😉), y las piscinas públicas tienden a estar llenas y abarrotadas. Afortunadamente, los SWM (los servicios públicos de Múnich) proporcionan un [sitio web](https://www.swm.de/baeder/auslastung) que nos informa de cuán ocupadas están las diferentes piscinas públicas.

Aunque trabajo 40 horas/semana (o algo así...), podría tener cierta flexibilidad en cuanto a cuándo voy a nadar: antes del trabajo, después del trabajo, tal vez incluso a la hora del almuerzo. Y surge la pregunta, cuándo es el mejor momento para ir. ¿Cuándo están las piscinas menos concurridas?

Por ejemplo: sospecho que ir lo más temprano posible por la mañana no es lo más inteligente, ya que muchos trabajadores de oficina deportistas lo hacen. Así que tal vez sea más inteligente tomar té con mi esposa por la mañana, y luego ir a nadar y a la oficina.

Lo mejor de este problema: es un problema típico de aprendizaje automático 😉

Entonces este sería el plan:

- Construir un raspador que recopile la ocupación de la piscina cada 10 minutos y la almacene en algún lugar
- Entrenar un modelo de aprendizaje automático con esos datos
- Construir una interfaz de usuario que pregunte cuándo podrías ir, y que te aconseje cuándo deberías ir
- Características adicionales: tener en cuenta los fines de semana y los días festivos, características de la piscina (es decir, prefiero nadar en una piscina de 50m)

¿Alguien se anima a construir tal herramienta? Envíame un correo electrónico si quieres hackear 😉