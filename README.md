# mezuniyet-project-
Bu bot, gençlerin ilgi alanlarına göre kariyer yollarını keşfetmesini sağlayan interaktif bir rehberdir. Amacı, kafa karışıklığı yaşayan kullanıcılara hızlı, eğlenceli ve verilere dayalı bir öneri sunarken; bu etkileşimleri arka planda analiz için kaydetmektir.

Kodun Çalışma Mantığı (Adım Adım)
Giriş ve Dinleme: Bot çalıştırıldığında Discord sunucusunu dinlemeye başlar. Kullanıcı !kariyer komutunu yazdığında, kodun içindeki CareerBot sınıfı devreye girer.

Arayüz (Frontend): Bot, kullanıcıya şık bir "Embed" (renkli kutu) ve altında 5 farklı kategori butonu (Teknoloji, Sağlık, vb.) gönderir.

Karar Mekanizması: Kullanıcı bir butona bastığında, kod o kategoriye ait meslek listesine gider ve random.choice fonksiyonunu kullanarak saniyeler içinde rastgele bir meslek seçer. Bu, "dinamik öneri" özelliğini sağlar.

Veritabanı Kaydı (Backend): Meslek önerildiği anda sqlite3 modülü çalışır. Kullanıcının kimliği, seçtiği kategori ve botun verdiği cevap kariyer_danismani.db dosyasına kalıcı olarak işlenir.

Geri Bildirim: Seçilen meslek kullanıcıya "Sadece senin görebileceğin" (ephemeral) şekilde iletilir, böylece kanal kalabalıklaşmaz.
