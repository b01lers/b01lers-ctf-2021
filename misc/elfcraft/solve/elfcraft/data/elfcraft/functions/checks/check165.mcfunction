scoreboard players set @a localChecks 0

execute as @a[scores={search=1}] if block ~0 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~991 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~991 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~0 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~1 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~2 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~5 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~4 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~6 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~991 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~991 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~8 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~9 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~10 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~13 ~-1 ~990 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~991 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~13 ~-1 ~991 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~13 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~992 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~993 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~12 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~13 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1
execute as @a[scores={search=1}] if block ~14 ~-1 ~994 minecraft:white_concrete run scoreboard players add @a localChecks 1

execute as @a[scores={search=1}] if score @s localChecks matches 41 run scoreboard players add @s checksPassed 1