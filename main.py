import discord
from discord.ext import commands
import random
import sqlite3
from datetime import datetime

# --- VERİ TABANI AYARLARI ---
def init_db():
    conn = sqlite3.connect('kariyer_danismani.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS career_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            category TEXT,
            suggested_career TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(user_id, username, category, career):
    conn = sqlite3.connect('kariyer_danismani.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO career_logs (user_id, username, category, suggested_career, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, category, career, now))
    conn.commit()
    conn.close()

# --- VERİ HAVUZU ---
CAREER_POOL = {
    "teknoloji": {"baslik": "🚀 Teknoloji", "meslekler": ["Yazılım Mühendisi", "Veri Bilimci", "Siber Güvenlik"], "color": discord.Color.blue()},
    "tasarim": {"baslik": "🎨 Tasarım", "meslekler": ["UI/UX Tasarımcısı", "3D Artist", "Oyun Tasarımcısı"], "color": discord.Color.purple()},
    "saglik": {"baslik": "🏥 Sağlık", "meslekler": ["Biyomedikal Mühendisi", "Genetik Uzmanı"], "color": discord.Color.red()},
    "finans": {"baslik": "💰 Finans", "meslekler": ["Risk Analisti", "Yatırım Danışmanı"], "color": discord.Color.green()},
    "hukuk": {"baslik": "⚖️ Hukuk", "meslekler": ["Bilişim Avukatı", "Patent Vekili"], "color": discord.Color.dark_grey()}
}

class CareerButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_selection(self, interaction: discord.Interaction, key: str):
        data = CAREER_POOL[key]
        career = random.choice(data["meslekler"])
        
        # VERİ TABANINA KAYDET
        save_to_db(interaction.user.id, str(interaction.user), key, career)
        
        embed = discord.Embed(
            title=data["baslik"],
            description=f"Önerilen Meslek: **{career}**\n\n*Bu seçim veri tabanına kaydedildi.*",
            color=data["color"]
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Teknoloji", style=discord.ButtonStyle.primary, custom_id="persistent_tech")
    async def tech(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "teknoloji")

    @discord.ui.button(label="Tasarım", style=discord.ButtonStyle.secondary, custom_id="persistent_design")
    async def design(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "tasarim")

    @discord.ui.button(label="Sağlık", style=discord.ButtonStyle.danger, custom_id="persistent_health")
    async def health(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "saglik")

    @discord.ui.button(label="Finans", style=discord.ButtonStyle.success, custom_id="persistent_fin")
    async def finance(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "finans")

    @discord.ui.button(label="Hukuk", style=discord.ButtonStyle.secondary, custom_id="persistent_law")
    async def law(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_selection(interaction, "hukuk")

class CareerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        init_db() # Bot açılırken veri tabanını hazırla
        self.add_view(CareerButtonView())

    async def on_ready(self):
        print(f'{self.user} aktif. Veri tabanı bağlandı.')

bot = CareerBot()

@bot.command()
async def kariyer(ctx):
    view = CareerButtonView()
    await ctx.send("🎯 Kariyerini belirlemek için bir kategori seç:", view=view)

# Admin komutu: Veri tabanını Discord'dan görmek için
@bot.command()
@commands.has_permissions(administrator=True)
async def veriler(ctx):
    conn = sqlite3.connect('kariyer_danismani.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, category, suggested_career FROM career_logs ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await ctx.send("Henüz kayıtlı veri yok.")
        return

    mesaj = "**Son 5 Kariyer Sorgusu:**\n"
    for row in rows:
        mesaj += f"👤 {row[0]} | 📁 {row[1]} | 💼 {row[2]}\n"
    await ctx.send(mesaj)

TOKEN = "TOKENİNİ BURAYA GİR LOWW"
bot.run(TOKEN)
