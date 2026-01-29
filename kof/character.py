import pygame
from utils.constants import *


class Character:
    def __init__(self, name, x, y, is_player1=True):
        self.name = name
        self.x = x
        self.y = y
        self.is_player1 = is_player1
        
        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.direction = 1 if is_player1 else -1  # 1 for right, -1 for left
        
        # Stats
        self.max_health = 100
        self.health = 100
        self.energy = 100
        self.max_energy = 100
        
        # Dimensions
        self.width = 50
        self.height = 100
        
        # Combat state
        self.is_blocking = False
        self.current_attack = None
        self.attack_cooldown = 0
        self.combo_counter = 0
        self.combo_timer = 0
        self.hit_cooldown = 0
        self.knockback_vel_x = 0
        
        # Animation
        self.anim_frame = 0
        self.anim_speed = 0.15
        
        # Character-specific attributes
        self.character_type = name
        self.set_character_stats()
    
    def set_character_stats(self):
        """Set character-specific stats"""
        if self.character_type == "Kyo":
            self.max_health = 100
            self.speed = 5
            self.jump_power = JUMP_STRENGTH
        elif self.character_type == "Iori":
            self.max_health = 95
            self.speed = 5.5
            self.jump_power = JUMP_STRENGTH - 1
        elif self.character_type == "Mai":
            self.max_health = 85
            self.speed = 6
            self.jump_power = JUMP_STRENGTH + 1
        elif self.character_type == "Ryo":
            self.max_health = 110
            self.speed = 4.5
            self.jump_power = JUMP_STRENGTH - 0.5
        else:
            self.speed = 5
            self.jump_power = JUMP_STRENGTH
        
        self.health = self.max_health
    
    def move(self, direction):
        """Move character left or right"""
        if direction == 0:
            self.vel_x = 0
        else:
            self.vel_x = direction * self.speed
            self.direction = 1 if direction > 0 else -1
    
    def jump(self):
        """Make character jump"""
        if self.on_ground and self.attack_cooldown <= 0:
            self.vel_y = self.jump_power
            self.on_ground = False
    
    def punch(self):
        """Light punch attack"""
        if self.attack_cooldown <= 0 and self.energy >= 10:
            self.current_attack = ("punch", 0)
            self.attack_cooldown = 15
            self.combo_counter += 1
            self.combo_timer = 30
            self.energy -= 10
    
    def kick(self):
        """Light kick attack"""
        if self.attack_cooldown <= 0 and self.energy >= 15:
            self.current_attack = ("kick", 0)
            self.attack_cooldown = 20
            self.combo_counter += 1
            self.combo_timer = 30
            self.energy -= 15
    
    def special_attack(self):
        """Special move"""
        if self.attack_cooldown <= 0 and self.energy >= 40:
            self.current_attack = ("special", 0)
            self.attack_cooldown = 40
            self.combo_counter = 0
            self.energy -= 40
    
    def block(self):
        """Block incoming attacks"""
        self.is_blocking = True
        self.vel_x = 0
    
    def unblock(self):
        """Stop blocking"""
        self.is_blocking = False
    
    def take_damage(self, damage, knockback=0):
        """Take damage from opponent"""
        if self.hit_cooldown <= 0:
            if self.is_blocking:
                damage = int(damage * BLOCK_DAMAGE_REDUCTION)
            self.health = max(0, self.health - damage)
            self.hit_cooldown = 10
            self.knockback_vel_x = knockback
    
    def recover_energy(self):
        """Gradually recover energy"""
        if not self.is_blocking and self.current_attack is None:
            self.energy = min(self.max_energy, self.energy + 0.5)
    
    def update(self):
        """Update character state"""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
            self.vel_y = min(self.vel_y, MAX_VELOCITY)
        
        # Apply knockback
        if self.knockback_vel_x != 0:
            self.x += self.knockback_vel_x
            self.knockback_vel_x *= 0.9
            if abs(self.knockback_vel_x) < 0.1:
                self.knockback_vel_x = 0
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Ground collision
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.on_ground = True
        
        # Screen boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        
        # Update timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_counter = 0
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        
        # Energy recovery
        self.recover_energy()
        
        # Animation
        self.anim_frame += self.anim_speed
        if self.anim_frame > 10:
            self.anim_frame = 0
    
    def get_rect(self):
        """Get character bounding box"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_attack_rect(self):
        """Get attack hitbox"""
        if self.current_attack is None:
            return None
        
        attack_type, _ = self.current_attack
        
        if attack_type == "punch":
            width = PUNCH_RANGE
            x_offset = self.direction * self.width
        elif attack_type == "kick":
            width = KICK_RANGE
            x_offset = self.direction * (self.width + 10)
        elif attack_type == "special":
            width = SPECIAL_RANGE
            x_offset = self.direction * (self.width + 20)
        else:
            return None
        
        if self.direction == -1:
            x = self.x - width
        else:
            x = self.x + width
        
        return pygame.Rect(x, self.y + 20, width, self.height - 40)
    
    def _get_character_color(self):
        """Get character base color"""
        if self.character_type == "Kyo":
            return (255, 120, 0)  # Orange
        elif self.character_type == "Iori":
            return (220, 20, 60)  # Crimson
        elif self.character_type == "Mai":
            return (255, 80, 120)  # Pink
        else:  # Ryo
            return (70, 130, 180)  # Steel blue
    
    def draw(self, surface):
        """Draw character with smooth cartoon style"""
        # Get character color
        if self.hit_cooldown > 0:
            base_color = self._get_character_color()
            # Flash effect when hit
            flash_intensity = (self.hit_cooldown / 10.0)
            color = (
                int(base_color[0] + (255 - base_color[0]) * flash_intensity),
                int(base_color[1] * (1 - flash_intensity * 0.5)),
                int(base_color[2] * (1 - flash_intensity * 0.5))
            )
        elif self.is_blocking:
            color = (100, 150, 255)  # Blue tint when blocking
        else:
            color = self._get_character_color()
        
        # Animation offset for idle bobbing
        bob = 0
        if self.on_ground and abs(self.vel_x) < 0.5:
            bob = int(2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500 - 2)
        
        # Center positions
        cx = self.x + self.width // 2
        cy = self.y + bob
        
        # ===== SHADOW =====
        shadow_width = int(self.width * 1.3)
        shadow_height = 12
        for i in range(shadow_height):
            alpha_ratio = 1 - (i / shadow_height)
            shadow_rect = pygame.Rect(cx - shadow_width // 2, GROUND_Y + i, shadow_width, 1)
            pygame.draw.line(surface, (20, 20, 30), (cx - shadow_width // 2, GROUND_Y + i), 
                           (cx + shadow_width // 2, GROUND_Y + i))
        
        # ===== HEAD =====
        head_radius = 16
        head_y = cy + 8
        
        # Main head circle
        pygame.draw.circle(surface, color, (int(cx), int(head_y)), head_radius)
        
        # Head highlight (3D sphere effect)
        highlight_color = tuple(min(255, c + 80) for c in color)
        pygame.draw.circle(surface, highlight_color, (int(cx - 7), int(head_y - 8)), 7)
        
        # Head shadow (darker bottom)
        shadow_color = tuple(max(0, c - 60) for c in color)
        pygame.draw.circle(surface, shadow_color, (int(cx + 8), int(head_y + 8)), 6)
        
        # Head outline
        pygame.draw.circle(surface, (0, 0, 0), (int(cx), int(head_y)), head_radius, 3)
        
        # ===== EYES - Cartoon Style =====
        eye_spacing = 10
        left_eye_x = cx - eye_spacing
        right_eye_x = cx + eye_spacing
        eye_y = head_y - 4
        
        # Eye whites (larger for cartoon look)
        pygame.draw.circle(surface, WHITE, (int(left_eye_x), int(eye_y)), 5)
        pygame.draw.circle(surface, WHITE, (int(right_eye_x), int(eye_y)), 5)
        
        # Eyebrows
        brow_color = (0, 0, 0)
        pygame.draw.line(surface, brow_color, (int(left_eye_x - 6), int(eye_y - 8)), 
                        (int(left_eye_x + 6), int(eye_y - 7)), 2)
        pygame.draw.line(surface, brow_color, (int(right_eye_x - 6), int(eye_y - 7)), 
                        (int(right_eye_x + 6), int(eye_y - 8)), 2)
        
        # Pupils looking toward opponent
        pupil_offset = 3 if self.direction > 0 else -3
        pygame.draw.circle(surface, BLACK, (int(left_eye_x + pupil_offset), int(eye_y)), 3)
        pygame.draw.circle(surface, BLACK, (int(right_eye_x + pupil_offset), int(eye_y)), 3)
        
        # Eye shine (glossy effect)
        pygame.draw.circle(surface, WHITE, (int(left_eye_x + pupil_offset - 1), int(eye_y - 1)), 1)
        pygame.draw.circle(surface, WHITE, (int(right_eye_x + pupil_offset - 1), int(eye_y - 1)), 1)
        
        # ===== NOSE =====
        nose_points = [
            (int(cx), int(eye_y + 4)),
            (int(cx - 2), int(eye_y + 9)),
            (int(cx + 2), int(eye_y + 9))
        ]
        pygame.draw.polygon(surface, (220, 150, 100), nose_points)
        pygame.draw.polygon(surface, (0, 0, 0), nose_points, 1)
        
        # ===== MOUTH - Expressive =====
        mouth_y = eye_y + 11
        mouth_width = 7
        mouth_color = (140, 0, 0)
        # Mouth line
        pygame.draw.line(surface, mouth_color, (int(cx - mouth_width), int(mouth_y)), 
                        (int(cx + mouth_width), int(mouth_y)), 2)
        # Smile curve
        pygame.draw.arc(surface, (100, 0, 0), 
                       pygame.Rect(int(cx - mouth_width - 2), int(mouth_y - 2), 
                                 mouth_width * 2 + 4, 6), 0, 3.14, 2)
        
        # ===== HAIR - Character Specific =====
        if self.character_type == "Kyo":
            # Spiky blonde hair
            hair_color = (255, 220, 0)
            dark_hair = (200, 170, 0)
            for i in range(-2, 3):
                spike_x = cx + i * 7
                spike_base_y = head_y - head_radius - 2
                spike_tip_y = spike_base_y - 12
                pygame.draw.line(surface, hair_color, (int(spike_x), int(spike_base_y)), 
                               (int(spike_x), int(spike_tip_y)), 3)
                pygame.draw.line(surface, dark_hair, (int(spike_x), int(spike_base_y)), 
                               (int(spike_x), int(spike_tip_y)), 1)
        elif self.character_type == "Iori":
            # Dark spiky/disheveled hair
            hair_color = (15, 15, 20)
            for i in range(-2, 3):
                spike_x = cx + i * 7
                spike_base_y = head_y - head_radius - 1
                spike_tip_y = spike_base_y - 13
                pygame.draw.line(surface, hair_color, (int(spike_x), int(spike_base_y)), 
                               (int(spike_x), int(spike_tip_y)), 3)
        elif self.character_type == "Mai":
            # Long flowing hair with bows
            hair_color = (100, 50, 100)
            pygame.draw.circle(surface, hair_color, (int(cx - 18), int(head_y + 5)), 8)
            pygame.draw.circle(surface, hair_color, (int(cx + 18), int(head_y + 5)), 8)
        
        # ===== TORSO =====
        torso_width = 20
        torso_height = 32
        torso_color = tuple(max(0, c - 30) for c in color)
        
        # Main torso body
        pygame.draw.rect(surface, torso_color, 
                        (int(cx - torso_width // 2), int(cy + 24), torso_width, torso_height))
        
        # Torso highlight (right side lighter)
        torso_light = tuple(min(255, c + 60) for c in torso_color)
        pygame.draw.rect(surface, torso_light, 
                        (int(cx - torso_width // 2 + 2), int(cy + 26), 5, torso_height - 4))
        
        # Torso shadow (left side darker)
        torso_dark = tuple(max(0, c - 50) for c in torso_color)
        pygame.draw.rect(surface, torso_dark, 
                        (int(cx + torso_width // 2 - 4), int(cy + 26), 4, torso_height - 4))
        
        # Torso outline
        pygame.draw.rect(surface, (0, 0, 0), 
                        (int(cx - torso_width // 2), int(cy + 24), torso_width, torso_height), 2)
        
        # ===== ARMS - With Joint Animation =====
        arm_length = 22
        arm_width = 6
        shoulder_y = cy + 28
        
        # Arm angle changes when attacking
        arm_angle_left = -40 if self.current_attack and self.direction > 0 else 20
        arm_angle_right = 40 if self.current_attack and self.direction < 0 else -20
        
        arm_color = color
        
        # Left arm
        left_shoulder_x = cx - torso_width // 2 - 3
        left_elbow_x = left_shoulder_x - int(arm_length * 0.6 * (1 if self.direction > 0 else -1))
        left_hand_x = left_shoulder_x - arm_length * (1 if self.direction > 0 else -1)
        left_hand_y = shoulder_y + 8
        
        # Upper arm
        pygame.draw.line(surface, arm_color, (int(left_shoulder_x), int(shoulder_y)), 
                        (int(left_elbow_x), int(left_hand_y - 3)), arm_width)
        # Lower arm (forearm)
        pygame.draw.line(surface, arm_color, (int(left_elbow_x), int(left_hand_y - 3)), 
                        (int(left_hand_x), int(left_hand_y)), arm_width)
        # Hand
        pygame.draw.circle(surface, arm_color, (int(left_hand_x), int(left_hand_y)), 4)
        
        # Right arm
        right_shoulder_x = cx + torso_width // 2 + 3
        right_elbow_x = right_shoulder_x + int(arm_length * 0.6 * (1 if self.direction > 0 else -1))
        right_hand_x = right_shoulder_x + arm_length * (1 if self.direction > 0 else -1)
        right_hand_y = shoulder_y + 8
        
        # Upper arm
        pygame.draw.line(surface, arm_color, (int(right_shoulder_x), int(shoulder_y)), 
                        (int(right_elbow_x), int(right_hand_y - 3)), arm_width)
        # Lower arm (forearm)
        pygame.draw.line(surface, arm_color, (int(right_elbow_x), int(right_hand_y - 3)), 
                        (int(right_hand_x), int(right_hand_y)), arm_width)
        # Hand
        pygame.draw.circle(surface, arm_color, (int(right_hand_x), int(right_hand_y)), 4)
        
        # ===== ATTACK GLOW EFFECT =====
        if self.current_attack:
            glow_color = (255, 180, 0)
            pygame.draw.circle(surface, glow_color, (int(left_hand_x), int(left_hand_y)), 8, 2)
            pygame.draw.circle(surface, glow_color, (int(right_hand_x), int(right_hand_y)), 8, 2)
        
        # ===== LEGS =====
        leg_width = 7
        leg_height = 28
        leg_color = tuple(max(0, c - 60) for c in color)
        
        # Leg animation (slight sway when moving)
        leg_offset = 0
        if abs(self.vel_x) > 0.3:
            leg_offset = int(3 * abs(pygame.time.get_ticks() % 600 - 300) / 300 - 3)
        
        # Left leg
        left_leg_x = cx - 6
        pygame.draw.rect(surface, leg_color, 
                        (int(left_leg_x + leg_offset), int(cy + 56), leg_width, leg_height))
        pygame.draw.rect(surface, (min(255, leg_color[0] + 40), min(255, leg_color[1] + 40), 
                                 min(255, leg_color[2] + 40)), 
                        (int(left_leg_x + leg_offset + 2), int(cy + 58), 2, leg_height - 4))
        pygame.draw.rect(surface, (0, 0, 0), 
                        (int(left_leg_x + leg_offset), int(cy + 56), leg_width, leg_height), 1)
        
        # Right leg
        right_leg_x = cx + 1
        pygame.draw.rect(surface, leg_color, 
                        (int(right_leg_x - leg_offset), int(cy + 56), leg_width, leg_height))
        pygame.draw.rect(surface, (min(255, leg_color[0] + 40), min(255, leg_color[1] + 40), 
                                 min(255, leg_color[2] + 40)), 
                        (int(right_leg_x - leg_offset + 2), int(cy + 58), 2, leg_height - 4))
        pygame.draw.rect(surface, (0, 0, 0), 
                        (int(right_leg_x - leg_offset), int(cy + 56), leg_width, leg_height), 1)
        
        # ===== SHOES =====
        shoe_color = (0, 0, 0)
        shoe_width = 9
        shoe_height = 5
        
        # Left shoe
        pygame.draw.ellipse(surface, shoe_color, 
                          pygame.Rect(int(left_leg_x + leg_offset - 1), int(cy + 84), shoe_width + 1, shoe_height))
        pygame.draw.line(surface, (60, 60, 80), (int(left_leg_x + leg_offset + 1), int(cy + 85)), 
                        (int(left_leg_x + leg_offset + shoe_width - 2), int(cy + 85)), 1)
        
        # Right shoe
        pygame.draw.ellipse(surface, shoe_color, 
                          pygame.Rect(int(right_leg_x - leg_offset - 1), int(cy + 84), shoe_width + 1, shoe_height))
        pygame.draw.line(surface, (60, 60, 80), (int(right_leg_x - leg_offset + 1), int(cy + 85)), 
                        (int(right_leg_x - leg_offset + shoe_width - 2), int(cy + 85)), 1)
        
        # ===== STATUS BARS WITH POLISH =====
        health_bar_width = 140
        health_bar_height = 18
        health_bar_x = cx - health_bar_width // 2
        health_bar_y = cy - 70
        
        # Bar background with glow
        pygame.draw.rect(surface, (0, 0, 0), (int(health_bar_x - 4), int(health_bar_y - 4), 
                                            health_bar_width + 8, health_bar_height + 8))
        pygame.draw.rect(surface, (30, 30, 40), (int(health_bar_x), int(health_bar_y), 
                                               health_bar_width, health_bar_height))
        
        # Health bar
        health_percent = self.health / self.max_health
        health_color = GREEN if health_percent > 0.5 else YELLOW if health_percent > 0.25 else RED
        health_fill_width = health_percent * health_bar_width
        pygame.draw.rect(surface, health_color, (int(health_bar_x), int(health_bar_y), 
                                               int(health_fill_width), health_bar_height))
        
        # Health bar shine
        if health_fill_width > 4:
            pygame.draw.line(surface, WHITE, (int(health_bar_x + 2), int(health_bar_y + 2)), 
                            (int(health_bar_x + health_fill_width - 2), int(health_bar_y + 2)), 1)
        
        # Health bar border
        pygame.draw.rect(surface, WHITE, (int(health_bar_x), int(health_bar_y), 
                                        health_bar_width, health_bar_height), 2)
        
        # Energy bar
        energy_bar_y = health_bar_y + 22
        pygame.draw.rect(surface, (30, 30, 60), (int(health_bar_x), int(energy_bar_y), 
                                               health_bar_width, 10))
        energy_percent = self.energy / self.max_energy
        pygame.draw.rect(surface, (100, 200, 255), (int(health_bar_x), int(energy_bar_y), 
                                        int(health_bar_width * energy_percent), 10))
        
        # Energy bar shine
        if energy_percent * health_bar_width > 2:
            pygame.draw.line(surface, WHITE, (int(health_bar_x + 2), int(energy_bar_y + 2)), 
                            (int(health_bar_x + health_bar_width * energy_percent - 2), int(energy_bar_y + 2)), 1)
        
        pygame.draw.rect(surface, (100, 200, 255), (int(health_bar_x), int(energy_bar_y), 
                                        health_bar_width, 10), 2)
        
        # ===== SPECIAL ATTACK AURA =====
        if self.current_attack:
            attack_type, _ = self.current_attack
            if attack_type == "special":
                # Dramatic multi-layer aura
                aura_y = cy + 30
                pygame.draw.circle(surface, (255, 200, 0), (int(cx), int(aura_y)), 32, 3)
                pygame.draw.circle(surface, (255, 150, 0), (int(cx), int(aura_y)), 38, 1)
                pygame.draw.circle(surface, (255, 100, 0), (int(cx), int(aura_y)), 26, 2)
        
        # ===== BLOCKING EFFECT =====
        if self.is_blocking:
            block_aura_y = cy + 30
            pygame.draw.circle(surface, (100, 150, 255), (int(cx), int(block_aura_y)), 50, 2)
            pygame.draw.circle(surface, (150, 200, 255), (int(cx), int(block_aura_y)), 45, 1)
