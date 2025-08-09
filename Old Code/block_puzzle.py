"""
Block Puzzle - Pygame
- 8x8 board
- Modern UI
- Horizontal tray (3x3 slots)
- 3-move combo window + simultaneous-clear multiplier
- High score persistence
- Piece Valid Checker + Smart Snap-to-valid
- Continuous no-move detection -> Game Over screen
- Home, Replay, and always-present Settings button
- Animated combo glow around Score when combo active
- "Combo xN" popup on board (scales, floats, fades)

Run:
    pip install pygame
    python block_puzzle.py
"""

import pygame
import random
import sys
import os
import math
from math import inf

# =======================
# CONFIG / CONSTANTS
# =======================
CELL = 40
BOARD_SIZE = 8
MARGIN = 10

# Tray: 3 slots horizontally, each 3x3 cells
TRAY_SLOTS = 3
SLOT_W_CELLS = 3
SLOT_H_CELLS = 3

# HUD height
HUD_H = 60

# Scoring & combo rules
POINTS_PER_LINE = 10             # base points per line
SIMUL_CLEAR_CAP = 6              # cap for simultaneous-clear multiplier
COMBO_LEVEL_BONUS = 0.10         # +10% per extra combo level after x1
COMBO_WINDOW_MOVES = 3           # must clear again within 3 placements to continue streak

# Colors
BG = (245, 246, 248)        # app background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PANEL = (235, 238, 242)     # panel fill (HUD, tray)
GRID_LINE = (70, 70, 80)    # softer grid lines
PREVIEW_OK = (60, 180, 75)  # green-ish for OK overlays
PREVIEW_BAD = (200, 60, 60) # red-ish for blocked overlays
BTN_BG = (230, 234, 240)
BTN_BG_HOVER = (210, 216, 225)

PIECE_COLORS = [
    (255, 99, 71), (60, 179, 113), (65, 105, 225), (218, 112, 214),
    (255, 215, 0), (70, 130, 180), (244, 164, 96), (199, 21, 133)
]

# Predefined pieces (no rotation)
PIECES = [
    [[1]],
    [[1, 1]],
    [[1, 1, 1]],
    [[1], [1]],
    [[1, 1], [1, 1]],
    [[1, 0], [1, 0], [1, 1]],           # L
    [[1, 1, 1], [0, 1, 0]],             # T
    [[1, 1, 0], [0, 1, 1]],             # S
    [[1, 1, 1, 1]],
    [[1, 0], [1, 0], [1, 0], [1, 0]],   # long vertical
    [[1, 1, 0], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
]

# --- Derived geometry ---
board_w = BOARD_SIZE * CELL
board_h = BOARD_SIZE * CELL

slot_w = SLOT_W_CELLS * CELL
slot_h = SLOT_H_CELLS * CELL
total_tray_w = TRAY_SLOTS * slot_w + (TRAY_SLOTS - 1) * MARGIN + 2 * MARGIN
TRAY_HEIGHT = slot_h + 2 * MARGIN

WIDTH = max(2 * MARGIN + board_w, total_tray_w)
HEIGHT = MARGIN + HUD_H + MARGIN + board_h + MARGIN + TRAY_HEIGHT + MARGIN
FPS = 60

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_SETTINGS = "settings"

# =======================
# UI HELPERS / EFFECTS
# =======================
def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_shadowed_panel(surface, fill_color, rect, radius=12, shadow_offset=(2, 2), shadow_color=(0, 0, 0, 40)):
    sx, sy = shadow_offset
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, shadow_color, shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.x + sx, rect.y + sy))
    draw_rounded_rect(surface, fill_color, rect, radius)

def lerp(a, b, t):
    return a + (b - a) * t

def color_lerp(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
    )

def draw_combo_glow(surface, rect, t, layers=12, radius=12):
    """
    Animated layered glow outlines around rect.
    't' animates color cycling. Cheap but pretty.
    """
    palette = [(255, 80, 80), (255, 200, 80), (80, 200, 255), (160, 80, 255)]
    phase = (math.sin(t * 1.3) + 1) * 0.5  # 0..1
    for i in range(layers):
        u = i / max(1, layers - 1)  # 0..1 innerness
        idx = int((u + phase) * (len(palette) - 1)) % (len(palette) - 1)
        c1 = palette[idx]
        c2 = palette[(idx + 1) % len(palette)]
        c = color_lerp(c1, c2, phase)
        alpha = int(120 * (1.0 - u))
        col = (*c, alpha)

        inset = int(lerp(0, 8, u))
        layer_rect = rect.inflate(-2 * inset, -2 * inset)

        s = pygame.Surface((layer_rect.width, layer_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, col, s.get_rect(), border_radius=radius, width=2)
        surface.blit(s, layer_rect.topleft)

# =======================
# WIDGETS
# =======================
class Button:
    def __init__(self, rect, label, font, on_click):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font
        self.on_click = on_click
        self.hover = False

    def draw(self, surf):
        color = BTN_BG_HOVER if self.hover else BTN_BG
        draw_rounded_rect(surf, color, self.rect, radius=10)
        txt = self.font.render(self.label, True, BLACK)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()

# =======================
# MODEL
# =======================
class Piece:
    def __init__(self, shape=None):
        self.shape = shape if shape is not None else random.choice(PIECES)
        self.color = random.choice(PIECE_COLORS)
        self.width = len(self.shape[0])
        self.height = len(self.shape)

    def cells(self):
        for r, row in enumerate(self.shape):
            for c, v in enumerate(row):
                if v:
                    yield (r, c)

class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def can_place(self, piece, board_r, board_c):
        for r, c in piece.cells():
            br = board_r + r
            bc = board_c + c
            if br < 0 or br >= BOARD_SIZE or bc < 0 or bc >= BOARD_SIZE:
                return False
            if self.grid[br][bc]:
                return False
        return True

    def place(self, piece, board_r, board_c, color_idx=1):
        for r, c in piece.cells():
            br = board_r + r
            bc = board_c + c
            self.grid[br][bc] = color_idx

    def clear_full_lines(self):
        full_rows = [i for i, row in enumerate(self.grid) if all(row)]
        full_cols = [j for j in range(BOARD_SIZE) if all(self.grid[i][j] for i in range(BOARD_SIZE))]
        cleared = 0
        if full_rows:
            for r in full_rows:
                for c in range(BOARD_SIZE):
                    self.grid[r][c] = 0
            cleared += len(full_rows)
        if full_cols:
            for c in full_cols:
                for r in range(BOARD_SIZE):
                    self.grid[r][c] = 0
            cleared += len(full_cols)
        return cleared

    def has_moves(self, pieces):
        for p in pieces:
            if p is None:
                continue
            for r in range(BOARD_SIZE - p.height + 1):
                for c in range(BOARD_SIZE - p.width + 1):
                    if self.can_place(p, r, c):
                        return True
        return False

# =======================
# GAME
# =======================
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Block Puzzle - Py (8x8)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeui,arial", 24)
        self.big_font = pygame.font.SysFont("segoeui,arial", 72)
        self.mid_font = pygame.font.SysFont("segoeui,arial", 32)

        # High score
        self.high_score_path = "highscore.txt"
        self.high_score = self.load_high_score()

        # Animation time
        self.anim_t = 0.0   # drives glow animation & can be reused

        self.state = STATE_MENU
        self.reset()

        # UI Buttons
        self.settings_btn = Button(pygame.Rect(MARGIN, MARGIN, 120, 36), "Settings", self.font, self.open_settings)
        self.menu_play_btn = Button(pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 20, 160, 44), "Play", self.mid_font, self.start_game)
        self.over_home_btn = Button(pygame.Rect(WIDTH//2 - 180, HEIGHT//2 + 60, 160, 44), "Home", self.mid_font, self.go_home)
        self.over_replay_btn = Button(pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 60, 160, 44), "Replay", self.mid_font, self.start_game)

    # --- High score ---
    def load_high_score(self):
        try:
            if os.path.exists(self.high_score_path):
                with open(self.high_score_path, "r", encoding="utf-8") as f:
                    return int(f.read().strip() or "0")
        except Exception:
            pass
        return 0

    def save_high_score(self):
        try:
            with open(self.high_score_path, "w", encoding="utf-8") as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    # --- Layout helpers ---
    def hud_rect(self):
        return pygame.Rect(MARGIN, MARGIN, WIDTH - 2 * MARGIN, HUD_H)

    def board_rect(self):
        x = (WIDTH - board_w) // 2
        y = MARGIN + HUD_H + MARGIN
        return pygame.Rect(x, y, board_w, board_h)

    def tray_rect(self):
        return pygame.Rect(0, HEIGHT - TRAY_HEIGHT, WIDTH, TRAY_HEIGHT)

    # --- State transitions ---
    def reset(self):
        self.board = Board()
        self.score = 0
        self.pieces = [Piece(random.choice(PIECES)) for _ in range(TRAY_SLOTS)]
        self.tray_positions = []
        self.selected = None

        # Combo (3-move window)
        self.combo_streak = 0
        self.max_combo_streak = 0
        self.last_clear_count = 0
        self.moves_since_last_clear = COMBO_WINDOW_MOVES  # start "expired"

        # Combo popups
        self.combo_popups = []

        self.update_tray_positions()

    def start_game(self):
        self.reset()
        self.state = STATE_PLAYING

    def go_home(self):
        self.state = STATE_MENU

    def open_settings(self):
        self.state = STATE_SETTINGS

    # --- Tray slots ---
    def update_tray_positions(self):
        self.tray_positions = []
        y = HEIGHT - MARGIN - (SLOT_H_CELLS * CELL)
        total_w = TRAY_SLOTS * (SLOT_W_CELLS * CELL) + (TRAY_SLOTS - 1) * MARGIN
        start_x = (WIDTH - total_w) // 2
        for i in range(TRAY_SLOTS):
            x = start_x + i * ((SLOT_W_CELLS * CELL) + MARGIN)
            self.tray_positions.append(pygame.Rect(x, y, SLOT_W_CELLS * CELL, SLOT_H_CELLS * CELL))

    # --- Main loop ---
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.anim_t += dt

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                # Global: settings button always present
                self.settings_btn.handle_event(event)

                if self.state == STATE_MENU:
                    self.menu_play_btn.handle_event(event)

                elif self.state == STATE_SETTINGS:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

                elif self.state == STATE_GAME_OVER:
                    self.over_home_btn.handle_event(event)
                    self.over_replay_btn.handle_event(event)

                elif self.state == STATE_PLAYING:
                    self.handle_play_events(event)

            # Auto game-over detection when playing (and not dragging)
            if self.state == STATE_PLAYING and self.selected is None:
                if not self.board.has_moves([p for p in self.pieces if p is not None]):
                    self.state = STATE_GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()

            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # --- Event handling during play ---
    def handle_play_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            # pick up a piece if clicked inside a slot
            for i, rect in enumerate(self.tray_positions):
                if rect.collidepoint(mx, my) and self.pieces[i] is not None:
                    self.selected = (i, mx, my)
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.selected is not None:
                self.try_place_selected_with_snap()
                self.selected = None

    # --- Smart snap-to-valid when releasing a piece ---
    def try_place_selected_with_snap(self):
        idx, sx, sy = self.selected
        p = self.pieces[idx]
        mx, my = pygame.mouse.get_pos()

        # Convert mouse to "intended" board top-left by centering the piece under the mouse
        br, bc = self.screen_to_board_anywhere(mx, my)
        if br is not None:
            # find the best valid placement near the intended top-left
            best = self.find_best_placement(p, br, bc)
            if best is not None:
                r0, c0 = best
                color_idx = PIECE_COLORS.index(p.color) + 1
                self.board.place(p, r0, c0, color_idx)
                placed_cells = sum(sum(row) for row in p.shape)
                self.score += placed_cells

                # clear + scoring
                cleared = self.board.clear_full_lines()
                self.last_clear_count = cleared

                if cleared > 0:
                    base_clear = POINTS_PER_LINE * cleared
                    multi = min(cleared, SIMUL_CLEAR_CAP)
                    clear_points = base_clear * multi
                    # combo window update
                    if self.moves_since_last_clear < COMBO_WINDOW_MOVES and self.combo_streak > 0:
                        self.combo_streak += 1
                    else:
                        self.combo_streak = 1
                    self.max_combo_streak = max(self.max_combo_streak, self.combo_streak)
                    self.moves_since_last_clear = 0

                    combo_multiplier = 1.0 + COMBO_LEVEL_BONUS * (self.combo_streak - 1)
                    clear_points = int(clear_points * combo_multiplier)
                    self.score += clear_points

                    # spawn "Combo xN" popup at the placed piece center
                    self.spawn_combo_popup(r0, c0)
                else:
                    self.moves_since_last_clear += 1
                    if self.moves_since_last_clear >= COMBO_WINDOW_MOVES:
                        self.combo_streak = 0

                # high score update now
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

                # consume piece, refill if needed
                self.pieces[idx] = None
                if all(x is None for x in self.pieces):
                    self.pieces = [Piece(random.choice(PIECES)) for _ in range(TRAY_SLOTS)]
                    # immediate no-move check on new set
                    if not self.board.has_moves(self.pieces):
                        self.state = STATE_GAME_OVER
                        return
                self.update_tray_positions()
                return
        # If we reach here, no valid placement found -> do nothing (piece returns to tray)

    def screen_to_board_anywhere(self, sx, sy):
        """Compute nearest integer cell (clamped) even if slightly off board."""
        brect = self.board_rect()
        fx = (sx - brect.x) / CELL
        fy = (sy - brect.y) / CELL
        bc = round(fx)
        br = round(fy)
        br = max(0, min(BOARD_SIZE - 1, br))
        bc = max(0, min(BOARD_SIZE - 1, bc))
        return br, bc

    def find_best_placement(self, piece, intended_r, intended_c):
        """Return valid (r,c) whose top-left is Manhattan-closest to intended."""
        best_pos = None
        best_dist = inf
        for r in range(BOARD_SIZE - piece.height + 1):
            for c in range(BOARD_SIZE - piece.width + 1):
                if self.board.can_place(piece, r, c):
                    d = abs(r - intended_r) + abs(c - intended_c)
                    if d < best_dist:
                        best_dist = d
                        best_pos = (r, c)
        return best_pos

    # --- Combo popup ---
    def spawn_combo_popup(self, r_cell, c_cell):
        # center of the placed piece area
        brect = self.board_rect()
        x = brect.x + c_cell * CELL + CELL // 2
        y = brect.y + r_cell * CELL + CELL // 2
        self.combo_popups.append({
            "t": 0.0,
            "duration": 1.0,      # seconds
            "x": x,
            "y_start": y,
            "y_end": y - 40,
            "scale_start": 1.0,
            "scale_end": 1.3,
            "text": f"Combo x{self.combo_streak}",
        })

    def update_and_draw_combo_popups(self):
        alive = []
        for p in self.combo_popups:
            p["t"] += self.dt  # use frame dt
            u = min(1.0, p["t"] / p["duration"])
            # smoothstep easing
            u_ease = u * u * (3 - 2 * u)

            y = int(lerp(p["y_start"], p["y_end"], u_ease))
            scale = lerp(p["scale_start"], p["scale_end"], u_ease)
            alpha = int(255 * (1.0 - u_ease))

            txt = self.big_font.render(p["text"], True, (30, 120, 30))
            w, h = txt.get_width(), txt.get_height()
            sw, sh = int(w * scale), int(h * scale)
            txt = pygame.transform.smoothscale(txt, (max(1, sw), max(1, sh)))
            txt.set_alpha(alpha)
            self.screen.blit(txt, txt.get_rect(center=(p["x"], y)))

            if u < 1.0:
                alive.append(p)
        self.combo_popups = alive

    # --- Helpers ---
    def screen_to_board(self, sx, sy):
        brect = self.board_rect()
        if not brect.collidepoint(sx, sy):
            return None, None
        c = (sx - brect.x) // CELL
        r = (sy - brect.y) // CELL
        if r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE:
            return None, None
        return r, c

    # --- Drawing ---
    def draw_board_panel(self):
        brect = self.board_rect()
        draw_shadowed_panel(self.screen, WHITE, brect, radius=12)
        # Grid
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell_rect = pygame.Rect(brect.x + c * CELL, brect.y + r * CELL, CELL - 1, CELL - 1)
                val = self.board.grid[r][c]
                if val:
                    color = PIECE_COLORS[(val - 1) % len(PIECE_COLORS)]
                    pygame.draw.rect(self.screen, color, cell_rect, border_radius=6)
                else:
                    pygame.draw.rect(self.screen, WHITE, cell_rect, border_radius=6)
                    pygame.draw.rect(self.screen, GRID_LINE, cell_rect, 1, border_radius=6)

    def draw_tray_panel(self):
        trect = self.tray_rect()
        draw_shadowed_panel(self.screen, PANEL, trect, radius=12)

        # Outline slots; color code by "has at least one valid move"
        for i, rect in enumerate(self.tray_positions):
            p = self.pieces[i] if i < len(self.pieces) else None
            can_fit = False
            if p is not None:
                can_fit = self.board.has_moves([p])
            border_color = PREVIEW_OK if can_fit else (220, 224, 230)
            pygame.draw.rect(self.screen, border_color, rect, border_radius=10, width=2)

        # pieces in tray (centered)
        for i, p in enumerate(self.pieces):
            rect = self.tray_positions[i]
            if p is None:
                continue
            if self.selected and self.selected[0] == i:
                mx, my = pygame.mouse.get_pos()
                draw_x = mx - (p.width * CELL) // 2
                draw_y = my - (p.height * CELL) // 2
                self.draw_piece_at(p, draw_x, draw_y)
            else:
                px = rect.x + (rect.width - p.width * CELL) // 2
                py = rect.y + (rect.height - p.height * CELL) // 2
                self.draw_piece_at(p, px, py)

    def draw_hud(self):
        hrect = self.hud_rect()
        draw_shadowed_panel(self.screen, PANEL, hrect, radius=12)
        # Always-visible Settings button
        self.settings_btn.draw(self.screen)

        # Prepare score text (but don't blit yet)
        score_surf = self.font.render(f"Score: {self.score}", True, BLACK)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (hrect.x + 140, hrect.y + 16)

        # If combo is active, draw an animated glow behind the score
        if self.combo_streak > 0:
            glow_pad = 12  # padding around the score text
            glow_rect = pygame.Rect(
                score_rect.x - glow_pad,
                score_rect.y - glow_pad,
                score_rect.width + 2 * glow_pad,
                score_rect.height + 2 * glow_pad
            )
            draw_combo_glow(self.screen, glow_rect, self.anim_t, layers=12, radius=10)

        # Now draw Score & High Score
        self.screen.blit(score_surf, score_rect)
        hs_txt = self.font.render(f"High: {self.high_score}", True, BLACK)
        self.screen.blit(hs_txt, (hrect.x + 280, hrect.y + 16))

        # HUD Combo: keep combo text + small bar, but NO window counter
        if self.combo_streak > 0:
            combo_txt = self.font.render(f"Combo x{self.combo_streak}", True, (30, 120, 30))
            self.screen.blit(combo_txt, (hrect.right - 260, hrect.y + 12))

            # small progress bar based on clears from last move (0..4 typical)
            bar_w, bar_h = 160, 10
            bar_x = hrect.right - 260
            bar_y = hrect.y + 38
            pygame.draw.rect(self.screen, (220, 220, 220), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
            fill_w = int(bar_w * min(self.last_clear_count, 4) / 4)
            pygame.draw.rect(self.screen, PREVIEW_OK, (bar_x, bar_y, fill_w, bar_h), border_radius=6)

    def draw_piece_at(self, p, x, y):
        for r, row in enumerate(p.shape):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(x + c * CELL, y + r * CELL, CELL - 1, CELL - 1)
                    pygame.draw.rect(self.screen, p.color, rect, border_radius=6)
                    pygame.draw.rect(self.screen, GRID_LINE, rect, 1, border_radius=6)

    def draw_preview(self):
        if self.state != STATE_PLAYING or self.selected is None:
            return
        idx, sx, sy = self.selected
        p = self.pieces[idx]
        mx, my = pygame.mouse.get_pos()

        # preview based on nearest integer cell to mouse (even off-board)
        br, bc = self.screen_to_board_anywhere(mx, my)
        brect = self.board_rect()
        ok = self.board.can_place(p, br, bc)

        for r, c in p.cells():
            pr = br + r
            pc = bc + c
            if 0 <= pr < BOARD_SIZE and 0 <= pc < BOARD_SIZE:
                cell_rect = pygame.Rect(brect.x + pc * CELL, brect.y + pr * CELL, CELL - 1, CELL - 1)
                s = pygame.Surface((CELL - 1, CELL - 1), pygame.SRCALPHA)
                col = (PREVIEW_OK if ok else PREVIEW_BAD)
                s.fill((*col, 90 if ok else 60))
                self.screen.blit(s, cell_rect.topleft)

    # --- Screens ---
    def draw_menu(self):
        self.screen.fill(BG)
        title = self.big_font.render("Block Puzzle", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        self.menu_play_btn.draw(self.screen)
        # Settings available from menu too
        self.settings_btn.draw(self.screen)

    def draw_settings(self):
        self.screen.fill(BG)
        hrect = self.hud_rect()
        draw_shadowed_panel(self.screen, PANEL, hrect, radius=12)
        self.settings_btn.draw(self.screen)

        # Simple overlay panel
        rect = pygame.Rect(WIDTH//2 - 220, HEIGHT//2 - 150, 440, 300)
        draw_shadowed_panel(self.screen, WHITE, rect, radius=16)
        head = self.mid_font.render("Settings (placeholder)", True, BLACK)
        tip = self.font.render("Press ESC to go back", True, BLACK)
        self.screen.blit(head, head.get_rect(center=(WIDTH//2, rect.y + 40)))
        self.screen.blit(tip, tip.get_rect(center=(WIDTH//2, rect.y + 90)))

    def draw_game_over(self):
        self.screen.fill(BG)
        title = self.big_font.render("GAME OVER", True, (200, 0, 0))
        self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 80)))

        score_line = self.mid_font.render(f"Score: {self.score}", True, BLACK)
        hs_line = self.mid_font.render(f"High Score: {self.high_score}", True, BLACK)
        self.screen.blit(score_line, score_line.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
        self.screen.blit(hs_line, hs_line.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

        self.over_home_btn.draw(self.screen)
        self.over_replay_btn.draw(self.screen)

        # Settings still present
        self.settings_btn.draw(self.screen)

    def draw(self):
        # store dt on self for popup updater
        self.dt = 1.0 / FPS  # backup default
        # (anim_t already updated from main loop using real dt)
        self.screen.fill(BG)

        if self.state == STATE_MENU:
            self.draw_menu()
            return
        if self.state == STATE_SETTINGS:
            self.draw_settings()
            return
        if self.state == STATE_GAME_OVER:
            self.draw_game_over()
            return

        # STATE_PLAYING
        self.draw_hud()
        self.draw_board_panel()
        self.draw_tray_panel()
        self.draw_preview()
        self.update_and_draw_combo_popups()

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    Game().run()
