#!/usr/bin/env python3
"""
PDF Generation Script for Comprehensive MyST Document
Based on the working approach from generate_pdf_book.py
Generates LaTeX and PDF with Springer book style and proper image linking
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import re
import time

# Configuration
# Get the project root (parent of pdf_generator folder)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DOCUMENT = PROJECT_ROOT / "content" / "Comprehensive MyST Documnet.md"
BUILD_DIR = PROJECT_ROOT / "_build"
LATEX_DIR = BUILD_DIR / "latex" / "comprehensive-myst"
OUTPUT_DIR = PROJECT_ROOT / "_build" / "exports"

# ImageMagick path (update if different)
IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def safe_print(text, encoding='utf-8', errors='replace'):
    """Print text safely handling encoding errors on Windows"""
    try:
        print(text)
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Fallback: sanitize text to ASCII-safe characters
        try:
            # Remove or replace problematic Unicode characters
            safe_text = text.encode('ascii', errors='replace').decode('ascii')
            print(safe_text)
        except:
            # Last resort: print to stderr with minimal formatting
            sys.stdout.buffer.write(b'[Warning: Could not display message due to encoding issues]\n')

def print_step(text):
    safe_print(f"{Colors.OKBLUE}[*] {text}{Colors.ENDC}")

def print_success(text):
    safe_print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")

def print_warning(text):
    safe_print(f"{Colors.WARNING}[!] {text}{Colors.ENDC}")

def print_error(text):
    safe_print(f"{Colors.FAIL}[X] {text}{Colors.ENDC}")

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout if hasattr(e, 'stdout') else '', e.stderr if hasattr(e, 'stderr') else ''

def build_and_execute():
    """Build and execute code cells using jupyter book build"""
    print_step("Building and executing code cells with jupyter book build...")
    
    # Try to find jupyter executable in venv
    venv_jupyter = PROJECT_ROOT / ".venv" / "Scripts" / "jupyter.exe"
    if venv_jupyter.exists():
        jupyter_cmd = str(venv_jupyter)
    else:
        jupyter_cmd = "jupyter"
    
    # First build with execution to generate all outputs
    cmd = f'"{jupyter_cmd}" book build . --execute'
    success, stdout, stderr = run_command(cmd, check=False)
    
    if not success:
        print_warning(f"Jupyter book build had warnings: {stderr[:500]}")
    else:
        print_success("Jupyter book build completed")
    
    # Wait for execution and file system sync
    time.sleep(3.0)

def export_to_latex():
    """Export MyST document to LaTeX using myst build --tex (faster than jupyter book build --pdf)"""
    print_step("Exporting Comprehensive MyST Document to LaTeX...")
    
    LATEX_DIR.mkdir(parents=True, exist_ok=True)
    files_dir = LATEX_DIR / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    
    # Use myst build --tex to export to LaTeX (no execution, we already did that)
    # This is much faster than building the entire book
    md_file_rel = DOCUMENT.relative_to(PROJECT_ROOT)
    output_dir_rel = LATEX_DIR.relative_to(PROJECT_ROOT)
    
    cmd = f'myst build "{md_file_rel}" --tex --output "{output_dir_rel}"'
    success, stdout, stderr = run_command(cmd, check=False)
    
    if stderr and ('error' in stderr.lower() or 'failed' in stderr.lower()):
        # Sanitize stderr to avoid encoding issues on Windows
        try:
            sanitized_stderr = stderr[:500].encode('ascii', errors='replace').decode('ascii')
            print_warning(f"MyST build --tex stderr: {sanitized_stderr}")
        except:
            print_warning("MyST build --tex produced stderr output (encoding issues prevented display)")
    
    # Wait for LaTeX export
    time.sleep(2.0)
    
    # Find the generated tex file in LATEX_DIR
    tex_file = None
    for possible_file in LATEX_DIR.glob("*.tex"):
        if "comprehensive" in possible_file.name.lower() or "myst" in possible_file.name.lower() or "documnet" in possible_file.name.lower():
            tex_file = possible_file
            print_success(f"Found LaTeX file: {tex_file.name}")
            break
    
    # Also check in _build/temp (fallback)
    if not tex_file or not tex_file.exists():
        temp_dir = BUILD_DIR / "temp"
        if temp_dir.exists():
            myst_dirs = [d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("myst")]
            if myst_dirs:
                try:
                    most_recent = max(myst_dirs, key=lambda d: d.stat().st_mtime if d.exists() else 0)
                    for tex_file_candidate in most_recent.glob("*.tex"):
                        if "comprehensive" in tex_file_candidate.name.lower() or "myst" in tex_file_candidate.name.lower():
                            # Copy to LATEX_DIR for easier processing
                            dest_tex = LATEX_DIR / tex_file_candidate.name
                            shutil.copy2(tex_file_candidate, dest_tex)
                            tex_file = dest_tex
                            
                            # Also copy files directory if it exists
                            src_files = tex_file_candidate.parent / "files"
                            if src_files.exists():
                                dest_files = LATEX_DIR / "files"
                                if dest_files.exists():
                                    shutil.rmtree(dest_files)
                                shutil.copytree(src_files, dest_files)
                                file_count = len([f for f in dest_files.rglob('*') if f.is_file()])
                                print_success(f"Copied {file_count} files from build")
                            
                            print_success(f"Found LaTeX file: {tex_file.name}")
                            break
                except (OSError, ValueError) as e:
                    print_warning(f"Error finding LaTeX file: {e}")
    
    if tex_file and tex_file.exists():
        print_success("Exported to LaTeX")
        return tex_file
    else:
        print_error("Failed to export to LaTeX - file not found")
        return None

def copy_build_images_to_latex():
    """Copy images from _build directories to LaTeX files folder"""
    files_dir = LATEX_DIR / "files"
    if not files_dir.exists():
        files_dir.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    copied_files = set()
    
    # Search in _build/site/public for images
    site_public = BUILD_DIR / "site" / "public"
    if site_public.exists():
        # Look for comprehensive-myst-documnet specific paths
        doc_patterns = [
            site_public / "comprehensive-myst-documnet",
            site_public / "comprehensive",
        ]
        
        for pattern_path in doc_patterns:
            if pattern_path.exists():
                for img_file in pattern_path.rglob("*.png"):
                    if img_file.name not in copied_files:
                        dest = files_dir / img_file.name
                        if not dest.exists():
                            try:
                                shutil.copy2(img_file, dest)
                                copied += 1
                                copied_files.add(img_file.name)
                            except Exception:
                                pass
        
        # Also search for images in paths containing comprehensive
        for img_file in site_public.rglob("*.png"):
            path_str = str(img_file).lower()
            if "comprehensive" in path_str or "myst-documnet" in path_str:
                if img_file.name not in copied_files:
                    dest = files_dir / img_file.name
                    if not dest.exists():
                        try:
                            shutil.copy2(img_file, dest)
                            copied += 1
                            copied_files.add(img_file.name)
                        except Exception:
                            pass
    
    # Search in _build/execute (where code outputs are stored)
    execute_dir = BUILD_DIR / "execute"
    if execute_dir.exists():
        for img_file in execute_dir.rglob("*.png"):
            if img_file.name not in copied_files:
                dest = files_dir / img_file.name
                if not dest.exists():
                    try:
                        shutil.copy2(img_file, dest)
                        copied += 1
                        copied_files.add(img_file.name)
                    except Exception:
                        pass
    
    # Search in _build/temp for most recent executed outputs
    temp_dir = BUILD_DIR / "temp"
    if temp_dir.exists():
        myst_dirs = [d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("myst")]
        if myst_dirs:
            try:
                most_recent = max(myst_dirs, key=lambda d: d.stat().st_mtime if d.exists() else 0)
                
                for img_file in most_recent.rglob("*.png"):
                    if "curvenote" not in img_file.name.lower() and img_file.name not in copied_files:
                        dest = files_dir / img_file.name
                        if not dest.exists():
                            try:
                                shutil.copy2(img_file, dest)
                                copied += 1
                                copied_files.add(img_file.name)
                            except Exception:
                                pass
            except (OSError, ValueError):
                pass
    
    # Search recursively in _build subdirectories for comprehensive document
    for root, dirs, files in os.walk(BUILD_DIR):
        if 'latex' in root:
            continue
        
        root_str = str(root).lower()
        if 'comprehensive' not in root_str and 'myst-documnet' not in root_str:
            continue
        
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')) and file not in copied_files:
                src_file = Path(root) / file
                dest = files_dir / file
                if not dest.exists():
                    try:
                        shutil.copy2(src_file, dest)
                        copied += 1
                        copied_files.add(file)
                    except Exception:
                        pass
    
    return copied

def copy_referenced_images(tex_file):
    """Copy only images that are referenced in the LaTeX file"""
    files_dir = LATEX_DIR / "files"
    if not files_dir.exists():
        files_dir.mkdir(parents=True, exist_ok=True)
    
    if not tex_file.exists():
        return 0
    
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return 0
    
    # Find all image references in LaTeX
    image_refs = set()
    patterns = [
        r'files/([^}]+\.(?:png|jpg|jpeg|pdf))',
        r'"files/([^"]+\.(?:png|jpg|jpeg|pdf))"',
        r"'files/([^']+\.(?:png|jpg|jpeg|pdf))'",
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        image_refs.update(matches)
    
    if not image_refs:
        return 0
    
    copied = 0
    copied_files = set()
    
    # Search for referenced images
    search_paths = []
    
    # 1. site/public
    site_public = BUILD_DIR / "site" / "public"
    if site_public.exists():
        search_paths.append(site_public)
    
    # 2. execute directory
    execute_dir = BUILD_DIR / "execute"
    if execute_dir.exists():
        search_paths.append(execute_dir)
    
    # 3. temp directories
    temp_dir = BUILD_DIR / "temp"
    if temp_dir.exists():
        myst_dirs = [d for d in temp_dir.iterdir() if d.is_dir() and d.name.startswith("myst")]
        if myst_dirs:
            try:
                most_recent = max(myst_dirs, key=lambda d: d.stat().st_mtime if d.exists() else 0)
                search_paths.append(most_recent)
            except (OSError, ValueError):
                pass
    
    for img_name in image_refs:
        if img_name in copied_files:
            continue
        
        found = False
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            # Try direct match
            candidate = search_path / img_name
            if candidate.exists():
                dest = files_dir / img_name
                if not dest.exists():
                    try:
                        shutil.copy2(candidate, dest)
                        copied += 1
                        copied_files.add(img_name)
                        found = True
                        break
                    except Exception:
                        pass
            
            # Try recursive search
            if not found:
                try:
                    for img_file in search_path.rglob(img_name):
                        dest = files_dir / img_name
                        if not dest.exists():
                            try:
                                shutil.copy2(img_file, dest)
                                copied += 1
                                copied_files.add(img_name)
                                found = True
                                break
                            except Exception:
                                pass
                    if found:
                        break
                except Exception:
                    pass
        
        if found:
            continue
    
    return copied

def link_images_to_figures(tex_file):
    """Link copied images to empty figure blocks in LaTeX file using robust execution order
    
    Strategy:
    1. Read markdown source to understand code cell and figure order
    2. Get all generated images sorted by creation time (Jupyter executes in document order)
    3. Match empty figures to images based on their sequential position
    4. Use labels when available for precise matching
    5. Prioritize code-cell figures over static figures
    """
    try:
        files_dir = tex_file.parent / "files"
        if not files_dir.exists():
            return 0
        
        # Get all available PNG images, sorted by modification time (execution order)
        all_images = list(files_dir.glob("*.png"))
        
        # Filter out curvenote logo
        images = [img for img in all_images if "curvenote" not in img.name.lower()]
        
        # Sort by modification time (execution order) - Jupyter Book executes code cells sequentially
        # Add name as secondary sort for deterministic ordering when times are equal
        available_images = sorted(images, key=lambda p: (p.stat().st_mtime if p.exists() else 0, p.name.lower()))
        
        if not available_images:
            return 0
        
        # Debug: Print image order with timestamps
        print_step("Image generation order:")
        for idx, img in enumerate(available_images):
            mtime = img.stat().st_mtime if img.exists() else 0
            import datetime
            timestamp = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f"  [{idx}] {img.name[:40]}... (modified: {timestamp})")
        
        used_images = set()
        image_index = 0
        
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        linked = 0
        
        # Find all figure blocks in document order
        figure_pattern = r'\\begin\{figure\}(.*?)\\end\{figure\}'
        
        # First pass: identify all figures and classify them
        figure_info = []
        for match in re.finditer(figure_pattern, content, flags=re.DOTALL):
            figure_content = match.group(1)
            has_image = '\\includegraphics{' in figure_content or '\\includegraphics[' in figure_content
            has_label = re.search(r'\\label\{([^}]+)\}', figure_content)
            has_caption = '\\caption' in figure_content
            is_code_block = '\\begin{verbatim}' in figure_content or '\\begin{pythoncode}' in figure_content
            
            label = has_label.group(1) if has_label else None
            
            # Determine if this is likely a code-generated figure
            is_code_figure = (
                not has_image and 
                not is_code_block and 
                has_caption and
                (label and ('fig:' in label or 'python' in label.lower() or 'plot' in label.lower()))
            )
            
            figure_info.append({
                'start': match.start(),
                'end': match.end(),
                'has_image': has_image,
                'label': label,
                'is_code_figure': is_code_figure,
                'is_code_block': is_code_block,
                'needs_image': not has_image and not is_code_block,
                'figure_content': figure_content
            })
        
        print_step(f"Found {len(figure_info)} figures: {sum(f['needs_image'] for f in figure_info)} need images")
        
        def replace_empty_figure(match):
            nonlocal linked, available_images, image_index, used_images
            figure_content = match.group(1)
            
            # Skip if already has includegraphics (real image, not just comments)
            if '\\includegraphics{' in figure_content or '\\includegraphics[' in figure_content:
                return match.group(0)
            
            # Skip if contains verbatim (code blocks or errors)
            if '\\begin{verbatim}' in figure_content or '\\begin{pythoncode}' in figure_content:
                return match.group(0)
            
            # Remove comments that were added (like "% Code block removed from figure")
            # These indicate empty figures that need images
            figure_content_clean = re.sub(r'%[^\n]*\n', '', figure_content)
            
            # Try to find image based on label first (strong match)
            image_file = None
            label_match = re.search(r'\\label\{([^}]+)\}', figure_content_clean)
            
            if label_match:
                label = label_match.group(1)
                # Try exact label match first (e.g., fig:python-plot)
                label_normalized = label.lower().replace('fig:', '').replace('_', '-')
                
                for img in available_images:
                    if img.name in used_images:
                        continue
                    
                    img_stem_lower = img.stem.lower()
                    
                    # Check for label components in filename
                    label_parts = label_normalized.split('-')
                    # Must match at least 2 significant parts (length >= 4)
                    significant_parts = [part for part in label_parts if len(part) >= 4]
                    matches = sum(1 for part in significant_parts if part in img_stem_lower)
                    
                    if matches >= min(2, len(significant_parts)) and significant_parts:
                        image_file = img
                        print(f"  Matched by label '{label}' -> {img.name[:40]}...")
                        break
            
            # If no match by label, use next image in execution order
            if not image_file:
                while image_index < len(available_images):
                    candidate = available_images[image_index]
                    if candidate.name not in used_images:
                        image_file = candidate
                        image_index += 1
                        label_info = f" (label: {label_match.group(1)})" if label_match else ""
                        print(f"  Matched by order [index {image_index-1}]{label_info} -> {image_file.name[:40]}...")
                        break
                    image_index += 1
            
            if image_file and image_file.name not in used_images:
                # Clean up the figure content - remove comments, keep structure
                cleaned_figure = re.sub(r'%[^\n]*\n\s*', '', figure_content)
                
                # Find insert position in cleaned content (after \centering, before caption)
                insert_pos = 0
                caption_match = re.search(r'\\caption', cleaned_figure)
                centering_match = re.search(r'\\centering', cleaned_figure)
                
                if centering_match:
                    # Insert after \centering
                    insert_pos = centering_match.end()
                    # Skip whitespace
                    while insert_pos < len(cleaned_figure) and cleaned_figure[insert_pos] in ['\n', '\r', ' ', '\t']:
                        insert_pos += 1
                elif caption_match:
                    # Insert before caption
                    insert_pos = caption_match.start()
                    # Skip backwards to find good position
                    while insert_pos > 0 and cleaned_figure[insert_pos-1] in ['\n', '\r', ' ', '\t']:
                        insert_pos -= 1
                
                # Determine width based on context
                width = '0.8\\linewidth'
                if 'wide' in figure_content.lower() or 'full' in figure_content.lower():
                    width = '1\\linewidth'
                elif 'small' in figure_content.lower() or 'thumbnail' in figure_content.lower():
                    width = '0.5\\linewidth'
                
                image_cmd = f'\\includegraphics[width={width}]{{files/{image_file.name}}}\n'
                
                # Insert image in cleaned figure content
                if insert_pos > 0 and insert_pos < len(cleaned_figure):
                    new_content = cleaned_figure[:insert_pos] + '\n' + image_cmd + cleaned_figure[insert_pos:]
                else:
                    # Insert at beginning after \centering or at start
                    if '\\centering' in cleaned_figure:
                        centering_pos = cleaned_figure.find('\\centering') + len('\\centering')
                        # Skip whitespace
                        while centering_pos < len(cleaned_figure) and cleaned_figure[centering_pos] in ['\n', '\r', ' ', '\t']:
                            centering_pos += 1
                        new_content = cleaned_figure[:centering_pos] + '\n' + image_cmd + cleaned_figure[centering_pos:]
                    else:
                        new_content = image_cmd + '\n' + cleaned_figure
                
                used_images.add(image_file.name)
                linked += 1
                return '\\begin{figure}' + new_content + '\\end{figure}'
            
            return match.group(0)
        
        # Replace empty figures (in order they appear in document)
        content = re.sub(figure_pattern, replace_empty_figure, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return linked
        
        return 0
    except Exception as e:
        print_error(f"Failed to link images: {e}")
        import traceback
        traceback.print_exc()
        return 0

def convert_images_in_directory(img_dir):
    """Convert SVG and GIF files to PNG in a directory"""
    if not os.path.exists(img_dir):
        return 0
    
    converted = 0
    img_path = Path(img_dir)
    
    # Convert SVG files
    if os.path.exists(IMAGEMAGICK_PATH):
        for svg_file in img_path.glob("*.svg"):
            png_file = svg_file.with_suffix('.png')
            if not png_file.exists():
                try:
                    result = subprocess.run(
                        [IMAGEMAGICK_PATH, "-density", "300", str(svg_file), str(png_file)],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    if result.returncode == 0 and png_file.exists():
                        converted += 1
                except (subprocess.TimeoutExpired, Exception):
                    pass
        
        # Convert GIF files (extract first frame)
        for gif_file in img_path.glob("*.gif"):
            png_file = gif_file.with_suffix('.png')
            if not png_file.exists():
                try:
                    result = subprocess.run(
                        [IMAGEMAGICK_PATH, "-density", "300", f"{gif_file}[0]", str(png_file)],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    if result.returncode == 0 and png_file.exists():
                        converted += 1
                except (subprocess.TimeoutExpired, Exception):
                    pass
    
    return converted

def add_code_block_definitions(content):
    """Add specialized code block and important block definitions"""
    packages_to_add = []
    
    # Check for tikz
    if '\\usepackage{tikz}' not in content:
        packages_to_add.append('\\usepackage{tikz}')
    
    # Check for tcolorbox - prefer [most] option
    if '\\usepackage[most]{tcolorbox}' not in content and '\\usepackage{tcolorbox}' not in content:
        packages_to_add.append('\\usepackage[most]{tcolorbox}')
    elif '\\usepackage{tcolorbox}' in content and '\\usepackage[most]{tcolorbox}' not in content:
        content = content.replace('\\usepackage{tcolorbox}', '\\usepackage[most]{tcolorbox}')
    
    # Color definitions
    color_defs = r"""
% Colors for specialized code blocks
\definecolor{lightgray}{RGB}{245, 245, 245}
\definecolor{coolgray}{RGB}{90, 90, 90}
\definecolor{darkblue}{RGB}{0, 47, 108}
\definecolor{codegreen}{RGB}{0, 100, 0}
\definecolor{codeorange}{RGB}{255, 140, 0}
\definecolor{accentblue}{RGB}{0, 120, 180}
\definecolor{warningred}{RGB}{220, 38, 127}
"""
    
    code_block_defs = r"""
% Generic styled code block for all languages with language label
\newtcblisting{styledcode}[2][lightgray]{
  listing engine=listings,
  colback=#1,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={#2},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{darkblue}\bfseries,
    commentstyle=\color{codegreen}\itshape,
    stringstyle=\color{codeorange},
    showstringspaces=false,
    numbers=none,
    escapeinside={(*@}{@*)},
    breaklines=true,
    breakatwhitespace=true,
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

% Specialized code blocks with language-specific options
\newtcblisting{pythoncode}[1][]{
  listing engine=listings,
  colback=lightgray,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={Python},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    language=Python,
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{darkblue}\bfseries,
    commentstyle=\color{codegreen}\itshape,
    stringstyle=\color{codeorange},
    showstringspaces=false,
    numbers=none,
    escapeinside={(*@}{@*)},
    breaklines=true,
    breakatwhitespace=true,
    #1
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

% Generic code block for other languages (bash, yaml, json, etc.)
\newtcblisting{bashcode}[1][]{
  listing engine=listings,
  colback=lightgray,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={Bash/Shell},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    language=bash,
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{darkblue}\bfseries,
    commentstyle=\color{codegreen}\itshape,
    stringstyle=\color{codeorange},
    showstringspaces=false,
    numbers=none,
    breaklines=true,
    breakatwhitespace=true,
    #1
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

\newtcblisting{yamlcode}[1][]{
  listing engine=listings,
  colback=lightgray,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={YAML},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    basicstyle=\ttfamily\footnotesize,
    commentstyle=\color{codegreen}\itshape,
    stringstyle=\color{codeorange},
    showstringspaces=false,
    numbers=none,
    breaklines=true,
    breakatwhitespace=true,
    #1
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

\newtcblisting{jsoncode}[1][]{
  listing engine=listings,
  colback=lightgray,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={JSON},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    language=json,
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{darkblue}\bfseries,
    stringstyle=\color{codeorange},
    showstringspaces=false,
    numbers=none,
    breaklines=true,
    breakatwhitespace=true,
    #1
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

\newtcblisting{markdowncode}[1][]{
  listing engine=listings,
  colback=lightgray,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={Markdown},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    basicstyle=\ttfamily\footnotesize,
    commentstyle=\color{codegreen}\itshape,
    stringstyle=\color{codeorange},
    showstringspaces=false,
    numbers=none,
    breaklines=true,
    breakatwhitespace=true,
    escapeinside={(*@}{@*)},
    #1
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

% Raw verbatim box for Markdown code blocks (no parsing, just raw text with line breaking)
\newtcblisting{markdownraw}{
  listing engine=listings,
  colback=lightgray,
  colframe=coolgray,
  fonttitle=\bfseries\sffamily\small,
  title={Markdown},
  listing only,
  enhanced jigsaw,
  breakable,
  listing options={
    basicstyle=\ttfamily\footnotesize,
    showstringspaces=false,
    numbers=none,
    breaklines=true,
    breakatwhitespace=true,
    escapeinside={(*@}{@*)},
    prebreak=\mbox{\textcolor{red}{$\hookleftarrow$}},
    postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
  },
  boxrule=0.5pt,
  arc=2pt,
  left=12pt,right=2pt,top=8pt,bottom=2pt,
  titlerule=0pt,
  toprule=0.5pt,
  bottomrule=0.5pt,
  leftrule=0.5pt,
  rightrule=0.5pt
}

% Admonition/Callout boxes with colors matching the design
% Note - Blue
\newtcolorbox{note}[1][]{
  colback=blue!5!white,
  colframe=blue!70!black,
  colbacktitle=blue!10!white,
  coltitle=blue!90!black,
  fonttitle=\bfseries\sffamily,
  title={Note},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Attention - Orange
\newtcolorbox{attention}[1][]{
  colback=orange!5!white,
  colframe=orange!70!black,
  colbacktitle=orange!10!white,
  coltitle=orange!90!black,
  fonttitle=\bfseries\sffamily,
  title={Attention},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Important - Blue (with lightning icon concept)
\newtcolorbox{important}[1][]{
  colback=blue!5!white,
  colframe=blue!70!black,
  colbacktitle=blue!10!white,
  coltitle=blue!90!black,
  fonttitle=\bfseries\sffamily,
  title={Important},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  before upper={\parindent0pt},
  #1
}

% Caution - Orange (with exclamation)
\newtcolorbox{caution}[1][]{
  colback=orange!5!white,
  colframe=orange!70!black,
  colbacktitle=orange!10!white,
  coltitle=orange!90!black,
  fonttitle=\bfseries\sffamily,
  title={Caution},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Hint - Green (with lightbulb)
\newtcolorbox{hint}[1][]{
  colback=green!5!white,
  colframe=green!70!black,
  colbacktitle=green!10!white,
  coltitle=green!90!black,
  fonttitle=\bfseries\sffamily,
  title={Hint},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Warning - Orange/Yellow (with triangle)
\newtcolorbox{warning}[1][]{
  colback=yellow!10!white,
  colframe=orange!70!black,
  colbacktitle=orange!10!white,
  coltitle=orange!90!black,
  fonttitle=\bfseries\sffamily,
  title={Warning},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% See Also - Green
\newtcolorbox{seealso}[1][]{
  colback=green!5!white,
  colframe=green!70!black,
  colbacktitle=green!10!white,
  coltitle=green!90!black,
  fonttitle=\bfseries\sffamily,
  title={See Also},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Danger - Red
\newtcolorbox{danger}[1][]{
  colback=red!5!white,
  colframe=red!70!black,
  colbacktitle=red!10!white,
  coltitle=red!90!black,
  fonttitle=\bfseries\sffamily,
  title={Danger},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Tip - Green
\newtcolorbox{tip}[1][]{
  colback=green!5!white,
  colframe=green!70!black,
  colbacktitle=green!10!white,
  coltitle=green!90!black,
  fonttitle=\bfseries\sffamily,
  title={Tip},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Error - Darker Red
\newtcolorbox{error}[1][]{
  colback=red!5!white,
  colframe=red!80!black,
  colbacktitle=red!15!white,
  coltitle=red!95!black,
  fonttitle=\bfseries\sffamily,
  title={Error},
  boxrule=1pt,
  arc=3pt,
  left=8pt,
  right=8pt,
  top=8pt,
  bottom=8pt,
  leftrule=4pt,
  #1
}

% Legacy boxes (for compatibility)
\newtcolorbox{requirement}[1][]{
  colback=blue!5!white,
  colframe=accentblue,
  fonttitle=\bfseries\sffamily,
  title={Requirements},
  boxrule=1pt,
  arc=2pt,
  #1
}
"""
    
    # Add packages if needed (before \begin{document})
    if packages_to_add:
        doc_begin_match = re.search(r'\\begin\{document\}', content)
        if doc_begin_match:
            insert_pos = doc_begin_match.start()
            packages_str = '\n'.join(packages_to_add) + '\n'
            content = content[:insert_pos] + packages_str + content[insert_pos:]
        else:
            usepackage_matches = list(re.finditer(r'\\usepackage(?:\[[^\]]*\])?\{[^}]+\}', content))
            if usepackage_matches:
                last_match = usepackage_matches[-1]
                insert_pos = content.find('\n', last_match.end())
                if insert_pos == -1:
                    insert_pos = last_match.end()
                packages_str = '\n' + '\n'.join(packages_to_add) + '\n'
                content = content[:insert_pos] + packages_str + content[insert_pos:]
    
    # Add color definitions if they don't exist
    if '\\definecolor{lightgray}' not in content:
        usepackage_matches = list(re.finditer(r'\\usepackage(?:\[[^\]]*\])?\{[^}]+\}', content))
        if usepackage_matches:
            last_match = usepackage_matches[-1]
            insert_pos = content.find('\n', last_match.end())
            if insert_pos == -1:
                insert_pos = last_match.end()
            code_block_pos = content.find('\\newtcblisting{pythoncode}')
            if code_block_pos != -1 and code_block_pos < insert_pos:
                content = content[:code_block_pos] + color_defs + '\n' + content[code_block_pos:]
            else:
                content = content[:insert_pos] + '\n' + color_defs + '\n' + content[insert_pos:]
        else:
            docclass_match = re.search(r'\\documentclass.*?\n', content)
            if docclass_match:
                insert_pos = docclass_match.end()
                content = content[:insert_pos] + color_defs + '\n' + content[insert_pos:]
    
    # Check if code block definitions already exist
    if '\\newtcblisting{pythoncode}' not in content:
        title_match = re.search(r'\\title\{', content)
        doc_begin_match = re.search(r'\\begin\{document\}', content)
        color_def_match = re.search(r'\\definecolor\{warningred\}', content)
        
        insert_pos = 0
        if color_def_match:
            insert_pos = content.find('\n', color_def_match.end())
            if insert_pos == -1:
                insert_pos = color_def_match.end()
        elif title_match:
            insert_pos = title_match.start()
        elif doc_begin_match:
            insert_pos = doc_begin_match.start()
        else:
            docclass_match = re.search(r'\\documentclass.*?\n', content)
            if docclass_match:
                insert_pos = docclass_match.end()
        
        if insert_pos > 0:
            content = content[:insert_pos] + '\n' + code_block_defs + '\n' + content[insert_pos:]
    
    return content

def replace_verbatim_with_styled_code(content):
    r"""Replace \begin{verbatim}...\end{verbatim} with styled code blocks for all languages"""
    verbatim_pattern = r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}'
    
    def detect_language(verbatim_content):
        """Detect the programming language from code content - check strongest indicators first"""
        content = verbatim_content.strip()
        content_lower = content.lower()
        
        # 0. Markdown definitive patterns (check FIRST - backticks, colons, math delimiters, or citations = Markdown)
        # Triple backticks (```), triple colons (:::), quadruple colons (::::), math delimiters ($, $$), 
        # citation patterns ([@ or @), or single backtick in code fence context are definitive Markdown/MyST syntax
        has_triple_backticks = '```' in content
        has_triple_colons = ':::' in content
        has_quadruple_colons = '::::' in content
        has_math_dollar = '$' in content  # Inline math delimiter
        has_math_double_dollar = '$$' in content  # Display math delimiter
        # Check for citation patterns: [@...] or @... (MyST citation syntax)
        # For short blocks (up to 2-3 lines), citation patterns indicate Markdown
        lines = [line for line in content.split('\n') if line.strip()]
        line_count = len(lines)
        # Check if content has citation patterns and is short (2-3 lines max)
        has_citation_pattern = (('[@' in content or re.search(r'@[a-zA-Z0-9\-_]+', content)) and line_count <= 3)
        # Check for single backtick in Markdown context (code fence markers or inline code)
        # Single backtick alone is too common, but if we also have triple backticks or it's clearly a code fence, it's Markdown
        has_single_backtick_in_context = ('`' in content and ('```' in content or re.search(r'`[^`\n]+`', content)))
        
        if has_triple_backticks or has_triple_colons or has_quadruple_colons or has_math_dollar or has_math_double_dollar or has_citation_pattern or has_single_backtick_in_context:
            return ('markdowncode', 'Markdown')
        
        # 1. Python definitive patterns (check SECOND - absolutely definitive Python syntax)
        # These patterns definitively indicate Python code - no need to check other languages
        python_definitive_patterns = [
            r'\bimport\s+[\w.]+(\s+as\s+\w+)?',       # import module [as alias] or import package.module [as alias]
            r'\bfrom\s+[\w.]+\s+import',               # from package.module import ... or from module import ...
            r'\bif\s+.*:\s*$',                         # if statement with colon (Python-style)
            r'\belse\s*:\s*$',                         # else statement with colon (Python-style)
            r'\belif\s+.*:\s*$',                       # elif statement with colon (Python-style)
            r'\bfor\s+.*\s+in\s+',                     # for ... in ... (Python for loop)
            r'\bprint\s*\(',                           # print() function call
        ]
        has_python_definitive = any(re.search(pattern, content, re.MULTILINE) for pattern in python_definitive_patterns)
        
        if has_python_definitive:
            # If we have any of these definitive Python patterns:
            # - import/from statements
            # - if/else/elif with colons
            # - for ... in loops
            # - print() function
            # It's definitely Python - no need to check other languages
            return ('pythoncode', 'Python')
        
        # 2. YAML definitive patterns (check early - 3+ key:value pairs = YAML)
        # Count key:value patterns (key: followed by value or on next line)
        yaml_key_value_pattern = r'^\s*\w+\s*:\s*'
        yaml_key_matches = len(re.findall(yaml_key_value_pattern, content, re.MULTILINE))
        
        # YAML frontmatter markers
        has_yaml_frontmatter = content.strip().startswith('---') or content.strip().startswith('- - -')
        
        # If we have 3 or more key:value patterns or frontmatter, it's definitely YAML
        if yaml_key_matches >= 3 or has_yaml_frontmatter:
            # It's YAML - no need to check bash or python patterns
            return ('yamlcode', 'YAML')
        
        # 3. Markdown indicators (check early - headings are very distinctive, BEFORE shell/bash)
        # Check if content has both level 2 (##) and level 3 (###) headings
        has_level2_heading = re.search(r'^##\s+', content, re.MULTILINE) is not None
        has_level3_heading = re.search(r'^###\s+', content, re.MULTILINE) is not None
        
        # Markdown should have at least 2 levels of headings (## and ###)
        has_multiple_heading_levels = has_level2_heading and has_level3_heading
        
        if has_multiple_heading_levels:
            # Remove comment lines (starting with #) to check for Python/Shell patterns
            content_without_comments = []
            for line in content.split('\n'):
                stripped = line.strip()
                # Skip comment-only lines (starting with #)
                if not stripped.startswith('#'):
                    content_without_comments.append(line)
            
            content_no_comments = '\n'.join(content_without_comments)
            
            # Check for Python patterns (excluding # comments)
            python_patterns_in_content = [
                r'\bimport\s+[\w.]+',          # import statements
                r'\bfrom\s+[\w.]+\s+import',   # from ... import
                r'\bdef\s+\w+\s*\(',           # def function(
                r'\bclass\s+\w+',              # class ClassName
                r'\bprint\s*\(',               # print()
                r'\bif\s+.*:\s*$',             # if ... :
                r'\bfor\s+.*\s+in\s+',         # for ... in ...
            ]
            has_python_patterns = any(re.search(pattern, content_no_comments, re.MULTILINE) for pattern in python_patterns_in_content)
            
            # Check for Bash/Shell patterns (excluding # comments)
            shell_patterns_in_content = [
                r'\bgit\s+', r'\bcd\s+', r'\bpip\s+', r'\bjupyter\s+',
                r'\bmkdir\s+', r'\bls\s+', r'\bsudo\s+',
            ]
            has_shell_patterns = any(re.search(pattern, content_no_comments, re.MULTILINE | re.IGNORECASE) for pattern in shell_patterns_in_content)
            
            # If no Python or Shell patterns, and has multiple heading levels, it's Markdown
            if not has_python_patterns and not has_shell_patterns and yaml_key_matches < 3:
                return ('markdowncode', 'Markdown')
        
        # 3. Shell/Bash indicators (check after Python imports, YAML, and Markdown)
        # Check for shell commands anywhere in the content (even with # comments)
        # Commands can appear before # comments on the same line
        shell_command_patterns = [
            r'\bgit\s+',                    # git commands
            r'\bcd\s+',                     # cd commands
            r'\bmkdir\s+',                  # mkdir commands
            r'\bls\s+',                     # ls commands
            r'\bsudo\s+',                   # sudo commands
            r'\bpip\s+',                    # pip commands
            r'\bjupyter\s+book\s+',         # jupyter book commands
            r'\bmyst\s+',                   # myst commands
            r'\bapt\s+', r'\byum\s+', r'\bbrew\s+',  # package managers
            r'\bpython\s+-m\s+',            # python -m commands
            r'\.\\venv', r'\./venv',        # virtual environment paths
            r'\.\\Scripts', r'\./bin',      # script paths
            r'\bwinget\s+',                 # Windows package manager
            r'\bsource\s+',                 # source command (bash)
            r'\bexport\s+',                 # export command (bash)
            r'\becho\s+',                   # echo command
            r'\bcat\s+',                    # cat command
            r'^\$',                         # Command prompt $ at start
        ]
        # Check if content contains shell commands
        # Strip # comments from each line before checking (handles inline comments)
        lines_for_checking = []
        for line in content.split('\n'):
            # Remove inline comments (everything after # that's not part of a string/path)
            # Simple approach: split on # and take the first part
            if '#' in line:
                before_comment = line.split('#')[0].strip()
                if before_comment:  # Only add if there's content before the comment
                    lines_for_checking.append(before_comment)
            else:
                lines_for_checking.append(line)
        
        content_for_shell_check = '\n'.join(lines_for_checking)
        has_shell_commands = any(re.search(pattern, content_for_shell_check, re.MULTILINE | re.IGNORECASE) for pattern in shell_command_patterns)
        
        # Check if content has Markdown headings (##, ###, etc.) - if so, skip shell detection
        has_markdown_headings = (
            re.search(r'^##\s+', content, re.MULTILINE) or  # Level 2 heading
            re.search(r'^###\s+', content, re.MULTILINE) or  # Level 3 heading
            re.search(r'^####\s+', content, re.MULTILINE)   # Level 4 heading
        )
        
        # Also check original content for command prompts and shell-specific patterns
        has_shell_indicators = (
            re.search(r'^[$#>]\s+', content, re.MULTILINE) or  # Command prompts
            re.search(r'\.\\', content) or                     # Windows paths
            re.search(r'\./', content) or                      # Unix paths
            has_shell_commands
        )
        
        # If we have shell commands and it's not YAML, JSON, or Markdown, it's bash
        # Check if it's NOT YAML/JSON/Markdown first
        is_yaml_format = (
            '---' in content[:10] or
            (re.search(r'^\s*\w+:\s*[^\s]+', content, re.MULTILINE) and 
             not any(cmd in content_lower for cmd in ['pip ', 'python ', 'jupyter ', 'git ', 'cd ', 'mkdir']))
        )
        is_json_format = content.strip().startswith(('{', '['))
        
        # Skip shell detection if it has Markdown headings (already handled earlier)
        if has_shell_indicators and not is_yaml_format and not is_json_format and not has_markdown_headings:
            return ('bashcode', 'Bash/Shell')
        
        # 3. Python indicators (check after shell/bash, YAML, and import statements)
        # Python has specific keywords: def, import, from, class, etc.
        # NOTE: We already checked import statements above, so this is for other Python patterns
        # NOTE: We don't use # as indicator since it's also used in shell scripts
        python_strong_indicators = [
            r'\bdef\s+\w+\s*\(',           # def function_name(
            r'\bclass\s+\w+',               # class ClassName
            # Note: import patterns already checked above, but keeping here for other cases
            r'\bimport\s+\w+',              # import module (if not caught above)
            r'\bfrom\s+\w+\s+import',       # from module import (if not caught above)
            r'\bif\s+__name__',             # if __name__
            r'\breturn\s+',                 # return statement
            r'\btry:\s*$',                  # try:
            r'\bexcept\s',                  # except
            r'\bwith\s+\w+',                # with statement
            r'\basync\s+def',               # async def
            r'np\.', r'pd\.', r'plt\.',     # Common libraries
            r'\bprint\s*\(',                # print() function
            r'\bif\s+.*:',                  # if statement with colon
            r'\bfor\s+.*:',                 # for loop with colon
            r'\bwhile\s+.*:',               # while loop with colon
        ]
        # Check for Python keywords - must have multiple indicators to be sure
        python_count = sum(1 for pattern in python_strong_indicators if re.search(pattern, content, re.MULTILINE | re.IGNORECASE))
        # Python code usually has indentation and colons after control structures
        has_python_structure = (
            python_count >= 2 or
            (python_count >= 1 and (':' in content and ('def ' in content or 'import ' in content or 'from ' in content)))
        )
        # Exclude if it looks like YAML (has key: value patterns without Python structure)
        is_yaml_like = (
            '---' in content[:10] or
            (re.search(r'^\s*\w+:\s*[^=]+$', content, re.MULTILINE) and 
             not ('def ' in content or 'import ' in content or 'print' in content))
        )
        if has_python_structure and not is_yaml_like:
            return ('pythoncode', 'Python')
        
        # 4. BibTeX indicators (check for @ entries and multiple {} patterns)
        bibtex_indicators = [
            r'@\w+\{',                      # @article{ or @book{
            r'\{[^}]+\}',                   # Multiple braces
        ]
        bibtex_count = sum(1 for pattern in bibtex_indicators if re.search(pattern, content))
        # BibTeX has @ entries and typically multiple {} patterns
        has_bibtex_entry = re.search(r'@\w+\{', content) is not None
        has_multiple_braces = content.count('{') >= 2 and content.count('}') >= 2
        if has_bibtex_entry or (bibtex_count >= 2) or (content.count('@') >= 1 and has_multiple_braces):
            return ('styledcode', 'BibTeX')
        
        # 5. YAML indicators (fallback - for cases with 1-2 key:value patterns + YAML keywords)
        # This is a fallback for YAML files with fewer key:value patterns but YAML-specific keywords
        if yaml_key_matches >= 1:
            yaml_keywords = [
                'version:', 'title:', 'yaml', 'jupytext:', 'kernelspec:', 
                'project:', 'toc:', 'site:', 'exports:', 'authors:', 
                'description:', 'keywords:', 'abbreviations:', 'date:',
                'name:', 'display_name:', 'language:', 'format:', 
                'text_representation:', 'jupytext_version:', 'numbering:',
                'headings:', 'code_cell:', 'figures:', 'tables:', 'equations:'
            ]
            has_yaml_keywords = any(keyword in content_lower for keyword in yaml_keywords)
            
            # If it has key:value patterns and YAML keywords, it's YAML
            if has_yaml_keywords and ':' in content:
                return ('yamlcode', 'YAML')
        
        # Fallback: Markdown with other indicators (single level heading + markdown features)
        markdown_indicators = [
            r'\*\*[^*]+\*\*',               # **bold**
            r'\[.*\]\(.*\)',                # [link](url)
            r'^\s*-\s+',                    # - list item
            r'^\s*\d+\.\s+',                # 1. numbered list
        ]
        markdown_count = sum(1 for pattern in markdown_indicators if re.search(pattern, content, re.MULTILINE))
        # Markdown with heading structure (single level)
        if markdown_count >= 2 and (content.strip().startswith('#') or re.search(r'^#{1,6}\s+\w+', content, re.MULTILINE)):
            # Double-check it's not Python/Bash/YAML
            # Check for Python patterns (excluding # comments)
            content_no_hash = '\n'.join([line for line in content.split('\n') if not line.strip().startswith('#')])
            has_python_in_content = any(re.search(pattern, content_no_hash, re.MULTILINE) 
                                      for pattern in [r'\bimport\s+', r'\bfrom\s+.*\s+import', r'\bdef\s+\w+\s*\(', r'\bprint\s*\('])
            # Check for shell patterns
            has_shell_in_content = any(re.search(pattern, content_no_hash, re.MULTILINE | re.IGNORECASE) 
                                     for pattern in [r'\bgit\s+', r'\bcd\s+', r'\bpip\s+'])
            
            if yaml_key_matches < 3 and not has_python_in_content and not has_shell_in_content:
                return ('markdowncode', 'Markdown')
        
        # 5. JSON indicators
        json_indicators = [
            r'^\s*[{\[]',                   # Starts with { or [
            r'"\w+":',                      # "key":
            r'"version"', r'"name"', r'"title"'
        ]
        if content.strip().startswith(('{', '[')) or any(re.search(pattern, content) for pattern in json_indicators):
            return ('jsoncode', 'JSON')
        
        # Shell/Bash detection already handled at the beginning
        # This section is now just a fallback for edge cases
        
        # Default: generic styled code block
        return ('styledcode', 'Code')
    
    def replace_verbatim(match):
        verbatim_content = match.group(1)
        
        # Skip if empty or just whitespace
        if not verbatim_content.strip():
            return match.group(0)
        
        # Detect language
        code_type, language_name = detect_language(verbatim_content)
        
        # For markdown code blocks (containing ``` or ::: or ::::), use raw listings box with line breaking
        # Uses listings engine with basic text mode (no syntax parsing) but with line breaking enabled
        if code_type == 'markdowncode':
            # Use markdownraw which uses listings with line breaking enabled
            # The escapeinside option in markdownraw allows special characters to be displayed as-is
            return f'\\begin{{markdownraw}}\n{verbatim_content}\\end{{markdownraw}}'
        
        # Use the appropriate styled code block with language label
        if code_type == 'styledcode':
            # Use generic styled code block with language parameter
            return f'\\begin{{{code_type}}}[lightgray]{{{language_name}}}\n{verbatim_content}\\end{{{code_type}}}'
        else:
            # Use language-specific code block (already has language label in definition)
            return f'\\begin{{{code_type}}}\n{verbatim_content}\\end{{{code_type}}}'
    
    content = re.sub(verbatim_pattern, replace_verbatim, content, flags=re.DOTALL)
    return content

def copy_bibliography_files(tex_file):
    """Copy bibliography files from content/ to LaTeX directory"""
    print_step("Copying bibliography files...")
    
    if not tex_file or not tex_file.exists():
        return 0
    
    tex_dir = tex_file.parent
    bib_files_found = 0
    
    # Find all .bib files in content/ directory
    content_dir = PROJECT_ROOT / "content"
    
    if content_dir.exists():
        for bib_file in content_dir.glob("*.bib"):
            dest_bib = tex_dir / bib_file.name
            try:
                shutil.copy2(bib_file, dest_bib)
                bib_files_found += 1
                print_success(f"Copied bibliography: {bib_file.name}")
            except Exception as e:
                print_warning(f"Failed to copy {bib_file.name}: {e}")
    
    if bib_files_found > 0:
        print_success(f"Copied {bib_files_found} bibliography file(s)")
    
    return bib_files_found

def fix_bibliography_references(content, tex_file):
    """Fix bibliography references in LaTeX content to point to correct .bib files"""
    if not tex_file or not tex_file.exists():
        return content
    
    tex_dir = tex_file.parent
    
    # Find available .bib files in the LaTeX directory
    bib_files = list(tex_dir.glob("*.bib"))
    
    if not bib_files:
        return content
    
    # Prefer main.bib (if it exists and has content), then references.bib, then any other .bib file
    preferred_bib = None
    # First check for main.bib (often contains all references)
    for bib_file in bib_files:
        if bib_file.name.lower() == 'main.bib':
            # Check if file has content (not empty)
            try:
                with open(bib_file, 'r', encoding='utf-8') as f:
                    if f.read().strip():
                        preferred_bib = bib_file.name
                        break
            except:
                pass
    
    # If not found, check for references.bib
    if not preferred_bib:
        for bib_file in bib_files:
            if bib_file.name.lower() == 'references.bib':
                preferred_bib = bib_file.name
                break
    
    # If still not found, use first available
    if not preferred_bib and bib_files:
        preferred_bib = bib_files[0].name
    
    if preferred_bib:
        # Replace \bibliography{...} with correct file (without .bib extension)
        bib_name_no_ext = preferred_bib.replace('.bib', '')
        # Remove duplicate or malformed bibliography commands
        # Remove commands like \b\bibliography or bibliography without backslash
        content = re.sub(r'\\b\\bibliography\{[^}]+\}', '', content)
        content = re.sub(r'[^\\]bibliography\{[^}]+\}', '', content)
        # Replace all \bibliography{...} with the correct one
        content = re.sub(r'\\bibliography\{[^}]+\}', f'\\bibliography{{{bib_name_no_ext}}}', content)
        # Ensure exactly one bibliography command exists before \end{document}
        end_doc_match = re.search(r'\\end\{document\}', content)
        if end_doc_match:
            before_end = content[:end_doc_match.start()]
            after_end = content[end_doc_match.start():]
            # Count bibliography commands
            bib_count = before_end.count('\\bibliography{')
            if bib_count == 0:
                # Add bibliography command before \end{document}
                content = before_end.rstrip() + f'\n\\bibliography{{{bib_name_no_ext}}}\n' + after_end
            elif bib_count > 1:
                # Remove all and add one correct one
                before_end = re.sub(r'\\bibliography\{[^}]+\}', '', before_end)
                content = before_end.rstrip() + f'\n\\bibliography{{{bib_name_no_ext}}}\n' + after_end
        print_success(f"Updated bibliography reference to: {preferred_bib}")
    
    return content

def apply_springer_book_style(tex_file):
    """Apply Springer book style with custom code blocks to LaTeX file"""
    print_step("Applying Springer book style with custom code blocks...")
    
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace documentclass from article to book
        content = re.sub(r'\\documentclass\{article\}', r'\\documentclass[11pt]{book}', content)
        
        # Find where packages start (after documentclass)
        docclass_match = re.search(r'\\documentclass.*?\n', content)
        if docclass_match:
            insert_pos = docclass_match.end()
            
            # Check if Springer style already applied
            style_already_applied = 'usepackage[margin=0.85in' in content
            
            if not style_already_applied:
                # Insert Springer book style preamble
                springer_preamble = r"""
\usepackage[margin=0.85in,top=0.9in,bottom=0.9in]{geometry}
\usepackage{amsmath,amssymb,amsfonts,amsthm}
\usepackage{booktabs}
\usepackage[colorlinks=true,linkcolor=blue!70!black,citecolor=blue!70!black,urlcolor=blue!70!black]{hyperref}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{float}
\usepackage{multicol}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage[most]{tcolorbox}
\usepackage{tikz}
\usepackage{framed}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{subcaption}

"""
                # Insert before existing packages
                content = content[:insert_pos] + springer_preamble + content[insert_pos:]
        
        # Add code block definitions (always, to ensure they exist)
        content = add_code_block_definitions(content)
        
        # Replace verbatim blocks with styled code blocks for all languages
        content = replace_verbatim_with_styled_code(content)
        
        # Force all figures and tables to appear HERE (not float) using [H] placement
        # Replace all figure placement options with [H] - ensures figures appear exactly where they are in text
        content = re.sub(r'\\begin\{figure\}(\[[^\]]*\])?', r'\\begin{figure}[H]', content)
        # Replace all table placement options with [H] - ensures tables appear exactly where they are in text
        content = re.sub(r'\\begin\{table\}(\[[^\]]*\])?', r'\\begin{table}[H]', content)
        
        # Fix bibliography references - ensure they point to correct .bib files
        content = fix_bibliography_references(content, tex_file)
        
        # Ensure bibliography command is properly formatted (fix missing backslash if any)
        # Fix any bibliography commands that might be missing the backslash
        content = re.sub(r'([^\\])ibliography\{', r'\1\\bibliography{', content)
        # Fix bibliography at start of line
        content = re.sub(r'^\s*ibliography\{', r'\\bibliography{', content, flags=re.MULTILINE)
        
        # Fix SVG references to PNG (if converted)
        content = re.sub(r'\.svg\}', '.png}', content)
        content = re.sub(r'\.gif\}', '.png}', content)
        content = re.sub(r'\.webp\}', '.png}', content)
        
        # Fix blank lines in code blocks (must be last, after all other modifications)
        # Remove blank lines immediately after code block begin commands
        code_block_types = ['pythoncode', 'verbatim', 'bashcode', 'yamlcode', 'jsoncode', 'markdowncode', 'styledcode', 'lstlisting']
        for code_type in code_block_types:
            # Remove leading blank lines after \begin{code_type}
            content = content.replace(f'\\begin{{{code_type}}}\n\n', f'\\begin{{{code_type}}}\n')
            # Handle styledcode with parameters: \begin{styledcode}[lightgray]{Code}\n\n
            if code_type == 'styledcode':
                content = re.sub(r'\\begin\{styledcode\}\[[^\]]+\]\{[^\}]+\}\n\n+', 
                               lambda m: m.group(0).replace('\n\n', '\n'), content)
            # Remove trailing blank lines before \end{code_type}
            content = content.replace(f'\n\n\\end{{{code_type}}}', f'\n\\end{{{code_type}}}')
            # Fix empty code blocks
            content = content.replace(f'\\begin{{{code_type}}}\n\\end{{{code_type}}}', 
                                    f'\\begin{{{code_type}}} \n\\end{{{code_type}}}')
        
        # Fix section numbering: In book class, sections before chapters are numbered 0.1, 0.2, etc.
        # Make sections start from 1 instead of 0.1
        doc_begin_match = re.search(r'\\begin\{document\}', content)
        if doc_begin_match:
            insert_pos = doc_begin_match.end()
            # Check if numbering fix already applied
            if '\\setcounter{section}{0}' not in content:
                numbering_fix = r"""
% Fix section numbering to start from 1 (not 0.1)
\setcounter{chapter}{0}
\setcounter{section}{0}
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}
"""
                # Insert right after \begin{document}
                content = content[:insert_pos] + numbering_fix + '\n' + content[insert_pos:]
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if style_already_applied:
            print_success("Springer style already applied (updated code blocks)")
        else:
            print_success("Springer book style applied")
        return True
    except Exception as e:
        print_error(f"Error applying Springer style: {e}")
        return False

def fix_nested_figures(content):
    """Fix nested figure blocks by converting nested figures to minipages using line-by-line parsing"""
    # Use a line-by-line approach with stack to correctly identify outer figures
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a figure block
        # Match \begin{figure} with optional [options] and optional \centering on same or next line
        if r'\begin{figure}' in line:
            # Collect all lines until we find matching \end{figure} using stack
            figure_start = i
            figure_lines = [line]
            depth = 1
            j = i + 1
            
            # Find matching \end{figure} by counting depth
            while j < len(lines) and depth > 0:
                next_line = lines[j]
                figure_lines.append(next_line)
                
                if r'\begin{figure}' in next_line:
                    depth += 1
                elif r'\end{figure}' in next_line:
                    depth -= 1
                
                j += 1
            
            # Check if this figure block contains nested figures
            figure_block = '\n'.join(figure_lines)
            if figure_block.count(r'\begin{figure}') > 1:
                # Contains nested figures - fix it
                # Find all nested figures (complete \begin{figure}...\end{figure} pairs)
                nested_pattern = r'\\begin\{figure\}(\[!htbp\])?\s*\\centering\s*(.*?)\\end\{figure\}'
                nested_matches = list(re.finditer(nested_pattern, figure_block, flags=re.DOTALL))
                
                if nested_matches:
                    # Extract outer caption and label (after nested figures)
                    remaining = figure_block
                    for nm in nested_matches:
                        remaining = remaining.replace(nm.group(0), '')
                    
                    outer_caption_match = re.search(r'\\caption\[\]?\{([^}]*)\}', remaining)
                    outer_label_match = re.search(r'\\label\{([^}]+)\}', remaining)
                    
                    # Build fixed figure
                    opts_match = re.search(r'\\begin\{figure\}(\[!htbp\]|\[H\])?', figure_block)
                    opts = '[H]'  # Always use [H] to force HERE placement
                    
                    fixed_figure = f'\\begin{{figure}}{opts}\n\\centering\n'
                    
                    # Convert nested figures to minipages
                    for nm in nested_matches:
                        nested_body = nm.group(2)
                        
                        img_match = re.search(r'\\includegraphics.*?\{([^}]+)\}', nested_body)
                        nested_caption = re.search(r'\\caption\[\]?\{([^}]*)\}', nested_body)
                        nested_label = re.search(r'\\label\{([^}]+)\}', nested_body)
                        
                        fixed_figure += '\\begin{minipage}{0.48\\linewidth}\n\\centering\n'
                        if img_match:
                            fixed_figure += f'\\includegraphics[width=\\linewidth]{{{img_match.group(1)}}}\n'
                        if nested_caption:
                            fixed_figure += f'\\subcaption{{{nested_caption.group(1)}}}\n'
                        if nested_label:
                            fixed_figure += f'\\label{{{nested_label.group(1)}}}\n'
                        fixed_figure += '\\end{minipage}\n'
                    
                    # Add outer caption and label
                    if outer_caption_match:
                        fixed_figure += f'{outer_caption_match.group(0)}\n'
                    if outer_label_match:
                        fixed_figure += f'{outer_label_match.group(0)}\n'
                    fixed_figure += '\\end{figure}'
                    
                    fixed_lines.append(fixed_figure)
                    i = j
                    continue
            
            # No nested figures, add lines normally
            fixed_lines.extend(figure_lines)
            i = j
            continue
        
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

def convert_admonitions_to_callouts(content):
    """Convert MyST admonitions (framed blocks) to styled callout boxes"""
    # Map admonition names to their LaTeX box environments
    # Handle variations like "See Also" and "SeeAlso"
    admonition_map = {
        'Note': 'note',
        'Attention': 'attention',
        'Important': 'important',
        'Caution': 'caution',
        'Hint': 'hint',
        'Warning': 'warning',
        'See Also': 'seealso',
        'SeeAlso': 'seealso',
        'Danger': 'danger',
        'Tip': 'tip',
        'Error': 'error',
    }
    
    # Keywords that indicate specific admonition types (for custom titles)
    warning_keywords = [
        'pdf exports require', 'require.*latex', 'require.*typst', 
        'warning will occur', 'cannot find', 'need.*install',
        'install.*required', 'missing.*dependency'
    ]
    danger_keywords = ['failure', 'critical', 'error', 'incorrect.*lead', 'structural failure']
    important_keywords = ['important', 'crucial', 'essential', 'must', 'should', 'required']
    tip_keywords = ['tip', 'hint', 'consider', 'try using', 'suggestion']
    note_keywords = ['note', 'notice', 'remember']
    caution_keywords = ['caution', 'careful', 'beware']
    
    # Pattern to match: \begin{framed}\textbf{AdmonitionName}\\...content...\end{framed}
    # The pattern needs to handle multiline content and extract the admonition name and content
    def replace_admonition(match):
        full = match.group(0)
        inner = match.group(1)
        
        # Extract the admonition name from \textbf{Name}\\
        admonition_match = re.search(r'\\textbf\{([^}]+)\}', inner)
        if not admonition_match:
            return full  # Return original if we can't find the name
        
        admonition_name = admonition_match.group(1).strip()
        box_type = admonition_map.get(admonition_name)
        
        # If exact match not found, try to detect by content/keywords
        if not box_type:
            # Get full content (including title) for keyword detection
            full_content = inner.lower()
            title_text = admonition_name.lower()
            
            # Check for warning keywords (highest priority for custom warnings)
            if any(re.search(keyword, title_text + ' ' + full_content, re.IGNORECASE) for keyword in warning_keywords):
                box_type = 'warning'
            # Check for danger keywords
            elif any(re.search(keyword, title_text + ' ' + full_content, re.IGNORECASE) for keyword in danger_keywords):
                box_type = 'danger'
            # Check for important keywords
            elif any(re.search(keyword, title_text + ' ' + full_content, re.IGNORECASE) for keyword in important_keywords):
                box_type = 'important'
            # Check for tip keywords
            elif any(re.search(keyword, title_text + ' ' + full_content, re.IGNORECASE) for keyword in tip_keywords):
                box_type = 'tip'
            # Check for note keywords
            elif any(re.search(keyword, title_text + ' ' + full_content, re.IGNORECASE) for keyword in note_keywords):
                box_type = 'note'
            # Check for caution keywords
            elif any(re.search(keyword, title_text + ' ' + full_content, re.IGNORECASE) for keyword in caution_keywords):
                box_type = 'caution'
            else:
                # Unknown admonition type, return original
                return full
        
        # Extract content after \textbf{Name}\\
        # Remove the \textbf{Name}\\ line(s)
        content = re.sub(r'\\textbf\{[^}]+\}\\\\?\s*\n?', '', inner, count=1)
        
        # Clean up any remaining \\ at the start of lines
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove leading \\ if present
            cleaned_line = line.lstrip('\\').lstrip()
            cleaned_lines.append(cleaned_line)
        
        content = '\n'.join(cleaned_lines).strip()
        
        # Remove empty lines at start and end
        while content.startswith('\n'):
            content = content[1:]
        while content.endswith('\n'):
            content = content[:-1]
        
        # Return the styled callout box
        if content:
            return f'\\begin{{{box_type}}}\n{content}\n\\end{{{box_type}}}'
        else:
            # Empty content, return empty box
            return f'\\begin{{{box_type}}}\n\\end{{{box_type}}}'
    
    # Pattern matches \begin{framed}...\end{framed} with nested content
    # Uses non-greedy match to handle multiple admonitions
    pattern = r'\\begin\{framed\}(.*?)\\end\{framed\}'
    content = re.sub(pattern, replace_admonition, content, flags=re.DOTALL)
    
    return content

def fix_all_latex_issues(tex_file):
    """Fix all LaTeX issues including Unicode, missing packages, etc."""
    print_step("Fixing LaTeX issues (Unicode, packages, etc.)...")
    
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix nested figures first
        content = fix_nested_figures(content)
        
        # Convert admonitions (framed blocks) to styled callout boxes
        content = convert_admonitions_to_callouts(content)
        
        # Fix verbatim blocks inside figure blocks (not allowed in LaTeX)
        def remove_verbatim_from_figure(match):
            """Remove verbatim blocks from inside figure blocks"""
            full = match.group(0)
            opts = match.group(1) or '[!htbp]'
            inner = match.group(2)
            
            # Check if inner contains verbatim blocks
            if '\\begin{verbatim}' in inner or '\\begin{pythoncode}' in inner:
                # Remove verbatim/pythoncode blocks from figure
                # Replace with comment or remove entirely
                inner_clean = re.sub(
                    r'\\begin\{(?:verbatim|pythoncode)\}.*?\\end\{(?:verbatim|pythoncode)\}',
                    '% Code block removed from figure (not allowed in LaTeX)',
                    inner,
                    flags=re.DOTALL
                )
                
                # Rebuild figure
                result = f'\\begin{{figure}}{opts}\n\\centering\n{inner_clean}\\end{{figure}}'
                return result
            
            return full
        
        # Find figure blocks that might contain verbatim blocks
        # Note: After this, all figures will be changed to [H] placement anyway
        figure_with_verbatim_pattern = r'\\begin\{figure\}(\[!htbp\]|\[h\]|\[t\]|\[b\]|\[p\]|\[H\])?\s*\\centering\s*([\s\S]*?)\\end\{figure\}'
        content = re.sub(figure_with_verbatim_pattern, remove_verbatim_from_figure, content, flags=re.DOTALL)
        
        # Fix blank lines at start/end of code blocks (can cause verbatim errors)
        # Use simple string replacement for more reliable fixing
        
        # Remove blank lines immediately after \begin{pythoncode} or \begin{verbatim}
        # Pattern: \begin{pythoncode}\n\n -> \begin{pythoncode}\n
        content = content.replace('\\begin{pythoncode}\n\n', '\\begin{pythoncode}\n')
        content = content.replace('\\begin{verbatim}\n\n', '\\begin{verbatim}\n')
        
        # Also handle multiple blank lines
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        
        # Remove trailing blank lines before \end
        content = content.replace('\n\n\\end{pythoncode}', '\n\\end{pythoncode}')
        content = content.replace('\n\n\\end{verbatim}', '\n\\end{verbatim}')
        
        # Fix empty code blocks
        content = content.replace('\\begin{pythoncode}\n\\end{pythoncode}', '\\begin{pythoncode} \n\\end{pythoncode}')
        content = content.replace('\\begin{verbatim}\n\\end{verbatim}', '\\begin{verbatim} \n\\end{verbatim}')
        
        # Fix Unicode characters
        replacements = {
            '√': r'$\sqrt{}$',
            '√Hz': r'$\sqrt{\text{Hz}}$',
            'ϵ': r'$\epsilon$',
            'ɛ': r'$\varepsilon$',
            'ε': r'$\varepsilon$',
            '₂': r'$_2$',
            '₁': r'$_1$',
            '₀': r'$_0$',
            '⁻': r'$^-$',
            '─': '--',
            '━': '==',
            '│': '|',
            '┃': '||',
            '┌': '+',
            '┐': '+',
            '└': '+',
            '┘': '+',
            '├': '+',
            '┤': '+',
            '┬': '+',
            '┴': '+',
            '┼': '+',
        }
        
        for char, replacement in replacements.items():
            content = content.replace(char, replacement)
        
        # Remove emoji and problematic Unicode
        try:
            import unicodedata
            content = unicodedata.normalize('NFKD', content)
            content = ''.join(c for c in content if unicodedata.category(c) != 'Mn')
            content = ''.join(c for c in content if not unicodedata.combining(c))
        except:
            pass
        
        # Fix titles with & characters
        content = re.sub(r'\\title\{([^}]*&[^}]*)\}', lambda m: '\\title{' + m.group(1).replace('&', r'\&') + '}', content)
        content = re.sub(r'\\chapter\{([^}]*&[^}]*)\}', lambda m: '\\chapter{' + m.group(1).replace('&', r'\&') + '}', content)
        
        # Comment out unsupported image formats
        content = re.sub(r'\\includegraphics.*?\{[^}]+\.svg[^}]*\}', r'% SVG removed: \0', content)
        content = re.sub(r'\\includegraphics.*?\{[^}]+\.webp[^}]*\}', r'% WebP removed: \0', content)
        content = re.sub(r'\\includegraphics.*?\{[^}]+\.gif[^}]*\}', r'% GIF removed: \0', content)
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_success("Fixed LaTeX issues")
        return True
    except Exception as e:
        print_error(f"Failed to fix LaTeX issues: {e}")
        return False

def compile_to_pdf(tex_file):
    """Compile LaTeX to PDF using pdflatex with BibTeX for bibliography"""
    print_step(f"Compiling {tex_file.name} to PDF (this may take a minute)...")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_dir = tex_file.parent
    tex_name_without_ext = tex_file.stem
    
    # Step 1: First pdflatex pass (generates .aux file with citation keys)
    print(f"  Pass 1/4: pdflatex (generate .aux file)...")
    cmd = f'pdflatex -interaction=nonstopmode "{tex_file.name}"'
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=tex_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            if result.stderr:
                print_warning(f"LaTeX warnings: {result.stderr[-500:]}")
    except subprocess.TimeoutExpired:
        print_error("Compilation timed out")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    
    time.sleep(0.5)
    
    # Step 2: Run BibTeX to process bibliography and resolve citations
    aux_file = tex_dir / f"{tex_name_without_ext}.aux"
    bib_files = list(tex_dir.glob("*.bib"))
    
    if aux_file.exists() and bib_files:
        print(f"  Pass 2/4: bibtex (process bibliography)...")
        # Find the bibliography file name (without .bib extension)
        preferred_bib = None
        for bib_file in bib_files:
            if bib_file.name.lower() in ['main.bib', 'references.bib']:
                preferred_bib = bib_file.stem
                break
        if not preferred_bib and bib_files:
            preferred_bib = bib_files[0].stem
        
        if preferred_bib:
            cmd = f'bibtex "{tex_name_without_ext}"'
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=tex_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    print_success(f"  BibTeX processed bibliography: {preferred_bib}.bib")
                else:
                    print_warning(f"  BibTeX warnings: {result.stdout[-500:]}")
            except subprocess.TimeoutExpired:
                print_warning("BibTeX timed out, continuing...")
            except Exception as e:
                print_warning(f"BibTeX error (continuing): {e}")
    
    time.sleep(0.5)
    
    # Step 3-4: Run pdflatex two more times to include bibliography and resolve all references
    for i in range(2):
        print(f"  Pass {i+3}/4: pdflatex (include bibliography and resolve references)...")
        cmd = f'pdflatex -interaction=nonstopmode "{tex_file.name}"'
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=tex_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0 and i == 0:
                if result.stderr:
                    print_warning(f"LaTeX warnings: {result.stderr[-500:]}")
        except subprocess.TimeoutExpired:
            print_error("Compilation timed out")
            return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False
        
        time.sleep(0.5)
    
    # Find the generated PDF
    pdf_file = tex_file.with_suffix('.pdf')
    
    if pdf_file.exists():
        output_pdf = OUTPUT_DIR / "Comprehensive-MyST-Document.pdf"
        shutil.copy2(pdf_file, output_pdf)
        
        # Copy PDF to downloads folder for website access
        downloads_dir = PROJECT_ROOT / "downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        downloads_pdf = downloads_dir / "Comprehensive-MyST-Document.pdf"
        shutil.copy2(pdf_file, downloads_pdf)
        print_success(f"PDF copied to downloads folder: {downloads_pdf}")
        
        # Keep final LaTeX file that was used for PDF generation
        final_tex = OUTPUT_DIR / "Comprehensive-MyST-Document.tex"
        shutil.copy2(tex_file, final_tex)
        print_success(f"Final LaTeX file saved: {final_tex}")
        
        size_mb = output_pdf.stat().st_size / (1024 * 1024)
        print_success(f"PDF created: {output_pdf} ({size_mb:.2f} MB)")
        return True
    else:
        print_error("PDF not created. Check LaTeX log for errors.")
        log_file = tex_file.with_suffix('.log')
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                log_content = f.read()
                errors = [line for line in log_content.split('\n') 
                         if '!' in line and ('Error' in line or 'Fatal' in line)][-10:]
                if errors:
                    print_error("Recent LaTeX errors:")
                    for err in errors:
                        print_error(f"  {err[:150]}")
        return False

def main():
    """Main execution function"""
    print_header("PDF Generation for Comprehensive MyST Document")
    
    # Step 1: Build and execute code cells
    build_and_execute()
    
    # Step 2: Export to LaTeX
    tex_file = export_to_latex()
    if not tex_file:
        print_error("Failed to export to LaTeX")
        sys.exit(1)
    
    # Step 3: Copy images from build directories
    copied = copy_build_images_to_latex()
    if copied > 0:
        print_success(f"Copied {copied} images from build directories")
    
    # Step 4: Copy referenced images
    copied_refs = copy_referenced_images(tex_file)
    if copied_refs > 0:
        print_success(f"Copied {copied_refs} referenced images")
    
    # Step 5: Convert images (SVG/GIF -> PNG)
    files_dir = LATEX_DIR / "files"
    if files_dir.exists():
        converted = convert_images_in_directory(files_dir)
        if converted > 0:
            print_success(f"Converted {converted} images (SVG/GIF -> PNG)")
    
    # Step 6: Link images to empty figure blocks
    linked = link_images_to_figures(tex_file)
    if linked > 0:
        print_success(f"Linked {linked} images to figure blocks")
    
    # Step 6b: Copy bibliography files to LaTeX directory
    copied_bib = copy_bibliography_files(tex_file)
    
    # Step 7: Fix LaTeX issues
    fix_all_latex_issues(tex_file)
    
    # Step 8: Apply Springer book style
    apply_springer_book_style(tex_file)
    
    # Step 8b: Link images again after removing verbatim blocks (figures with comments need images)
    linked_after = link_images_to_figures(tex_file)
    if linked_after > 0:
        print_success(f"Linked {linked_after} additional images after code block removal")
    
    # Step 9: Compile to PDF
    if compile_to_pdf(tex_file):
        print_success("\nPDF generation completed successfully!")
        print(f"Output: {OUTPUT_DIR / 'Comprehensive-MyST-Document.pdf'}")
    else:
        print_error("\nPDF generation failed")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

