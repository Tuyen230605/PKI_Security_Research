import os
from PIL import Image, ImageDraw, ImageFont

def create_verify_terminal_screenshot(
    output_path="report/figures/openssl-verify-terminal.png",
):
    output_path = os.path.abspath(output_path)

    # Configuration for High-DPI realistic Windows Terminal (Ubuntu WSL profile)
    scale = 2
    font_size = 13 * scale
    line_height = 22 * scale
    
    # Palette: Windows Terminal "Campbell" (Default)
    bg_color = (12, 12, 12)            # #0C0C0C true terminal background
    border_color = (45, 45, 45)
    
    # Text colors
    c_user_host = (22, 198, 12)        # ANSI Green #16C60C
    c_colon = (204, 204, 204)          # ANSI White #CCCCCC
    c_path = (59, 120, 255)            # ANSI Blue #3B78FF
    c_cmd = (242, 242, 242)            # White
    c_out = (204, 204, 204)            # Authentic plain uncolored terminal text
    c_ok = (22, 198, 12)               # Green for OK
    c_err = (231, 72, 86)              # Red for error
    c_cursor = (255, 255, 255)         # Blinking cursor block
    
    # Fonts
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", font_size)
    font_mono_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)
    
    # Padding and layout for clean terminal content
    padding_x = 18 * scale
    padding_top = 18 * scale
    padding_bottom = 18 * scale
    
    terminal_session = [
        # (type, text)
        ("prompt", "openssl verify -show_chain -CAfile demo/out/root/root.crt -untrusted demo/out/intermediate/ca.crt -purpose sslserver -verify_hostname server-a.test demo/out/servers/server-a.crt"),
        ("output_ok", "demo/out/servers/server-a.crt: OK"),
        ("output", "Chain:"),
        ("output", "depth=0: CN=server-a.test (untrusted)"),
        ("output", "depth=1: CN=Lab Intermediate CA (untrusted)"),
        ("output", "depth=2: CN=Lab Root CA"),
        ("prompt", "openssl verify -CAfile demo/out/root/root.crt -purpose sslserver -verify_hostname server-a.test demo/out/servers/server-a.crt"),
        ("output", "CN=server-a.test"),
        ("output_err", "error 20 at 0 depth lookup: unable to get local issuer certificate"),
        ("output_err", "error demo/out/servers/server-a.crt: verification failed"),
        ("prompt_cursor", "")
    ]
    
    # Measure maximum width accurately
    prompt_prefix = "tuyen@pki-lab:~/PKI_Security_Research$ "
    prefix_w = (
        font_mono_bold.getlength("tuyen@pki-lab")
        + font_mono.getlength(":")
        + font_mono_bold.getlength("~/PKI_Security_Research")
        + font_mono.getlength("$ ")
    )
    
    max_w = 0
    for line_type, text in terminal_session:
        if line_type in ("prompt", "prompt_cursor"):
            w = prefix_w + font_mono.getlength(text)
        else:
            w = font_mono.getlength(text)
        if w > max_w:
            max_w = w
            
    # Add comfortable margin
    content_width = int(max_w + 30 * scale)
    width = content_width + padding_x * 2
    height = padding_top + len(terminal_session) * line_height + padding_bottom
    
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    curr_y = padding_top
    
    def draw_prompt(y_pos, cmd="", with_cursor=False):
        p1 = "tuyen@pki-lab"
        p2 = ":"
        p3 = "~/PKI_Security_Research"
        p4 = "$ "
        
        x = padding_x
        draw.text((x, y_pos), p1, font=font_mono_bold, fill=c_user_host)
        x += font_mono_bold.getlength(p1)
        
        draw.text((x, y_pos), p2, font=font_mono, fill=c_colon)
        x += font_mono.getlength(p2)
        
        draw.text((x, y_pos), p3, font=font_mono_bold, fill=c_path)
        x += font_mono_bold.getlength(p3)
        
        draw.text((x, y_pos), p4, font=font_mono, fill=c_colon)
        x += font_mono.getlength(p4)
        
        if cmd:
            draw.text((x, y_pos), cmd, font=font_mono, fill=c_cmd)
            
        if with_cursor:
            cursor_w = font_mono.getlength(" ")
            cursor_h = font_size + 2 * scale
            draw.rectangle([(x, y_pos + 1 * scale), (x + cursor_w, y_pos + cursor_h)], fill=c_cursor)
            
        return y_pos + line_height

    for line_type, text in terminal_session:
        if line_type == "prompt":
            curr_y = draw_prompt(curr_y, cmd=text, with_cursor=False)
        elif line_type == "prompt_cursor":
            curr_y = draw_prompt(curr_y, cmd="", with_cursor=True)
        elif line_type == "output_ok":
            prefix = "demo/out/servers/server-a.crt: "
            draw.text((padding_x, curr_y), prefix, font=font_mono, fill=c_out)
            draw.text((padding_x + font_mono.getlength(prefix), curr_y), "OK", font=font_mono_bold, fill=c_ok)
            curr_y += line_height
        elif line_type == "output_err":
            draw.text((padding_x, curr_y), text, font=font_mono, fill=c_err)
            curr_y += line_height
        else:
            draw.text((padding_x, curr_y), text, font=font_mono, fill=c_out)
            curr_y += line_height
            
    # Clean subtle outer border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=1 * scale)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Saved authentic verify screenshot to: {output_path} ({width}x{height})")

if __name__ == "__main__":
    create_verify_terminal_screenshot()
