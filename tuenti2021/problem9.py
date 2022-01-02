from collections import defaultdict
import sys
from typing import Iterator, Tuple
from typing import List


class Sprite(object):
    def __init__(self, shape: List[Tuple[int, int]], width: int, height: int):
        self.shape = shape
        self.width = width
        self.height = height


class GameObject(object):
    def __init__(self, id: int, x: int, y: int, sprite: Sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.id = id


def get_pair_collisions(ids: List[int]) -> List[Tuple[int, int]]:
    pairs = []
    for (i, sprite_id) in enumerate(ids):
        for j in range(i + 1, len(ids)):
            pairs.append((sprite_id, ids[j]))
    return pairs


class GameStatus(object):
    def __init__(self, objects: Iterator[GameObject]):
        game_map = defaultdict(list)
        for game_object in objects:
            for (x, y) in game_object.sprite.shape:
                game_map[hash("{}x{}".format(game_object.y + y, game_object.x + x))].append(game_object.id)
        keys_to_process = set()
        for collisions in game_map.values():
            if len(collisions) >= 2:
                collisions_key = ",".join([str(c) for c in collisions])
                keys_to_process.add(collisions_key)
        self.keys_to_process = keys_to_process

    def get_collisions(self):
        pairs_of_collided_sprites = set()
        for key in self.keys_to_process:
            collisions = key.split(",")
            for (obj1, obj2) in get_pair_collisions(collisions):
                pairs_of_collided_sprites.add("{},{}".format(obj1, obj2))
        return len(pairs_of_collided_sprites)


def parse_sprites() -> [Sprite]:
    n_sprites = int(sys.stdin.readline().strip())
    sprites = []
    for _ in range(n_sprites):
        width, height = [int(c) for c in sys.stdin.readline().strip().split(" ")]
        sprite = []
        for y in range(height):
            for x, value in enumerate([int(c) for c in sys.stdin.readline().strip()]):
                if value == 1:
                    sprite.append((x, y))
        sprites.append(Sprite(sprite, width, height))
    return sprites


def parse_game_status(sprites: List[Sprite]) -> GameStatus:
    n_objects = int(sys.stdin.readline().strip())
    objects = []
    for id in range(n_objects):
        (sprite_id, x, y) = [int(c) for c in sys.stdin.readline().strip().split(" ")]
        sprite = sprites[int(sprite_id)]
        objects.append(GameObject(id, x, y, sprite))
    return GameStatus(objects)


def solve():
    tests = int(sys.stdin.readline().strip())
    sprites = parse_sprites()
    for test in range(tests):
        game_status = parse_game_status(sprites)
        print("Case #{}: {}".format(test + 1, game_status.get_collisions()))


if __name__ == '__main__':
    solve()

