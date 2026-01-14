import discord
from discord.ext import commands
import random
import sqlite3
from datetime import datetime

# --- 1. GENİŞLETİLMİŞ VERİ HAVUZU ---
# Her kategoride en az 5 meslek ve detayları mevcut
CAREER_DATA = {
    "teknoloji": [
        {"meslek": "Yazılım Mühendisi", "ozellik": "Analitik düşünme ve problem çözme.", "neden": "Teknik becerilerin yazılım dünyasına çok uygun."},
        {"meslek": "Veri Bilimci", "ozellik": "Veri analizi ve istatistiksel modelleme.", "neden": "Sayılarla aranın iyi olması seni bu alanda parlatır."},
        {"meslek": "Siber Güvenlik Uzmanı", "ozellik": "Sistem koruma ve sızma testleri.", "neden": "Dikkatli ve detaycı yapın güvenliğin anahtarı."},
        {"meslek": "Bulut Mimarı", "ozellik": "Sanal altyapı yönetimi ve depolama.", "neden": "Karmaşık sistemleri yönetme yeteneğin tam bu işe göre."},
        {"meslek": "Yapay Zeka Eğitmeni", "ozellik": "Model eğitimi ve veri etiketleme.", "neden": "Geleceğin teknolojisine yön verme isteğin çok güçlü."}
    ],
    "tasarim": [
        {"meslek": "UI/UX Tasarımcısı", "ozellik": "Kullanıcı deneyimi ve arayüz estetiği.", "neden": "Görsel zekan dijital ürünleri güzelleştirebilir."},
        {"meslek": "3D Modelleme Uzmanı", "ozellik": "Üç boyutlu nesne ve mekan tasarımı.", "neden": "Hacimsel düşünme yeteneğin bu alanda fark yaratır."},
        {"meslek": "Oyun Tasarımcısı", "ozellik": "Oyun mekaniği ve hikaye kurgusu.", "neden": "Hayal gücün ve oyunlara ilgin seni başarılı kılar."},
        {"meslek": "Hareketli Grafik Tasarımcısı", "ozellik": "Animasyon ve video kurgu.", "neden": "Dinamik görsellere olan ilgin bu meslek için biçilmiş kaftan."},
        {"meslek": "Moda Tasarımcısı", "ozellik": "Tekstil ve stil geliştirme.", "neden": "Estetik algın ve trend takibin bu alanda seni ön plana çıkarır."}
    ],
    "saglik": [
        {"meslek": "Biyomedikal Mühendisi", "ozellik": "Tıbbi cihaz tasarımı ve bakımı.", "neden": "Mühendislik ve sağlığı birleştirme yetin harika."},
        {"meslek": "Genetik Uzmanı", "ozellik": "DNA analizi ve kalıtsal hastalık araştırması.", "neden": "Bilime ve araştırmaya olan merakın bu iş için ideal."},
        {"meslek": "Nöropsikolog", "ozellik": "Beyin ve davranış ilişkisi uzmanı.", "neden": "İnsan zihnini anlama isteğin bu alanda derinleşmeni sağlar."},
        {"meslek": "Dijital Sağlık Danışmanı", "ozellik": "Tele-tıp ve sağlık uygulamaları yönetimi.", "neden": "Teknoloji ve sağlığı harmanlama vizyonun çok modern."},
        {"meslek": "Epidemiyolog", "ozellik": "Salgın hastalık takibi ve veri analizi.", "neden": "Toplumsal fayda sağlama isteğin bu meslekle örtüşüyor."}
    ],
    "ekonomi": [
        {"meslek": "Yatırım Danışmanı", "ozellik": "Portföy yönetimi ve piyasa analizi.", "neden": "Finansal öngörülerin sermayeyi doğru yönetmeni sağlar."},
        {"meslek": "Kripto Varlık Analisti", "ozellik": "Dijital piyasalar ve blockchain ekonomisi.", "neden": "Yeni nesil finansa olan ilgin seni bu alanda uzman yapar."},
        {"meslek": "Risk Yönetim Uzmanı", "ozellik": "Finansal tehlikeleri öngörme ve önleme.", "neden": "Tedbirli ve stratejik düşünmen bu işin temeli."},
        {"meslek": "E-Ticaret Stratejisti", "ozellik": "Online satış ve pazarlama yönetimi.", "neden": "Ticari zekan dijital pazarda sana yol açar."},
        {"meslek": "Aktüer", "ozellik": "İstatistiksel risk ve sigorta hesabı.", "neden": "Matematiksel kesinlik takıntın bu işte en büyük avantajın."}
    ],
    "hukuk": [
        {"meslek": "Bilişim Hukuku Avukatı", "ozellik": "Dijital suçlar ve internet hukuku.", "neden": "Teknolojiye olan ilgin hukuk bilginle birleşince rakipsiz olursun."},
        {"meslek": "Arabulucu", "ozellik": "Uyuşmazlık çözümü ve uzlaştırma.", "neden": "Güçlü iletişim ve ikna kabiliyetin bu iş için yaratılmış."},
        {"meslek": "Patent Vekili", "ozellik": "Fikri mülkiyet ve buluş koruma.", "neden": "Yeniliklere değer vermen ve korumacı yapın seni başarılı kılar."},
        {"meslek": "Kişisel Veri Danışmanı (KVKK)", "ozellik": "Veri güvenliği ve gizlilik hukuku.", "neden": "Gizliliğe verdiğin önem bu modern hukuk dalında seni uzman yapar."},
        {"meslek": "Uluslararası Hukukçu", "ozellik": "Devletler arası hukuk ve ticaret.", "neden": "Geniş vizyonun ve dil yeteneğin seni dünyaya açar."}
    ]
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
        view = CareerSelectionView(user_info={
            "name": self.name.value,
            "age": self.age.value,
            "interests": self.interests.value
        })
        embed = discord.Embed(
            title=f"Memnun Oldum {self.name.value}!",
            description=f"Verdiğin bilgileri aldım. Yaşın **{self.age.value}** ve ilgi alanların harika görünüyor.\n\nŞimdi bir **sektör seç**, sana en uygun 5 meslek arasından bir analiz yapayım.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# --- 4. SEKTÖR SEÇİMİ VE ANALİZ ---
class CareerSelectionView(discord.ui.View):
    def __init__(self, user_info):
        super().__init__(timeout=None)
        self.user_info = user_info

    async def suggest_career(self, interaction: discord.Interaction, category: str):
        # Seçilen kategoriden rastgele 1 meslek seçiyoruz (Hepsinde en az 5 tane var)
        data = random.choice(CAREER_DATA[category])
        
        conn = sqlite3.connect('kariyer_danismani.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, username, age, interests, suggested, timestamp) VALUES (?,?,?,?,?,?)",
                       (str(interaction.user.id), self.user_info['name'], self.user_info['age'], 
                        self.user_info['interests'], data['meslek'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        embed = discord.Embed(title="📊 Detaylı Kariyer Analiz Sonucu", color=discord.Color.gold())
        embed.add_field(name="🎯 Senin İçin En İyi Meslek", value=f"**{data['meslek']}**", inline=False)
        embed.add_field(name="💡 Neden Bu Mesleği Önerdik?", value=data['neden'], inline=False)
        embed.add_field(name="📜 Mesleğin Temel Özellikleri", value=data['ozellik'], inline=False)
        embed.set_footer(text=f"Analiz tamamlandı. Yolun açık olsun {self.user_info['name']}!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Teknoloji", style=discord.ButtonStyle.blurple, emoji="💻")
    async def tech(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "teknoloji")

    @discord.ui.button(label="Tasarım", style=discord.ButtonStyle.green, emoji="🎨")
    async def design(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "tasarim")

    @discord.ui.button(label="Sağlık", style=discord.ButtonStyle.red, emoji="🩺")
    async def health(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "saglik")

    @discord.ui.button(label="Ekonomi", style=discord.ButtonStyle.gray, emoji="💰")
    async def economy(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "ekonomi")

    @discord.ui.button(label="Hukuk", style=discord.ButtonStyle.secondary, emoji="⚖️")
    async def law(self, interaction: discord.Interaction, btn: discord.ui.Button):
        await self.suggest_career(interaction, "hukuk")

# --- 5. BOT BAŞLATMA ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    init_db()
    print(f"Bot {bot.user} aktif ve veri tabanı bağlandı!")

@bot.command()
async def kariyer(ctx):
    view = discord.ui.View()
    button = discord.ui.Button(label="Tanışmaya Başla ve Profil Oluştur", style=discord.ButtonStyle.primary, emoji="📝")
    
    async def button_callback(interaction):
        await interaction.response.send_modal(IntroModal())
    
    button.callback = button_callback
    view.add_item(button)
    
    embed = discord.Embed(
        title="🚀 Geleceğini Tasarla: Kariyer Rehberi",
        description="Hoş geldin! Seni tanımak ve sana en uygun kariyer yolunu çizmek için sabırsızlanıyorum.\n\nLütfen aşağıdaki butona tıkla ve kısa formu doldur.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=view)

bot.run("TOKENİNİ BURAYA GİR !!!")
