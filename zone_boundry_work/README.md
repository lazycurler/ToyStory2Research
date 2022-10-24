Hello everyone! 

As you may know, I've been helping @Andet look into the boss warp seen after going out-of-bounds on Al's Space Land. What you may not know is I also really enjoyed long winded write-ups about my research findings. :wink: If the technical details behind why this glitch happens interest you, I encourage you to read about the interesting things we've found. If you're more interested in the speedrunning applications or just want a quick overview, check out the key takeaways at the bottom.

Note: In order to cut down on both the length of this write-up and to avoid misrepresenting the intent or actual behavior of `updateBuzzZone()` some details of the function have been left purposely vague. If the specifics are of interest to you, or the community at large, I would be happy to share (more of) my thoughts, decompiled code, and/or tools for generating graphs.

# Buzz's Zone Control Flow
Zones, for the sake of this write-up, are the current area of a level that Buzz (or another object) is in. Every iteration of what is suspected to be the main loop, the camera's zone is first updated based on its current position using a generic position->zone function referred to as: `getZoneFromPos()`. Buzz's zone is then updated to match the camera's zone. In a later function, assuming Buzz's zone is not `-1` and the current level is not `2`, Buzz's zone is updated a second time at `0x004402d6` using a different function referred to as: `updateBuzzZone()`. It is this update that has the potential to cause a Boss warp on Al's Space Land.

The function known as `updateBuzzZone()` is not for the faint of heart. Upon first entry, it appears a labyrinth of obscure calculations entangled in a jungle of nested `if`s and function calls. Thankfully, looks can be deceiving. :wink: While many of the specifics of the function are not yet fully understood, the intent of the function is clear: Update Buzz's zone using his current zone, current position, and previous position. Furthermore, the need to understand the intricate details of the function can be somewhat mitigated via empirical study.

# Zones and Boundaries
In order to address some of the more complicated parts of `updateBuzzZone()` the concept of zone boundaries must be introduced. Boundaries (also known as Area Portals?) mark the area where one zone transitions into another. Essentially, invisible walls that if crossed result in Buzz being in a new zone. Any level that has more than one zone will have at least one boundary, likely two*. Given this write-up's focus on the boss warp on Al's Space Land, ASL will be used as an example. The below image shows the approximate location of each of the seven zones in ASL with white lines marking the boundaries between the zones.
![spaceLand](https://i.imgur.com/iMT2aCx.png)
*Note: while the image only depicts 8 zone boundaries, there are in actuality 16. It is suspected each zone has its own zone boundary that provides directionality and hysteresis when Buzz is near/transiting from one zone to another.

Internally, the boundaries associated with each zone are stored in an array/lookup table referred to as: `adjacentZoneLUT`. The `adjacentZoneLUT` is composed of multiple entries each with a Zone ID (denoting which zone this boundary borders) and an index/offset that can be used to retrieve more information about a given boundary. The offset can be used to index into a secondary lookup table referred to as: `boundaryLUT`. The `boundaryLUT` contains the pointer needed to access the `0x20 Bytes` used to describe a boundary referred to as a: `BoundaryInfo_t` object. Not every field of the `BoundaryInfo_t` object is known, but the ones relevant to `updateBuzzZone()` have been identified. It appears each `BoundaryInfo_t` entry shares the same first two bytes, the following 8 entries appear to be `Vec3<int16_t>` in the order `Z, Y, X` (in theory another coordinate system/order could be chosen but that's outside the scope of this write-up). The final 6 bytes` purpose are unknown. The first (0th) vec corresponds to the bottom left hand corner of a quad, the second seems to be used as a scalar (more on that later). [3, 5, 7] are all unknown and [2, 4, 6] are the upper left, upper right, and bottom right of the quad respectively.
![lookupTables](https://i.imgur.com/mqoz5hA.png)

Graphing and connecting the coordinates of each of the boundaries for a given level provides a good visual representation of the boundaries.
![boundaries](https://i.imgur.com/Z6Wu02S.gif)

Here the same graph is shown but with the scalar included. A correlation between the relative `X` position of the boundary and the magnitude of the scalar's `Y` can be observed.
![withScalars](https://i.imgur.com/Oj8BneO.gif)

# `updateBuzzZone()`: At a Glance
The heart of the function is a `do...while` that iterates through each boundary associated with Buzz's current zone. The `while` loop terminates when it has reached the end of this list (denoted by a `LUT Index/Offset` of `0xff`. The loop consists of a series of increasingly complex checks that verify if Buzz has crossed a boundary and has entered a new zone. The checks are as follows:
1. The current zone's number is not `0xf` OR an unknown level specific(?) flag at `0x005d2a90` is `0` (this is the case for ASL)
2. Buzz's current position relative to the boundary is calculated (and verifies he is behind it??)
3. Buzz's _previous_ position relative to the boundary is calculated (and verifies he is in front of it??)
4. A function referred to as `isInBoundaryRange()` is called (to verify Buzz is within range of the boundary??)
5. If the previous function call returned `false` it is called again with different corners of the boundary passed in
6. If one of the calls to `isInBoundaryRange()` is true `buzzZone` is updated to the evaluated zone
Again, this is a very rough overview of the function in question with many details left out. Please feel free to ask questions or otherwise reach out if you are curious.

# Mechanics of the Boss Warp
Having established what zones and boundaries are and roughly how `updateBuzzZone()` works, it is now finally possible to explain _why_ a warp to the boss on ASL happens. It has been previously discovered that the series of checks starting at `0x0042426c` are responsible for determining when the boss fight on ASL should happen. Since the first two conditions (Buzz is standing and Buzz's current `Y` position < `-162431`) are met at spawn, the only condition left to meet is `buzzZone == 5`. At level load, Buzz's current location is set to the spawn point of the level. In the case of ASL, the spawn location is `(315274,  61,  -4082) in (x, y, z)`. Crucially, since `updateBuzzZone()` uses Buzz's previous position which is not updated until _after_ that function is called, the first call to the function after a new level loads uses Buzz's last known position from the last exited level. This gives the determined player control over the zone on the first tick of the new level. It is through these means the zone can temporarily be set to `5`, fulfilling the final condition needed to trigger the boss fight, and warping Buzz to the location.

# Exploitation?
This begs the question: What previous location(s) can cause Buzz to be moved to zone `5`? One could spend tens of hours reverse engineering the code in `updateBuzzZone()` and `isInBoundaryRange()` functions _or_ they could rewrite the underlying code in Python and explore the state-space with brute force. :sunglasses: To that end, below is a visual approximation of a subset of valid previous Buzz locations that will result in a boss warp on ASL. The resulting graph reveals a series of concentric spheres/shells of valid locations. Further below, a graph with `X` and `Z` fixed at `0` provides a 1D projection of the spheres.
![spheres](https://i.imgur.com/LTsMoiA.png)
![x0z0](https://i.imgur.com/B5uY3b6.png)

Given the magnitude of the distance from the origin required to trigger a boss warp (on the order of `6e6` or ~6,000,000 units minimum) the only (known) viable way to achieve this distance is by going OOB. Unfortunately, the time required to fall this distance is ~50 seconds, much too long to be viable in a speedrun. In theory, this type of behavior could be exploitable on other levels, but a cursory search didn't reveal anything. The level would have to have an event that resulted in Buzz being forcibly moved to a new location where the only (remaining) condition required at spawn is a change in zone. Additionally, the zone would have to be adjacent to the spawn zone.

# Conclusion
If you made it this far, thanks for reading! While it's a bit of a bummer this doesn't have any interesting implications for speedruns at this time, I did enjoy falling down this deep rabbit hole. Perhaps while not useful to speedrunners, this information may prove useful for modding. As I mentioned before, if you have any questions please do not hesitate to reach out to me or @Andet. I plan to continue to work on various unanswered questions related to this game as they come up, so if you've seen something weird or would like something investigated just ping me! :smile:

# The Key Takeaways
- The Boss warp on ASL happens because Buzz's zone is (for a single tick) the same zone as the Boss (and the other conditions are already met)
- The observed boss warp behavior is dependent on Buzz's current and previous position
- Previous position when first entering a level is the position where the last level was left
- The specifics of the math used to determine the new zone are not fully understood but have been empirically studied and modeled
- The minimum position required for a warp on ASL starting at `X == 0` and `Z == 0` is `Y == ~6e6` or ~6,000,000
- While technically not directly caused by going out-of-bounds, going OOB is almost assuredly the only way to move Buzz to the perquisite position
- While it is possible to change Buzz's zone when entering other levels in the manner described above, it is not currently believed to be applicable anywhere else
- A warp can be tested by entering a level and using cheat engine to modify Buzz's current zone
- Probably not useful for speedruns :(

# Appendix
- `camZone` == `0x0054dea0`
- `buzzZone` == `0x005d2a8c`
- `getZoneFromPos()`  == `0x004885c0`
- `updateBuzzZone()` == `0x0043fef0`
- `adjecentZoneLUT` == `0x0054f39c`
- `boundaryLUT` == `0x00559c70`
- `isInBoundaryRange()` == `0x00480ae0`