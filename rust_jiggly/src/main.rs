use enigo::{Enigo, MouseControllable, KeyboardControllable};
use rand::{thread_rng, Rng};
use std::{thread, time::{Duration, SystemTime}};
use chrono::Local;

struct JigglyMuse {
    enigo: Enigo,
    screen_width: i32,
    screen_height: i32,
    reading_direction: i32,
    safe_keys: Vec<enigo::Key>,
}

impl JigglyMuse {
    fn new() -> Self {
        let enigo = Enigo::new();
        // Assuming standard HD resolution as fallback
        let screen_width = 1920;
        let screen_height = 1080;
        
        JigglyMuse {
            enigo,
            screen_width,
            screen_height,
            reading_direction: 1,
            safe_keys: vec![enigo::Key::Shift, enigo::Key::Alt, enigo::Key::Control],
        }
    }

    fn simulate_reading(&mut self) {
        let mut rng = thread_rng();
        let (current_x, current_y) = self.enigo.mouse_location();
        
        let scroll_amount = rng.gen_range(-2.0..2.0) * self.reading_direction as f64;
        let new_y = (current_y as f64 + scroll_amount) as i32;
        
        // Change direction if needed
        if new_y > (self.screen_height as f64 * 0.8) as i32 {
            self.reading_direction = -1;
        } else if new_y < (self.screen_height as f64 * 0.2) as i32 {
            self.reading_direction = 1;
        }
        
        let new_x = current_x + rng.gen_range(-1..2);
        
        // Smooth movement
        self.enigo.mouse_move_to(new_x, new_y);
        
        thread::sleep(Duration::from_millis(rng.gen_range(2000..5000)));
    }

    fn micro_movement(&mut self) {
        let mut rng = thread_rng();
        let (current_x, current_y) = self.enigo.mouse_location();
        
        let offset_x = rng.gen_range(-1..2);
        let offset_y = rng.gen_range(-1..2);
        
        self.enigo.mouse_move_relative(offset_x, offset_y);
        
        // Occasional key press
        if rng.gen_bool(0.2) {
            let key = self.safe_keys[rng.gen_range(0..self.safe_keys.len())];
            self.enigo.key_down(key);
            thread::sleep(Duration::from_millis(100));
            self.enigo.key_up(key);
        }
        
        thread::sleep(Duration::from_millis(rng.gen_range(3000..7000)));
    }

    fn prevent_idle(&mut self) {
        let mut rng = thread_rng();
        
        if rng.gen_bool(0.15) {
            let key = self.safe_keys[rng.gen_range(0..self.safe_keys.len())];
            self.enigo.key_down(key);
            thread::sleep(Duration::from_millis(100));
            self.enigo.key_up(key);
            thread::sleep(Duration::from_millis(200));
        }
    }

    fn run(&mut self) {
        println!("Rust JigglyMuse is active... (Ctrl+C to stop)");
        
        let mut rng = thread_rng();
        let mut last_time = SystemTime::now();
        
        loop {
            let hour = Local::now().hour();
            
            if (8..=18).contains(&hour) {
                if rng.gen_bool(0.7) {
                    self.simulate_reading();
                } else {
                    self.micro_movement();
                }
                self.prevent_idle();
            } else {
                self.micro_movement();
            }
            
            if rng.gen_bool(0.1) {
                thread::sleep(Duration::from_secs(rng.gen_range(15..45)));
            }
        }
    }
}

fn main() {
    let mut jiggler = JigglyMuse::new();
    
    ctrlc::set_handler(move || {
        println!("\nStopping Rust JigglyMuse...");
        std::process::exit(0);
    }).expect("Error setting Ctrl-C handler");
    
    jiggler.run();
}
