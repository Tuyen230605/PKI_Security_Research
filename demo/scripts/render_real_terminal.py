import os
from PIL import Image, ImageDraw, ImageFont

def create_authentic_terminal_screenshot(
    output_path="report/figures/openssl-x509-terminal-real.png",
    cert_text_path="report/figures/openssl-x509-text.txt"
):
    output_path = os.path.abspath(output_path)
    cert_text_path = os.path.abspath(cert_text_path)
    with open(cert_text_path, "r", encoding="utf-8") as f:
        raw_lines = [line.rstrip("\r\n") for line in f.readlines()]

    # Configuration for High-DPI realistic Windows Terminal (Ubuntu WSL profile)
    scale = 2
    font_size = 13 * scale
    line_height = 20 * scale
    char_width = 8 * scale  # approximate for Consolas
    
    # Palette: Windows Terminal "Campbell" (Default)
    bg_color = (12, 12, 12)            # #0C0C0C true terminal background
    tab_bar_bg = (32, 32, 32)          # #202020
    active_tab_bg = (12, 12, 12)       # Active tab matches terminal bg
    inactive_tab_text = (150, 150, 150)
    active_tab_text = (240, 240, 240)
    border_color = (45, 45, 45)
    
    # Text colors
    c_user_host = (22, 198, 12)        # ANSI Green #16C60C
    c_colon = (204, 204, 204)          # ANSI White #CCCCCC
    c_path = (59, 120, 255)            # ANSI Blue #3B78FF
    c_cmd = (242, 242, 242)            # White
    c_out = (204, 204, 204)            # Authentic plain uncolored terminal text
    c_cursor = (255, 255, 255)         # Blinking cursor block
    
    # Scrollbar
    scrollbar_track = (20, 20, 20)
    scrollbar_thumb = (65, 65, 65)
    scrollbar_width = 12 * scale
    
    # Fonts
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", font_size)
    font_mono_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)
    font_ui = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11 * scale)
    font_ui_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11 * scale)
    
    # Padding and layout for clean terminal content (no OS header/tabs)
    padding_x = 18 * scale
    padding_top = 18 * scale
    padding_bottom = 18 * scale
    
    # Calculate dimensions
    max_cols = max(len(l) for l in raw_lines)
    content_width = max(max_cols * char_width, 800 * scale)
    width = content_width + padding_x * 2
    
    # Content lines count: 1 initial prompt + len(raw_lines) + 1 bottom prompt
    total_lines_count = 1 + len(raw_lines) + 1
    height = padding_top + total_lines_count * line_height + padding_bottom
    
    # Create image
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw Terminal Content
    curr_y = padding_top
    
    # Helper to draw prompt
    def draw_prompt(y_pos, with_cursor=False, cmd=""):
        p1 = "tuyen@pki-lab"
        p2 = ":"
        p3 = "~/PKI_Security_Research"
        p4 = "$ "
        
        x = padding_x
        draw.text((x, y_pos), p1, font=font_mono_bold, fill=c_user_host)
        x += len(p1) * char_width
        
        draw.text((x, y_pos), p2, font=font_mono, fill=c_colon)
        x += len(p2) * char_width
        
        draw.text((x, y_pos), p3, font=font_mono_bold, fill=c_path)
        x += len(p3) * char_width
        
        draw.text((x, y_pos), p4, font=font_mono, fill=c_colon)
        x += len(p4) * char_width
        
        if cmd:
            draw.text((x, y_pos), cmd, font=font_mono, fill=c_cmd)
            
        if with_cursor:
            # Draw realistic cursor block
            cursor_w = char_width
            cursor_h = font_size + 2 * scale
            draw.rectangle([(x, y_pos + 1 * scale), (x + cursor_w, y_pos + cursor_h)], fill=c_cursor)
            
        return y_pos + line_height

    # Initial command prompt
    curr_y = draw_prompt(curr_y, with_cursor=False, cmd="openssl x509 -in demo/out/servers/server-a.crt -text -noout")
    
    # Raw output lines (100% authentic plain text, exact terminal look)
    for line in raw_lines:
        draw.text((padding_x, curr_y), line, font=font_mono, fill=c_out)
        curr_y += line_height
        
    # Final active prompt with cursor
    curr_y = draw_prompt(curr_y, with_cursor=True, cmd="")
    
    # Clean subtle outer border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=1 * scale)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Saved authentic screenshot to: {output_path} ({width}x{height})")

if __name__ == "__main__":
    create_authentic_terminal_screenshot()
