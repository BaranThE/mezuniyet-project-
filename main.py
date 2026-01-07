import discord
from discord.ext import commands
import random
import sqlite3
from datetime import datetime

# --- 1. VERİ HAVUZU VE ÖZELLİKLER ---
CAREER_DETAILS = {
    "teknoloji": {
        "meslek": "Yazılım Mühendisi",
        "ozellik": "Analitik düşünme, problem çözme ve sürekli öğrenme odaklı bir kariyer.",
        "neden": "Verdiğin bilgilere göre teknolojiye yatkınlığın bu alanda fark yaratmanı sağlar."
    },
    "tasarim": {
        "meslek": "UI/UX Tasarımcısı",
        "ozellik": "Kullanıcı deneyimini iyileştiren, estetik ve fonksiyonelliği birleştiren bir alan.",
        "neden": "Yaratıcı yönün, dijital dünyada insanlara rehberlik edebilir."
    },
    "saglik": {
        "meslek": "Biyomedikal Mühendisi",
        "ozellik": "Mühendislik tekniklerini tıp alanındaki sorunları çözmek için kullanma yetisi.",
        "neden": "Bilime olan ilgin ve yardımseverliğin bu meslekte seni zirveye taşır."
    },
    "finans": {
        "meslek": "Kripto Varlık Analisti",
        "ozellik": "Dijital piyasaları takip eden, risk yönetimi ve matematiksel modelleme yapan bir uzmanlık.",
        "neden": "Hızlı karar verme yeteneğin finansal piyasalarda sana avantaj sağlar."
    }
}

# --- 2. VERİ TABANI ---
def init_db():
    conn = sqlite3.connect('kariyer_danismani.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, username TEXT, 
        age TEXT, interests TEXT, suggested TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# --- 3. TANIŞMA FORMU (MODAL) ---
class IntroModal(discord.ui.Modal, title='Kariyer Danışmanı Tanışma Formu'):
    name = discord.ui.TextInput(label='Adın Soyadın', placeholder='Lütfen buraya yaz...')
    age = discord.ui.TextInput(label='Yaşın', placeholder='Örn: 22')
    interests = discord.ui.TextInput(
        label='İlgi Alanların / Hobilerin', 
        style=discord.TextStyle.long,
        placeholder='Nelerden hoşlanırsın? Neleri iyi yaparsın?',
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Kullanıcı verilerini aldık, şimdi seçim ekranını gönderiyoruz
        view = CareerSelectionView(user_info={
            "name": self.name.value,
            "age": self.age.value,
            "interests": self.interests.value
        })
        embed = discord.Embed(
            title=f"Memnun Oldum {self.name.value}!",
            description=f"Verdiğin bilgileri aldım. Yaşın **{self.age.value}** ve ilgi alanların harika görünüyor.\n\nŞimdi sana en uygun mesleği bulmam için bir **sektör seç**.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# --- 4. SEKTÖR SEÇİMİ VE ANALİZ ---
class CareerSelectionView(discord.ui.View):
    def __init__(self, user_info):
        super().__init__(timeout=None)
        self.user_info = user_info

    async def suggest_career(self, interaction: discord.Interaction, category: str):
        data = CAREER_DETAILS[category]
        
        # SQL Kaydı
        conn = sqlite3.connect('kariyer_danismani.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, username, age, interests, suggested, timestamp) VALUES (?,?,?,?,?,?)",
                       (str(interaction.user.id), self.user_info['name'], self.user_info['age'], 
                        self.user_info['interests'], data['meslek'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        embed = discord.Embed(title="📊 Kariyer Analiz Sonucu", color=discord.Color.gold())
        embed.add_field(name="🎯 Tavsiye Edilen Meslek", value=f"**{data['meslek']}**", inline=False)
        embed.add_field(name="💡 Neden Bu Meslek?", value=data['neden'], inline=False)
        embed.add_field(name="📜 Mesleğin Özellikleri", value=data['ozellik'], inline=False)
        embed.set_footer(text=f"Sayın {self.user_info['name']}, bu analiz senin için özel hazırlandı.")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Teknoloji", style=discord.ButtonStyle.blurple)
    async def tech(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "teknoloji")

    @discord.ui.button(label="Tasarım", style=discord.ButtonStyle.green)
    async def design(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "tasarim")

    @discord.ui.button(label="Sağlık", style=discord.ButtonStyle.red)
    async def health(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "saglik")

# --- 5. ANA BOT KOMUTLARI ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    init_db()
    print(f"Bot {bot.user} hazır!")

@bot.command()
async def kariyer(ctx):
    # Kullanıcıya önce tanıtım ve tanışma butonu gönderilir
    view = discord.ui.View()
    button = discord.ui.Button(label="Tanışmaya Başla", style=discord.ButtonStyle.primary)
    
    async def button_callback(interaction):
        await interaction.response.send_modal(IntroModal())
    
    button.callback = button_callback
    view.add_item(button)
    
    embed = discord.Embed(
        title="🤖 Kariyer Danışmanına Hoş Geldin",
        description="Merhaba! Ben senin profesyonel rehberinim. Sana en doğru mesleği önerebilmem için önce seni biraz tanımam gerekiyor.\n\nAşağıdaki butona tıklayarak kendini tanıtmaya başlayabilirsin.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=view)

TOKEN = "TOKENİNİ BURAYA GİRRR"
bot.run(TOKEN)
