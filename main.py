import discord
from discord.ext import commands
import random
import sqlite3
from datetime import datetime

# --- 1. GENİŞLETİLMİŞ VE DETAYLANDIRILMIŞ VERİ HAVUZU ---
CAREER_DATA = {
    "teknoloji": [
        {"meslek": "Yazılım Mühendisi", "ozellik": "Karmaşık algoritmalar ve sistem mimarileri tasarlar.", "neden": "Teknik problem çözme yeteneğin ve mantıksal yaklaşımın yazılım dünyası için mükemmel bir temel oluşturuyor."},
        {"meslek": "Veri Bilimci", "ozellik": "Büyük veri setlerinden anlamlı stratejik sonuçlar çıkarır.", "neden": "Verileri analiz etme ve örüntüleri yakalama becerin, şirketlerin geleceğini şekillendirebilir."},
        {"meslek": "Siber Güvenlik Uzmanı", "ozellik": "Dijital varlıkları saldırılara karşı savunur ve sızma testleri yapar.", "neden": "Detaycı ve korumacı yapın, dijital dünyadaki güvenlik açıklarını kapatmak için çok değerli."},
        {"meslek": "Bulut Mimarı", "ozellik": "Modern şirketlerin tüm dijital altyapısını bulut üzerinde kurar.", "neden": "Sistemli düşünme tarzın, devasa veri ağlarını yönetmek için gereken disiplini sağlıyor."},
        {"meslek": "Yapay Zeka Mühendisi", "ozellik": "Kendi kendine öğrenen akıllı sistemler ve botlar geliştirir.", "neden": "Yenilikçi vizyonun, teknolojinin en ileri sınırında yer alan bu meslek için biçilmiş kaftan."},
        {"meslek": "DevOps Mühendisi", "ozellik": "Yazılım geliştirme ve operasyon süreçlerini otomatikleştirir.", "neden": "Süreç yönetimi ve hız odaklı yapın, teknoloji ekiplerinin verimliliğini artıracaktır."},
        {"meslek": "Mobil Uygulama Geliştirici", "ozellik": "iOS ve Android platformları için yenilikçi çözümler üretir.", "neden": "Yaratıcılığını pratik çözümlerle birleştirme yeteneğin, her an yanımızda olan uygulamalara dönüşebilir."},
        {"meslek": "Blokzincir Geliştirici", "ozellik": "Merkeziyetsiz finans ve güvenli veri sistemleri kurar.", "neden": "Şeffaflık ve ileri teknolojiye olan ilgin, geleceğin ekonomi altyapısını kurmanı sağlayabilir."},
        {"meslek": "Oyun Programcısı", "ozellik": "Fizik motorları ve interaktif oyun dünyaları yazar.", "neden": "Teknik becerilerini eğlence dünyasıyla birleştirerek milyonlara ulaşan dünyalar yaratabilirsin."},
        {"meslek": "Gömülü Sistemler Uzmanı", "ozellik": "Akıllı cihazların ve robotların iç yazılımlarını tasarlar.", "neden": "Donanım ve yazılımı bir arada kullanma yeteneğin, fiziksel dünyayı dijitalle kontrol etmeni sağlar."}
    ],
    "tasarim": [
        {"meslek": "UI/UX Tasarımcısı", "ozellik": "Kullanıcıların dijital ürünlerle olan etkileşimini en estetik hale getirir.", "neden": "Empati yeteneğin ve görsel estetik algın, kullanıcıların hayatını kolaylaştıran tasarımlara dönüşebilir."},
        {"meslek": "3D Modelleme Uzmanı", "ozellik": "Sinema ve oyunlar için gerçekçi üç boyutlu varlıklar üretir.", "neden": "Hacimsel düşünme ve sabırlı çalışma tarzın, hayalindeki dünyaları gerçeğe en yakın şekilde görselleştirebilir."},
        {"meslek": "Oyun Tasarımcısı", "ozellik": "Oyunların kurallarını, dünyasını ve hikaye akışını kurgular.", "neden": "Sınırsız hayal gücün ve oyun mekaniklerine olan merakın, unutulmaz deneyimler yaratmanı sağlayacaktır."},
        {"meslek": "Hareketli Grafik Tasarımcısı", "ozellik": "Videolar ve reklamlar için dinamik animasyonlar hazırlar.", "neden": "Zamanlama duygun ve dinamik görsel anlatım tarzın, mesajları etkileyici bir şekilde iletmeni sağlıyor."},
        {"meslek": "Endüstriyel Ürün Tasarımcısı", "ozellik": "Fiziksel ürünlerin kullanım ergonomisini ve şeklini tasarlar.", "neden": "Pratik zekan ve estetik bakış açın, günlük hayatta kullandığımız nesnelere ruh katabilir."},
        {"meslek": "Moda Tasarımcısı", "ozellik": "Kıyafet ve aksesuarlarda yeni trendler ve koleksiyonlar oluşturur.", "neden": "Stil duygun ve kültürel trendleri takip etme becerin, seni moda dünyasında öncü yapabilir."},
        {"meslek": "İç Mimarı", "ozellik": "Yaşam alanlarını fonksiyonel ve estetik şekilde dekore eder.", "neden": "Mekan algın ve renk uyumu konusundaki hassasiyetin, insanların huzur bulacağı alanlar yaratmanı sağlar."},
        {"meslek": "Grafik Tasarımcı", "ozellik": "Markaların görsel kimliğini ve iletişim materyallerini tasarlar.", "neden": "Sembolleri ve renkleri kullanarak mesaj iletme gücün, markaların sesini dünyaya duyurabilir."},
        {"meslek": "Dijital İllüstratör", "ozellik": "Kitaplar, oyunlar ve konsept tasarımlar için sanatsal çizimler yapar.", "neden": "Eşsiz çizim tarzın ve sanatsal derinliğin, hikayeleri görsel bir şölene dönüştürebilir."},
        {"meslek": "Karakter Tasarımcısı", "ozellik": "Animasyon projeleri için ikonik ve akılda kalıcı karakterler çizer.", "neden": "İnsan ve canlı formlarını yaratıcı bir şekilde yorumlama yeteneğin, efsanevi karakterler doğurabilir."}
    ],
    "saglik": [
        {"meslek": "Biyomedikal Mühendisi", "ozellik": "Tıp dünyası için ileri teknoloji cihazlar ve yapay organlar tasarlar.", "neden": "Mühendislik zekan ile insan hayatına dokunma isteğin, sağlık teknolojilerinde devrim yaratmanı sağlayabilir."},
        {"meslek": "Genetik Uzmanı", "ozellik": "DNA ve hücre seviyesinde hastalıkların tedavisini araştırır.", "neden": "Analitik merakın ve yaşamın şifrelerine olan ilgin, tıp dünyasındaki en zor soruları çözmeni sağlayabilir."},
        {"meslek": "Nöropsikolog", "ozellik": "Beyin fonksiyonları ile insan davranışları arasındaki bağı inceler.", "neden": "İnsan zihninin derinliklerine duyduğun merak, psikoloji ve biyolojiyi harika bir şekilde birleştiriyor."},
        {"meslek": "Dijital Sağlık Danışmanı", "ozellik": "Sağlık sistemlerinin dijitalleşmesini ve tele-tıp süreçlerini yönetir.", "neden": "Teknolojiyi sağlıkla birleştirme vizyonun, geleceğin hastanelerini yönetmen için ideal."},
        {"meslek": "Epidemiyolog", "ozellik": "Toplumsal hastalıkların yayılımını izler ve önleyici stratejiler geliştirir.", "neden": "Toplum sağlığını koruma arzun ve veri analizi yeteneğin, kriz anlarında hayat kurtarıcı olabilir."},
        {"meslek": "Diyetisyen", "ozellik": "Kişiye özel beslenme programları ile yaşam kalitesini artırır.", "neden": "Sağlıklı yaşam bilincin ve insanlara rehberlik etme isteğin, bu alanda seni çok başarılı kılacaktır."},
        {"meslek": "Fizyoterapist", "ozellik": "Hareket bozukluklarını fiziksel yöntemlerle tedavi eder.", "neden": "Sabırlı yapın ve insan anatomisine olan ilgin, hastaların hayata dönmesini sağlayacak en büyük gücün."},
        {"meslek": "Moleküler Biyolog", "ozellik": "Hücre seviyesinde yaşamın temel mekanizmalarını laboratuvarda inceler.", "neden": "Bilimsel titizliğin ve detaylara odaklanma becerin, temel bilimlerde büyük keşifler yapmanı sağlayabilir."},
        {"meslek": "Tıbbi Görüntüleme Teknikeri", "ozellik": "MR, BT gibi cihazlarla hastalıkların teşhis edilmesini sağlar.", "neden": "Teknik cihazlara olan ilgin ve dikkatli çalışma prensibin, doğru teşhisin ilk adımını oluşturur."},
        {"meslek": "Halk Sağlığı Uzmanı", "ozellik": "Tüm toplumun sağlık standartlarını yükseltecek politikalar üretir.", "neden": "Organizasyon yeteneğin ve geniş bakış açın, kitlesel refahı artırmak için çok uygun."}
    ],
    "ekonomi": [
        {"meslek": "Yatırım Danışmanı", "ozellik": "Piyasa trendlerini analiz ederek sermaye yönetimi yapar.", "neden": "Finansal öngörülerin ve stratejik karar alma becerin, yatırımların en verimli şekilde değerlendirilmesini sağlar."},
        {"meslek": "Kripto Varlık Analisti", "ozellik": "Blockchain tabanlı ekonomileri ve dijital paraları inceler.", "neden": "Yenilikçi finansal sistemlere olan ilgin, seni yeni dünyanın ekonomi uzmanı yapabilir."},
        {"meslek": "Risk Yönetim Uzmanı", "ozellik": "Şirketlerin karşı karşıya kalabileceği finansal tehlikeleri hesaplar.", "neden": "Temkinli yapın ve olasılıkları önceden görme yeteneğin, büyük krizlerin engellenmesini sağlar."},
        {"meslek": "E-Ticaret Stratejisti", "ozellik": "Online satış platformlarının büyüme ve pazarlama yollarını tasarlar.", "neden": "Dijital pazara olan hakimiyetin ve ticari zekan, global satış rekorları kırmanı sağlayabilir."},
        {"meslek": "Aktüer", "ozellik": "İstatistik kullanarak gelecek risklerin maliyetini hesaplar.", "neden": "Matematiksel kesinlik takıntın ve olasılık hesaplarındaki başarın, sigorta ve finans dünyasının temelini oluşturur."},
        {"meslek": "Finansal Denetçi", "ozellik": "Şirketlerin mali kayıtlarının doğruluğunu ve yasallığını inceler.", "neden": "Dürüstlük ilken ve detayları yakalama becerin, güvenilir bir finans dünyası için çok kritik."},
        {"meslek": "Pazarlama Müdürü", "ozellik": "Ürünlerin hedef kitleye ulaşması için yaratıcı kampanyalar yönetir.", "neden": "İletişim gücün ve insan psikolojisini anlama yeteneğin, markaları zirveye taşıyabilir."},
        {"meslek": "Uluslararası Ticaret Uzmanı", "ozellik": "Ülkeler arası mal ve hizmet akışını organize eder.", "neden": "Global vizyonun ve organizasyon yeteneğin, sınır ötesi iş birliklerini yönetmeni sağlar."},
        {"meslek": "Veri Analisti (Ekonomi)", "ozellik": "Ekonomik verileri görselleştirerek yönetimsel kararlar alınmasını sağlar.", "neden": "Karmaşık tabloları anlamlı hikayelere dönüştürme yeteneğin, iş dünyasının yönünü belirler."},
        {"meslek": "Girişimci", "ozellik": "Kendi iş fikrini hayata geçirerek sıfırdan bir değer yaratır.", "neden": "Liderlik özelliklerin ve risk alma cesaretin, seni kendi hayalinin patronu yapacaktır."}
    ],
    "hukuk": [
        {"meslek": "Bilişim Hukuku Avukatı", "ozellik": "İnternet suçları, veri gizliliği ve yapay zeka haklarını savunur.", "neden": "Teknoloji merakın hukuk bilginle birleşince, dijital çağın en aranan savunucusu olmanı sağlıyor."},
        {"meslek": "Arabulucu", "ozellik": "Taraflar arasındaki anlaşmazlıkları mahkemeye gitmeden çözer.", "neden": "Sakin yapın ve adil çözüm üretme yeteneğin, toplumsal barışa büyük katkı sağlar."},
        {"meslek": "Patent Vekili", "ozellik": "Yeni buluşların ve fikirlerin yasal haklarını koruma altına alır.", "neden": "Yaratıcı fikirlere duyduğun saygı ve korumacı yaklaşımın, mucitlerin en büyük desteği olacaktır."},
        {"meslek": "KVKK Danışmanı", "ozellik": "Kişisel verilerin korunması kanununa uyum süreçlerini yönetir.", "neden": "Gizliliğe verdiğin önem ve hukuki detaylara hakimiyetin, dijital dünyada güven inşa etmeni sağlar."},
        {"meslek": "Uluslararası Hukukçu", "ozellik": "Devletler arası anlaşmaları ve global ticaret davalarını yürütür.", "neden": "Yabancı dil yeteneğin ve geniş bakış açın, seni dünya sahnesinde bir hukuk temsilcisi yapabilir."},
        {"meslek": "Savcı", "ozellik": "Kamu adına suçları soruşturur ve adaletin tesisi için dava açar.", "neden": "Keskin adalet duygun ve kararlı duruşun, toplumun güvenliği için gereken disiplini sağlıyor."},
        {"meslek": "Noter", "ozellik": "Hukuki işlemlerin resmiyet kazanmasını ve güvenliğini onaylar.", "neden": "Güvenilir kişiliğin ve resmi süreçlere olan hakimiyetin, hukuki işlemlerin temel direği olmanı sağlıyor."},
        {"meslek": "Fikri Mülkiyet Uzmanı", "ozellik": "Telif hakları ve sanatçı haklarının korunmasını sağlar.", "neden": "Sanata ve emeğe verdiğin değer, yaratıcı insanların haklarını korumak için en büyük motivasyonun."},
        {"meslek": "Kurumsal Avukat", "ozellik": "Büyük şirketlerin tüm hukuki süreçlerini ve sözleşmelerini yönetir.", "neden": "Analitik düşünme tarzın ve stratejik planlama becerin, iş dünyasının karmaşık yapısını yönetebilir."},
        {"meslek": "İnsan Hakları Savunucusu", "ozellik": "Evrensel hakların korunması için global düzeyde çalışmalar yapar.", "neden": "Empati gücün ve haksızlığa karşı duyduğun büyük tepki, dünyayı daha adil bir yer yapmanı sağlayabilir."}
    ]
}

# --- 2. VERİ TABANI ---
DB_NAME = 'kariyer_danismani.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, username TEXT, 
            age TEXT, interests TEXT, suggested TEXT, timestamp TEXT)''')
        conn.commit()

def save_user_data(user_id, username, age, interests, suggested):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?)''', 
                            (str(user_id), username, age, interests, suggested, timestamp))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Hata: {e}")

# --- 3. AKILLI ANALİZ VE MODAL ---
class IntroModal(discord.ui.Modal, title='Kariyer Yolculuğun Başlıyor'):
    name = discord.ui.TextInput(label='Adın Soyadın', placeholder='Adınızı buraya yazınız...')
    age = discord.ui.TextInput(label='Yaşın', placeholder='Örn: 22')
    interests = discord.ui.TextInput(
        label='İlgi Alanların ve Hobilerin', 
        style=discord.TextStyle.long,
        placeholder='Nelerden hoşlanırsın? Bilgisayarlar, çizim, insanlara yardım etmek, para yönetimi...',
        min_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Akıllı Kategori Seçimi (Hobilerdeki kelimelere göre)
        text = self.interests.value.lower()
        recommended_categories = []
        
        # Basit NLP - Anahtar kelime eşleştirme
        keywords = {
            "teknoloji": ["bilgisayar", "yazılım", "oyun", "kod", "teknoloji", "robot", "internet", "dijital"],
            "tasarim": ["çizim", "resim", "tasarım", "sanat", "estetik", "moda", "boyama", "görsel"],
            "saglik": ["yardım", "insan", "doktor", "hastane", "sağlık", "biyoloji", "ilaç", "spor"],
            "ekonomi": ["para", "borsa", "ticaret", "ekonomi", "satış", "pazarlama", "banka", "iş"],
            "hukuk": ["adalet", "hak", "avukat", "savunma", "kitap", "konuşma", "tartışma", "kanun"]
        }

        for cat, words in keywords.items():
            if any(word in text for word in words):
                recommended_categories.append(cat)
        
        # Eğer eşleşme yoksa rastgele 3 tane öner
        if len(recommended_categories) == 0:
            recommended_categories = random.sample(list(CAREER_DATA.keys()), 3)
        
        view = CareerSelectionView(user_info={
            "name": self.name.value, 
            "age": self.age.value, 
            "interests": self.interests.value
        }, recommended=recommended_categories[:3])

        embed = discord.Embed(
            title=f"Analiz Tamamlandı, {self.name.value}!",
            description=(
                f"Yaşın: **{self.age.value}**\n"
                f"İlgi Alanların: *{self.interests.value}*\n\n"
                "💡 **Hobilerine göre sana en uygun gördüğüm sektörleri aşağıda işaretledim.**\n"
                "Bir sektöre tıkla ve senin için seçtiğim özel mesleği gör!"
            ),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# --- 4. ÖZELLEŞTİRİLMİŞ SEKTÖR SEÇİMİ ---
class CareerSelectionView(discord.ui.View):
    def __init__(self, user_info, recommended):
        super().__init__(timeout=None)
        self.user_info = user_info
        
        # Sadece önerilen ve diğer kategorileri ekle
        for cat_id in CAREER_DATA.keys():
            style = discord.ButtonStyle.primary if cat_id in recommended else discord.ButtonStyle.secondary
            label = f"{cat_id.capitalize()} (Önerilen)" if cat_id in recommended else cat_id.capitalize()
            
            button = discord.ui.Button(label=label, style=style, custom_id=cat_id)
            button.callback = self.create_callback(cat_id)
            self.add_item(button)

    def create_callback(self, cat_id):
        async def callback(interaction):
            await self.suggest(interaction, cat_id)
        return callback

    async def suggest(self, interaction, cat):
        data = random.choice(CAREER_DATA[cat])
        save_user_data(interaction.user.id, self.user_info['name'], self.user_info['age'], self.user_info['interests'], data['meslek'])
        
        embed = discord.Embed(
            title="🎯 Özel Kariyer Analiz Raporu",
            description=f"Merhaba **{self.user_info['name']}**, ilgi alanlarını derinlemesine inceledim ve senin için en ideal eşleşmeyi buldum!",
            color=discord.Color.gold()
        )
        embed.add_field(name="📌 Önerilen Meslek", value=f"**{data['meslek']}**", inline=False)
        embed.add_field(name="📝 Meslek Tanımı", value=data['ozellik'], inline=False)
        embed.add_field(name="⚖️ Neden Sen?", value=data['neden'], inline=False)
        embed.set_footer(text="Bu veri kariyer veri tabanına başarıyla işlendi.")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# --- 5. BOT BAŞLATMA ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

KANAL_ID = 1458528622263664779 # Kendi ID'niz

@bot.event
async def on_ready():
    init_db()
    print(f"Bot {bot.user} aktif!")
    
    channel = bot.get_channel(KANAL_ID)
    if channel:
        view = discord.ui.View()
        button = discord.ui.Button(label="Kariyer Testine Başla", style=discord.ButtonStyle.success, emoji="🚀")
        
        async def callback(interaction):
            await interaction.response.send_modal(IntroModal())
        
        button.callback = callback
        view.add_item(button)
        
        embed = discord.Embed(
            title="🌟 Geleceğini Birlikte İnşa Edelim",
            description=(
                "Hobilerinden yola çıkarak sana en uygun mesleği bulmaya ne dersin?\n\n"
                "✅ **Kişisel Analiz**\n"
                "✅ **Yapay Zeka Destekli Kategori Önerisi**\n"
                "✅ **Veri Tabanı Kaydı**\n\n"
                "Başlamak için aşağıdaki butona tıkla!"
            ),
            color=discord.Color.blue()
        )
        await channel.send(embed=embed, view=view)

if __name__ == "__main__":
    bot.run("TOKENİ BURAYA GİRİN !!!")
