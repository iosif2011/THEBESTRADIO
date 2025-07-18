import os
import sys

def install_mutagen():
    """Install mutagen library if not present"""
    try:
        import mutagen
        return True
    except ImportError:
        print("Installing mutagen library...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
            print("Mutagen installed successfully!")
            return True
        except Exception as e:
            print(f"Failed to install mutagen: {e}")
            return False

def get_audio_duration(file_path):
    """Get the duration of an audio file in seconds"""
    try:
        # Import here after ensuring mutagen is installed
        from mutagen import File
        
        audio_file = File(file_path)
        if audio_file is not None and hasattr(audio_file, 'info') and audio_file.info is not None:
            duration = audio_file.info.length
            return int(duration) if duration else 0
        else:
            print(f"Could not read audio info from: {os.path.basename(file_path)}")
            return 0
    except Exception as e:
        print(f"Error reading {os.path.basename(file_path)}: {e}")
        return 0

def format_filename(filename):
    """Convert filename to uppercase first letters and remove spaces"""
    # Remove file extension
    name_without_ext = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    
    # Split by spaces, underscores, hyphens, and dots
    import re
    words = re.split(r'[\s_\-\.]+', name_without_ext)
    
    # Process each word to handle camelCase within words
    formatted_words = []
    for word in words:
        if word:  # Skip empty strings
            # Split camelCase words (like "yourSelf" -> "your", "Self")
            camel_parts = re.sub(r'([a-z])([A-Z])', r'\1 \2', word).split()
            
            # Capitalize each part
            for part in camel_parts:
                formatted_words.append(part.capitalize())
    
    # Join without spaces
    formatted_name = ''.join(formatted_words)
    
    return formatted_name + extension

def process_music_folder():
    # Check and install mutagen first
    if not install_mutagen():
        print("Cannot proceed without mutagen library!")
        return
    
    # Define the folder path
    folder_path = r"C:\Users\GIGABYTE\Desktop\code shits\raidio\ToKaliteroRadiofono\music"
    
    print(f"Looking for folder: {folder_path}")
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found!")
        print("Current directory:", os.getcwd())
        print("Please check if the path is correct.")
        return
    
    print(f"Folder found! Processing files...")
    
    # Supported audio formats
    audio_extensions = {'.mp3', '.flac', '.m4a', '.aac', '.ogg', '.wav', '.wma'}
    
    # List to store song information
    songs_info = []
    
    # Get all files in folder
    try:
        all_files = os.listdir(folder_path)
        print(f"Found {len(all_files)} files in folder")
    except Exception as e:
        print(f"Error reading folder: {e}")
        return
    
    audio_files_found = 0
    
    # Process each file in the folder
    for filename in all_files:
        file_path = os.path.join(folder_path, filename)
        
        # Skip if not a file
        if not os.path.isfile(file_path):
            print(f"Skipping (not a file): {filename}")
            continue
            
        # Check if it's an audio file
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in audio_extensions:
            print(f"Skipping (not audio): {filename}")
            continue
        
        audio_files_found += 1
        print(f"Processing audio file {audio_files_found}: {filename}")
        
        # Format the filename
        formatted_filename = format_filename(filename)
        
        # Get duration BEFORE renaming
        duration = get_audio_duration(file_path)
        
        # Rename the actual file if the name changed
        if formatted_filename != filename:
            new_file_path = os.path.join(folder_path, formatted_filename)
            try:
                os.rename(file_path, new_file_path)
                print(f"  -> Renamed: {filename} -> {formatted_filename}")
            except Exception as e:
                print(f"  -> Error renaming {filename}: {e}")
                formatted_filename = filename  # Keep original name if rename failed
        else:
            print(f"  -> No rename needed: {filename}")
        
        # Add to songs list
        songs_info.append({
            'filename': formatted_filename,
            'duration': duration
        })
        
        print(f"  -> Duration: {duration}s")
    
    print(f"\nTotal audio files processed: {len(songs_info)}")
    
    if len(songs_info) == 0:
        print("No audio files found to process!")
        return
    
    # Sort songs by filename for consistent output
    songs_info.sort(key=lambda x: x['filename'])
    
    # Create output text file
    output_path = os.path.join(folder_path, "songs_list.txt")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for song in songs_info:
                f.write(f'{{ filename: "{song["filename"]}", duration: {song["duration"]} }},\n')
        
        print(f"\nSUCCESS! Created '{output_path}' with {len(songs_info)} songs.")
        print(f"Output file location: {output_path}")
        
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    print("=== Music File Processor ===")
    print("Starting process...\n")
    process_music_folder()
    print("\nProcess completed!")
    input("Press Enter to exit...")