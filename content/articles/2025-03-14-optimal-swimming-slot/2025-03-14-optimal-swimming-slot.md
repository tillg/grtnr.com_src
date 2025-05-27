---
date: 2025-03-14
image: pools.png
excerpt: I’d love to build a little website that optimizes my swimming slots in Munich’s public pools.
---

![Pools](pools.png)

As Most of u probably know I live in [Munich/Germany](https://maps.app.goo.gl/QXy56tXkBf6tJ2s98). And since we lived in Vietnam I got hooked on swimming - maybe not really hooked, but I enjoy it. I learned to freestyle for over 1 km in the sea in Vietnam, and from time to time I work on keeping alive this skill here in Munich.

The problem is, in Munich u need a public pool (because I don’t have a private one 😉), and public pools tend to be full & crowded. Luckily, the SWM (the Munich public services) provide a [website](https://www.swm.de/baeder/auslastung) that tells us how busy the different public swimming pools are.

Even thow I work 40 hours / week (or so…), I might have some flexibility as of when I go swimming: before work, after work, maybe even at lunchtime. And the question arises, when best to go. When are the pools the less crowded?

For example: I suspect that going as early as possible in the morning is not the smartest, as many sportive white-collar worker do so. So maybe it’s smarter to have tea with my wife in the morning, and then go for a swim and to the office.

The best about this problem: it’s a typical machine learning problem 😉

So this would be the plan:

- Build a scraper that gathers the pool occupancy every 10 minutes and stores it somewhere
- Train a machine learning model on that data
- Build a UI that asks when u could go, and that gives u advice when u should go
- Extra features: take into account week-ends and public holidays, pool-features (i.e. I prefer swimming in a 50m pool)

Anyone up for building such a tool? Send me an email if u want to hack 😉
