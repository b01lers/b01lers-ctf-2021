scoreboard players set @a localChecks 0

execute as @a[scores={search=1}] if block ~0 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~241 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~241 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~243 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~243 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~5 ~-1 ~243 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~241 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~243 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~240 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~241 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~241 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~13 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~242 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~243 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~244 minecraft:white_concrete run scoreboard players add @a localChecks 1

execute as @a[scores={search=1}] if score @s localChecks matches 37 run scoreboard players add @s checksPassed 1