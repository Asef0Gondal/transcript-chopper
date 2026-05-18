import tkinter as tk
from tkinter import filedialog, messagebox
import os

def chop_transcript():
    root = tk.Tk()
    root.withdraw()
    
    # 1. Ask the user for the file
    file_path = filedialog.askopenfilename(title="Select your massive transcript file", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not file_path:
        return
        
    try:
        # 2. Read the massive file
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        words = text.split()
        max_words = 10000 # Roughly 30-40 pages
        
        # 3. Create a folder to hold the chunks
        folder_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        out_folder = os.path.join(folder_dir, f"{base_name}_Chunks_For_Gemini")
        os.makedirs(out_folder, exist_ok=True)
        
        current_chunk = []
        part_num = 1
        count = 0
        
        # 4. Chop it up
        for w in words:
            current_chunk.append(w)
            count += 1
            if count >= max_words:
                # Wait for the end of a sentence so we don't cut mid-sentence!
                if w.endswith('.') or w.endswith('?') or w.endswith('!') or count >= max_words + 500:
                    with open(os.path.join(out_folder, f"Part_{part_num}.txt"), "w", encoding="utf-8") as out:
                        out.write(" ".join(current_chunk))
                    part_num += 1
                    current_chunk = []
                    count = 0
                    
        # Write whatever is left
        if current_chunk:
            with open(os.path.join(out_folder, f"Part_{part_num}.txt"), "w", encoding="utf-8") as out:
                out.write(" ".join(current_chunk))
                
        # 5. Success Message & Open the folder
        messagebox.showinfo("Done!", f"Successfully chopped into {part_num} perfectly-sized text files!\n\nYou can now easily drag and drop these into Gemini.")
        os.system(f'open "{out_folder}"')
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    chop_transcript()
