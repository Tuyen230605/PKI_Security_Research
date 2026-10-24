import os
import re
from PIL import Image, ImageDraw, ImageFont

def render_terminal(lines, output_path, title="Terminal — openssl x509 -in server-a.crt -text -noout", scale=2):
    # Font configuration
    font_path = "C:/Windows/Fonts/consola.ttf"
    bold_font_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 14 * scale
    line_height = 22 * scale
    padding_x = 24 * scale
    padding_top = 48 * scale
    padding_bottom = 24 * scale
    
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(bold_font_path, font_size)
    title_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11 * scale)
    
    # Calculate dimensions
    max_line_len = max(len(l[0]) for l in lines)
    width = max(880 * scale, int((max_line_len + 6) * font_size * 0.62) + padding_x * 2)
    height = padding_top + len(lines) * line_height + padding_bottom
    
    # Colors (GitHub Dark / Modern Terminal palette)
    bg_color = (13, 17, 23)        # #0D1117
    title_bar_bg = (22, 27, 34)    # #161B22
    border_color = (48, 54, 61)    # #30363D
    title_text_color = (139, 148, 158) # #8B949E
    
    # Create image
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, padding_top - 6 * scale)], fill=title_bar_bg)
    draw.line([(0, padding_top - 6 * scale), (width, padding_top - 6 * scale)], fill=border_color, width=1 * scale)
    
    # Window buttons (macOS style)
    btn_y = (padding_top - 6 * scale) // 2
    btn_r = 6 * scale
    btn_spacing = 18 * scale
    btn_start_x = 18 * scale
    
    # Red, Yellow, Green
    draw.ellipse([(btn_start_x - btn_r, btn_y - btn_r), (btn_start_x + btn_r, btn_y + btn_r)], fill=(255, 95, 86))
    draw.ellipse([(btn_start_x + btn_spacing - btn_r, btn_y - btn_r), (btn_start_x + btn_spacing + btn_r, btn_y + btn_r)], fill=(255, 189, 46))
    draw.ellipse([(btn_start_x + btn_spacing * 2 - btn_r, btn_y - btn_r), (btn_start_x + btn_spacing * 2 + btn_r, btn_y + btn_r)], fill=(39, 201, 63))
    
    # Title text
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, btn_y - (title_bbox[3] - title_bbox[1]) // 2), title, font=title_font, fill=title_text_color)
    
    # Render lines
    y = padding_top + 4 * scale
    for text, style, color in lines:
        use_font = bold_font if style == "bold" else font
        draw.text((padding_x, y), text, font=use_font, fill=color)
        y += line_height
        
    # Window outer border
    draw.rounded_rectangle([(0, 0), (width - 1, height - 1)], radius=10 * scale, outline=border_color, width=2 * scale)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path} ({width}x{height})")

def colorize_cert(raw_lines, condensed=True):
    # Palette
    c_cmd = (126, 231, 135)       # Green #7ee787
    c_prompt = (88, 166, 255)     # Blue #58a6ff
    c_section = (121, 192, 255)   # Light Cyan #79c0ff
    c_field = (210, 168, 255)     # Light Purple #d2a8ff
    c_ext = (255, 166, 87)        # Orange #ffa657
    c_crit = (255, 123, 114)      # Red #ff7b72
    c_val = (86, 211, 100)        # Bright Green #56d364
    c_date = (227, 179, 65)       # Gold #e3b341
    c_hex = (139, 148, 158)       # Dim gray #8b949e
    c_text = (240, 246, 252)      # Default text #f0f6fc
    c_dim = (110, 118, 129)       # Dim italic #6e7681

    formatted = []
    formatted.append(("$ openssl x509 -in demo/out/servers/server-a.crt -text -noout", "bold", c_cmd))
    
    in_modulus = False
    in_signature = False
    modulus_count = 0
    sig_count = 0
    
    for line in raw_lines:
        s = line.rstrip("\n")
        stripped = s.strip()
        
        # Check sections
        if stripped in ["Certificate:", "Data:"]:
            formatted.append((s, "bold", c_section))
        elif stripped.startswith("Version:"):
            formatted.append((s, "normal", c_field))
        elif stripped.startswith("Serial Number:"):
            formatted.append((s, "bold", c_field))
        elif stripped.startswith("Signature Algorithm:"):
            formatted.append((s, "normal", c_field))
        elif stripped.startswith("Issuer:"):
            formatted.append((s, "bold", c_field))
        elif stripped == "Validity":
            formatted.append((s, "bold", c_section))
        elif stripped.startswith("Not Before:"):
            formatted.append((s, "normal", c_date))
        elif stripped.startswith("Not After :") or stripped.startswith("Not After:"):
            formatted.append((s, "normal", c_date))
        elif stripped.startswith("Subject:"):
            formatted.append((s, "bold", c_field))
        elif stripped.startswith("Subject Public Key Info:") or stripped.startswith("Public Key Algorithm:") or stripped.startswith("Public-Key:"):
            formatted.append((s, "normal", c_field))
        elif stripped.startswith("Modulus:"):
            formatted.append((s, "normal", c_field))
            in_modulus = True
            modulus_count = 0
        elif stripped.startswith("Exponent:"):
            in_modulus = False
            formatted.append((s, "normal", c_field))
        elif stripped.startswith("X509v3 extensions:"):
            formatted.append((s, "bold", c_section))
        elif stripped.startswith("X509v3 Basic Constraints:"):
            formatted.append((s, "bold", c_ext))
        elif stripped in ["CA:FALSE", "CA:TRUE"]:
            formatted.append((s, "bold", c_crit))
        elif stripped.startswith("X509v3 Key Usage:"):
            formatted.append((s, "bold", c_ext))
        elif "Digital Signature" in stripped or "Key Encipherment" in stripped:
            formatted.append((s, "bold", c_val))
        elif stripped.startswith("X509v3 Extended Key Usage:"):
            formatted.append((s, "bold", c_ext))
        elif "TLS Web Server Authentication" in stripped:
            formatted.append((s, "bold", c_val))
        elif stripped.startswith("X509v3 Subject Alternative Name:"):
            formatted.append((s, "bold", c_ext))
        elif stripped.startswith("DNS:"):
            formatted.append((s, "bold", c_val))
        elif stripped.startswith("X509v3 Subject Key Identifier:") or stripped.startswith("X509v3 Authority Key Identifier:"):
            formatted.append((s, "normal", c_ext))
        elif stripped.startswith("Signature Value:"):
            formatted.append((s, "bold", c_field))
            in_signature = True
            sig_count = 0
        else:
            if in_modulus:
                modulus_count += 1
                if condensed:
                    if modulus_count <= 2:
                        formatted.append((s, "normal", c_hex))
                    elif modulus_count == 3:
                        formatted.append(("                    ... [2048-bit RSA Modulus: 256 bytes] ...", "bold", c_dim))
                    elif modulus_count >= 17:
                        formatted.append((s, "normal", c_hex))
                else:
                    formatted.append((s, "normal", c_hex))
            elif in_signature:
                sig_count += 1
                if condensed:
                    if sig_count <= 2:
                        formatted.append((s, "normal", c_hex))
                    elif sig_count == 3:
                        formatted.append(("        ... [sha256WithRSA Signature: 256 bytes] ...", "bold", c_dim))
                    elif sig_count >= 15:
                        formatted.append((s, "normal", c_hex))
                else:
                    formatted.append((s, "normal", c_hex))
            else:
                formatted.append((s, "normal", c_text))
                
    return formatted

if __name__ == "__main__":
    with open("report/figures/openssl-x509-text.txt", "r", encoding="utf-8") as f:
        raw_lines = f.readlines()
        
    # 1. Condensed (focused on academic fields)
    condensed_lines = colorize_cert(raw_lines, condensed=True)
    render_terminal(condensed_lines, "report/figures/openssl-x509-text.png")
    
    # 2. Full verbatim
    full_lines = colorize_cert(raw_lines, condensed=False)
    render_terminal(full_lines, "report/figures/openssl-x509-text-full.png")
