"""
Enhanced Snake Game - User-Friendly & Dynamic
Features:
- Multiple difficulty levels
- Score tracking with high score
- Colorful visuals and smooth animations
- Pause/Resume functionality
- Speed progression
- Game over screen with restart
- Keyboard controls with visual feedback
"""

import turtle
import time
import random
import os
from turtle import Screen, Turtle

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
DELAY_BASE = 0.15

# Colors
COLORS = {
    'background': '#1a1a2e',
    'snake_head': '#00ff88',
    'snake_body': '#00cc6a',
    'food': '#ff4757',
    'food_glow': '#ff6b81',
    'score': '#ffd93d',
    'text': '#ffffff',
    'border': '#4a4a6a',
    'button': '#6c5ce7',
    'button_hover': '#a29bfe'
}

class SnakeGame:
    def __init__(self):
        self.screen = Screen()
        self.setup_screen()
        self.score = 0
        self.high_score = self.load_high_score()
        self.difficulty = 'medium'
        self.paused = False
        self.game_over = False
        self.snake = []
        self.food = None
        self.direction = 'stop'
        self.current_speed = DELAY_BASE
        self.setup_game()
        self.bind_controls()
        
    def setup_screen(self):
        """Setup the game screen with visual styling"""
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.bgcolor(COLORS['background'])
        self.screen.title("🐍 Enhanced Snake Game")
        self.screen.tracer(0)
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists('high_score.txt'):
                with open('high_score.txt', 'r') as f:
                    return int(f.read())
        except:
            pass
        return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def setup_game(self):
        """Initialize/reset the game"""
        # Clear previous elements
        self.screen.clear()
        self.setup_screen()
        
        self.snake = []
        self.score = 0
        self.direction = 'stop'
        self.game_over = False
        self.paused = False
        
        # Set difficulty settings
        self.set_difficulty(self.difficulty)
        
        # Create border
        self.draw_border()
        
        # Create snake
        self.create_snake()
        
        # Create food
        self.create_food()
        
        # Create UI
        self.create_ui()
        
        # Draw initial state
        self.screen.update()
    
    def set_difficulty(self, level):
        """Set game difficulty"""
        self.difficulty = level
        speeds = {
            'easy': 0.12,
            'medium': 0.1,
            'hard': 0.07,
            'expert': 0.04
        }
        self.current_speed = speeds.get(level, 0.1)
    
    def draw_border(self):
        """Draw game border"""
        border = Turtle()
        border.hideturtle()
        border.penup()
        border.color(COLORS['border'])
        border.pensize(3)
        
        # Draw rectangle border
        x = -SCREEN_WIDTH//2 + 30
        y = SCREEN_HEIGHT//2 - 50
        border.goto(x, y)
        border.pendown()
        
        for _ in range(2):
            border.forward(SCREEN_WIDTH - 60)
            border.right(90)
            border.forward(SCREEN_HEIGHT - 100)
            border.right(90)
        border.penup()
    
    def create_snake(self):
        """Create initial snake"""
        start_positions = [(-20, 0), (-40, 0), (-60, 0)]
        
        for i, pos in enumerate(start_positions):
            segment = self.create_snake_segment()
            segment.goto(pos)
            if i == 0:
                segment.color(COLORS['snake_head'])
                segment.shape('square')
            self.snake.append(segment)
    
    def create_snake_segment(self):
        """Create a snake segment"""
        segment = Turtle()
        segment.speed(0)
        segment.penup()
        segment.shape('square')
        segment.color(COLORS['snake_body'])
        return segment
    
    def create_food(self):
        """Create food with visual effects"""
        if self.food:
            self.food.hideturtle()
        
        self.food = Turtle()
        self.food.speed(0)
        self.food.penup()
        self.food.shape('circle')
        self.food.color(COLORS['food'])
        self.move_food()
        self.food.showturtle()
    
    def move_food(self):
        """Move food to random position"""
        x = random.randint(-SCREEN_WIDTH//2 + 50, SCREEN_WIDTH//2 - 50)
        y = random.randint(-SCREEN_HEIGHT//2 + 70, SCREEN_HEIGHT//2 - 70)
        # Snap to grid
        x = (x // GRID_SIZE) * GRID_SIZE
        y = (y // GRID_SIZE) * GRID_SIZE
        self.food.goto(x, y)
    
    def create_ui(self):
        """Create game UI elements"""
        # Title
        title = Turtle()
        title.hideturtle()
        title.penup()
        title.color(COLORS['text'])
        title.goto(0, SCREEN_HEIGHT//2 - 35)
        title.write("🐍 SNAKE GAME", align='center', font=('Arial', 20, 'bold'))
        
        # Score display
        self.score_display = Turtle()
        self.score_display.hideturtle()
        self.score_display.penup()
        self.score_display.color(COLORS['score'])
        self.update_score_display()
        
        # High Score display
        self.high_score_display = Turtle()
        self.high_score_display.hideturtle()
        self.high_score_display.penup()
        self.high_score_display.color(COLORS['score'])
        self.update_high_score_display()
        
        # Difficulty indicator
        self.diff_display = Turtle()
        self.diff_display.hideturtle()
        self.diff_display.penup()
        self.diff_display.color(COLORS['text'])
        self.diff_display.goto(-SCREEN_WIDTH//2 + 80, SCREEN_HEIGHT//2 - 35)
        self.diff_display.write(f"Level: {self.difficulty.upper()}", font=('Arial', 12, 'bold'))
        
        # Instructions
        self.create_instructions()
    
    def create_instructions(self):
        """Create instruction text"""
        instructions = [
            "Arrow Keys: Move",
            "Space: Pause | R: Restart",
            "1-4: Change Difficulty"
        ]
        
        inst_turtle = Turtle()
        inst_turtle.hideturtle()
        inst_turtle.penup()
        inst_turtle.color(COLORS['border'])
        inst_turtle.goto(0, -SCREEN_HEIGHT//2 + 30)
        
        for i, text in enumerate(instructions):
            inst_turtle.goto(0, -SCREEN_HEIGHT//2 + 25 + i * 18)
            inst_turtle.write(text, align='center', font=('Arial', 10, 'normal'))
    
    def update_score_display(self):
        """Update score display"""
        self.score_display.clear()
        self.score_display.goto(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 35)
        self.score_display.write(f"Score: {self.score}", font=('Arial', 14, 'bold'))
    
    def update_high_score_display(self):
        """Update high score display"""
        self.high_score_display.clear()
        self.high_score_display.goto(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 60)
        self.high_score_display.write(f"Best: {self.high_score}", font=('Arial', 12, 'normal'))
    
    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(self.go_up, 'Up')
        self.screen.onkeypress(self.go_down, 'Down')
        self.screen.onkeypress(self.go_left, 'Left')
        self.screen.onkeypress(self.go_right, 'Right')
        self.screen.onkeypress(self.toggle_pause, 'space')
        self.screen.onkeypress(self.restart, 'r')
        self.screen.onkeypress(lambda: self.change_difficulty('easy'), '1')
        self.screen.onkeypress(lambda: self.change_difficulty('medium'), '2')
        self.screen.onkeypress(lambda: self.change_difficulty('hard'), '3')
        self.screen.onkeypress(lambda: self.change_difficulty('expert'), '4')
    
    def change_difficulty(self, level):
        """Change game difficulty"""
        self.difficulty = level
        self.set_difficulty(level)
        
        # Update difficulty display
        self.diff_display.clear()
        self.diff_display.goto(-SCREEN_WIDTH//2 + 80, SCREEN_HEIGHT//2 - 35)
        self.diff_display.write(f"Level: {self.difficulty.upper()}", font=('Arial', 12, 'bold'))
    
    def go_up(self):
        """Move snake up"""
        if self.direction != 'down' and not self.game_over and not self.paused:
            self.direction = 'up'
    
    def go_down(self):
        """Move snake down"""
        if self.direction != 'up' and not self.game_over and not self.paused:
            self.direction = 'down'
    
    def go_left(self):
        """Move snake left"""
        if self.direction != 'right' and not self.game_over and not self.paused:
            self.direction = 'left'
    
    def go_right(self):
        """Move snake right"""
        if self.direction != 'left' and not self.game_over and not self.paused:
            self.direction = 'right'
    
    def toggle_pause(self):
        """Toggle pause state"""
        if not self.game_over:
            self.paused = not self.paused
            if self.paused:
                self.show_paused_message()
            else:
                self.clear_message()
    
    def show_paused_message(self):
        """Show pause message"""
        self.message_turtle = Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color(COLORS['score'])
        self.message_turtle.goto(0, 0)
        self.message_turtle.write("⏸️ PAUSED", align='center', font=('Arial', 30, 'bold'))
        self.screen.update()
    
    def clear_message(self):
        """Clear any message"""
        if hasattr(self, 'message_turtle'):
            self.message_turtle.clear()
            self.message_turtle.hideturtle()
    
    def restart(self):
        """Restart the game"""
        self.setup_game()
    
    def move(self):
        """Move snake in current direction"""
        if self.direction == 'stop' or self.paused or self.game_over:
            return
        
        # Get head position
        head = self.snake[0]
        x = head.xcor()
        y = head.ycor()
        
        if self.direction == 'up':
            y += GRID_SIZE
        elif self.direction == 'down':
            y -= GRID_SIZE
        elif self.direction == 'left':
            x -= GRID_SIZE
        elif self.direction == 'right':
            x += GRID_SIZE
        
        # Check boundary collision
        if x > SCREEN_WIDTH//2 - 40 or x < -SCREEN_WIDTH//2 + 40 or \
           y > SCREEN_HEIGHT//2 - 60 or y < -SCREEN_HEIGHT//2 + 40:
            self.end_game()
            return
        
        # Check self collision
        for segment in self.snake[1:]:
            if head.distance(segment) < 10:
                self.end_game()
                return
        
        # Move snake body
        for i in range(len(self.snake) - 1, 0, -1):
            x = self.snake[i - 1].xcor()
            y = self.snake[i - 1].ycor()
            self.snake[i].goto(x, y)
        
        # Move head
        self.snake[0].goto(x, y)
        
        # Check food collision
        if self.snake[0].distance(self.food) < 15:
            self.eat_food()
    
    def eat_food(self):
        """Handle food consumption"""
        # Add score
        self.score += 10
        
        # Speed up slightly
        if self.current_speed > 0.03:
            self.current_speed -= 0.001
        
        # Update displays
        self.update_score_display()
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.update_high_score_display()
        
        # Add new segment
        segment = self.create_snake_segment()
        segment.goto(self.snake[-1].position())
        self.snake.append(segment)
        
        # Move food
        self.move_food()
        
        # Flash effect
        self.food.color(COLORS['food_glow'])
        self.screen.ontimer(lambda: self.food.color(COLORS['food']), 100)
    
    def end_game(self):
        """Handle game over"""
        self.game_over = True
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        # Show game over screen
        self.show_game_over()
    
    def show_game_over(self):
        """Display game over screen"""
        # Overlay
        overlay = Turtle()
        overlay.speed(0)
        overlay.penup()
        overlay.color(COLORS['background'])
        overlay.goto(0, 0)
        overlay.begin_fill()
        for _ in range(4):
            overlay.forward(300)
            overlay.right(90)
        overlay.end_fill()
        
        # Game Over text
        go_turtle = Turtle()
        go_turtle.hideturtle()
        go_turtle.penup()
        go_turtle.color(COLORS['food'])
        go_turtle.goto(0, 50)
        go_turtle.write("GAME OVER", align='center', font=('Arial', 40, 'bold'))
        
        # Score
        score_turtle = Turtle()
        score_turtle.hideturtle()
        score_turtle.penup()
        score_turtle.color(COLORS['score'])
        score_turtle.goto(0, -10)
        score_turtle.write(f"Final Score: {self.score}", align='center', font=('Arial', 24, 'bold'))
        
        # High Score
        if self.score >= self.high_score:
            hs_turtle = Turtle()
            hs_turtle.hideturtle()
            hs_turtle.penup()
            hs_turtle.color(COLORS['snake_head'])
            hs_turtle.goto(0, -50)
            hs_turtle.write("🎉 NEW HIGH SCORE! 🎉", align='center', font=('Arial', 18, 'bold'))
        
        # Restart instruction
        restart_turtle = Turtle()
        restart_turtle.hideturtle()
        restart_turtle.penup()
        restart_turtle.color(COLORS['text'])
        restart_turtle.goto(0, -100)
        restart_turtle.write("Press 'R' to Restart", align='center', font=('Arial', 16, 'normal'))
        
        self.screen.update()
    
    def run(self):
        """Main game loop"""
        while True:
            self.screen.update()
            
            if not self.game_over and not self.paused:
                self.move()
            
            time.sleep(self.current_speed)


def show_difficulty_menu():
    """Show difficulty selection menu"""
    screen = Screen()
    screen.bgcolor(COLORS['background'])
    screen.title("🐍 Snake Game - Select Difficulty")
    screen.setup(400, 300)
    
    # Title
    title = Turtle()
    title.hideturtle()
    title.penup()
    title.color(COLORS['text'])
    title.goto(0, 80)
    title.write("🐍 SNAKE GAME", align='center', font=('Arial', 24, 'bold'))
    
    # Instructions
    inst = Turtle()
    inst.hideturtle()
    inst.penup()
    inst.color(COLORS['score'])
    inst.goto(0, 30)
    inst.write("Select Difficulty:", align='center', font=('Arial', 16, 'bold'))
    
    # Options
    options = [
        ("1 - Easy", -20, 'easy'),
        ("2 - Medium", -50, 'medium'),
        ("3 - Hard", -80, 'hard'),
        ("4 - Expert", -110, 'expert')
    ]
    
    for text, y, _ in options:
        opt = Turtle()
        opt.hideturtle()
        opt.penup()
        opt.color(COLORS['text'])
        opt.goto(0, y)
        opt.write(text, align='center', font=('Arial', 14, 'normal'))
    
    screen.listen()
    
    selected = [None]
    
    def select_difficulty(level):
        selected[0] = level
        screen.bye()
    
    screen.onkeypress(lambda: select_difficulty('easy'), '1')
    screen.onkeypress(lambda: select_difficulty('medium'), '2')
    screen.onkeypress(lambda: select_difficulty('hard'), '3')
    screen.onkeypress(lambda: select_difficulty('expert'), '4')
    screen.onkeypress(lambda: select_difficulty('medium'), 'Return')
    
    # Auto-select medium after timeout
    screen.ontimer(lambda: screen.bye() if not selected[0] else None, 3000)
    
    screen.mainloop()
    return selected[0] if selected[0] else 'medium'


def main():
    """Main entry point"""
    # Show difficulty selection (commented out for direct start)
    # difficulty = show_difficulty_menu()
    
    # Start game directly
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    
    main()

