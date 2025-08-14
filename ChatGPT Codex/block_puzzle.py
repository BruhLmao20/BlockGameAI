"""
Block Puzzle - Pygame (Finalized Placement + Scoring)
- 8x8 board
- You ALWAYS hold the piece relative to where you grabbed it (no magnet drift)
- Predictive ghost shows ONLY the exact intended placement (no auto-snap to neighbors)
- Fixed right-edge placement (floor-based anchoring + clamping)
- Line-clear points use combo multiplier (e.g., 2 lines = 20pts, then × combo)
- Cell placement points are NOT multiplied
- Mid Info Bar: shows Combo xN (when active) + Last Points
- High score persistence
- Animated combo glow around Score when combo active
- “Combo xN” on-board popup (scale+float+fade)
- Game Over, Home, Settings

Run:
    pip install pygame
    python block_puzzle.py
"""

import pygame
import random
import sys
import os
import math
from math import inf, floor

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

# Heights
HUD_H = 60
MID_INFO_H = 40

# Scoring & combo rules
POINTS_PER_LINE = 10             # base points per line
SIMUL_CLEAR_CAP = 6              # cap for simultaneous-clear multiplier
COMBO_LEVEL_BONUS = 0.10         # +10% per extra combo level after x1
COMBO_WINDOW_MOVES = 3           # must clear again within 3 placements to continue streak

# Colors
BG = (245, 246, 248)        # app background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PANEL = (235, 238, 242)     # panel fill (HUD, info bar, tray)
GRID_LINE = (70, 70, 80)    # grid lines
PREVIEW_GHOST = (0, 0, 0, 70)  # ghost alpha fill
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
HEIGHT = (
    MARGIN + HUD_H + MARGIN +
    board_h + MARGIN +
    MID_INFO_H + MARGIN +
    TRAY_HEIGHT + MARGIN
)
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
    """Animated layered glow outlines around rect."""
    palette = [(255, 80, 80), (255, 200, 80), (80, 200, 255), (160, 80, 255)]
    phase = (math.sin(t * 1.3) + 1) * 0.5  # 0..1
    for i in range(layers):
        u = i / max(1, layers - 1)  # 0..1
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
        self.high_score_path = "../highscore.txt"
        self.high_score = self.load_high_score()

        # Animation time
        self.anim_t = 0.0   # drives glow animation

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

    def mid_info_rect(self):
        y = self.board_rect().bottom + MARGIN
        return pygame.Rect(MARGIN, y, WIDTH - 2 * MARGIN, MID_INFO_H)

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

        # Points accounting
        self.last_points = 0  # what you earned on your most recent placement

        # Combo popups
        self.combo_popups = []

        # Drag state
        self.drag_px_offset = (0, 0)   # pixel offset inside the piece at grab
        self.drag_cell_offset = (0, 0) # which cell in the piece was grabbed (r,c)

        # Effects
        self.place_pops = []

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
            self.dt = dt
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
                    # anchored drag offsets (keep hold position exact)
                    p = self.pieces[i]
                    px = rect.x + (rect.width - p.width * CELL) // 2
                    py = rect.y + (rect.height - p.height * CELL) // 2
                    self.drag_px_offset = (mx - px, my - py)
                    local_x = mx - px
                    local_y = my - py
                    cell_c = max(0, min(p.width  - 1,  local_x // CELL))
                    cell_r = max(0, min(p.height - 1,  local_y // CELL))
                    self.drag_cell_offset = (cell_r, cell_c)
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.selected is not None:
                self.try_place_selected_exact()
                self.selected = None

    # --- Convert cursor to intended TOP-LEFT for piece (floor + clamp) ---
    def intended_top_left(self, mouse_x, mouse_y, p):
        """
        Use floor (not round) to reduce right-edge jitter.
        Convert the anchor cell under cursor to TOP-LEFT based on grabbed cell.
        Clamp so the whole piece fits on board.
        """
        brect = self.board_rect()
        fx = (mouse_x - brect.x) / CELL
        fy = (mouse_y - brect.y) / CELL

        bc_anchor = int(math.floor(fx))
        br_anchor = int(math.floor(fy))

        grabbed_r, grabbed_c = self.drag_cell_offset
        br_tl = br_anchor - grabbed_r
        bc_tl = bc_anchor - grabbed_c

        # Clamp to keep the whole piece inside the board
        br_tl = max(0, min(BOARD_SIZE - p.height, br_tl))
        bc_tl = max(0, min(BOARD_SIZE - p.width,  bc_tl))
        return br_tl, bc_tl

    # --- Exact placement only (no neighbor snap). If invalid -> return to tray ---
    def try_place_selected_exact(self):
        idx, sx, sy = self.selected
        p = self.pieces[idx]
        mx, my = pygame.mouse.get_pos()

        br, bc = self.intended_top_left(mx, my, p)

        if not self.board.can_place(p, br, bc):
            return  # invalid -> back to tray

        # Place
        color_idx = PIECE_COLORS.index(p.color) + 1
        self.board.place(p, br, bc, color_idx)

        # Scoring: cells (no multiplier) + line clears (with combo multiplier)
        placed_cells = sum(sum(row) for row in p.shape)
        points_from_cells = placed_cells

        cleared = self.board.clear_full_lines()
        self.last_clear_count = cleared

        clear_points = 0
        if cleared > 0:
            # update combo window + streak
            if self.moves_since_last_clear < COMBO_WINDOW_MOVES and self.combo_streak > 0:
                self.combo_streak += 1
            else:
                self.combo_streak = 1
            self.max_combo_streak = max(self.max_combo_streak, self.combo_streak)
            self.moves_since_last_clear = 0

            base_clear = POINTS_PER_LINE * cleared
            # Apply combo multiplier ONLY to clear points
            combo_multiplier = 1.0 + COMBO_LEVEL_BONUS * (self.combo_streak - 1)
            clear_points = int(base_clear * min(cleared, SIMUL_CLEAR_CAP) * combo_multiplier)

            # Combo popup
            self.spawn_combo_popup(br, bc)
        else:
            self.moves_since_last_clear += 1
            if self.moves_since_last_clear >= COMBO_WINDOW_MOVES:
                self.combo_streak = 0

        self.last_points = points_from_cells + clear_points
        self.score += self.last_points

        # High score update
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        # Effect
        self.spawn_place_pop_effect(p, br, bc)

        # Consume piece; refill if all used
        self.pieces[idx] = None
        if all(x is None for x in self.pieces):
            self.pieces = [Piece(random.choice(PIECES)) for _ in range(TRAY_SLOTS)]
            if not self.board.has_moves(self.pieces):
                self.state = STATE_GAME_OVER
                return
        self.update_tray_positions()

    # --- Effects: combo popup + place pop ---
    def spawn_combo_popup(self, r_cell, c_cell):
        brect = self.board_rect()
        x = brect.x + c_cell * CELL + CELL // 2
        y = brect.y + r_cell * CELL + CELL // 2
        self.combo_popups.append({
            "t": 0.0,
            "duration": 1.0,
            "x": x,
            "y_start": y,
            "y_end": y - 40,
            "scale_start": 1.0,
            "scale_end": 1.3,
            "text": f"Combo x{self.combo_streak}",
        })

    def spawn_place_pop_effect(self, piece, r0, c0):
        brect = self.board_rect()
        for r, c in piece.cells():
            rr, cc = r0 + r, c0 + c
            rect = pygame.Rect(brect.x + cc * CELL, brect.y + rr * CELL, CELL - 1, CELL - 1)
            self.place_pops.append({"t": 0.0, "dur": 0.15, "rect": rect})

    def update_and_draw_combo_popups(self):
        alive = []
        for p in self.combo_popups:
            p["t"] += self.dt
            u = min(1.0, p["t"] / p["duration"])
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

    def update_and_draw_place_pops(self):
        alive = []
        for e in self.place_pops:
            e["t"] += self.dt
            u = min(1.0, e["t"] / e["dur"])
            alpha = int(180 * (1.0 - u))
            inset = int(3 * u)
            rect = e["rect"].inflate(-2 * inset, -2 * inset)
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((255, 255, 255, alpha))
            self.screen.blit(s, rect.topleft)
            if u < 1.0:
                alive.append(e)
        self.place_pops = alive

    # --- Drawing helpers ---
    def draw_piece_at(self, p, x, y):
        for r, row in enumerate(p.shape):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(x + c * CELL, y + r * CELL, CELL - 1, CELL - 1)
                    pygame.draw.rect(self.screen, p.color, rect, border_radius=6)
                    pygame.draw.rect(self.screen, GRID_LINE, rect, 1, border_radius=6)

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

    def draw_predictive_ghost(self):
        """Draw a snapped ghost ONLY at the exact intended placement (no neighbor snap)."""
        if self.state != STATE_PLAYING or self.selected is None:
            return
        idx, _, _ = self.selected
        p = self.pieces[idx]
        mx, my = pygame.mouse.get_pos()

        br, bc = self.intended_top_left(mx, my, p)
        if not self.board.can_place(p, br, bc):
            return  # invalid -> no ghost

        brect = self.board_rect()
        for r, c in p.cells():
            rr, cc = br + r, bc + c
            if 0 <= rr < BOARD_SIZE and 0 <= cc < BOARD_SIZE:
                cell_rect = pygame.Rect(brect.x + cc * CELL, brect.y + rr * CELL, CELL - 1, CELL - 1)
                s = pygame.Surface((CELL - 1, CELL - 1), pygame.SRCALPHA)
                s.fill(PREVIEW_GHOST)
                self.screen.blit(s, cell_rect.topleft)

    def draw_tray_panel(self):
        trect = self.tray_rect()
        draw_shadowed_panel(self.screen, PANEL, trect, radius=12)

        # pieces in tray (centered) or dragged (cursor-held)
        for i, p in enumerate(self.pieces):
            rect = self.tray_positions[i]
            pygame.draw.rect(self.screen, (220, 224, 230), rect, border_radius=10, width=2)

            if p is None:
                continue
            if self.selected and self.selected[0] == i:
                # You ALWAYS hold the piece under the cursor (no easing)
                mx, my = pygame.mouse.get_pos()
                draw_x = mx - self.drag_px_offset[0]
                draw_y = my - self.drag_px_offset[1]
                # tiny shadow
                shadow = pygame.Surface((p.width * CELL, p.height * CELL), pygame.SRCALPHA)
                shadow.fill((0, 0, 0, 60))
                self.screen.blit(shadow, (draw_x + 3, draw_y + 3))
                self.draw_piece_at(p, draw_x, draw_y)
            else:
                # piece resting in tray
                px = rect.x + (rect.width - p.width * CELL) // 2
                py = rect.y + (rect.height - p.height * CELL) // 2
                self.draw_piece_at(p, px, py)

    def draw_hud(self):
        hrect = self.hud_rect()
        draw_shadowed_panel(self.screen, PANEL, hrect, radius=12)
        # Settings button
        self.settings_btn.draw(self.screen)

        # Score (with optional combo glow only)
        score_surf = self.font.render(f"Score: {self.score}", True, BLACK)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (hrect.x + 140, hrect.y + 16)

        if self.combo_streak > 0:
            glow_pad = 12
            glow_rect = pygame.Rect(
                score_rect.x - glow_pad,
                score_rect.y - glow_pad,
                score_rect.width + 2 * glow_pad,
                score_rect.height + 2 * glow_pad
            )
            draw_combo_glow(self.screen, glow_rect, self.anim_t, layers=12, radius=10)

        self.screen.blit(score_surf, score_rect)

        hs_txt = self.font.render(f"High: {self.high_score}", True, BLACK)
        self.screen.blit(hs_txt, (hrect.x + 280, hrect.y + 16))
        # No combo text on HUD.

    def draw_mid_info(self):
        """Small bar between board and tray that shows Combo and Last Points."""
        rect = self.mid_info_rect()
        draw_shadowed_panel(self.screen, PANEL, rect, radius=12)

        x = rect.x + 14
        y = rect.y + 10

        # Last points earned
        lp_txt = self.font.render(f"+{self.last_points} pts" if self.last_points > 0 else "+0 pts", True, BLACK)
        self.screen.blit(lp_txt, (x, y))

        # Combo (only when active)
        if self.combo_streak > 0:
            combo_txt = self.font.render(f"Combo x{self.combo_streak}", True, (30, 120, 30))
            self.screen.blit(combo_txt, (rect.right - combo_txt.get_width() - 14, y))

    def draw_settings(self):
        self.screen.fill(BG)
        hrect = self.hud_rect()
        draw_shadowed_panel(self.screen, PANEL, hrect, radius=12)
        self.settings_btn.draw(self.screen)
        rect = pygame.Rect(WIDTH//2 - 220, HEIGHT//2 - 150, 440, 300)
        draw_shadowed_panel(self.screen, WHITE, rect, radius=16)
        head = self.mid_font.render("Settings (placeholder)", True, BLACK)
        tip = self.font.render("Press ESC to go back", True, BLACK)
        self.screen.blit(head, head.get_rect(center=(WIDTH//2, rect.y + 40)))
        self.screen.blit(tip, tip.get_rect(center=(WIDTH//2, rect.y + 90)))

    def draw_menu(self):
        self.screen.fill(BG)
        title = self.big_font.render("Block Puzzle", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        self.menu_play_btn.draw(self.screen)
        self.settings_btn.draw(self.screen)

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
        self.settings_btn.draw(self.screen)

    def draw(self):
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
        self.draw_predictive_ghost()  # ghost under the piece
        self.draw_tray_panel()        # then draw the held piece on top
        self.draw_mid_info()
        self.update_and_draw_combo_popups()
        self.update_and_draw_place_pops()

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    Game().run()
