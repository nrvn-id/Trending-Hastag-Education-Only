import customtkinter as ctk
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import traceback
import time
import os

# --- KONFIGURASI TEMA ELEGANT DARK ---
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class ViralScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TrendScout Elite v2.1")
        self.geometry("850x900")
        
        # Palette Warna Elegan
        self.bg_color = "#121212"        # Deep Black
        self.card_color = "#1E1E1E"      # Charcoal Grey
        self.accent_color = "#BB86FC"    # Soft Purple / Rose Gold hint
        self.text_primary = "#E1E1E1"    # Off White
        self.text_secondary = "#A0A0A0"  # Muted Grey
        
        self.configure(fg_color=self.bg_color)

        # --- UI LAYOUT ---
        # Header Area
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(pady=(40, 20), padx=40, fill="x")

        self.title_label = ctk.CTkLabel(
            self.header, 
            text="TrendScout", 
            font=("Inter", 36, "bold"),
            text_color=self.accent_color
        )
        self.title_label.pack(side="left")

        self.badge = ctk.CTkLabel(
            self.header,
            text="PREMIUM ELITE",
            font=("Inter", 10, "bold"),
            fg_color="#332940",
            text_color=self.accent_color,
            corner_radius=8,
            width=110,
            height=24
        )
        self.badge.pack(side="left", padx=15, pady=(8, 0))

        # Main Button (Glassmorphism style)
        self.scan_btn = ctk.CTkButton(
            self, 
            text="START DEEP ANALYSIS", 
            command=self.start_scan_thread, 
            height=55, 
            font=("Inter", 15, "bold"),
            fg_color=self.accent_color,
            hover_color="#9965f4",
            text_color="#000000",
            corner_radius=12
        )
        self.scan_btn.pack(pady=10, padx=50, fill="x")

        # Result Box Area (Charcoal Card)
        self.res_container = ctk.CTkFrame(self, fg_color=self.card_color, corner_radius=15, border_width=1, border_color="#333333")
        self.res_container.pack(padx=40, pady=15, fill="both", expand=True)

        self.result_text = ctk.CTkTextbox(
            self.res_container, 
            font=("Consolas", 15), 
            fg_color="transparent", 
            text_color=self.text_primary,
            border_width=0
        )
        self.result_text.pack(padx=20, pady=20, fill="both", expand=True)

        # Log Area (Minimalist Dark)
        self.log_label = ctk.CTkLabel(self, text="System Diagnostics", font=("Inter", 11, "bold"), text_color=self.text_secondary)
        self.log_label.pack(padx=55, anchor="w")

        self.log_text = ctk.CTkTextbox(
            self, 
            height=130, 
            font=("Consolas", 11), 
            fg_color="#0A0A0A", 
            text_color="#00FF41", # Classic Matrix Green for logs
            border_width=0,
            corner_radius=12
        )
        self.log_text.pack(padx=40, pady=(5, 30), fill="x")

    def write_log(self, message):
        self.log_text.insert("end", f"[log] › {message}\n")
        self.log_text.see("end")

    def start_scan_thread(self):
        self.scan_btn.configure(state="disabled", text="ANALYZING DATA...")
        self.result_text.delete("1.0", "end")
        self.log_text.delete("1.0", "end")
        self.write_log("Initializing core engine...")
        threading.Thread(target=self.scrape_logic, daemon=True).start()

    def scrape_logic(self):
        driver = None
        try:
            user_name = "Keisei"
            brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            user_data = f"C:\\Users\\{user_name}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"

            self.write_log("Syncing Brave profile...")
            options = uc.ChromeOptions()
            options.add_argument(f"--user-data-dir={user_data}")
            options.add_argument("--profile-directory=Default")
            
            driver = uc.Chrome(options=options, browser_executable_path=brave_path, version_main=145)
            
            self.write_log("Establishing connection to TikTok servers...")
            driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en")
            
            time.sleep(15)
            driver.refresh()
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 500);")
            
            self.write_log("Executing JS Extraction Module...")
            
            js_extract = """
            let results = [];
            let container = document.getElementById('hashtagItemContainer');
            if (container) {
                let items = container.querySelectorAll('span[class*="hashtagName"]');
                items.forEach(el => results.push(el.innerText.trim()));
            }
            return results;
            """
            
            data = driver.execute_script(js_extract)
            
            if not data:
                elements = driver.find_elements(By.TAG_NAME, "span")
                data = [el.text.strip() for el in elements if "#" in el.text or len(el.text) > 3]

            hashtags = []
            blacklist = ["Analytics", "Ranking", "Country", "Region", "Industry", "Popularity"]
            
            for item in data:
                text = item.replace("#", "").strip()
                if text and text not in blacklist and len(text) > 1:
                    hashtags.append(f"#{text}")

            hashtags = list(dict.fromkeys(hashtags))

            if hashtags:
                self.write_log(f"Process complete. Found {len(hashtags)} unique entries.")
                self.after(0, lambda: self.display_results(hashtags))
            else:
                self.write_log("Warning: No data stream detected.")

        except Exception:
            self.write_log(f"Critical Failure:\n{traceback.format_exc()}")
        finally:
            if driver:
                self.write_log("Securing session and closing...")
                time.sleep(3)
                driver.quit()
                self.after(0, self.reset_ui)

    def reset_ui(self):
        self.scan_btn.configure(state="normal", text="START DEEP ANALYSIS")

    def display_results(self, data):
        if data:
            self.result_text.insert("end", "  ANALYSIS RESULT: TOP TRENDS\n")
            self.result_text.insert("end", "  " + "─"*30 + "\n\n")
            for i, tag in enumerate(data[:25], 1):
                self.result_text.insert("end", f"  [{i:02d}]  {tag.upper()}\n")
            self.write_log("Data rendered successfully.")
        else:
            self.result_text.insert("end", "  STATUS: NO DATA DETECTED")

if __name__ == "__main__":
    app = ViralScannerApp()
    app.mainloop()