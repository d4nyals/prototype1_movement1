# prototypes
The first prototype for my Computer Science Coursework, focusing on the movement of the player, generating the player, generating structures


START
↓
Player presses shoot key?
↓
YES → Create bullet at player position
        **↓**

        **Set bullet direction**

        **↓**

        **Add bullet to bullet list**

↓
FOR each bullet in bullet list
↓
Move bullet
↓
Bullet hit zombie?
├─ YES → Remove bullet
│        Reduce zombie health
│        Zombie dead?
│           ├─ YES → Remove zombie
│           └─ NO → Continue
↓
Bullet off screen?
├─ YES → Remove bullet
└─ NO → Keep bullet
↓
REPEAT every frame
