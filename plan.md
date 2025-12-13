# development plan

## mvp (minimum viable product)
- player auto-moves forward
- jump mechanic (space)
- scrolling level with basic obstacles (spikes, gaps)
- energy drink collectibles
- interference system with multiple levels (visual & gameplay effects)
- death and restart screen (r to restart, esc to quit)
- score based on distance and multiplier

## level system
- implement level data as arrays or simple files
- each level: unique obstacle patterns, collectible placement, and interference pacing
- level progression: unlock next level after completing previous
- endless mode: after last level, loop or generate infinite random sections

## infinite scrolling background
- create a seamless, looping background image or pattern
- background scrolls continuously to simulate infinite movement
- add parallax layers for depth (foreground, midground, background)
- background color and effects change with interference/apocalypse level

## custom backgrounds
- each level can have its own color palette and background style
- backgrounds react to interference (glitch, flicker, color shift)
- apocalypse events trigger special background effects (collapsing, static, distortion)

## stretch goals
- procedural level generation for endless replayability
- boss-style glitch events and unique level hazards
- local high score tracking and leaderboard
- multiple music tracks and audio effects that react to interference

## polish
- minimalist ui for score, multiplier, and interference level
- smooth transitions between levels and game states
- add tutorial or intro level
- optimize for performance and input responsiveness