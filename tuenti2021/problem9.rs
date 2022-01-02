use std::cell::RefCell;
use std::collections::BTreeSet;
use std::io::Stdin;
use std::io;
use std::iter::FromIterator;

struct Sprite {
    width: usize,
    height: usize,
    shape: BTreeSet<(usize, usize)>,
}

impl Sprite {
    fn parse_sprites(stdin: &mut Stdin) -> io::Result<Vec<Sprite>> {
        let n_sprites = read_line(stdin)?.parse::<usize>().unwrap();
        let mut sprites = Vec::with_capacity(n_sprites);
        for _ in 0..n_sprites {
            let width_height: Vec<usize> = read_line(stdin)?.split(" ").map(|s| s.parse::<usize>().unwrap()).collect();
            let mut shape = BTreeSet::new();
            for y in 0..width_height[1] {
                for (x, value) in read_line(stdin)?.chars().map(|s| s.to_digit(10).unwrap()).enumerate() {
                    if value == 1 {
                        shape.insert((x, y));
                    }
                }
            }
            sprites.push(Sprite {
                height: width_height[1],
                width: width_height[0],
                shape,
            });
        }
        Ok(sprites)
    }
}

struct GameObject<'a> {
    x: usize,
    y: usize,
    sprite: &'a Sprite,
    shape: Option<BTreeSet<(usize, usize)>>,
}

impl<'a> GameObject<'a> {
    fn get_points(&mut self) -> &BTreeSet<(usize, usize)> {
        if self.shape.is_none() {
            let hs = BTreeSet::from_iter(self.sprite.shape.iter().map(|p| (p.0 + self.x, p.1 + self.y)));
            self.shape = Some(hs);
        }
        self.shape.as_ref().unwrap()
    }
    fn clear_points(&mut self) {
        self.shape.iter_mut().for_each(|s| s.clear());
        self.shape = None;
    }
}

struct GameStatus<'a> {
    objects: Vec<RefCell<GameObject<'a>>>,
}

impl<'a> GameStatus<'a> {
    fn get_collisions(&self) -> usize {
        let mut collisions = 0;
        for (i, game_object) in self.objects.iter().enumerate() {
            for other_game_object in self.objects[i+1..].iter() {
                if !game_object.borrow_mut().get_points().is_disjoint(other_game_object.borrow_mut().get_points()) {
                    collisions += 1
                }
            }
            game_object.borrow_mut().clear_points();
            // println!("Finished point {}", i);
        }
        collisions
    }

    fn parse_game_status(stdin: &mut Stdin, sprites: &'a [Sprite]) -> io::Result<GameStatus<'a>> {
        let n_objects = read_line(stdin)?.parse::<usize>().unwrap();
        let mut objects = vec![];
        for _ in 0..n_objects {
            let sprite_id_x_y: Vec<usize> = read_line(stdin)?.split(" ").map(|s| s.parse::<usize>().unwrap()).collect();
            objects.push(RefCell::new(GameObject { x: sprite_id_x_y[1], y: sprite_id_x_y[2], sprite: &sprites[sprite_id_x_y[0]], shape: None }));
        }
        Ok(GameStatus { objects })
    }
}

fn read_line(stdin: &mut Stdin) -> io::Result<String> {
    let mut buffer = String::new();
    stdin.read_line(&mut buffer)?;
    Ok(buffer.trim_end().to_owned())
}

fn main() -> io::Result<()> {
    let mut stdin = io::stdin();
    let tests = read_line(&mut stdin)?.parse::<usize>().unwrap();
    let sprites = Sprite::parse_sprites(&mut stdin)?;
    for test in 0..tests {
        let game_status = GameStatus::parse_game_status(&mut stdin, &sprites)?;
        println!("{}", format!("Case #{}: {}", test + 1, game_status.get_collisions()));
    }
    Ok(())
}