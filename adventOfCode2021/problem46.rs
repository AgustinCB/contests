#![feature(int_abs_diff)]
use std::collections::{BinaryHeap, HashMap};
use std::io;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialOrd, PartialEq)]
enum Amphipod {
    A,
    B,
    C,
    D
}

impl Amphipod {
    fn energy_cost(&self) -> usize {
        match self {
            Amphipod::A => 1,
            Amphipod::B => 10,
            Amphipod::C => 100,
            Amphipod::D => 1000,
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialOrd, PartialEq)]
enum BoardCell {
    Hallway(u8),
    AQueue(u8),
    BQueue(u8),
    CQueue(u8),
    DQueue(u8),
}

fn diff_from_hallway_to_queue(from_cell: u8, to_cell: u8, queue_starting_point: u8) -> u8 {
    if from_cell < queue_starting_point {
        (queue_starting_point - from_cell) + to_cell + 1
    } else {
        (from_cell - queue_starting_point) + to_cell + 1
    }
}

fn from_queue_to_queue(from_cell: u8, to_cell: u8, from_starting_point: u8, to_starting_point: u8) -> u8 {
    from_cell + 1 + to_cell + 1  + from_starting_point.abs_diff(to_starting_point) + 1
}

impl BoardCell {
    fn is_hallway(&self) -> bool {
        match self {
            BoardCell::Hallway(_) => true,
            _ => false,
        }
    }

    fn is_moving_position(&self) -> bool {
        match self {
            BoardCell::Hallway(_) => true,
            BoardCell::AQueue(p) => *p == 0,
            BoardCell::BQueue(p) => *p == 0,
            BoardCell::CQueue(p) => *p == 0,
            BoardCell::DQueue(p) => *p == 0,
        }
    }

    fn distance(&self, other: BoardCell) -> u8 {
        match (self, &other) {
            (BoardCell::Hallway(from_cell), BoardCell::Hallway(to_cell)) => from_cell.abs_diff(*to_cell),
            (BoardCell::Hallway(from_cell), BoardCell::AQueue(to_cell)) =>
                diff_from_hallway_to_queue(*from_cell, *to_cell, 2),
            (BoardCell::AQueue(_), BoardCell::Hallway(_)) => other.distance(*self),
            (BoardCell::Hallway(from_cell), BoardCell::BQueue(to_cell)) =>
                diff_from_hallway_to_queue(*from_cell, *to_cell, 4),
            (BoardCell::BQueue(_), BoardCell::Hallway(_)) => other.distance(*self),
            (BoardCell::Hallway(from_cell), BoardCell::CQueue(to_cell)) =>
                diff_from_hallway_to_queue(*from_cell, *to_cell, 6),
            (BoardCell::CQueue(_), BoardCell::Hallway(_)) => other.distance(*self),
            (BoardCell::Hallway(from_cell), BoardCell::DQueue(to_cell)) =>
                diff_from_hallway_to_queue(*from_cell, *to_cell, 8),
            (BoardCell::DQueue(_), BoardCell::Hallway(_)) => other.distance(*self),
            (BoardCell::AQueue(from_cell), BoardCell::AQueue(to_cell)) |
                (BoardCell::BQueue(from_cell), BoardCell::BQueue(to_cell)) |
                (BoardCell::CQueue(from_cell), BoardCell::CQueue(to_cell)) |
                (BoardCell::DQueue(from_cell), BoardCell::DQueue(to_cell)) => from_cell.abs_diff(*to_cell),
            (BoardCell::AQueue(from_cell), BoardCell::BQueue(to_cell)) |
                (BoardCell::BQueue(to_cell), BoardCell::AQueue(from_cell)) => from_queue_to_queue(*from_cell, *to_cell, 2, 4),
            (BoardCell::AQueue(from_cell), BoardCell::CQueue(to_cell)) |
                (BoardCell::CQueue(to_cell), BoardCell::AQueue(from_cell)) => from_queue_to_queue(*from_cell, *to_cell, 2, 6),
            (BoardCell::AQueue(from_cell), BoardCell::DQueue(to_cell)) |
                (BoardCell::DQueue(to_cell), BoardCell::AQueue(from_cell)) => from_queue_to_queue(*from_cell, *to_cell, 2, 8),
            (BoardCell::BQueue(from_cell), BoardCell::CQueue(to_cell)) |
                (BoardCell::CQueue(to_cell), BoardCell::BQueue(from_cell)) => from_queue_to_queue(*from_cell, *to_cell, 4, 6),
            (BoardCell::BQueue(from_cell), BoardCell::DQueue(to_cell)) |
                (BoardCell::DQueue(to_cell), BoardCell::BQueue(from_cell)) => from_queue_to_queue(*from_cell, *to_cell, 4, 8),
            (BoardCell::CQueue(from_cell), BoardCell::DQueue(to_cell)) |
                (BoardCell::DQueue(to_cell), BoardCell::CQueue(from_cell)) => from_queue_to_queue(*from_cell, *to_cell, 6, 8),
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct GameBoardStatus {
    possible_moves: Vec<((BoardCell, Amphipod), BoardCell)>,
    positions: HashMap<BoardCell, Amphipod>,
    points: usize,
}

type GameKey = Vec<(BoardCell, Amphipod)>;

impl GameBoardStatus {
    fn key(&self) -> GameKey {
        let mut positions = self.positions.iter().map(|(b, a)| (*b, *a)).collect::<Vec<(BoardCell, Amphipod)>>();
        positions.sort();
        positions
    }

    fn perform_move(&mut self, ((from_cell, amphipod), to_cell): ((BoardCell, Amphipod), BoardCell)) {
        self.positions.remove(&from_cell);
        self.positions.insert(to_cell, amphipod);
        self.points += from_cell.distance(to_cell) as usize * amphipod.energy_cost();
        if from_cell.is_moving_position() && !from_cell.is_hallway() {
            let queue_starting_point = match from_cell {
                BoardCell::AQueue(_) => 2,
                BoardCell::BQueue(_) => 4,
                BoardCell::CQueue(_) => 6,
                BoardCell::DQueue(_) => 8,
                _ => panic!("Can't happen")
            };
            let expected_amphipod = match from_cell {
                BoardCell::AQueue(_) => Amphipod::A,
                BoardCell::BQueue(_) => Amphipod::B,
                BoardCell::CQueue(_) => Amphipod::C,
                BoardCell::DQueue(_) => Amphipod::D,
                _ => panic!("Can't happen")
            };
            if !self.is_queue_ingoing(queue_starting_point) {
                for queue_index in 1..4 {
                    let current_cell = match from_cell {
                        BoardCell::AQueue(_) => BoardCell::AQueue(queue_index),
                        BoardCell::BQueue(_) => BoardCell::BQueue(queue_index),
                        BoardCell::CQueue(_) => BoardCell::CQueue(queue_index),
                        BoardCell::DQueue(_) => BoardCell::DQueue(queue_index),
                        _ => panic!("Can't happen")
                    };
                    let to_cell = match from_cell {
                        BoardCell::AQueue(_) => BoardCell::AQueue(queue_index - 1),
                        BoardCell::BQueue(_) => BoardCell::BQueue(queue_index - 1),
                        BoardCell::CQueue(_) => BoardCell::CQueue(queue_index - 1),
                        BoardCell::DQueue(_) => BoardCell::DQueue(queue_index - 1),
                        _ => panic!("Can't happen")
                    };
                    if self.positions.contains_key(&current_cell) {
                        let amphipod = self.positions.get(&current_cell).unwrap().clone();
                        if !(amphipod == expected_amphipod && queue_index == 3) {
                            self.positions.remove(&current_cell);
                            self.positions.insert(to_cell, amphipod);
                            self.points += current_cell.distance(to_cell) as usize * amphipod.energy_cost();
                        }
                    }
                }
            }
        }
        self.calculate_new_possible_moves();
    }

    fn is_game_complete(&self) -> bool {
        self.is_queue_ingoing(2) && self.is_queue_ingoing(4) && self.is_queue_ingoing(6) && self.is_queue_ingoing(8) &&
            self.positions.keys().all(|cell| {
                match cell {
                    BoardCell::Hallway(_) => false,
                    _ => true,
                }
            })
    }

    fn calculate_new_possible_moves(&mut self) {
        let mut new_possible_moves = vec![];
        self.positions.iter().for_each(|(cell, amphipod)| {
            if cell.is_moving_position() {
                match cell {
                    BoardCell::Hallway(from_index) =>
                        self.calculate_new_possible_moves_for_position(*cell, *amphipod, *from_index, &mut new_possible_moves),
                    BoardCell::AQueue(0) if !self.is_queue_ingoing(2) =>
                        self.calculate_new_possible_moves_for_position(*cell, *amphipod, 2, &mut new_possible_moves),
                    BoardCell::BQueue(0) if !self.is_queue_ingoing(4) =>
                        self.calculate_new_possible_moves_for_position(*cell, *amphipod, 4, &mut new_possible_moves),
                    BoardCell::CQueue(0) if !self.is_queue_ingoing(6) =>
                        self.calculate_new_possible_moves_for_position(*cell, *amphipod, 6, &mut new_possible_moves),
                    BoardCell::DQueue(0) if !self.is_queue_ingoing(8) =>
                        self.calculate_new_possible_moves_for_position(*cell, *amphipod, 8, &mut new_possible_moves),
                    _ => {},
                }
            }
        });
        new_possible_moves.sort_by(|((first_from, first_amphipod), first_to), ((second_from, second_amphipod), second_to)| {
            let first_move_energy = first_from.distance(*first_to) as usize * first_amphipod.energy_cost();
            let second_move_energy = second_from.distance(*second_to) as usize * second_amphipod.energy_cost();
            first_move_energy.cmp(&second_move_energy).reverse()
        });
        self.possible_moves = new_possible_moves;
    }

    fn calculate_new_possible_moves_for_position(
        &self,
        cell: BoardCell,
        amphipod: Amphipod,
        from_index: u8,
        new_possible_moves: &mut Vec<((BoardCell, Amphipod), BoardCell)>
    ) {
        for to_index in from_index + 1..11 {
            if self.positions.contains_key(&BoardCell::Hallway(to_index)) {
                break;
            }
            self.calculate_new_possible_moves_for_position_and_cell(cell, amphipod, to_index, new_possible_moves);
        }
        for to_index in (0..from_index).rev() {
            if self.positions.contains_key(&BoardCell::Hallway(to_index)) {
                break;
            }
            self.calculate_new_possible_moves_for_position_and_cell(cell, amphipod, to_index, new_possible_moves);
        }
    }

    fn calculate_new_possible_moves_for_position_and_cell(
        &self,
        cell: BoardCell,
        amphipod: Amphipod,
        to_index: u8,
        new_possible_moves: &mut Vec<((BoardCell, Amphipod), BoardCell)>
    ) {
        if to_index != 0 && to_index != 10 && to_index % 2 == 0 &&
            ((amphipod == Amphipod::A && to_index == 2 && self.is_queue_ingoing(2))
                || (amphipod == Amphipod::B && to_index == 4 && self.is_queue_ingoing(4))
                || (amphipod == Amphipod::C && to_index == 6 && self.is_queue_ingoing(6))
                || (amphipod == Amphipod::D && to_index == 8 && self.is_queue_ingoing(8))) {
            for queue_index in (0..4).rev() {
                let to_cell = match to_index {
                    2 => BoardCell::AQueue(queue_index),
                    4 => BoardCell::BQueue(queue_index),
                    6 => BoardCell::CQueue(queue_index),
                    8 => BoardCell::DQueue(queue_index),
                    _ => panic!("Can't happen"),
                };
                if !self.positions.contains_key(&to_cell) {
                    new_possible_moves.push(((cell, amphipod), to_cell));
                    break;
                }
            }
        } else if to_index != 2 && to_index != 4 && to_index != 6 && to_index != 8 && !cell.is_hallway() {
            new_possible_moves.push(((cell, amphipod), BoardCell::Hallway(to_index)));
        }
    }

    fn is_queue_ingoing(&self, queue: u8) -> bool {
        let expected_amphipod = match queue {
            2 => Amphipod::A,
            4 => Amphipod::B,
            6 => Amphipod::C,
            8 => Amphipod::D,
            _ => panic!("can't happen"),
        };
        (0..4).all(|queue_index| {
            let to_cell = match queue {
                2 => BoardCell::AQueue(queue_index),
                4 => BoardCell::BQueue(queue_index),
                6 => BoardCell::CQueue(queue_index),
                8 => BoardCell::DQueue(queue_index),
                _ => panic!("Can't happen"),
            };
            self.positions.get(&to_cell).unwrap_or(&expected_amphipod) == &expected_amphipod
        })
    }
}

impl Ord for GameBoardStatus {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.points.cmp(&self.points)
    }
}

impl PartialOrd for GameBoardStatus {
    fn partial_cmp(&self, other: &GameBoardStatus) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

fn find_lowest_energy_cost_in_parallel(mut game_board: GameBoardStatus) -> usize {
    game_board.calculate_new_possible_moves();
    let mut distances = HashMap::from([(game_board.key(), game_board.points)]);
    let mut working_stack = BinaryHeap::from(vec![game_board]);
    while !working_stack.is_empty() {
        let current_status = working_stack.pop().unwrap();
        let current_points = current_status.points;
        if current_status.is_game_complete() {
            return current_points;
        }
        for next_move in current_status.possible_moves.iter().cloned() {
            let mut next_status = current_status.clone();
            next_status.perform_move(next_move);
            let key = next_status.key();
            if distances.get(&key).cloned().unwrap_or(usize::MAX) > next_status.points {
                distances.insert(key, next_status.points);
                working_stack.push(next_status);
            }
        }
    }
    panic!("No valid way to win!")
}

fn main() -> io::Result<()> {
    println!("Starting computation");
    /*
    #############
    #...........#
    ###B#B#C#D###
      #D#C#B#A#
      #D#B#A#C#
      #D#C#A#A#
      #########
    */
    let positions = HashMap::from([
        (BoardCell::AQueue(0), Amphipod::B),
        (BoardCell::AQueue(1), Amphipod::D),
        (BoardCell::AQueue(2), Amphipod::D),
        (BoardCell::AQueue(3), Amphipod::D),
        (BoardCell::BQueue(0), Amphipod::B),
        (BoardCell::BQueue(1), Amphipod::C),
        (BoardCell::BQueue(2), Amphipod::B),
        (BoardCell::BQueue(3), Amphipod::C),
        (BoardCell::CQueue(0), Amphipod::C),
        (BoardCell::CQueue(1), Amphipod::B),
        (BoardCell::CQueue(2), Amphipod::A),
        (BoardCell::CQueue(3), Amphipod::A),
        (BoardCell::DQueue(0), Amphipod::D),
        (BoardCell::DQueue(1), Amphipod::A),
        (BoardCell::DQueue(2), Amphipod::C),
        (BoardCell::DQueue(3), Amphipod::A),
    ]);
    let status = GameBoardStatus {
        possible_moves: vec![],
        points: 0,
        positions,
    };
    println!("Lowest energy cost: {}", find_lowest_energy_cost_in_parallel(status));
    Ok(())
}