import json
import math
import os
from datetime import date, datetime, timedelta
from pathlib import Path
try:
    from widget_notification_bridge import sync_prayer_surface, request_pin_widget
except Exception:
    def sync_prayer_surface(app):
        return False

    def request_pin_widget():
        return False
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import (
    Color, Ellipse, Line, Rectangle, RoundedRectangle,
    PushMatrix, PopMatrix, Rotate, Triangle
)
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

API = "https://ezanvakti.emushaf.net"
COUNTRY_ID = "2"
APP_VERSION = "1.0.0"

BG = (0.91, 0.96, 0.96, 1)
GREEN = (0.015, 0.52, 0.55, 1)
DARK = (0.015, 0.30, 0.33, 1)
MINT = (0.74, 0.92, 0.93, 1)
WHITE = (1, 1, 1, 1)
TEXT = (0.66, 0.22, 0.03, 1)
MUTED = (0.76, 0.34, 0.08, 1)
GOLD = (0.95, 0.67, 0.10, 1)
RED = (0.72, 0.25, 0.22, 1)
KAABA_LAT, KAABA_LON = 21.422487, 39.826206
AUDIO_EXTS = (".wav", ".ogg", ".mp3", ".m4a", ".aac")


DAILY_VERSES = [
    (
        "Şüphesiz güçlükle beraber bir kolaylık vardır.",
        "İnşirâh 94/5",
    ),
    (
        "Gerçekten güçlükle beraber bir kolaylık daha vardır.",
        "İnşirâh 94/6",
    ),
    (
        "Boş kaldığında hemen başka bir hayırlı işe yönel.",
        "İnşirâh 94/7",
    ),
    (
        "Yalnız Rabbine yönel.",
        "İnşirâh 94/8",
    ),
    (
        "Yalnız sana ibadet eder, yalnız senden yardım dileriz.",
        "Fâtiha 1/5",
    ),
    (
        "Bizi dosdoğru yola ilet.",
        "Fâtiha 1/6",
    ),
    (
        "Sabır ve namazla Allah'tan yardım isteyin.",
        "Bakara 2/45",
    ),
    (
        "Siz beni anın ki ben de sizi anayım.",
        "Bakara 2/152",
    ),
    (
        "Bana şükredin, nankörlük etmeyin.",
        "Bakara 2/152",
    ),
    (
        "Allah sabredenlerle beraberdir.",
        "Bakara 2/153",
    ),
    (
        "Sabredenleri müjdele.",
        "Bakara 2/155",
    ),
    (
        "Biz Allah'a aidiz ve sonunda O'na döneceğiz.",
        "Bakara 2/156",
    ),
    (
        "Allah sizin için kolaylık ister, güçlük istemez.",
        "Bakara 2/185",
    ),
    (
        "Ben yakınım; bana dua edenin duasına karşılık veririm.",
        "Bakara 2/186",
    ),
    (
        "Rabbimiz, bize dünyada da âhirette de iyilik ver.",
        "Bakara 2/201",
    ),
    (
        "Bazen hoşlanmadığınız bir şey sizin için hayırlı olabilir.",
        "Bakara 2/216",
    ),
    (
        "Allah tövbe edenleri ve temizlenenleri sever.",
        "Bakara 2/222",
    ),
    (
        "Güzel söz ve bağışlama, inciterek yapılan yardımdan daha hayırlıdır.",
        "Bakara 2/263",
    ),
    (
        "Allah hiç kimseye gücünün yettiğinden fazlasını yüklemez.",
        "Bakara 2/286",
    ),
    (
        "Rabbimiz, unutur veya yanılırsak bizi sorumlu tutma.",
        "Bakara 2/286",
    ),
    (
        "Allah'ın ipine hep birlikte sımsıkı sarılın.",
        "Âl-i İmrân 3/103",
    ),
    (
        "Gevşemeyin ve üzülmeyin.",
        "Âl-i İmrân 3/139",
    ),
    (
        "Allah kendisine güvenenleri sever.",
        "Âl-i İmrân 3/159",
    ),
    (
        "Allah bize yeter; O ne güzel vekildir.",
        "Âl-i İmrân 3/173",
    ),
    (
        "Rabbinizin bağışlamasına doğru yarışın.",
        "Âl-i İmrân 3/133",
    ),
    (
        "Öfkelerini yenenler ve insanları bağışlayanlar iyilik sahipleridir.",
        "Âl-i İmrân 3/134",
    ),
    (
        "Rabbimiz, bizi doğru yola ilettikten sonra kalplerimizi eğriltme.",
        "Âl-i İmrân 3/8",
    ),
    (
        "İyilik ve sorumluluk bilinci konusunda yardımlaşın.",
        "Mâide 5/2",
    ),
    (
        "Bir topluluğa olan öfkeniz sizi adaletsizliğe yöneltmesin.",
        "Mâide 5/8",
    ),
    (
        "Adaletli olun; bu, sorumluluk bilincine daha yakındır.",
        "Mâide 5/8",
    ),
    (
        "Kim bir canı kurtarırsa bütün insanları kurtarmış gibi olur.",
        "Mâide 5/32",
    ),
    (
        "Allah'ın rahmeti iyilik yapanlara yakındır.",
        "A'râf 7/56",
    ),
    (
        "Rabbimiz, bize sabır ver ve canımızı Müslüman olarak al.",
        "A'râf 7/126",
    ),
    (
        "Allah'ın rahmetinden ümit kesmeyin.",
        "Yûsuf 12/87",
    ),
    (
        "Kalpler ancak Allah'ı anmakla huzur bulur.",
        "Ra'd 13/28",
    ),
    (
        "Allah bir toplum kendisini değiştirmedikçe onların durumunu değiştirmez.",
        "Ra'd 13/11",
    ),
    (
        "Şükrederseniz size verdiğim nimetleri artırırım.",
        "İbrâhîm 14/7",
    ),
    (
        "Rabbim, beni ve soyumdan gelenleri namaza devam edenlerden eyle.",
        "İbrâhîm 14/40",
    ),
    (
        "Rabbimiz, hesap gününde beni, anne babamı ve inananları bağışla.",
        "İbrâhîm 14/41",
    ),
    (
        "Allah adaleti, iyiliği ve yakınlara yardım etmeyi emreder.",
        "Nahl 16/90",
    ),
    (
        "Anne babana güzel davran.",
        "İsrâ 17/23",
    ),
    (
        "Rabbim, anne babama merhamet et.",
        "İsrâ 17/24",
    ),
    (
        "Verdiğiniz sözü yerine getirin.",
        "İsrâ 17/34",
    ),
    (
        "Bilmediğin şeyin peşine düşme.",
        "İsrâ 17/36",
    ),
    (
        "Yeryüzünde büyüklük taslayarak yürüme.",
        "İsrâ 17/37",
    ),
    (
        "Rabbimiz, bize katından rahmet ver ve işimizi doğruya ulaştır.",
        "Kehf 18/10",
    ),
    (
        "Allah'ın dilediği olur; güç ancak Allah'ın yardımıyladır.",
        "Kehf 18/39",
    ),
    (
        "Rabbim, göğsüme genişlik ver.",
        "Tâhâ 20/25",
    ),
    (
        "Rabbim, işimi kolaylaştır.",
        "Tâhâ 20/26",
    ),
    (
        "Rabbim, ilmimi artır.",
        "Tâhâ 20/114",
    ),
    (
        "Senden başka ilâh yoktur; seni her türlü eksiklikten uzak tutarım.",
        "Enbiyâ 21/87",
    ),
    (
        "Rabbim, beni yalnız bırakma; sen varislerin en hayırlısısın.",
        "Enbiyâ 21/89",
    ),
    (
        "Rabbim, bağışla ve merhamet et.",
        "Mü'minûn 23/118",
    ),
    (
        "Allah göklerin ve yerin nurudur.",
        "Nûr 24/35",
    ),
    (
        "Allah'ın kulları yeryüzünde alçak gönüllülükle yürürler.",
        "Furkân 25/63",
    ),
    (
        "Kendilerine sataşıldığında güzel ve esenlik dolu söz söylerler.",
        "Furkân 25/63",
    ),
    (
        "Rabbimiz, eşlerimizi ve çocuklarımızı göz aydınlığı eyle.",
        "Furkân 25/74",
    ),
    (
        "Rabbim, bana vereceğin her türlü hayra muhtacım.",
        "Kasas 28/24",
    ),
    (
        "Allah'ın sana verdikleriyle âhiret yurdunu kazanmaya çalış.",
        "Kasas 28/77",
    ),
    (
        "Namaz insanı kötülükten ve uygunsuz davranışlardan alıkoyar.",
        "Ankebût 29/45",
    ),
    (
        "Allah yolunda gayret edenleri yollarımıza ulaştırırız.",
        "Ankebût 29/69",
    ),
    (
        "İyiliği emret, kötülükten sakındır ve başına gelene sabret.",
        "Lokmân 31/17",
    ),
    (
        "Allah'a güven; vekil olarak Allah yeter.",
        "Ahzâb 33/3",
    ),
    (
        "Allah'ı çokça anın.",
        "Ahzâb 33/41",
    ),
    (
        "Dosdoğru söz söyleyin.",
        "Ahzâb 33/70",
    ),
    (
        "Allah'ın bağışlamasından ümidinizi kesmeyin.",
        "Zümer 39/53",
    ),
    (
        "Rabbinize yönelin ve O'na teslim olun.",
        "Zümer 39/54",
    ),
    (
        "İyilikle kötülük bir olmaz; kötülüğü en güzel davranışla uzaklaştır.",
        "Fussilet 41/34",
    ),
    (
        "Kim iyilik yaparsa kendi yararına, kim kötülük yaparsa kendi zararına yapar.",
        "Fussilet 41/46",
    ),
    (
        "İşlerinizi aranızda danışarak yürütün.",
        "Şûrâ 42/38",
    ),
    (
        "Kim bağışlar ve barışı sağlarsa onun ödülü Allah'a aittir.",
        "Şûrâ 42/40",
    ),
    (
        "Müminler ancak kardeştir; kardeşlerinizin arasını düzeltin.",
        "Hucurât 49/10",
    ),
    (
        "Bir topluluk diğer bir toplulukla alay etmesin.",
        "Hucurât 49/11",
    ),
    (
        "Birbirinizin kusurlarını araştırmayın.",
        "Hucurât 49/12",
    ),
    (
        "Allah katında en değerliniz, sorumluluk bilinci en güçlü olanınızdır.",
        "Hucurât 49/13",
    ),
    (
        "İnsan için ancak çalışmasının karşılığı vardır.",
        "Necm 53/39",
    ),
    (
        "Rabbinizin hangi nimetlerini inkâr edebilirsiniz?",
        "Rahmân 55/13",
    ),
    (
        "İyiliğin karşılığı ancak iyiliktir.",
        "Rahmân 55/60",
    ),
    (
        "Kim Allah'a karşı sorumluluk bilinci taşırsa Allah ona bir çıkış yolu açar.",
        "Talâk 65/2",
    ),
    (
        "Kim Allah'a güvenirse Allah ona yeter.",
        "Talâk 65/3",
    ),
    (
        "Allah zorluktan sonra bir kolaylık yaratacaktır.",
        "Talâk 65/7",
    ),
    (
        "Rabbin seni terk etmedi ve sana darılmadı.",
        "Duhâ 93/3",
    ),
    (
        "Senin için âhiret dünyadan daha hayırlıdır.",
        "Duhâ 93/4",
    ),
    (
        "Rabbin sana verecek ve sen hoşnut olacaksın.",
        "Duhâ 93/5",
    ),
    (
        "Yetimi sakın ezme.",
        "Duhâ 93/9",
    ),
    (
        "İsteyeni azarlama.",
        "Duhâ 93/10",
    ),
    (
        "Rabbinin nimetini minnet ve şükranla an.",
        "Duhâ 93/11",
    ),
    (
        "Kim zerre kadar iyilik yaparsa karşılığını görür.",
        "Zilzâl 99/7",
    ),
    (
        "Kim zerre kadar kötülük yaparsa karşılığını görür.",
        "Zilzâl 99/8",
    ),
    (
        "İnsan gerçekten ziyandadır; iman edip iyi işler yapanlar hariç.",
        "Asr 103/2-3",
    ),
    (
        "Birbirinize hakkı ve sabrı tavsiye edin.",
        "Asr 103/3",
    ),
]


DAILY_HADITHS = [
    (
        "Ben, güzel ahlâkı tamamlamak için gönderildim.",
        "İbn Hanbel, II, 381",
    ),
    (
        "Ameller niyetlere göre değer kazanır.",
        "Buhârî, Bed'ü'l-vahy, 1",
    ),
    (
        "Müminlerin iman bakımından en mükemmeli, ahlâk bakımından en güzel olanıdır.",
        "Ebû Dâvûd, Sünnet, 15",
    ),
    (
        "Nerede olursan ol, Allah'a karşı sorumluluğunun bilincinde ol.",
        "Tirmizî, Birr, 55",
    ),
    (
        "Hiçbir baba, evlâdına güzel terbiyeden daha üstün bir hediye vermemiştir.",
        "Tirmizî, Birr, 33",
    ),
    (
        "Sizin en hayırlınız, ahlâkı en güzel olanınızdır.",
        "Buhârî, Menâkıb, 23",
    ),
    (
        "Kolaylaştırın, güçleştirmeyin; müjdeleyin, nefret ettirmeyin.",
        "Buhârî, İlim, 11",
    ),
    (
        "Allah güzeldir, güzelliği sever.",
        "Müslim, Îmân, 147",
    ),
    (
        "Allah sizin dış görünüşünüze değil, kalplerinize ve amellerinize bakar.",
        "Müslim, Birr, 34",
    ),
    (
        "Müslüman, insanların elinden ve dilinden güvende olduğu kişidir.",
        "Buhârî, Îmân, 4",
    ),
    (
        "Kendisi için istediğini kardeşi için de isteyen kişi olgun mümindir.",
        "Buhârî, Îmân, 7",
    ),
    (
        "Güzel söz sadakadır.",
        "Buhârî, Edeb, 34",
    ),
    (
        "Güler yüzle karşılaşmak da bir iyiliktir.",
        "Müslim, Birr, 144",
    ),
    (
        "İnsanlara teşekkür etmeyen, Allah'a da gereğince şükretmiş olmaz.",
        "Tirmizî, Birr, 35",
    ),
    (
        "Merhamet etmeyene merhamet edilmez.",
        "Buhârî, Edeb, 18",
    ),
    (
        "Merhamet edenlere Rahmân merhamet eder.",
        "Tirmizî, Birr, 16",
    ),
    (
        "Yeryüzündekilere merhamet edin ki size de merhamet edilsin.",
        "Tirmizî, Birr, 16",
    ),
    (
        "İyilik güzel ahlâktır.",
        "Müslim, Birr, 14",
    ),
    (
        "Hayâ yalnızca güzellik getirir.",
        "Buhârî, Edeb, 77",
    ),
    (
        "Hayâ imandandır.",
        "Buhârî, Îmân, 16",
    ),
    (
        "Doğruluk iyiliğe, iyilik de cennete götürür.",
        "Buhârî, Edeb, 69",
    ),
    (
        "Yalandan sakının; çünkü yalan insanı kötülüğe götürür.",
        "Buhârî, Edeb, 69",
    ),
    (
        "Güçlü kişi, öfkelendiğinde kendisine hâkim olabilen kişidir.",
        "Buhârî, Edeb, 76",
    ),
    (
        "Öfkelenme.",
        "Buhârî, Edeb, 76",
    ),
    (
        "Allah yumuşak davranmayı sever.",
        "Müslim, Selâm, 10",
    ),
    (
        "Yumuşak davranış bulunduğu şeyi güzelleştirir.",
        "Müslim, Birr, 78",
    ),
    (
        "Sabır, musibetin ilk anında gösterilendir.",
        "Buhârî, Cenâiz, 32",
    ),
    (
        "Müminin her hâli kendisi için hayırlıdır.",
        "Müslim, Zühd, 64",
    ),
    (
        "Mümin nimete şükreder, sıkıntıya sabreder.",
        "Müslim, Zühd, 64",
    ),
    (
        "Allah'a ve âhiret gününe inanan ya hayır söylesin ya da sussun.",
        "Buhârî, Edeb, 31",
    ),
    (
        "Allah'a ve âhiret gününe inanan komşusuna iyilik etsin.",
        "Buhârî, Edeb, 31",
    ),
    (
        "Allah'a ve âhiret gününe inanan misafirine ikram etsin.",
        "Buhârî, Edeb, 31",
    ),
    (
        "Komşusu kötülüklerinden güvende olmayan kişi olgun mümin değildir.",
        "Buhârî, Edeb, 29",
    ),
    (
        "Akrabalık bağını gözeten kimsenin rızkı genişler.",
        "Buhârî, Edeb, 12",
    ),
    (
        "Allah'ın hoşnutluğu anne ve babanın hoşnutluğundadır.",
        "Tirmizî, Birr, 3",
    ),
    (
        "Sizin en hayırlınız, ailesine karşı en hayırlı olanınızdır.",
        "Tirmizî, Menâkıb, 63",
    ),
    (
        "Küçüklere merhamet etmeyen ve büyüklere saygı göstermeyen bizden değildir.",
        "Tirmizî, Birr, 15",
    ),
    (
        "İki kişinin arasını düzeltmek sadakadır.",
        "Buhârî, Sulh, 11",
    ),
    (
        "Yoldan insanlara zarar veren bir şeyi kaldırmak sadakadır.",
        "Buhârî, Cihâd, 128",
    ),
    (
        "Temizlik imanın yarısıdır.",
        "Müslim, Tahâret, 1",
    ),
    (
        "Veren el, alan elden daha hayırlıdır.",
        "Buhârî, Zekât, 18",
    ),
    (
        "Sadaka malı eksiltmez.",
        "Müslim, Birr, 69",
    ),
    (
        "Kim bir müminin sıkıntısını giderirse Allah da onun sıkıntısını giderir.",
        "Müslim, Zikir, 38",
    ),
    (
        "Kul, kardeşine yardım ettiği sürece Allah da kula yardım eder.",
        "Müslim, Zikir, 38",
    ),
    (
        "İlim öğrenmek için yola çıkan kimseye Allah kolaylık gösterir.",
        "Müslim, Zikir, 38",
    ),
    (
        "Kur'an'ı öğrenen ve öğretenler insanların hayırlılarındandır.",
        "Buhârî, Fezâilü'l-Kur'ân, 21",
    ),
    (
        "Sizin en hayırlınız, Kur'an'ı öğrenen ve öğreteninizdir.",
        "Buhârî, Fezâilü'l-Kur'ân, 21",
    ),
    (
        "Namaz dinde önemli bir yere sahiptir.",
        "Tirmizî, Îmân, 8",
    ),
    (
        "Dua ibadetin özüdür.",
        "Tirmizî, Deavât, 1",
    ),
    (
        "Allah'a en sevimli amel, az da olsa devamlı yapılan ameldir.",
        "Buhârî, Rikâk, 18",
    ),
    (
        "Allah sizin için kolaylık ister.",
        "Buhârî, Îmân, 29",
    ),
    (
        "Din kolaylıktır.",
        "Buhârî, Îmân, 29",
    ),
    (
        "Bir iyiliğe öncülük eden, o iyiliği yapan gibi sevap kazanır.",
        "Müslim, İmâre, 133",
    ),
    (
        "Kardeşinin yüzüne gülümsemen senin için sadakadır.",
        "Tirmizî, Birr, 36",
    ),
    (
        "İnsanların kusurlarını örten kimsenin kusurlarını Allah örter.",
        "Müslim, Birr, 72",
    ),
    (
        "Mümin, müminin kardeşidir; ona haksızlık etmez.",
        "Buhârî, Mezâlim, 3",
    ),
    (
        "Müminler birbirlerini sevmede ve korumada bir beden gibidir.",
        "Müslim, Birr, 66",
    ),
    (
        "Mümin, diğer mümin için birbirini destekleyen bina gibidir.",
        "Buhârî, Salât, 88",
    ),
    (
        "Kanaat, tükenmeyen bir zenginliktir.",
        "Beyhakî, Zühd",
    ),
    (
        "Asıl zenginlik mal çokluğu değil, gönül zenginliğidir.",
        "Buhârî, Rikâk, 15",
    ),
    (
        "İnsanların en hayırlısı, insanlara faydalı olandır.",
        "Beyhakî, Şuabü'l-îmân",
    ),
    (
        "Allah temizdir ve temizliği sever.",
        "Tirmizî, Edeb, 41",
    ),
    (
        "Allah yapılan işin güzel ve sağlam yapılmasını sever.",
        "Beyhakî, Şuabü'l-îmân",
    ),
    (
        "Mümin aynı hataya iki defa düşmemeye dikkat eder.",
        "Buhârî, Edeb, 83",
    ),
    (
        "Şüpheli olanı bırak, şüphe vermeyene yönel.",
        "Tirmizî, Sıfatü'l-kıyâme, 60",
    ),
    (
        "Sana fayda veren şeye yönel ve Allah'tan yardım iste.",
        "Müslim, Kader, 34",
    ),
    (
        "Ümitsizliğe düşme ve güçsüzlük gösterme.",
        "Müslim, Kader, 34",
    ),
    (
        "Allah bir kuluna hayır dilerse ona anlayış kazandırır.",
        "Buhârî, İlim, 10",
    ),
    (
        "Kişi sevdiğiyle beraberdir.",
        "Buhârî, Edeb, 96",
    ),
    (
        "Dünyada bir yolcu gibi ol.",
        "Buhârî, Rikâk, 3",
    ),
    (
        "İki nimet vardır ki insanların çoğu onların değerini bilmez: sağlık ve boş zaman.",
        "Buhârî, Rikâk, 1",
    ),
    (
        "Her canlıya yapılan iyilikte sevap vardır.",
        "Buhârî, Müsâkât, 9",
    ),
    (
        "Bir ağaç diken veya ürün eken kişi, ondan yararlanıldığı sürece sevap kazanır.",
        "Buhârî, Müzâraa, 1",
    ),
    (
        "Allah israfı ve malı boş yere harcamayı hoş görmez.",
        "Buhârî, Zekât, 53",
    ),
    (
        "Helal bellidir, haram da bellidir.",
        "Buhârî, Îmân, 39",
    ),
    (
        "Kişinin kendisini ilgilendirmeyen şeyleri terk etmesi güzel Müslümanlıktandır.",
        "Tirmizî, Zühd, 11",
    ),
    (
        "Mümin güzel ahlâkıyla yüksek derecelere ulaşır.",
        "Ebû Dâvûd, Edeb, 7",
    ),
    (
        "Kıyamet gününde mizanda güzel ahlâktan daha ağır bir şey yoktur.",
        "Tirmizî, Birr, 62",
    ),
]

QURAN_SURAH_NAMES = ['Fâtiha', 'Bakara', 'Âl-i İmrân', 'Nisâ', 'Mâide', "En'âm", "A'râf", 'Enfâl', 'Tevbe', 'Yûnus', 'Hûd', 'Yûsuf', "Ra'd", 'İbrâhîm', 'Hicr', 'Nahl', 'İsrâ', 'Kehf', 'Meryem', 'Tâhâ', 'Enbiyâ', 'Hac', "Mü'minûn", 'Nûr', 'Furkân', 'Şuarâ', 'Neml', 'Kasas', 'Ankebût', 'Rûm', 'Lokmân', 'Secde', 'Ahzâb', "Sebe'", 'Fâtır', 'Yâsîn', 'Sâffât', 'Sâd', 'Zümer', "Mü'min", 'Fussilet', 'Şûrâ', 'Zuhruf', 'Duhân', 'Câsiye', 'Ahkâf', 'Muhammed', 'Fetih', 'Hucurât', 'Kâf', 'Zâriyât', 'Tûr', 'Necm', 'Kamer', 'Rahmân', 'Vâkıa', 'Hadîd', 'Mücâdele', 'Haşr', 'Mümtehine', 'Saf', 'Cuma', 'Münâfikûn', 'Tegâbün', 'Talâk', 'Tahrîm', 'Mülk', 'Kalem', 'Hâkka', 'Meâric', 'Nûh', 'Cin', 'Müzzemmil', 'Müddessir', 'Kıyâmet', 'İnsan', 'Mürselât', "Nebe'", 'Nâziât', 'Abese', 'Tekvîr', 'İnfitâr', 'Mutaffifîn', 'İnşikâk', 'Bürûc', 'Târık', "A'lâ", 'Gâşiye', 'Fecr', 'Beled', 'Şems', 'Leyl', 'Duhâ', 'İnşirâh', 'Tîn', 'Alak', 'Kadr', 'Beyyine', 'Zilzâl', 'Âdiyât', 'Kâria', 'Tekâsür', 'Asr', 'Hümeze', 'Fîl', 'Kureyş', 'Mâûn', 'Kevser', 'Kâfirûn', 'Nasr', 'Tebbet', 'İhlâs', 'Felak', 'Nâs']

ESMAUL_HUSNA = [('Allah', 'Bütün güzel isim ve sıfatları kendinde toplayan'), ('Er-Rahmân', 'Bütün varlıklara merhamet eden'), ('Er-Rahîm', 'Çok merhamet eden, bağışlayan'), ('El-Melik', 'Mülkün gerçek sahibi'), ('El-Kuddûs', 'Her türlü eksiklikten uzak olan'), ('Es-Selâm', 'Esenlik veren'), ("El-Mü'min", 'Güven veren'), ('El-Müheymin', 'Gözetip koruyan'), ('El-Azîz', 'Mutlak üstün ve güçlü olan'), ('El-Cebbâr', 'Kudretiyle dilediğini yapan'), ('El-Mütekebbir', 'Büyüklükte eşsiz olan'), ('El-Hâlık', 'Her şeyi yaratan'), ("El-Bâri'", 'Kusursuzca var eden'), ('El-Musavvir', 'Varlıklara şekil veren'), ('El-Gaffâr', 'Günahları çokça örten'), ('El-Kahhâr', 'Her şeye galip olan'), ('El-Vehhâb', 'Karşılıksız nimet veren'), ('Er-Rezzâk', 'Rızık veren'), ('El-Fettâh', 'Hayır kapılarını açan'), ('El-Alîm', 'Her şeyi bilen'), ('El-Kâbıd', 'Dilediğine darlık veren'), ('El-Bâsıt', 'Dilediğine bolluk veren'), ('El-Hâfıd', 'Dilediğini alçaltan'), ("Er-Râfi'", 'Dilediğini yükselten'), ('El-Muizz', 'İzzet ve şeref veren'), ('El-Müzill', 'Dilediğini zelil eden'), ("Es-Semî'", 'Her şeyi işiten'), ('El-Basîr', 'Her şeyi gören'), ('El-Hakem', 'Mutlak hükmeden'), ('El-Adl', 'Mutlak adalet sahibi'), ('El-Latîf', 'Lütuf ve incelik sahibi'), ('El-Habîr', 'Her şeyden haberdar olan'), ('El-Halîm', 'Cezada acele etmeyen'), ('El-Azîm', 'Azameti sonsuz olan'), ('El-Gafûr', 'Çok bağışlayan'), ('Eş-Şekûr', 'Az amele çok karşılık veren'), ('El-Aliyy', 'Çok yüce olan'), ('El-Kebîr', 'Büyüklüğü sonsuz olan'), ('El-Hafîz', 'Koruyup gözeten'), ('El-Mukît', 'Rızık ve güç veren'), ('El-Hasîb', 'Hesap gören, yeten'), ('El-Celîl', 'Celâl ve azamet sahibi'), ('El-Kerîm', 'Çok cömert olan'), ('Er-Rakîb', 'Her şeyi gözeten'), ('El-Mücîb', 'Dualara cevap veren'), ("El-Vâsi'", 'Rahmeti ve ilmi geniş olan'), ('El-Hakîm', 'Her işi hikmetli olan'), ('El-Vedûd', 'Çok seven ve sevilen'), ('El-Mecîd', 'Şanı ve şerefi yüce olan'), ('El-Bâis', 'Ölüleri dirilten'), ('Eş-Şehîd', 'Her şeye şahit olan'), ('El-Hakk', 'Varlığı ve sözü gerçek olan'), ('El-Vekîl', 'Kendisine güvenilip dayanılan'), ('El-Kaviyy', 'Çok güçlü olan'), ('El-Metîn', 'Kudreti sarsılmaz olan'), ('El-Veliyy', 'Dost ve yardımcı olan'), ('El-Hamîd', 'Övgüye layık olan'), ('El-Muhsî', 'Her şeyi tek tek bilen'), ("El-Mübdi'", 'İlk defa yaratan'), ('El-Muîd', 'Yeniden yaratan'), ('El-Muhyî', 'Hayat veren'), ('El-Mümît', 'Ölümü yaratan'), ('El-Hayy', 'Diri ve hayat sahibi'), ('El-Kayyûm', 'Her şeyi ayakta tutan'), ('El-Vâcid', 'Dilediğini bulan, hiçbir şeye muhtaç olmayan'), ('El-Vâhid', 'Tek olan'), ('El-Ehad', 'Bir ve eşsiz olan'), ('Es-Samed', 'Her şeyin kendisine muhtaç olduğu'), ('El-Kâdir', 'Her şeye gücü yeten'), ('El-Muktedir', 'Kudreti her şeyi kuşatan'), ('El-Mukaddim', 'Dilediğini öne alan'), ('El-Muahhir', 'Dilediğini geri bırakan'), ('El-Evvel', 'Başlangıcı olmayan'), ('El-Âhir', 'Sonu olmayan'), ('Ez-Zâhir', 'Varlığı açık olan'), ('El-Bâtın', 'Mahiyeti idrak edilemeyen'), ('El-Vâlî', 'Kâinatı yöneten'), ('El-Müteâlî', 'Çok yüce olan'), ('El-Berr', 'İyiliği ve ihsanı bol olan'), ('Et-Tevvâb', 'Tövbeleri kabul eden'), ('El-Müntekim', 'Adaletiyle karşılık veren'), ('El-Afüvv', 'Günahları affeden'), ('Er-Raûf', 'Çok şefkatli olan'), ("Mâlikü'l-Mülk", 'Mülkün tek sahibi'), ("Zü'l-Celâli ve'l-İkrâm", 'Celâl ve ikram sahibi'), ('El-Muksit', 'Adaletle hükmeden'), ("El-Câmi'", 'Dilediklerini bir araya getiren'), ('El-Ganiyy', 'Hiçbir şeye muhtaç olmayan'), ('El-Mugnî', 'Zenginlik veren'), ("El-Mâni'", 'Dilediğine engel olan'), ('Ed-Dârr', 'Hikmetiyle zarar yaratan'), ("En-Nâfi'", 'Fayda veren'), ('En-Nûr', 'Âlemleri aydınlatan'), ('El-Hâdî', 'Doğru yola ileten'), ("El-Bedî'", 'Eşi olmadan yaratan'), ('El-Bâkî', 'Varlığının sonu olmayan'), ('El-Vâris', 'Her şeyin gerçek varisi'), ('Er-Reşîd', 'Doğru yolu gösteren'), ('Es-Sabûr', 'Cezada acele etmeyen')]

PRAYERS = [
    ("İmsak", "Imsak", "moon"),
    ("Güneş", "Gunes", "sun"),
    ("Öğle", "Ogle", "sun_high"),
    ("İkindi", "Ikindi", "cloud"),
    ("Akşam", "Aksam", "sunset"),
    ("Yatsı", "Yatsi", "moon_star"),
]

PROVINCES = {
    "Adana": (37.0000, 35.3213), "Adıyaman": (37.7648, 38.2786),
    "Afyonkarahisar": (38.7507, 30.5567), "Ağrı": (39.7191, 43.0503),
    "Amasya": (40.6499, 35.8353), "Ankara": (39.9334, 32.8597),
    "Antalya": (36.8969, 30.7133), "Artvin": (41.1828, 41.8183),
    "Aydın": (37.8560, 27.8416), "Balıkesir": (39.6484, 27.8826),
    "Bilecik": (40.0567, 30.0665), "Bingöl": (38.8853, 40.4983),
    "Bitlis": (38.3938, 42.1232), "Bolu": (40.5760, 31.5788),
    "Burdur": (37.7203, 30.2908), "Bursa": (40.1950, 29.0600),
    "Çanakkale": (40.1553, 26.4142), "Çankırı": (40.6013, 33.6134),
    "Çorum": (40.5506, 34.9556), "Denizli": (37.7765, 29.0864),
    "Diyarbakır": (37.9144, 40.2306), "Edirne": (41.6818, 26.5623),
    "Elazığ": (38.6810, 39.2264), "Erzincan": (39.7500, 39.5000),
    "Erzurum": (39.9000, 41.2700), "Eskişehir": (39.7767, 30.5206),
    "Gaziantep": (37.0662, 37.3833), "Giresun": (40.9128, 38.3895),
    "Gümüşhane": (40.4603, 39.4814), "Hakkari": (37.5833, 43.7333),
    "Hatay": (36.4018, 36.3498), "Isparta": (37.7648, 30.5566),
    "Mersin": (36.8121, 34.6415), "İstanbul": (41.0082, 28.9784),
    "İzmir": (38.4192, 27.1287), "Kars": (40.6013, 43.0975),
    "Kastamonu": (41.3887, 33.7827), "Kayseri": (38.7312, 35.4787),
    "Kırklareli": (41.7351, 27.2252), "Kırşehir": (39.1425, 34.1709),
    "Kocaeli": (40.8533, 29.8815), "Konya": (37.8746, 32.4932),
    "Kütahya": (39.4167, 29.9833), "Malatya": (38.3552, 38.3095),
    "Manisa": (38.6191, 27.4289), "Kahramanmaraş": (37.5858, 36.9371),
    "Mardin": (37.3212, 40.7245), "Muğla": (37.2153, 28.3636),
    "Muş": (38.9462, 41.7539), "Nevşehir": (38.6939, 34.6857),
    "Niğde": (37.9667, 34.6833), "Ordu": (40.9839, 37.8764),
    "Rize": (41.0201, 40.5234), "Sakarya": (40.7731, 30.3948),
    "Samsun": (41.2867, 36.3300), "Siirt": (37.9333, 41.9500),
    "Sinop": (42.0231, 35.1531), "Sivas": (39.7477, 37.0179),
    "Tekirdağ": (40.9833, 27.5167), "Tokat": (40.3167, 36.5500),
    "Trabzon": (41.0015, 39.7178), "Tunceli": (39.1079, 39.5401),
    "Şanlıurfa": (37.1674, 38.7955), "Uşak": (38.6823, 29.4082),
    "Van": (38.4891, 43.4089), "Yozgat": (39.8181, 34.8147),
    "Zonguldak": (41.4564, 31.7987), "Aksaray": (38.3687, 34.0370),
    "Bayburt": (40.2552, 40.2249), "Karaman": (37.1759, 33.2287),
    "Kırıkkale": (39.8468, 33.5153), "Batman": (37.8812, 41.1351),
    "Şırnak": (37.4187, 42.4918), "Bartın": (41.6344, 32.3375),
    "Ardahan": (41.1105, 42.7022), "Iğdır": (39.9167, 44.0333),
    "Yalova": (40.6500, 29.2667), "Karabük": (41.2061, 32.6204),
    "Kilis": (36.7184, 37.1212), "Osmaniye": (37.0742, 36.2478),
    "Düzce": (40.8438, 31.1565),
}

KAYSERI_DISTRICTS = (
    "Akkışla", "Bünyan", "Develi", "Felahiye", "Hacılar", "İncesu",
    "Kocasinan", "Melikgazi", "Özvatan", "Pınarbaşı", "Sarıoğlan",
    "Sarız", "Talas", "Tomarza", "Yahyalı", "Yeşilhisar",
)

DISTRICTS = {
    ("Kayseri", "Hacılar"): (38.6463, 35.4494),
    ("Kayseri", "Kocasinan"): (38.7330, 35.4850),
    ("Kayseri", "Melikgazi"): (38.7219, 35.4933),
    ("Kayseri", "Talas"): (38.6908, 35.5538),
    ("Kayseri", "Develi"): (38.3906, 35.4922),
    ("Kayseri", "Yahyalı"): (38.1023, 35.3573),
    ("Kayseri", "Bünyan"): (38.8463, 35.8603),
    ("Kayseri", "Pınarbaşı"): (38.7222, 36.3931),
    ("Kayseri", "İncesu"): (38.6224, 35.1826),
}


def rounded(widget, color=WHITE, radius=22, border=None):
    with widget.canvas.before:
        Color(*color)
        widget._bg = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(radius)])
        if border:
            Color(*border)
            widget._border = Line(rounded_rectangle=(*widget.pos, *widget.size, dp(radius)), width=1)
    def update(*_):
        widget._bg.pos, widget._bg.size = widget.pos, widget.size
        if hasattr(widget, "_border"):
            widget._border.rounded_rectangle = (*widget.pos, *widget.size, dp(radius))
    widget.bind(pos=update, size=update)
    return widget


def lbl(text, color=TEXT, size="15sp", markup=False, **kwargs):
    obj = Label(text=text, color=color, font_size=size, markup=markup, **kwargs)
    obj.bind(size=lambda w, v: setattr(w, "text_size", (v[0], None)))
    return obj


class FlatButton(Button):
    def __init__(self, bg=GREEN, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", bg)
        kwargs.setdefault("color", WHITE)
        super().__init__(**kwargs)


class CanvasIcon(Widget):
    """Her platformda gorunen, font gerektirmeyen cizim ikonlari."""
    def __init__(self, icon="home", color=GREEN, **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.icon_color = color
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(self.redraw, 0)

    def redraw(self, *_):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        size = max(dp(1), min(w, h))
        cx, cy = x + w / 2, y + h / 2
        c = self.icon_color
        thin = max(dp(1.4), size * .035)
        normal = max(dp(2.0), size * .050)
        thick = max(dp(2.7), size * .070)

        with self.canvas:
            Color(*c)

            if self.icon == "home":
                Line(points=[
                    cx-size*.31, cy-size*.02,
                    cx, cy+size*.28,
                    cx+size*.31, cy-size*.02,
                ], width=normal, joint="round", cap="round")
                Line(rectangle=(cx-size*.23, cy-size*.27,
                                size*.46, size*.28),
                     width=normal, joint="round")
                Line(rectangle=(cx-size*.055, cy-size*.27,
                                size*.11, size*.18), width=thin)

            elif self.icon == "clock":
                Line(circle=(cx, cy, size*.30), width=normal)
                Line(points=[cx, cy, cx, cy+size*.17],
                     width=normal, cap="round")
                Line(points=[cx, cy, cx+size*.15, cy-size*.09],
                     width=normal, cap="round")
                Ellipse(pos=(cx-size*.032, cy-size*.032),
                        size=(size*.064, size*.064))

            elif self.icon == "compass":
                Line(circle=(cx, cy, size*.31), width=normal)
                Line(circle=(cx, cy, size*.23), width=thin)
                Triangle(points=[
                    cx, cy+size*.27,
                    cx-size*.105, cy-size*.10,
                    cx, cy-size*.025,
                ])
                Color(*GOLD)
                Triangle(points=[
                    cx, cy-size*.27,
                    cx+size*.105, cy+size*.10,
                    cx, cy+size*.025,
                ])
                Color(*c)
                Ellipse(pos=(cx-size*.037, cy-size*.037),
                        size=(size*.074, size*.074))

            elif self.icon == "tasbih":
                bead = size*.072
                for i in range(12):
                    angle = math.radians(i * 30)
                    bx = cx + math.cos(angle) * size*.235
                    by = cy + math.sin(angle) * size*.235
                    Ellipse(pos=(bx-bead/2, by-bead/2), size=(bead, bead))
                Line(points=[cx, cy-size*.24, cx, cy-size*.35],
                     width=normal, cap="round")
                Ellipse(pos=(cx-size*.045, cy-size*.42),
                        size=(size*.09, size*.13))

            elif self.icon == "settings":
                Line(circle=(cx, cy, size*.13), width=thick)
                Line(circle=(cx, cy, size*.25), width=normal)
                for i in range(8):
                    angle = math.radians(i * 45)
                    x1 = cx + math.cos(angle) * size*.25
                    y1 = cy + math.sin(angle) * size*.25
                    x2 = cx + math.cos(angle) * size*.34
                    y2 = cy + math.sin(angle) * size*.34
                    Line(points=[x1, y1, x2, y2],
                         width=thick, cap="round")

            elif self.icon in ("moon", "moon_star"):
                Ellipse(pos=(cx-size*.26, cy-size*.26),
                        size=(size*.52, size*.52))
                Color(*WHITE)
                Ellipse(pos=(cx-size*.07, cy-size*.12),
                        size=(size*.40, size*.40))
                if self.icon == "moon_star":
                    Color(*GOLD)
                    star = size*.075
                    Ellipse(pos=(cx+size*.12, cy+size*.12),
                            size=(star, star))

            elif self.icon in ("sun", "sun_high", "sunset"):
                Ellipse(pos=(cx-size*.135, cy-size*.135),
                        size=(size*.27, size*.27))
                for i in range(8):
                    angle = math.radians(i * 45)
                    Line(points=[
                        cx+math.cos(angle)*size*.20,
                        cy+math.sin(angle)*size*.20,
                        cx+math.cos(angle)*size*.30,
                        cy+math.sin(angle)*size*.30,
                    ], width=normal, cap="round")
                if self.icon == "sunset":
                    Line(points=[cx-size*.34, cy-size*.25,
                                 cx+size*.34, cy-size*.25],
                         width=normal, cap="round")

            elif self.icon == "cloud":
                Line(points=[cx-size*.28, cy-size*.12,
                             cx+size*.27, cy-size*.12],
                     width=thick, cap="round")
                Line(circle=(cx-size*.16, cy-size*.04, size*.15,
                             15, 175), width=normal)
                Line(circle=(cx+size*.01, cy+size*.02, size*.20,
                             20, 165), width=normal)
                Line(circle=(cx+size*.20, cy-size*.04, size*.13,
                             10, 160), width=normal)

            elif self.icon == "pin":
                Line(circle=(cx, cy+size*.09, size*.17), width=normal)
                Line(points=[cx-size*.145, cy+size*.01,
                             cx, cy-size*.30,
                             cx+size*.145, cy+size*.01],
                     width=normal, joint="round")
                Ellipse(pos=(cx-size*.052, cy+size*.038),
                        size=(size*.104, size*.104))




class MosqueSilhouette(Widget):
    """Modern, ince çizgili ve metin okunabilirliğini koruyan cami arka planı."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(self.redraw, 0)

    def redraw(self, *_):
        self.canvas.clear()
        x, y = self.pos
        w, h = self.size
        if w < dp(20) or h < dp(20):
            return

        # Silüet kartın sağ-alt kısmında kalır. Sol sayaç bölümü temiz tutulur.
        base_y = y + h * .055
        cx = x + w * .735
        unit = min(w * .48, h * 1.22)
        line = max(dp(1.0), unit * .006)

        dome_left = cx - unit * .205
        dome_right = cx + unit * .205
        dome_base = base_y + unit * .245
        dome_top = base_y + unit * .555

        with self.canvas:
            # Çok hafif ana hacim. Metni kapatmadan derinlik verir.
            Color(1, 1, 1, .026)
            RoundedRectangle(
                pos=(cx-unit*.31, base_y),
                size=(unit*.62, unit*.265),
                radius=[(dp(10), dp(10), 0, 0)],
            )

            # İkinci katman yumuşak dolgu.
            Color(.55, .92, .94, .050)
            Ellipse(
                pos=(cx-unit*.235, dome_base-unit*.03),
                size=(unit*.47, unit*.35),
                angle_start=0,
                angle_end=180,
            )

            # Mimari kontur. İnce ve premium görünüm.
            Color(1, 1, 1, .105)
            Line(
                points=[
                    dome_left, dome_base,
                    cx-unit*.178, dome_base+unit*.105,
                    cx-unit*.112, dome_base+unit*.205,
                    cx, dome_top,
                    cx+unit*.112, dome_base+unit*.205,
                    cx+unit*.178, dome_base+unit*.105,
                    dome_right, dome_base,
                ],
                width=line,
                joint="round",
                cap="round",
            )

            # Kubbe alemi ve küçük hilal.
            Line(
                points=[cx, dome_top, cx, dome_top+unit*.105],
                width=line,
                cap="round",
            )
            Line(
                circle=(cx+unit*.014, dome_top+unit*.125, unit*.036, 55, 305),
                width=line,
                cap="round",
            )

            # Ana bina ve kemerli girişler.
            Line(
                rounded_rectangle=(
                    cx-unit*.31, base_y, unit*.62, unit*.285, dp(9)
                ),
                width=line,
            )
            for offset in (-.17, 0, .17):
                door_cx = cx + unit * offset
                door_w = unit * .09
                door_h = unit * .145
                Line(
                    points=[
                        door_cx-door_w/2, base_y,
                        door_cx-door_w/2, base_y+door_h*.60,
                    ],
                    width=line,
                    cap="round",
                )
                Line(
                    circle=(door_cx, base_y+door_h*.60,
                            door_w/2, 0, 180),
                    width=line,
                )
                Line(
                    points=[
                        door_cx+door_w/2, base_y+door_h*.60,
                        door_cx+door_w/2, base_y,
                    ],
                    width=line,
                    cap="round",
                )

            # Sol minare. Dışa yakın ve ince.
            left_m = cx - unit * .405
            Line(
                points=[left_m-unit*.021, base_y,
                        left_m-unit*.013, base_y+unit*.515],
                width=line,
                cap="round",
            )
            Line(
                points=[left_m+unit*.021, base_y,
                        left_m+unit*.013, base_y+unit*.515],
                width=line,
                cap="round",
            )
            Line(
                points=[left_m-unit*.055, base_y+unit*.395,
                        left_m+unit*.055, base_y+unit*.395],
                width=line,
                cap="round",
            )
            Line(
                points=[left_m-unit*.04, base_y+unit*.42,
                        left_m+unit*.04, base_y+unit*.42],
                width=line,
                cap="round",
            )
            Line(
                points=[left_m-unit*.014, base_y+unit*.515,
                        left_m, base_y+unit*.675,
                        left_m+unit*.014, base_y+unit*.515],
                width=line,
                joint="round",
            )

            # Sağ minare.
            right_m = cx + unit * .405
            Line(
                points=[right_m-unit*.021, base_y,
                        right_m-unit*.013, base_y+unit*.515],
                width=line,
                cap="round",
            )
            Line(
                points=[right_m+unit*.021, base_y,
                        right_m+unit*.013, base_y+unit*.515],
                width=line,
                cap="round",
            )
            Line(
                points=[right_m-unit*.055, base_y+unit*.395,
                        right_m+unit*.055, base_y+unit*.395],
                width=line,
                cap="round",
            )
            Line(
                points=[right_m-unit*.04, base_y+unit*.42,
                        right_m+unit*.04, base_y+unit*.42],
                width=line,
                cap="round",
            )
            Line(
                points=[right_m-unit*.014, base_y+unit*.515,
                        right_m, base_y+unit*.675,
                        right_m+unit*.014, base_y+unit*.515],
                width=line,
                joint="round",
            )

            # Altta zarif şehir çizgisi. Kartın zemine oturmasını sağlar.
            Color(1, 1, 1, .075)
            Line(
                points=[
                    x+w*.43, base_y,
                    cx-unit*.50, base_y,
                    cx-unit*.46, base_y+unit*.035,
                    cx-unit*.43, base_y,
                    cx+unit*.43, base_y,
                    cx+unit*.47, base_y+unit*.025,
                    cx+unit*.51, base_y,
                    x+w*.965, base_y,
                ],
                width=max(dp(.8), line*.8),
                joint="round",
                cap="round",
            )


class IconButton(BoxLayout):
    def __init__(self, title, icon, callback, vertical=True, **kwargs):
        super().__init__(orientation="vertical" if vertical else "horizontal", spacing=dp(2), **kwargs)
        self.callback = callback
        self.icon_widget = CanvasIcon(icon=icon, color=GREEN)
        self.add_widget(self.icon_widget)
        self.title_widget = lbl(title, color=TEXT, size="11sp", bold=True,
                                size_hint_y=None, height=dp(23))
        self.add_widget(self.title_widget)
        self.bind(on_touch_down=self._touch)

    def _touch(self, widget, touch):
        if self.collide_point(*touch.pos):
            self.callback()
            return True
        return False


class PrayerCard(BoxLayout):
    def __init__(self, title, icon, time_text, active=False, **kwargs):
        super().__init__(orientation="vertical", padding=dp(4), spacing=dp(2), **kwargs)
        rounded(self, GREEN if active else WHITE, 17, MINT)
        color = WHITE if active else TEXT
        self.add_widget(CanvasIcon(icon=icon, color=WHITE if active else GREEN,
                                   size_hint_y=None, height=dp(32)))
        self.add_widget(lbl(title, color=color, size="12sp", bold=True))
        self.add_widget(lbl(time_text, color=color, size="15sp", bold=True))






class SettingsMenuRow(BoxLayout):
    """Ayarlar ana menusu icin ikonlu, acik zeminli kategori satiri."""
    def __init__(self, title, icon="settings", callback=None,
                 value_text="", toggle_value=None, toggle_callback=None, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None,
                         height=dp(84), padding=(dp(14), dp(8)), spacing=dp(12), **kwargs)
        self.callback = callback
        rounded(self, (0.97, 0.94, 0.84, 1), 0, (0.84, 0.82, 0.74, 1))
        self.add_widget(CanvasIcon(icon=icon, color=DARK,
                                   size_hint_x=None, width=dp(58)))
        text = title if not value_text else f"{title} [b]({value_text})[/b]"
        self.add_widget(lbl(text, color=(0.04, 0.04, 0.03, 1), size="18sp",
                            markup=True, halign="left", valign="middle"))
        if toggle_value is None:
            arrow = lbl("›", color=DARK, size="42sp", bold=True,
                        size_hint_x=None, width=dp(42))
            self.add_widget(arrow)
        else:
            control = CheckBox(active=bool(toggle_value), size_hint_x=None, width=dp(58))
            if toggle_callback:
                control.bind(active=lambda _, value: toggle_callback(value))
            self.add_widget(control)
        self.bind(on_touch_down=self._pressed)

    def _pressed(self, _, touch):
        if self.callback and self.collide_point(*touch.pos):
            self.callback()
            return True
        return False


class PermissionIcon(Widget):
    """Harici dosya kullanmadan izin durum simgesi cizer."""
    def __init__(self, granted=False, **kwargs):
        super().__init__(**kwargs)
        self.granted = granted
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_once(self.redraw, 0)

    def redraw(self, *_):
        self.canvas.clear()
        cx, cy = self.center
        radius = min(self.width, self.height) * .32
        color = (0.05, .62, .36, 1) if self.granted else (.86, .18, .12, 1)
        with self.canvas:
            Color(*color)
            Ellipse(pos=(cx-radius, cy-radius), size=(radius*2, radius*2))
            Color(*WHITE)
            if self.granted:
                Line(points=[
                    cx-radius*.48, cy,
                    cx-radius*.12, cy-radius*.36,
                    cx+radius*.53, cy+radius*.40,
                ], width=dp(3.2), joint="round", cap="round")
            else:
                Line(points=[cx, cy+radius*.48, cx, cy-radius*.15],
                     width=dp(3.2), cap="round")
                Ellipse(pos=(cx-dp(2.2), cy-radius*.52), size=(dp(4.4), dp(4.4)))


class EzanApp(App):
    def build(self):
        self.brand_icon_path = (
            Path(__file__).resolve().parent / "assets" / "huzur_vakti_icon.png"
        )
        if self.brand_icon_path.exists():
            self.icon = str(self.brand_icon_path)
        Window.clearcolor = BG
        self.root_dir = Path(__file__).resolve().parent
        self.sound_dirs = [
            self.root_dir / "ses_kutuphanesi",
            self.root_dir / "sounds",
            self.root_dir / "assets" / "sounds",
            self.root_dir / "audio",
        ]
        for folder in self.sound_dirs:
            folder.mkdir(parents=True, exist_ok=True)
        Path(self.user_data_dir).mkdir(parents=True, exist_ok=True)
        self.settings_file = Path(self.user_data_dir) / "settings.json"
        self.times_file = Path(self.user_data_dir) / "times.json"
        self.tasbih_file = Path(self.user_data_dir) / "tasbih.json"
        self.settings = self.load(self.settings_file, self.defaults())
        self.migrate_settings()
        self.times = self.load(self.times_file, [])
        self.tasbih = self.load(self.tasbih_file, {
            "count": 0, "total": 0, "target": 33,
            "phrase": "Sübhanallah", "date": date.today().isoformat(), "daily": 0,
        })
        self.preview_sound = None
        self.compass_active = False
        self.sound_catalog = self.scan_sounds()
        self.ensure_times()
        self.root_box = BoxLayout(orientation="vertical")
        self.body = BoxLayout()
        self.root_box.add_widget(self.body)
        self.root_box.add_widget(self.app_info_bar())
        self.root_box.add_widget(self.bottom_nav())
        self.show_home()
        Clock.schedule_interval(self.update_countdown, 1)
        Clock.schedule_interval(self.rotate_esma, 8)
        Clock.schedule_interval(lambda *_: self.sync_android_surfaces(), 60)
        Clock.schedule_once(lambda *_: self.sync_android_surfaces(), 2)
        Clock.schedule_once(lambda *_: self.ask_runtime_permissions(), .8)
        Clock.schedule_once(self.check_permissions_on_start, 1.4)
        if not self.settings.get("first_run", False):
            Clock.schedule_once(self.setup_popup, .5)
        return self.root_box

    @staticmethod
    def defaults():
        return {
            "app_silent_mode": True,
            "silent_mode_vibration": True,
            "silent_audio_stream": "ALARM",
            "play_pre_sound_during_silent": False,
            "play_prayer_sound_during_silent": True,
            "city": "Kayseri", "district": "Hacılar", "first_run": False,
            "persistent_notification": False,
            "iftar_countdown": False,
            "global_time_offset": 0,
            "prayer_offsets": {k: 0 for _, k, _ in PRAYERS},
            "kerahat_sunrise_minutes": 45,
            "kerahat_noon_minutes": 10,
            "kerahat_sunset_minutes": 45,
            "enabled": {k: True for _, k, _ in PRAYERS},
            "pre_enabled": {k: True for _, k, _ in PRAYERS},
            "pre": {k: 10 for _, k, _ in PRAYERS},
            "silent_enabled": {k: True for _, k, _ in PRAYERS},
            "silent": {k: 30 for _, k, _ in PRAYERS},
            "pre_sound": {k: "DEFAULT" for _, k, _ in PRAYERS},
            "prayer_sound": {k: "DEFAULT" for _, k, _ in PRAYERS},
        }

    @staticmethod
    def load(path, default):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            return value if isinstance(value, type(default)) else default
        except Exception:
            return default

    @staticmethod
    def save(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def migrate_settings(self):
        defaults = self.defaults()
        old = self.settings.get("sound", {})
        for group, value in defaults.items():
            if group not in self.settings or not isinstance(self.settings[group], type(value)):
                self.settings[group] = value.copy() if isinstance(value, dict) else value
        for _, key, _ in PRAYERS:
            for group in ("enabled", "pre_enabled", "pre", "silent_enabled", "silent"):
                self.settings[group].setdefault(key, defaults[group][key])
            old_value = old.get(key, "DEFAULT") if isinstance(old, dict) else "DEFAULT"
            self.settings["pre_sound"].setdefault(key, old_value)
            self.settings["prayer_sound"].setdefault(key, old_value)
        self.save(self.settings_file, self.settings)

    def current_coords(self):
        return DISTRICTS.get(
            (self.settings["city"], self.settings["district"]),
            PROVINCES.get(self.settings["city"], PROVINCES["Kayseri"]),
        )

    def clear(self):
        self.stop_compass()
        self.body.clear_widgets()

    def scroll(self):
        scroll = ScrollView(bar_width=dp(3))
        content = BoxLayout(orientation="vertical", size_hint_y=None,
                            padding=dp(15), spacing=dp(13))
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)
        self.body.add_widget(scroll)
        return content


    def app_info_bar(self):
        """Alt menunun ustunde her ekranda gorunen surum bilgi cubugu."""
        bar = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(34),
            padding=(dp(10), dp(3)), spacing=dp(6)
        )
        rounded(bar, (0.96, 0.98, 0.97, 1), 0, MINT)
        version_label = lbl(
            f"Miraç Ezan Vakti  •  Sürüm {APP_VERSION}",
            color=MUTED, size="10sp", halign="left", valign="middle"
        )
        info_button = FlatButton(
            text="UYGULAMA BİLGİSİ", size_hint_x=None, width=dp(138),
            bg=(0, 0, 0, 0), color=GREEN, font_size="10sp", bold=True
        )
        info_button.bind(on_release=self.show_app_info)
        bar.add_widget(version_label)
        bar.add_widget(info_button)
        return bar

    def show_app_info(self, *_):
        box = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(9))
        rounded(box, BG, 22)
        box.add_widget(lbl(
            "[b]Miraç Ezan Vakti[/b]", color=TEXT, size="24sp", markup=True,
            size_hint_y=None, height=dp(45)
        ))
        box.add_widget(lbl(
            f"Sürüm {APP_VERSION}\n\n"
            "Çevrimdışı namaz vakitleri, vakit hatırlatmaları, sessiz mod, "
            "kıble pusulası, tesbih, Kur'an okuma, kerahat vakitleri, "
            "Esmâü'l-Hüsnâ, ana ekran widget'ı ve üst bildirim özelliklerini "
            "bir arada sunar.\n\n"
            "Vakitlerin yerel farklılık gösterebildiği durumlarda Ayarlar "
            "bölümündeki dakika düzeltmesini kullanabilirsiniz. \n\n"
            "Bu uygulama Babam ve Annem adına hayrattır. Ruhlarına bir Fatiha okursanız bizleri çok mutlu edersiniz. \n\n"
            "Uygulama ücretsiz ve reklamsızdır. Rabbim Ümmeti Muhammed'in günahlarını af etsin. \n\n"
            "Uygulama 'Mustafa YILDIZ' tarafından geliştirilmiştir. ",
            color=TEXT, size="14sp", halign="left", valign="middle"
        ))
        close_button = FlatButton(
            text="KAPAT", size_hint_y=None, height=dp(50), bg=GREEN
        )
        box.add_widget(close_button)
        popup = Popup(
            title="", separator_height=0, content=box,
            size_hint=(.90, .70), background_color=(0, 0, 0, 0)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def bottom_nav(self):
        nav = BoxLayout(size_hint_y=None, height=dp(86), padding=(dp(8), dp(5)), spacing=dp(8))
        rounded(nav, WHITE, 0)
        for title, icon, action in [
            ("NAMAZ", "home", self.show_home),
            ("KUR'AN", "clock", self.show_quran),
            ("KIBLE", "compass", self.show_qibla),
            ("TESBİH", "tasbih", self.show_tasbih),
            ("AYARLAR", "settings", self.show_settings),
        ]:
            nav.add_widget(IconButton(title, icon, action))
        return nav

    def header(self, title):
        box = BoxLayout(
            size_hint_y=None, height=dp(72),
            padding=(dp(9), dp(6)), spacing=dp(8)
        )
        rounded(box, WHITE, 20, (.76, .87, .82, 1))

        icon_path = getattr(
            self,
            "brand_icon_path",
            Path(__file__).resolve().parent / "assets" / "huzur_vakti_icon.png",
        )
        if Path(icon_path).exists():
            logo = Image(
                source=str(icon_path),
                size_hint_x=None,
                width=dp(56),
                fit_mode="contain",
                mipmap=True,
            )
            box.add_widget(logo)

        box.add_widget(lbl(
            "[b]Miraç Ezan[/b]", size="23sp", markup=True, halign="left"
        ))
        tag = BoxLayout(size_hint_x=.55, padding=dp(5))
        rounded(tag, DARK, 15)
        tag.add_widget(lbl(
            f"[b]{title}[/b]", color=WHITE, size="20sp", markup=True
        ))
        box.add_widget(tag)
        return box

    def show_home(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.header("Vakti"))
        location = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        location.add_widget(CanvasIcon(icon="pin", color=GREEN, size_hint_x=None, width=dp(30)))
        location.add_widget(lbl(
            f"[b]{self.settings['city']} / {self.settings['district']}[/b]",
            color=TEXT, size="17sp", markup=True, halign="left"
        ))
        c.add_widget(location)
        card = FloatLayout(size_hint_y=None, height=dp(280))
        rounded(card, GREEN, 28)

        # Cami silüeti içerikten önce eklenir; böylece yazıların arkasında kalır.
        mosque_background = MosqueSilhouette(
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        card.add_widget(mosque_background)

        card_content = BoxLayout(
            orientation="horizontal",
            padding=dp(18), spacing=dp(12),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )

        countdown_side = BoxLayout(orientation="vertical", size_hint_x=.49,
                                   padding=(0, dp(14)), spacing=dp(8))
        self.next_title = lbl("Sonraki Vakit", color=WHITE, size="23sp",
                              bold=True, halign="left")
        self.countdown = lbl("00:00:00", color=WHITE, size="53sp",
                             bold=True, halign="left")
        countdown_side.add_widget(self.next_title)
        countdown_side.add_widget(self.countdown)
        card_content.add_widget(countdown_side)

        divider = Widget(size_hint_x=None, width=dp(2))
        with divider.canvas:
            Color(1, 1, 1, .30)
            divider._line = Rectangle(pos=divider.pos, size=divider.size)
        def update_esma_divider(*_):
            divider._line.pos = divider.pos
            divider._line.size = divider.size
        divider.bind(pos=update_esma_divider, size=update_esma_divider)
        card_content.add_widget(divider)

        esma_side = BoxLayout(orientation="vertical", size_hint_x=.51,
                              padding=(dp(10), dp(12)), spacing=dp(5))
        esma_side.add_widget(lbl("[b]Esmâü'l-Hüsnâ[/b]", color=(.86, 1, .95, 1),
                                 size="15sp", markup=True, size_hint_y=None,
                                 height=dp(32)))
        self.esma_name_label = lbl("", color=WHITE, size="29sp", bold=True,
                                   size_hint_y=None, height=dp(70))
        self.esma_meaning_label = lbl("", color=(.92, 1, .97, 1), size="15sp",
                                      halign="center", valign="middle")
        self.esma_counter_label = lbl("", color=(.78, .96, .90, 1), size="11sp",
                                      size_hint_y=None, height=dp(25))
        esma_side.add_widget(self.esma_name_label)
        esma_side.add_widget(self.esma_meaning_label)
        esma_side.add_widget(self.esma_counter_label)
        card_content.add_widget(esma_side)
        card.add_widget(card_content)
        c.add_widget(card)
        self.update_esma_display()
        row = BoxLayout(size_hint_y=None, height=dp(120), spacing=dp(6))
        rec = self.effective_record(self.today_record())
        _, next_key, _ = self.next_prayer()
        for title, key, icon in PRAYERS:
            row.add_widget(PrayerCard(title, icon, rec.get(key, "--:--"), key == next_key))
        c.add_widget(row)
        c.add_widget(self.build_kerahat_card())
        tools = BoxLayout(size_hint_y=None, height=dp(165), spacing=dp(10))
        for title, icon, action in [
            ("Kıble", "compass", self.show_qibla),
            ("Tesbih", "tasbih", self.show_tasbih),
            ("Ayarlar", "settings", self.show_settings),
        ]:
            panel = BoxLayout(orientation="vertical", padding=dp(10))
            rounded(panel, WHITE, 18, MINT)
            button = IconButton(title, icon, action)
            panel.add_widget(button)
            tools.add_widget(panel)
        c.add_widget(tools)
        c.add_widget(self.build_daily_card())
        self.update_countdown()


    def update_esma_display(self, *_):
        if not hasattr(self, "esma_name_label"):
            return
        index = getattr(self, "esma_index", date.today().toordinal() % len(ESMAUL_HUSNA))
        name, meaning = ESMAUL_HUSNA[index]
        self.esma_name_label.text = name
        self.esma_meaning_label.text = meaning
        self.esma_counter_label.text = f"{index + 1} / {len(ESMAUL_HUSNA)}"

    def rotate_esma(self, *_):
        self.esma_index = (getattr(self, "esma_index", -1) + 1) % len(ESMAUL_HUSNA)
        self.update_esma_display()

    def daily_content_index(self, collection):
        day_number = date.today().toordinal()
        return day_number % len(collection)

    def build_daily_card(self):
        verse_text, verse_source = DAILY_VERSES[self.daily_content_index(DAILY_VERSES)]
        hadith_text, hadith_source = DAILY_HADITHS[self.daily_content_index(DAILY_HADITHS)]
        card = BoxLayout(
            orientation="vertical", size_hint_y=None, height=dp(315),
            padding=dp(16), spacing=dp(10)
        )
        rounded(card, WHITE, 24, MINT)
        title = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        title.add_widget(CanvasIcon(icon="moon_star", color=GREEN,
                                    size_hint_x=None, width=dp(42)))
        title.add_widget(lbl("[b]Günün Âyeti ve Hadisi[/b]", color=TEXT,
                             size="19sp", markup=True, halign="left"))
        card.add_widget(title)
        verse_box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(4))
        rounded(verse_box, MINT, 17)
        verse_box.add_widget(lbl("[b]GÜNÜN ÂYETİ[/b]", color=TEXT,
                                 size="13sp", markup=True,
                                 size_hint_y=None, height=dp(25), halign="left"))
        verse_box.add_widget(lbl(f'“{verse_text}”', color=TEXT,
                                 size="16sp", halign="left", valign="middle"))
        verse_box.add_widget(lbl(verse_source, color=GREEN, size="12sp",
                                 bold=True, size_hint_y=None, height=dp(24),
                                 halign="right"))
        card.add_widget(verse_box)
        hadith_box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(4))
        rounded(hadith_box, (0.88, 0.97, 0.93, 1), 17)
        hadith_box.add_widget(lbl("[b]GÜNÜN HADİSİ[/b]", color=TEXT,
                                  size="13sp", markup=True,
                                  size_hint_y=None, height=dp(25), halign="left"))
        hadith_box.add_widget(lbl(f'“{hadith_text}”', color=TEXT,
                                  size="15sp", halign="left", valign="middle"))
        hadith_box.add_widget(lbl(hadith_source, color=GREEN, size="12sp",
                                  bold=True, size_hint_y=None, height=dp(24),
                                  halign="right"))
        card.add_widget(hadith_box)
        return card

    def today_record(self):
        return next((x for x in self.times if x.get("date") == date.today().isoformat()), None)

    def next_prayer(self):
        now = datetime.now()
        for offset in (0, 1):
            target_day = date.today() + timedelta(days=offset)
            record = next((x for x in self.times if x.get("date") == target_day.isoformat()), None)
            if not record:
                continue
            for title, key, _ in PRAYERS:
                try:
                    hour, minute = map(int, self.effective_time(record, key).split(":"))
                    target = datetime.combine(target_day, datetime.min.time()).replace(
                        hour=hour, minute=minute
                    )
                    if target > now:
                        return title, key, target
                except Exception:
                    continue
        return "İmsak", "Imsak", now + timedelta(hours=1)

    def update_countdown(self, *_):
        if not hasattr(self, "countdown"):
            return
        title, _, target = self.next_prayer()
        seconds = max(0, int((target - datetime.now()).total_seconds()))
        self.next_title.text = f"{title} Vakti"
        self.countdown.text = f"{seconds//3600:02d}:{(seconds%3600)//60:02d}:{seconds%60:02d}"


    def sync_android_surfaces(self):
        """Widget ve kalici ust bildirime guncel vakitleri aktarir."""
        try:
            return bool(sync_prayer_surface(self))
        except Exception as error:
            print("Widget ve ust bildirim esitleme hatasi:", error)
            return False

    def add_prayer_widget(self, *_):
        """Android ana ekranina widget sabitleme istegi acar."""
        if not self.is_android():
            self.alert("Widget", "Ana ekran widget'i yalnizca Android APK surumunde kullanilabilir.")
            return
        try:
            if request_pin_widget():
                self.alert("Widget Ekle", "Android widget ekleme penceresi acildi. Miraç Vakti widget'ini onaylayin.")
            else:
                self.alert("Widget Ekle", "Ana ekranda bos bir alana uzun basin. Widget'lar bolumunden Miraç Vakti'ni secin.")
        except Exception as error:
            self.alert("Widget Hatasi", str(error))


    @staticmethod
    def shift_time_text(time_text, minutes):
        try:
            hour, minute = map(int, time_text.split(":"))
            total = (hour * 60 + minute + int(minutes)) % 1440
            return f"{total // 60:02d}:{total % 60:02d}"
        except Exception:
            return time_text

    def effective_time(self, record, key):
        global_offset = int(self.settings.get("global_time_offset", 0))
        prayer_offset = int(self.settings.get("prayer_offsets", {}).get(key, 0))
        return self.shift_time_text(record.get(key, "--:--"), global_offset + prayer_offset)

    def effective_record(self, record):
        if not record:
            return {}
        result = dict(record)
        for _, key, _ in PRAYERS:
            result[key] = self.effective_time(record, key)
        return result

    def kerahat_periods(self, record=None):
        record = self.effective_record(record or self.today_record())
        if not record:
            return []
        def minute_value(text):
            h, m = map(int, text.split(":"))
            return h * 60 + m
        def text_value(total):
            total %= 1440
            return f"{total // 60:02d}:{total % 60:02d}"
        sunrise = minute_value(record["Gunes"])
        noon = minute_value(record["Ogle"])
        sunset = minute_value(record["Aksam"])
        sunrise_minutes = int(self.settings.get("kerahat_sunrise_minutes", 45))
        noon_minutes = int(self.settings.get("kerahat_noon_minutes", 10))
        sunset_minutes = int(self.settings.get("kerahat_sunset_minutes", 45))
        return [
            ("Doğuş Kerahati", text_value(sunrise), text_value(sunrise + sunrise_minutes)),
            ("İstivâ Kerahati", text_value(noon - noon_minutes), text_value(noon)),
            ("Batış Kerahati", text_value(sunset - sunset_minutes), text_value(sunset)),
        ]

    def current_kerahat(self):
        now = datetime.now().hour * 60 + datetime.now().minute
        for title, start, end in self.kerahat_periods():
            sh, sm = map(int, start.split(":"))
            eh, em = map(int, end.split(":"))
            if sh * 60 + sm <= now < eh * 60 + em:
                return title, start, end
        return None

    def build_kerahat_card(self):
        card = BoxLayout(orientation="vertical", size_hint_y=None,
                         height=dp(185), padding=dp(12), spacing=dp(6))
        rounded(card, WHITE, 20, (1, .55, .48, 1))
        card.add_widget(lbl("[b]Kerahat Vakitleri[/b]", color=RED,
                            size="17sp", markup=True, size_hint_y=None,
                            height=dp(32), halign="left"))
        active = self.current_kerahat()
        for title, start, end in self.kerahat_periods():
            is_active = bool(active and active[0] == title)
            card.add_widget(lbl(
                f"{title}: {start} - {end}" + ("   AKTİF" if is_active else ""),
                color=RED if is_active else TEXT, size="14sp", bold=is_active,
                size_hint_y=None, height=dp(35), halign="left"))
        return card

    def save_time_adjustments(self, *_):
        try:
            self.settings["global_time_offset"] = max(-120, min(120, int(self.global_offset_input.text or 0)))
        except ValueError:
            self.settings["global_time_offset"] = 0
        for _, key, _ in PRAYERS:
            try:
                value = int(self.prayer_offset_inputs[key].text or 0)
            except ValueError:
                value = 0
            self.settings["prayer_offsets"][key] = max(-120, min(120, value))
        self.save(self.settings_file, self.settings)
        self.schedule_all_alarms()
        self.sync_android_surfaces()
        self.show_home()
        self.alert("Vakit Ayarı", "Dakika düzeltmeleri uygulandı. Widget ve bildirim yenilendi.")

    @staticmethod
    def qibla_bearing(lat, lon):
        lat1, lat2 = math.radians(lat), math.radians(KAABA_LAT)
        difference = math.radians(KAABA_LON - lon)
        y = math.sin(difference) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(difference)
        return (math.degrees(math.atan2(y, x)) + 360) % 360


    def show_quran(self, *_):
        self.clear()
        content = self.scroll()
        content.add_widget(self.header("Kur'an-ı Kerim"))
        info = lbl(
            "114 sûrenin Arapça metnini ve Türkçe mealini okuyabilirsiniz. "
            "İlk açılışta internet gerekir; açılan sûreler cihazda saklanır.",
            color=TEXT, size="14sp", size_hint_y=None, height=dp(72)
        )
        content.add_widget(info)
        names = tuple(f"{i + 1}. {name}" for i, name in enumerate(QURAN_SURAH_NAMES))
        self.quran_surah_spinner = Spinner(
            text=names[0], values=names, size_hint_y=None, height=dp(54),
            background_normal="", background_color=MINT, color=TEXT
        )
        content.add_widget(self.quran_surah_spinner)
        controls = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        open_button = FlatButton(text="Sûreyi Aç")
        open_button.bind(on_release=self.open_selected_surah)
        clear_button = FlatButton(text="Önbelleği Temizle", bg=(.45, .48, .45, 1))
        clear_button.bind(on_release=self.clear_quran_cache)
        controls.add_widget(open_button)
        controls.add_widget(clear_button)
        content.add_widget(controls)
        self.quran_status = lbl("Bir sûre seçip Sûreyi Aç düğmesine basın.",
                                color=MUTED, size="13sp", size_hint_y=None, height=dp(42))
        content.add_widget(self.quran_status)
        self.quran_text_box = TextInput(
            text="", readonly=True, multiline=True, size_hint_y=None, height=dp(680),
            background_normal="", background_color=WHITE, foreground_color=TEXT,
            padding=(dp(15), dp(15)), font_size="17sp"
        )
        content.add_widget(self.quran_text_box)

    def open_selected_surah(self, *_):
        try:
            number = int(self.quran_surah_spinner.text.split(".", 1)[0])
        except Exception:
            number = 1
        self.quran_status.text = "Sûre yükleniyor..."
        self.quran_text_box.text = ""
        Clock.schedule_once(lambda *_: self.load_surah(number), .05)

    def quran_cache_dir(self):
        directory = Path(self.user_data_dir) / "quran_cache"
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def load_surah(self, number):
        cache_file = self.quran_cache_dir() / f"surah_{number:03d}.json"
        data = None
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text(encoding="utf-8"))
            except Exception:
                data = None
        if data is None:
            try:
                import urllib.request
                ar_url = f"https://kuranapp.com/veri/surah-{number}-ar.json"
                tr_url = f"https://kuranapp.com/veri/surah-{number}-tr.json"
                request_headers = {"User-Agent": "MiracVakti/1.0"}
                with urllib.request.urlopen(urllib.request.Request(ar_url, headers=request_headers), timeout=20) as response:
                    arabic = json.loads(response.read().decode("utf-8"))
                with urllib.request.urlopen(urllib.request.Request(tr_url, headers=request_headers), timeout=20) as response:
                    turkish = json.loads(response.read().decode("utf-8"))
                data = {"arabic": arabic, "turkish": turkish}
                cache_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            except Exception as error:
                self.quran_status.text = "Sûre yüklenemedi. İnternet bağlantısını kontrol edin."
                self.quran_text_box.text = f"Bağlantı hatası:\n{error}"
                return
        try:
            ar_data = data["arabic"]["data"]
            tr_data = data["turkish"]["data"]
            ar_ayahs = ar_data.get("ayahs", [])
            tr_ayahs = tr_data.get("ayahs", [])
            title = QURAN_SURAH_NAMES[number - 1]
            lines = [f"{number}. {title} Sûresi", ""]
            for index, ar_ayah in enumerate(ar_ayahs):
                ayah_no = ar_ayah.get("numberInSurah", index + 1)
                ar_text = ar_ayah.get("text", "")
                tr_text = tr_ayahs[index].get("text", "") if index < len(tr_ayahs) else ""
                lines.extend([f"{ayah_no}", ar_text, tr_text, ""])
            self.quran_text_box.text = "\n".join(lines)
            self.quran_status.text = f"{title} Sûresi açıldı. {len(ar_ayahs)} âyet."
        except Exception as error:
            self.quran_status.text = "Sûre verisi okunamadı."
            self.quran_text_box.text = str(error)

    def clear_quran_cache(self, *_):
        directory = self.quran_cache_dir()
        removed = 0
        for path in directory.glob("surah_*.json"):
            try:
                path.unlink()
                removed += 1
            except Exception:
                pass
        self.quran_status.text = f"{removed} kayıtlı sûre önbellekten silindi."

    def show_qibla(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.header("Kıble"))
        lat, lon = self.current_coords()
        self.qibla_angle = self.qibla_bearing(lat, lon)
        c.add_widget(lbl(
            f"[b]{self.settings['city']} / {self.settings['district']}[/b]\n"
            f"Kıble açısı: {self.qibla_angle:.1f} derece",
            color=TEXT, size="17sp", markup=True, size_hint_y=None, height=dp(65)
        ))
        compass = FloatLayout(size_hint_y=None, height=dp(350))
        rounded(compass, WHITE, 28, MINT)
        with compass.canvas:
            Color(*DARK)
            self.compass_outer = Line(circle=(0, 0, 1), width=dp(3))
            Color(*MINT)
            self.compass_inner = Line(circle=(0, 0, 1), width=dp(2))
            PushMatrix()
            self.arrow_rotation = Rotate(angle=0, origin=compass.center)
            Color(*GREEN)
            self.arrow = Triangle(points=[0, 0, 0, 0, 0, 0])
            Color(*GOLD)
            self.arrow_tail = Triangle(points=[0, 0, 0, 0, 0, 0])
            PopMatrix()
            # Kible yonundeki Kabe isareti. Ok donerken Kabe dik kalir.
            Color(0.02, 0.02, 0.02, 1)
            self.kaaba_body = RoundedRectangle(pos=(0, 0), size=(1, 1), radius=[dp(3)])
            Color(*GOLD)
            self.kaaba_band = Rectangle(pos=(0, 0), size=(1, 1))
            self.kaaba_door = Rectangle(pos=(0, 0), size=(1, 1))
            Color(*WHITE)
            self.kaaba_outline = Line(rounded_rectangle=(0, 0, 1, 1, dp(3)), width=dp(1.2))
        compass.bind(pos=lambda *_: self.draw_compass(compass),
                     size=lambda *_: self.draw_compass(compass))
        for text, px, py in [("K", .5, .88), ("D", .86, .5), ("G", .5, .12), ("B", .14, .5)]:
            compass.add_widget(lbl(text, color=TEXT, size="18sp", bold=True,
                                   size_hint=(None, None), width=dp(35), height=dp(35),
                                   pos_hint={"center_x": px, "center_y": py}))
        self.qibla_status = lbl("Pusula başlatılıyor...", color=MUTED, size="14sp",
                                size_hint=(.9, None), height=dp(58),
                                pos_hint={"center_x": .5, "y": .02})
        compass.add_widget(self.qibla_status)
        self.compass_widget = compass
        c.add_widget(compass)
        Clock.schedule_once(lambda *_: self.draw_compass(compass), 0)
        Clock.schedule_once(lambda *_: self.draw_compass(compass), .15)
        c.add_widget(lbl(
            "Telefonu düz tutun. Sapma varsa telefonu havada 8 çizerek kalibre edin.",
            color=MUTED, size="14sp", size_hint_y=None, height=dp(65)
        ))
        self.start_compass()

    def draw_compass(self, widget):
        cx, cy = widget.center
        radius = min(widget.width, widget.height) * .35
        self.compass_outer.circle = (cx, cy, radius)
        self.compass_inner.circle = (cx, cy, radius * .78)
        self.arrow.points = [cx, cy+radius*.72, cx-radius*.13, cy-radius*.16, cx, cy-radius*.03]
        self.arrow_tail.points = [cx, cy-radius*.72, cx+radius*.13, cy+radius*.16, cx, cy+radius*.03]
        self.arrow_rotation.origin = (cx, cy)
        self.compass_center = (cx, cy)
        self.compass_radius = radius
        relative = getattr(self, "current_qibla_relative", self.qibla_angle)
        self.update_kaaba_marker(relative)

    def update_kaaba_marker(self, relative_angle):
        if not hasattr(self, "kaaba_body") or not hasattr(self, "compass_center"):
            return
        cx, cy = self.compass_center
        radius = self.compass_radius
        angle = math.radians(relative_angle)
        marker_distance = radius * .79
        marker_x = cx + math.sin(angle) * marker_distance
        marker_y = cy + math.cos(angle) * marker_distance
        width = max(dp(30), radius * .25)
        height = max(dp(34), radius * .29)
        left = marker_x - width / 2
        bottom = marker_y - height / 2
        self.kaaba_body.pos = (left, bottom)
        self.kaaba_body.size = (width, height)
        self.kaaba_body.radius = [dp(3)]
        self.kaaba_band.pos = (left, bottom + height * .64)
        self.kaaba_band.size = (width, max(dp(4), height * .11))
        self.kaaba_door.pos = (left + width * .39, bottom)
        self.kaaba_door.size = (width * .22, height * .36)
        self.kaaba_outline.rounded_rectangle = (left, bottom, width, height, dp(3))

    def start_compass(self):
        self.compass_active = True
        try:
            from plyer import spatialorientation
            spatialorientation.enable()
            self.orientation_sensor = spatialorientation
        except Exception:
            self.orientation_sensor = None
        self.compass_event = Clock.schedule_interval(self.read_compass, .18)

    def read_compass(self, *_):
        if not self.compass_active:
            return
        compass_widget = getattr(self, "compass_widget", None)
        if compass_widget is not None:
            self.draw_compass(compass_widget)
        heading = None
        try:
            values = self.orientation_sensor.orientation if self.orientation_sensor else None
            if values and values[0] is not None:
                heading = float(values[0]) % 360
        except Exception:
            heading = None
        if heading is None:
            heading = 0.0
            sensor_text = "Sensör verisi yok, kuzey 0 derece kabul edildi"
        else:
            sensor_text = f"Kuzey yönü: {heading:.1f} derece"
        relative = (self.qibla_angle - heading) % 360
        self.current_qibla_relative = relative
        self.arrow_rotation.angle = -relative
        self.update_kaaba_marker(relative)
        side = "sağa" if relative <= 180 else "sola"
        turn = relative if relative <= 180 else 360 - relative
        self.qibla_status.text = f"{sensor_text}\nKıble için {turn:.1f} derece {side} dönün"

    def stop_compass(self):
        self.compass_active = False
        event = getattr(self, "compass_event", None)
        if event:
            event.cancel()
            self.compass_event = None
        try:
            sensor = getattr(self, "orientation_sensor", None)
            if sensor:
                sensor.disable()
        except Exception:
            pass

    def show_tasbih(self, *_):
        self.clear()
        self.check_tasbih_day()
        c = self.scroll()
        c.add_widget(self.header("Tesbih"))
        phrase = Spinner(
            text=self.tasbih["phrase"],
            values=("Sübhanallah", "Elhamdülillah", "Allahu Ekber",
                    "Lâ ilâhe illallah", "Salavat", "Özel Zikir"),
            size_hint_y=None, height=dp(52), background_normal="",
            background_color=MINT, color=TEXT,
        )
        phrase.bind(text=lambda _, value: self.set_phrase(value))
        c.add_widget(phrase)
        targets = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        for target in (33, 99, 100, 500):
            button = FlatButton(text=str(target), bg=GOLD if self.tasbih["target"] == target else GREEN)
            button.bind(on_release=lambda _, value=target: self.set_target(value))
            targets.add_widget(button)
        c.add_widget(targets)
        counter_panel = FloatLayout(size_hint_y=None, height=dp(310))
        rounded(counter_panel, GREEN, 30)
        counter_panel.add_widget(CanvasIcon(icon="tasbih", color=(1, 1, 1, .18),
                                            size_hint=(.8, .8), pos_hint={"center_x": .5, "center_y": .5}))
        self.tasbih_counter = FlatButton(
            text=str(self.tasbih["count"]), bg=(0, 0, 0, 0), font_size="78sp",
            pos_hint={"center_x": .5, "center_y": .5}, size_hint=(1, 1)
        )
        self.tasbih_counter.bind(on_release=self.increment_tasbih)
        counter_panel.add_widget(self.tasbih_counter)
        c.add_widget(counter_panel)
        self.tasbih_info = lbl("", color=TEXT, size="16sp", size_hint_y=None, height=dp(70))
        c.add_widget(self.tasbih_info)
        controls = BoxLayout(size_hint_y=None, height=dp(55), spacing=dp(8))
        undo = FlatButton(text="Geri Al", bg=(.40, .46, .43, 1))
        undo.bind(on_release=self.undo_tasbih)
        reset = FlatButton(text="Sıfırla", bg=RED)
        reset.bind(on_release=self.reset_tasbih)
        controls.add_widget(undo)
        controls.add_widget(reset)
        c.add_widget(controls)
        self.update_tasbih_ui()

    def check_tasbih_day(self):
        today = date.today().isoformat()
        if self.tasbih.get("date") != today:
            self.tasbih["date"] = today
            self.tasbih["daily"] = 0
            self.save(self.tasbih_file, self.tasbih)

    def set_phrase(self, value):
        self.tasbih["phrase"] = value
        self.save(self.tasbih_file, self.tasbih)

    def set_target(self, value):
        self.tasbih["target"] = value
        self.save(self.tasbih_file, self.tasbih)
        self.show_tasbih()

    def increment_tasbih(self, *_):
        self.tasbih["count"] += 1
        self.tasbih["total"] += 1
        self.tasbih["daily"] += 1
        self.vibrate(.035)
        if self.tasbih["count"] >= self.tasbih["target"]:
            self.vibrate(.25)
            self.alert("Hedef Tamamlandı",
                       f"{self.tasbih['target']} adet {self.tasbih['phrase']} tamamlandı.")
            self.tasbih["count"] = 0
        self.save(self.tasbih_file, self.tasbih)
        self.update_tasbih_ui()

    def undo_tasbih(self, *_):
        if self.tasbih["count"] > 0:
            self.tasbih["count"] -= 1
        if self.tasbih["total"] > 0:
            self.tasbih["total"] -= 1
        if self.tasbih["daily"] > 0:
            self.tasbih["daily"] -= 1
        self.save(self.tasbih_file, self.tasbih)
        self.update_tasbih_ui()

    def reset_tasbih(self, *_):
        self.tasbih["count"] = 0
        self.save(self.tasbih_file, self.tasbih)
        self.update_tasbih_ui()

    def update_tasbih_ui(self):
        if hasattr(self, "tasbih_counter"):
            self.tasbih_counter.text = str(self.tasbih["count"])
        if hasattr(self, "tasbih_info"):
            self.tasbih_info.text = (
                f"Hedef: {self.tasbih['target']}   |   Bugün: {self.tasbih['daily']}"
                f"   |   Toplam: {self.tasbih['total']}"
            )

    @staticmethod
    def vibrate(seconds):
        try:
            from plyer import vibrator
            vibrator.vibrate(seconds)
        except Exception:
            pass

    def scan_sounds(self):
        result = {"Varsayılan Android Sesi": "DEFAULT", "Sessiz": "SILENT"}
        unique = {}
        priority = {".wav": 0, ".ogg": 1, ".mp3": 2, ".m4a": 3, ".aac": 4}
        for folder in self.sound_dirs:
            if not folder.exists():
                continue
            for path in folder.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
                    continue
                if any(part.lower() in ("yedek", "backup", "old", "orijinal_mp3_yedek")
                       for part in path.parts):
                    continue
                key = " ".join(path.stem.replace("_", " ").replace("-", " ").lower().split())
                rank = priority.get(path.suffix.lower(), 9)
                if key not in unique or rank < unique[key][0]:
                    unique[key] = (rank, path)
        for key, (_, path) in sorted(unique.items()):
            name = " ".join(word.capitalize() for word in key.split())
            result[name] = "FILE::" + str(path.resolve())
        return result



    def settings_page_header(self, title):
        row = BoxLayout(size_hint_y=None, height=dp(62), spacing=dp(8))
        back = FlatButton(text="GERİ", size_hint_x=None, width=dp(78), bg=DARK)
        back.bind(on_release=self.show_settings)
        row.add_widget(back)
        title_box = BoxLayout(padding=(dp(12), dp(4)))
        rounded(title_box, WHITE, 18, MINT)
        title_box.add_widget(lbl(f"[b]{title}[/b]", color=TEXT, size="19sp",
                                 markup=True, halign="left"))
        row.add_widget(title_box)
        return row

    def settings_menu_item(self, title, icon, callback, subtitle="", toggle=None):
        card = BoxLayout(orientation="horizontal", size_hint_y=None,
                         height=dp(82), padding=(dp(12), dp(8)), spacing=dp(10))
        rounded(card, WHITE, 18, MINT)
        card.add_widget(CanvasIcon(icon=icon, color=GREEN,
                                   size_hint_x=None, width=dp(54)))
        texts = BoxLayout(orientation="vertical", spacing=dp(1))
        texts.add_widget(lbl(f"[b]{title}[/b]", color=TEXT, size="16sp",
                             markup=True, halign="left"))
        if subtitle:
            texts.add_widget(lbl(subtitle, color=MUTED, size="11sp",
                                 size_hint_y=None, height=dp(24), halign="left"))
        card.add_widget(texts)
        if toggle is None:
            arrow = FlatButton(text=">", size_hint_x=None, width=dp(52),
                               bg=(0, 0, 0, 0), color=GREEN, font_size="28sp")
            arrow.bind(on_release=callback)
            card.add_widget(arrow)
            card.bind(on_touch_down=lambda widget, touch:
                      self._open_settings_card(widget, touch, callback))
        else:
            check = CheckBox(active=bool(toggle[0]), size_hint_x=None, width=dp(58))
            check.bind(active=lambda _, value: toggle[1](value))
            card.add_widget(check)
        return card

    @staticmethod
    def _open_settings_card(widget, touch, callback):
        if widget.collide_point(*touch.pos):
            callback()
            return True
        return False

    def show_settings(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.header("Ayarlar"))
        c.add_widget(lbl(
            "Değiştirmek istediğiniz ayar bölümünü seçin.",
            color=MUTED, size="13sp", size_hint_y=None, height=dp(42),
            halign="left"))

        offset = int(self.settings.get("global_time_offset", 0))
        kerahat = int(self.settings.get("kerahat_sunrise_minutes", 45))
        c.add_widget(self.settings_menu_item(
            "Konum Ayarları", "pin", self.show_location_settings,
            f"{self.settings.get('city', 'Kayseri')} / {self.settings.get('district', 'Hacılar')}"))
        c.add_widget(self.settings_menu_item(
            "Hatırlatma Ayarları", "clock", self.show_notification_settings,
            "Ön uyarı, vakit bildirimi ve ses seçimleri"))
        c.add_widget(self.settings_menu_item(
            "Vakitlerde Sessize Al", "moon", self.show_silent_settings,
            "Her vakit için sessiz kalma süresi"))
        c.add_widget(self.settings_menu_item(
            "Vakit ve Konum Sapma Ayarı", "compass", self.show_offset_settings,
            f"Tüm vakitler için {offset:+d} dakika"))
        c.add_widget(self.settings_menu_item(
            "Kerahat Vakti", "sunset", self.show_kerahat_settings,
            f"Doğuş sonrası varsayılan {kerahat} dakika"))
        c.add_widget(self.settings_menu_item(
            "Üst Bildirim ve Widget", "clock", self.show_widget_settings,
            "Kalıcı bildirim ve ana ekran widget'ı"))
        c.add_widget(self.settings_menu_item(
            "İzin Kontrolü", "settings", self.show_permissions,
            "Bildirim, konum, alarm ve pil izinleri"))
        c.add_widget(self.settings_menu_item(
            "Ses Dosyaları", "settings", self.show_sound_library_settings,
            f"{max(0, len(self.scan_sounds()) - 2)} özel ses bulundu"))
        update = FlatButton(text="VAKİTLERİ ŞİMDİ GÜNCELLE",
                            size_hint_y=None, height=dp(54), bg=GREEN)
        update.bind(on_release=self.force_update_times)
        c.add_widget(update)

    def show_location_settings(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.settings_page_header("Konum Ayarları"))
        c.add_widget(lbl(
            "Bulunduğunuz il ve ilçeyi seçin. İlçeniz listede yoksa en yakın konumu "
            "seçip Vakit ve Konum Sapma Ayarı bölümünden dakika farkı uygulayın.",
            color=MUTED, size="13sp", size_hint_y=None, height=dp(78),
            halign="left", valign="middle"))
        city = Spinner(text=self.settings.get("city", "Kayseri"),
                       values=tuple(sorted(PROVINCES)), size_hint_y=None,
                       height=dp(54), background_normal="", background_color=MINT,
                       color=TEXT)
        districts = tuple(sorted(KAYSERI_DISTRICTS)) if city.text == "Kayseri" else ("Merkez",)
        current_district = self.settings.get("district", districts[0])
        if current_district not in districts:
            current_district = districts[0]
        district = Spinner(text=current_district, values=districts,
                           size_hint_y=None, height=dp(54), background_normal="",
                           background_color=MINT, color=TEXT)
        city.bind(text=lambda _, value: self.update_setup_district(district, value))
        c.add_widget(lbl("İl", color=TEXT, size="13sp", size_hint_y=None,
                         height=dp(28), halign="left"))
        c.add_widget(city)
        c.add_widget(lbl("İlçe", color=TEXT, size="13sp", size_hint_y=None,
                         height=dp(28), halign="left"))
        c.add_widget(district)
        save_button = FlatButton(text="KONUMU KAYDET VE VAKİTLERİ YENİLE",
                                 size_hint_y=None, height=dp(56))
        save_button.bind(on_release=lambda *_:
                         self.save_location_settings(city.text, district.text))
        c.add_widget(save_button)

    def save_location_settings(self, city, district):
        self.settings["city"] = city
        self.settings["district"] = district if city == "Kayseri" else "Merkez"
        self.settings["first_run"] = True
        self.save(self.settings_file, self.settings)
        self.ensure_times(True)
        self.sync_android_surfaces()
        self.alert("Konum Kaydedildi", "Konum, vakitler, alarmlar ve widget yenilendi.")
        self.show_settings()

    def show_notification_settings(self, *_):
        self.clear()
        self.sound_catalog = self.scan_sounds()
        self.notification_widgets = {}
        c = self.scroll()
        c.add_widget(self.settings_page_header("Hatırlatma Ayarları"))
        c.add_widget(lbl(
            "Bu bölümde yalnızca ön uyarı, vakit bildirimi ve bildirim sesleri ayarlanır.",
            color=MUTED, size="13sp", size_hint_y=None, height=dp(58), halign="left"))
        for title, key, icon in PRAYERS:
            card = BoxLayout(orientation="vertical", size_hint_y=None,
                             height=dp(245), padding=dp(12), spacing=dp(7))
            rounded(card, WHITE, 20, MINT)
            head = BoxLayout(size_hint_y=None, height=dp(42))
            head.add_widget(CanvasIcon(icon=icon, color=GREEN,
                                       size_hint_x=None, width=dp(42)))
            enabled = CheckBox(active=self.settings["enabled"][key],
                               size_hint_x=None, width=dp(45))
            head.add_widget(enabled)
            head.add_widget(lbl(f"[b]{title} bildirimi[/b]", markup=True,
                                color=TEXT, size="16sp", halign="left"))
            card.add_widget(head)
            pre_check, pre_input, pre_row = self.minute_row(
                "Ön uyarı", self.settings["pre_enabled"][key],
                self.settings["pre"][key])
            card.add_widget(pre_row)
            pre_sound = self.sound_row(card, "Ön bildirim sesi",
                                       self.settings["pre_sound"][key])
            prayer_sound = self.sound_row(card, "Vakit giriş sesi",
                                          self.settings["prayer_sound"][key])
            self.notification_widgets[key] = (
                enabled, pre_check, pre_input, pre_sound, prayer_sound)
            c.add_widget(card)
        save_button = FlatButton(text="HATIRLATMA AYARLARINI KAYDET",
                                 size_hint_y=None, height=dp(56))
        save_button.bind(on_release=self.save_notification_settings)
        c.add_widget(save_button)

    def save_notification_settings(self, *_):
        for _, key, _ in PRAYERS:
            enabled, pre_check, pre_input, pre_sound, prayer_sound = self.notification_widgets[key]
            self.settings["enabled"][key] = bool(enabled.active)
            self.settings["pre_enabled"][key] = bool(pre_check.active)
            try:
                self.settings["pre"][key] = max(0, min(1440, int(pre_input.text or 0)))
            except ValueError:
                self.settings["pre"][key] = 10
            self.settings["pre_sound"][key] = self.sound_catalog[pre_sound.text]
            self.settings["prayer_sound"][key] = self.sound_catalog[prayer_sound.text]
        self.save(self.settings_file, self.settings)
        self.schedule_all_alarms()
        self.alert("Kaydedildi", "Hatırlatma ve ses ayarları kaydedildi.")

    def audio_stream_display_name(self):
        value = self.settings.get("silent_audio_stream", "ALARM")
        return {
            "ALARM": "Alarm sesi",
            "MEDIA": "Medya sesi",
            "NOTIFICATION": "Bildirim sesi",
        }.get(value, "Alarm sesi")

    def show_silent_settings(self, *_):
        self.clear()
        self.silent_widgets = {}
        c = self.scroll()
        c.add_widget(self.settings_page_header("Vakitlerde Sessize Al"))

        info = BoxLayout(orientation="vertical", size_hint_y=None,
                         height=dp(118), padding=dp(12), spacing=dp(4))
        rounded(info, WHITE, 18, MINT)
        info.add_widget(lbl(
            "[b]Uygulama Sessiz Modu[/b]", color=TEXT, size="17sp",
            markup=True, size_hint_y=None, height=dp(34), halign="left"))
        info.add_widget(lbl(
            "Telefonun genel zil veya Rahatsız Etmeyin ayarı değiştirilmez. "
            "Miraç Ezan Vakti kendi bildirim sesini, ses kategorisini ve "
            "titreşimini kullanıcı tercihlerine göre yönetir.",
            color=MUTED, size="12sp", halign="left", valign="middle"))
        c.add_widget(info)

        mode_row = BoxLayout(size_hint_y=None, height=dp(62), padding=dp(10), spacing=dp(8))
        rounded(mode_row, WHITE, 17, MINT)
        self.app_silent_mode_check = CheckBox(
            active=self.settings.get("app_silent_mode", True),
            size_hint_x=None, width=dp(48))
        mode_row.add_widget(self.app_silent_mode_check)
        mode_row.add_widget(lbl("Uygulama sessiz modu etkin", color=TEXT,
                                size="14sp", halign="left"))
        c.add_widget(mode_row)

        vibration_row = BoxLayout(size_hint_y=None, height=dp(62), padding=dp(10), spacing=dp(8))
        rounded(vibration_row, WHITE, 17, MINT)
        self.silent_vibration_check = CheckBox(
            active=self.settings.get("silent_mode_vibration", True),
            size_hint_x=None, width=dp(48))
        vibration_row.add_widget(self.silent_vibration_check)
        vibration_row.add_widget(lbl(
            "Uygulama bildirimlerinde titreşim kullan",
            color=TEXT, size="13sp", halign="left"))
        c.add_widget(vibration_row)

        c.add_widget(lbl("Bildirim ses kategorisi", color=TEXT, size="13sp",
                         size_hint_y=None, height=dp(30), halign="left"))
        names = {"ALARM": "Alarm sesi", "MEDIA": "Medya sesi",
                 "NOTIFICATION": "Bildirim sesi"}
        current = self.settings.get("silent_audio_stream", "ALARM")
        self.silent_audio_stream_spinner = Spinner(
            text=names.get(current, "Alarm sesi"),
            values=("Alarm sesi", "Medya sesi", "Bildirim sesi"),
            size_hint_y=None, height=dp(54), background_normal="",
            background_color=MINT, color=TEXT)
        c.add_widget(self.silent_audio_stream_spinner)

        pre_row = BoxLayout(size_hint_y=None, height=dp(62), padding=dp(10), spacing=dp(8))
        rounded(pre_row, WHITE, 17, MINT)
        self.play_pre_during_silent_check = CheckBox(
            active=self.settings.get("play_pre_sound_during_silent", False),
            size_hint_x=None, width=dp(48))
        pre_row.add_widget(self.play_pre_during_silent_check)
        pre_row.add_widget(lbl("Ön uyarı sesini sessiz sürede çal", color=TEXT,
                               size="13sp", halign="left"))
        c.add_widget(pre_row)

        prayer_row = BoxLayout(size_hint_y=None, height=dp(62), padding=dp(10), spacing=dp(8))
        rounded(prayer_row, WHITE, 17, MINT)
        self.play_prayer_during_silent_check = CheckBox(
            active=self.settings.get("play_prayer_sound_during_silent", True),
            size_hint_x=None, width=dp(48))
        prayer_row.add_widget(self.play_prayer_during_silent_check)
        prayer_row.add_widget(lbl("Vakit giriş sesini sessiz sürede çal", color=TEXT,
                                  size="13sp", halign="left"))
        c.add_widget(prayer_row)

        c.add_widget(lbl("Vakitlere göre sessiz kalma süresi", color=TEXT,
                         size="15sp", bold=True, size_hint_y=None,
                         height=dp(38), halign="left"))
        for title, key, icon in PRAYERS:
            row = BoxLayout(size_hint_y=None, height=dp(72), padding=dp(10), spacing=dp(8))
            rounded(row, WHITE, 17, MINT)
            row.add_widget(CanvasIcon(icon=icon, color=GREEN,
                                      size_hint_x=None, width=dp(48)))
            check = CheckBox(active=self.settings["silent_enabled"][key],
                             size_hint_x=None, width=dp(46))
            field = TextInput(text=str(self.settings["silent"][key]),
                              input_filter="int", multiline=False,
                              halign="center", size_hint_x=None, width=dp(82),
                              background_normal="", background_color=MINT,
                              foreground_color=TEXT)
            row.add_widget(check)
            row.add_widget(lbl(title, color=TEXT, size="15sp", halign="left"))
            row.add_widget(field)
            row.add_widget(lbl("dk", color=TEXT, size_hint_x=None, width=dp(34)))
            self.silent_widgets[key] = (check, field)
            c.add_widget(row)

        save_button = FlatButton(text="UYGULAMA SESSİZ MODUNU KAYDET",
                                 size_hint_y=None, height=dp(56))
        save_button.bind(on_release=self.save_silent_settings)
        c.add_widget(save_button)

    def save_silent_settings(self, *_):
        streams = {"Alarm sesi": "ALARM", "Medya sesi": "MEDIA",
                   "Bildirim sesi": "NOTIFICATION"}
        self.settings["app_silent_mode"] = bool(self.app_silent_mode_check.active)
        self.settings["silent_mode_vibration"] = bool(self.silent_vibration_check.active)
        self.settings["silent_audio_stream"] = streams.get(
            self.silent_audio_stream_spinner.text, "ALARM")
        self.settings["play_pre_sound_during_silent"] = bool(
            self.play_pre_during_silent_check.active)
        self.settings["play_prayer_sound_during_silent"] = bool(
            self.play_prayer_during_silent_check.active)
        for _, key, _ in PRAYERS:
            check, field = self.silent_widgets[key]
            self.settings["silent_enabled"][key] = bool(check.active)
            try:
                self.settings["silent"][key] = max(0, min(1440, int(field.text or 0)))
            except ValueError:
                self.settings["silent"][key] = 30
        self.save(self.settings_file, self.settings)
        self.schedule_all_alarms()
        self.sync_android_surfaces()
        self.alert("Kaydedildi", "Sessiz mod, titreşim ve ses kategorisi kaydedildi.")
    def show_offset_settings(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.settings_page_header("Vakit ve Konum Sapma Ayarı"))
        c.add_widget(lbl(
            "Yerel ezan uygulamadaki vakitten 1 dakika önce okunuyorsa -1, "
            "1 dakika sonra okunuyorsa +1 girin. Genel düzeltme bütün vakitlere, "
            "özel düzeltme yalnız seçilen vakte uygulanır.",
            color=MUTED, size="13sp", size_hint_y=None, height=dp(88),
            halign="left", valign="middle"))
        self.global_offset_input = TextInput(
            text=str(self.settings.get("global_time_offset", 0)),
            input_filter="int", multiline=False, halign="center",
            size_hint_y=None, height=dp(52), background_normal="",
            background_color=MINT, foreground_color=TEXT)
        c.add_widget(lbl("Tüm vakitler için dakika farkı", color=TEXT,
                         size="13sp", size_hint_y=None, height=dp(30), halign="left"))
        c.add_widget(self.global_offset_input)
        self.prayer_offset_inputs = {}
        for title, key, _ in PRAYERS:
            row = BoxLayout(size_hint_y=None, height=dp(58), padding=dp(8), spacing=dp(8))
            rounded(row, WHITE, 16, MINT)
            row.add_widget(lbl(title, color=TEXT, size="14sp", halign="left"))
            field = TextInput(
                text=str(self.settings.get("prayer_offsets", {}).get(key, 0)),
                input_filter="int", multiline=False, halign="center",
                size_hint_x=None, width=dp(90), background_normal="",
                background_color=MINT, foreground_color=TEXT)
            self.prayer_offset_inputs[key] = field
            row.add_widget(field)
            row.add_widget(lbl("dk", color=TEXT, size_hint_x=None, width=dp(34)))
            c.add_widget(row)
        save_button = FlatButton(text="DAKİKA DÜZELTMELERİNİ UYGULA",
                                 size_hint_y=None, height=dp(56))
        save_button.bind(on_release=self.save_time_adjustments)
        c.add_widget(save_button)

    def show_kerahat_settings(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.settings_page_header("Kerahat Vakti"))
        c.add_widget(lbl(
            "Kerahat sürelerini dakika olarak belirleyin. Hesaplanan başlangıç ve "
            "bitiş saatleri ana ekran ile widget üzerinde gösterilir.",
            color=MUTED, size="13sp", size_hint_y=None, height=dp(70),
            halign="left", valign="middle"))
        self.kerahat_inputs = {}
        definitions = [
            ("Doğuş sonrası", "kerahat_sunrise_minutes", 45),
            ("Öğle öncesi", "kerahat_noon_minutes", 10),
            ("Akşam öncesi", "kerahat_sunset_minutes", 45),
        ]
        for title, key, default in definitions:
            row = BoxLayout(size_hint_y=None, height=dp(68), padding=dp(10), spacing=dp(8))
            rounded(row, WHITE, 17, MINT)
            row.add_widget(lbl(title, color=TEXT, size="15sp", halign="left"))
            field = TextInput(text=str(self.settings.get(key, default)),
                              input_filter="int", multiline=False, halign="center",
                              size_hint_x=None, width=dp(88), background_normal="",
                              background_color=MINT, foreground_color=TEXT)
            self.kerahat_inputs[key] = field
            row.add_widget(field)
            row.add_widget(lbl("dk", color=TEXT, size_hint_x=None, width=dp(34)))
            c.add_widget(row)
        preview = self.kerahat_periods()
        if preview:
            c.add_widget(lbl(
                "Bugünkü aralıklar:\n" + "\n".join(
                    f"{title}: {start} - {end}" for title, start, end in preview),
                color=RED, size="13sp", size_hint_y=None, height=dp(105),
                halign="left"))
        save_button = FlatButton(text="KERAHAT SÜRELERİNİ KAYDET",
                                 size_hint_y=None, height=dp(56))
        save_button.bind(on_release=self.save_kerahat_settings)
        c.add_widget(save_button)

    def save_kerahat_settings(self, *_):
        defaults = {"kerahat_sunrise_minutes": 45,
                    "kerahat_noon_minutes": 10,
                    "kerahat_sunset_minutes": 45}
        for key, field in self.kerahat_inputs.items():
            try:
                self.settings[key] = max(0, min(180, int(field.text or defaults[key])))
            except ValueError:
                self.settings[key] = defaults[key]
        self.save(self.settings_file, self.settings)
        self.sync_android_surfaces()
        self.alert("Kaydedildi", "Kerahat süreleri ve widget yenilendi.")
        self.show_kerahat_settings()

    def show_widget_settings(self, *_):
        self.clear()
        c = self.scroll()
        c.add_widget(self.settings_page_header("Üst Bildirim ve Widget"))
        card = BoxLayout(orientation="vertical", size_hint_y=None,
                         height=dp(210), padding=dp(14), spacing=dp(10))
        rounded(card, WHITE, 20, MINT)
        row = BoxLayout(size_hint_y=None, height=dp(62), spacing=dp(8))
        check = CheckBox(active=self.settings.get("persistent_notification", True),
                         size_hint_x=None, width=dp(55))
        check.bind(active=lambda _, value: self.toggle_persistent_notification(value))
        row.add_widget(check)
        row.add_widget(lbl("Namaz vakitlerini üst bildirimde göster",
                           color=TEXT, size="14sp", halign="left"))
        card.add_widget(row)
        widget_button = FlatButton(text="ANA EKRANA WIDGET EKLE",
                                   size_hint_y=None, height=dp(56))
        widget_button.bind(on_release=self.add_prayer_widget)
        card.add_widget(widget_button)
        refresh = FlatButton(text="WIDGET VE BİLDİRİMİ YENİLE",
                             size_hint_y=None, height=dp(52), bg=DARK)
        refresh.bind(on_release=lambda *_: self.sync_android_surfaces())
        card.add_widget(refresh)
        c.add_widget(card)

    def show_sound_library_settings(self, *_):
        self.clear()
        self.sound_catalog = self.scan_sounds()
        c = self.scroll()
        c.add_widget(self.settings_page_header("Ses Dosyaları"))
        c.add_widget(lbl(
            f"{max(0, len(self.sound_catalog)-2)} özel ses dosyası bulundu. "
            "Seslerin hangi vakitte kullanılacağını Hatırlatma Ayarları bölümünden seçebilirsiniz.",
            color=MUTED, size="13sp", size_hint_y=None, height=dp(70),
            halign="left", valign="middle"))
        for name, value in self.sound_catalog.items():
            row = BoxLayout(size_hint_y=None, height=dp(58), padding=dp(8), spacing=dp(8))
            rounded(row, WHITE, 16, MINT)
            row.add_widget(lbl(name, color=TEXT, size="13sp", halign="left"))
            play = FlatButton(text="ÇAL", size_hint_x=None, width=dp(70))
            play.bind(on_release=lambda _, item=value: self.preview(item))
            row.add_widget(play)
            c.add_widget(row)

    def force_update_times(self, *_):
        self.ensure_times(True)
        self.sync_android_surfaces()
        self.alert("Vakitler Güncellendi", "Vakitler, alarmlar, widget ve üst bildirim yenilendi.")

    def toggle_persistent_notification(self, value):
        self.settings["persistent_notification"] = bool(value)
        self.save(self.settings_file, self.settings)
        self.sync_android_surfaces()

    def show_theme_settings(self, *_):
        self.alert("Tema", "Tema seçimi sonraki güncellemede açık, koyu ve yeşil seçenekleriyle eklenecektir.")

    def force_update_times(self, *_):
        self.ensure_times(True)
        self.sync_android_surfaces()
        self.alert("Vakitler Güncellendi", "Namaz vakitleri, widget ve üst bildirim yenilendi.")

    def show_time_adjustment_settings(self, *_):
        self.show_reminder_settings()
        Clock.schedule_once(lambda *_: self.alert(
            "Vakit Sapma Ayarı",
            "Konum ve Vakit Dakika Düzeltmesi bölümünden tüm vakitleri veya her vakti ayrı ayarlayabilirsiniz."
        ), .25)

    def show_kerahat_settings(self, *_):
        self.show_reminder_settings()
        Clock.schedule_once(lambda *_: self.alert(
            "Kerahat Vakti",
            "Kerahat süreleri mevcut ayarlara göre ana ekran ve widget üzerinde gösterilir."
        ), .25)

    def toggle_persistent_notification(self, value):
        self.settings["persistent_notification"] = bool(value)
        self.save(self.settings_file, self.settings)
        self.sync_android_surfaces()

    def toggle_iftar_countdown(self, value):
        self.settings["iftar_countdown"] = bool(value)
        self.save(self.settings_file, self.settings)

    def show_reminder_settings(self, *_):
        self.clear()
        self.sound_catalog = self.scan_sounds()
        self.sound_widgets = {}
        c = self.scroll()
        c.add_widget(self.header("Ayarlar"))
        c.add_widget(lbl(
            f"{max(0, len(self.sound_catalog)-2)} ses dosyası bulundu",
            color=TEXT, size="15sp", size_hint_y=None, height=dp(40)
        ))

        adjustment_card = BoxLayout(
            orientation="vertical", size_hint_y=None, height=dp(545),
            padding=dp(14), spacing=dp(8)
        )
        rounded(adjustment_card, WHITE, 22, MINT)

        adjustment_card.add_widget(lbl(
            "[b]Konum ve Vakit Dakika Düzeltmesi[/b]",
            color=TEXT, size="17sp", markup=True,
            size_hint_y=None, height=dp(38), halign="left"
        ))

        adjustment_card.add_widget(lbl(
            "Bulunduğunuz yer listede yoksa yakın konumu seçin. Yerel ezan "
            "seçilen vakitten 1 dakika önce okunuyorsa -1, 1 dakika sonra "
            "okunuyorsa +1 yazın. Genel düzeltme bütün vakitlere, alt "
            "satırlar yalnız ilgili vakte uygulanır.",
            color=MUTED, size="12sp", size_hint_y=None, height=dp(92),
            halign="left", valign="middle"
        ))

        global_row = BoxLayout(
            size_hint_y=None, height=dp(48), spacing=dp(8),
            padding=(dp(2), 0)
        )
        global_row.add_widget(lbl(
            "[b]Tüm vakitler[/b]", color=TEXT, size="13sp", markup=True,
            halign="left"
        ))
        self.global_offset_input = TextInput(
            text=str(self.settings.get("global_time_offset", 0)),
            input_filter="int", multiline=False, halign="center",
            size_hint_x=None, width=dp(82), background_normal="",
            background_color=MINT, foreground_color=TEXT,
            padding=(dp(8), dp(12))
        )
        global_row.add_widget(self.global_offset_input)
        global_row.add_widget(lbl(
            "dk", color=TEXT, size_hint_x=None, width=dp(32)
        ))
        adjustment_card.add_widget(global_row)

        separator = Widget(size_hint_y=None, height=dp(2))
        with separator.canvas:
            Color(*MINT)
            separator._line = Rectangle(pos=separator.pos, size=separator.size)
        def update_separator(*_):
            separator._line.pos = separator.pos
            separator._line.size = separator.size
        separator.bind(pos=update_separator, size=update_separator)
        adjustment_card.add_widget(separator)

        self.prayer_offset_inputs = {}
        offsets_grid = BoxLayout(
            orientation="vertical", size_hint_y=None,
            height=dp(6 * 44), spacing=dp(4)
        )
        for prayer_title, prayer_key, _ in PRAYERS:
            offset_row = BoxLayout(
                size_hint_y=None, height=dp(40), spacing=dp(8),
                padding=(dp(2), 0)
            )
            offset_row.add_widget(lbl(
                prayer_title, color=TEXT, size="13sp", halign="left"
            ))
            offset_input = TextInput(
                text=str(self.settings.get("prayer_offsets", {}).get(prayer_key, 0)),
                input_filter="int", multiline=False, halign="center",
                size_hint_x=None, width=dp(82), background_normal="",
                background_color=MINT, foreground_color=TEXT,
                padding=(dp(8), dp(9))
            )
            self.prayer_offset_inputs[prayer_key] = offset_input
            offset_row.add_widget(offset_input)
            offset_row.add_widget(lbl(
                "dk", color=TEXT, size_hint_x=None, width=dp(32)
            ))
            offsets_grid.add_widget(offset_row)
        adjustment_card.add_widget(offsets_grid)

        apply_offset = FlatButton(
            text="VAKİT DÜZELTMESİNİ UYGULA",
            size_hint_y=None, height=dp(54), bg=GREEN,
            color=WHITE, font_size="14sp"
        )
        apply_offset.bind(on_release=self.save_time_adjustments)
        adjustment_card.add_widget(apply_offset)
        c.add_widget(adjustment_card)

        surface_card = BoxLayout(orientation="vertical", size_hint_y=None,
                                 height=dp(190), padding=dp(14), spacing=dp(9))
        rounded(surface_card, WHITE, 22, MINT)
        surface_head = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(8))
        surface_head.add_widget(CanvasIcon(icon="clock", color=GREEN,
                                           size_hint_x=None, width=dp(48)))
        surface_head.add_widget(lbl("[b]Üst Bildirim ve Widget[/b]", color=TEXT,
                                    size="17sp", markup=True, halign="left"))
        surface_card.add_widget(surface_head)

        notification_row = BoxLayout(size_hint_y=None, height=dp(55), spacing=dp(8))
        self.persistent_notification_check = CheckBox(
            active=self.settings.get("persistent_notification", True),
            size_hint_x=None, width=dp(48))
        notification_row.add_widget(self.persistent_notification_check)
        notification_row.add_widget(lbl(
            "Namaz vakitlerini üst bildirimde göster",
            color=TEXT, size="14sp", halign="left"))
        surface_card.add_widget(notification_row)

        widget_button = FlatButton(text="ANA EKRANA WIDGET EKLE",
                                   size_hint_y=None, height=dp(52),
                                   bg=GREEN, color=WHITE, font_size="14sp")
        widget_button.bind(on_release=self.add_prayer_widget)
        surface_card.add_widget(widget_button)
        c.add_widget(surface_card)
        for title, key, icon in PRAYERS:
            card = BoxLayout(orientation="vertical", size_hint_y=None,
                             height=dp(385), padding=dp(12), spacing=dp(7))
            rounded(card, WHITE, 20, MINT)
            head = BoxLayout(size_hint_y=None, height=dp(42))
            head.add_widget(CanvasIcon(icon=icon, color=GREEN,
                                       size_hint_x=None, width=dp(42)))
            enabled = CheckBox(active=self.settings["enabled"][key],
                               size_hint_x=None, width=dp(45))
            head.add_widget(enabled)
            head.add_widget(lbl(f"[b]{title} vakti[/b]", markup=True, size="17sp"))
            card.add_widget(head)
            pre_check, pre_input, pre_row = self.minute_row(
                "Ön uyarı", self.settings["pre_enabled"][key], self.settings["pre"][key]
            )
            card.add_widget(pre_row)
            pre_spinner = self.sound_row(card, "Ön bildirim sesi", self.settings["pre_sound"][key])
            silent_check, silent_input, silent_row = self.minute_row(
                "Sessiz kalma", self.settings["silent_enabled"][key], self.settings["silent"][key]
            )
            card.add_widget(silent_row)
            prayer_spinner = self.sound_row(card, "Vakit giriş sesi", self.settings["prayer_sound"][key])
            self.sound_widgets[key] = (
                enabled, pre_check, pre_input, silent_check, silent_input,
                pre_spinner, prayer_spinner,
            )
            c.add_widget(card)
        save_button = FlatButton(text="Kaydet ve Alarmları Yenile",
                                 size_hint_y=None, height=dp(55))
        save_button.bind(on_release=self.save_settings)
        c.add_widget(save_button)
        permission_panel = BoxLayout(orientation="horizontal", size_hint_y=None,
                                     height=dp(122), padding=dp(12), spacing=dp(10))
        rounded(permission_panel, (0.93, 1.0, 0.97, 1), 24, GREEN)
        permission_panel.add_widget(PermissionIcon(
            granted=False, size_hint_x=None, width=dp(82)))
        permission_text = FlatButton(
            text="İZİNLERİ GÖRÜNTÜLE\nVE KONTROL ET",
            bg=GREEN, color=WHITE, font_size="16sp", bold=True)
        permission_text.bind(on_release=self.show_permissions)
        permission_panel.add_widget(permission_text)
        c.add_widget(permission_panel)

    def minute_row(self, title, active, value):
        row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        check = CheckBox(active=active, size_hint_x=None, width=dp(42))
        field = TextInput(text=str(value), input_filter="int", multiline=False,
                          halign="center", size_hint_x=None, width=dp(70),
                          background_normal="", background_color=MINT)
        row.add_widget(check)
        row.add_widget(lbl(title, size="13sp"))
        row.add_widget(field)
        row.add_widget(lbl("dk", size_hint_x=None, width=dp(28)))
        return check, field, row

    def sound_row(self, card, title, value):
        row = BoxLayout(size_hint_y=None, height=dp(72), spacing=dp(5))
        left = BoxLayout(orientation="vertical")
        left.add_widget(lbl(title, color=TEXT, size="12sp",
                            size_hint_y=None, height=dp(24), halign="left"))
        text = next((name for name, item in self.sound_catalog.items() if item == value),
                    "Varsayılan Android Sesi")
        spinner = Spinner(text=text, values=tuple(self.sound_catalog),
                          background_normal="", background_color=MINT, color=TEXT)
        left.add_widget(spinner)
        row.add_widget(left)
        play = FlatButton(text="ÇAL", size_hint_x=None, width=dp(60), font_size="11sp")
        play.bind(on_release=lambda _, control=spinner: self.preview(self.sound_catalog[control.text]))
        stop = FlatButton(text="DUR", size_hint_x=None, width=dp(60),
                          bg=(.40, .46, .43, 1), font_size="11sp")
        stop.bind(on_release=lambda *_: self.stop_preview())
        row.add_widget(play)
        row.add_widget(stop)
        card.add_widget(row)
        return spinner

    def preview(self, value):
        self.stop_preview()
        if not value.startswith("FILE::"):
            self.alert("Bilgi", "Bu seçim uygulama içinde önizlenemez.")
            return
        path = value.split("::", 1)[1]
        self.preview_sound = SoundLoader.load(path)
        if self.preview_sound:
            self.preview_sound.play()
        else:
            self.alert("Ses Hatası", "Ses açılamadı. WAV PCM biçimini kullanın.")

    def stop_preview(self):
        if self.preview_sound:
            try:
                self.preview_sound.stop()
                self.preview_sound.unload()
            except Exception:
                pass
        self.preview_sound = None

    def save_settings(self, *_):
        for _, key, _ in PRAYERS:
            enabled, pre_check, pre_input, silent_check, silent_input, pre_sound, prayer_sound = self.sound_widgets[key]
            self.settings["enabled"][key] = enabled.active
            self.settings["pre_enabled"][key] = pre_check.active
            self.settings["silent_enabled"][key] = silent_check.active
            try:
                self.settings["pre"][key] = max(0, min(int(pre_input.text or 0), 1440))
            except ValueError:
                self.settings["pre"][key] = 10
            try:
                self.settings["silent"][key] = max(0, min(int(silent_input.text or 0), 1440))
            except ValueError:
                self.settings["silent"][key] = 30
            self.settings["pre_sound"][key] = self.sound_catalog[pre_sound.text]
            self.settings["prayer_sound"][key] = self.sound_catalog[prayer_sound.text]
        if hasattr(self, "persistent_notification_check"):
            self.settings["persistent_notification"] = bool(
                self.persistent_notification_check.active
            )
        self.save(self.settings_file, self.settings)
        self.schedule_all_alarms()
        self.sync_android_surfaces()
        self.alert("Kaydedildi", "Ayarlar, alarmlar, widget ve üst bildirim yenilendi.")

    def is_android(self):
        return os.environ.get("ANDROID_ARGUMENT") is not None

    def ask_runtime_permissions(self):
        if not self.is_android():
            return
        try:
            from android.permissions import Permission, request_permissions
            permissions = [Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION]
            try:
                permissions.append(Permission.POST_NOTIFICATIONS)
            except AttributeError:
                pass
            request_permissions(permissions)
        except Exception:
            pass

    def alarm_sound_value(self, value):
        if value.startswith("FILE::"):
            return "PRESET::" + Path(value.split("::", 1)[1]).stem
        return value

    def schedule_all_alarms(self):
        if not self.is_android() or not self.times:
            return
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            PendingIntent = autoclass("android.app.PendingIntent")
            AlarmManager = autoclass("android.app.AlarmManager")
            Build = autoclass("android.os.Build")
            AlarmReceiver = autoclass("org.mustafayildiz.ezan.AlarmReceiver")
            context = PythonActivity.mActivity
            manager = context.getSystemService(context.ALARM_SERVICE)
            now = datetime.now()
            request_code = 1000
            for record in self.times:
                date_text = record.get("date", "")
                for title, key, _ in PRAYERS:
                    if not self.settings["enabled"].get(key, True):
                        continue
                    try:
                        prayer_time = datetime.strptime(
                            date_text + " " + self.effective_time(record, key), "%Y-%m-%d %H:%M"
                        )
                    except Exception:
                        continue
                    events = []
                    pre_minutes = int(self.settings["pre"].get(key, 0))
                    if self.settings["pre_enabled"].get(key, True) and pre_minutes > 0:
                        events.append((
                            prayer_time - timedelta(minutes=pre_minutes),
                            "PRE", f"{title} vaktine {pre_minutes} dakika kaldı",
                            self.settings["pre_sound"].get(key, "DEFAULT"),
                        ))
                    events.append((
                        prayer_time, "PRAYER", f"{title} vakti girdi",
                        self.settings["prayer_sound"].get(key, "DEFAULT"),
                    ))
                    silent_minutes = int(self.settings["silent"].get(key, 0))
                    if self.settings["silent_enabled"].get(key, True) and silent_minutes > 0:
                        events.append((prayer_time + timedelta(seconds=3), "SILENCE", title, "SILENT"))
                        events.append((prayer_time + timedelta(minutes=silent_minutes), "RESTORE", title, "SILENT"))
                    for event_time, action, message, sound_value in events:
                        if event_time <= now:
                            continue
                        intent = Intent(context, AlarmReceiver)
                        intent.putExtra("action", action)
                        intent.putExtra("title", "Miraç Ezan Vakti")
                        intent.putExtra("message", message)
                        intent.putExtra("id", request_code)
                        intent.putExtra("prayer_key", key + "_" + action.lower())
                        intent.putExtra("sound_uri", self.alarm_sound_value(sound_value))
                        intent.putExtra("app_silent_mode", bool(self.settings.get("app_silent_mode", True)))
                        intent.putExtra("vibration_enabled", bool(self.settings.get("silent_mode_vibration", True)))
                        intent.putExtra("audio_stream", str(self.settings.get("silent_audio_stream", "ALARM")))
                        intent.putExtra("play_pre_in_silent", bool(self.settings.get("play_pre_sound_during_silent", False)))
                        intent.putExtra("play_prayer_in_silent", bool(self.settings.get("play_prayer_sound_during_silent", True)))
                        intent.putExtra("silent_minutes", silent_minutes)
                        pending = PendingIntent.getBroadcast(
                            context, request_code, intent,
                            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE,
                        )
                        trigger = int(event_time.timestamp() * 1000)
                        if Build.VERSION.SDK_INT >= 31 and not manager.canScheduleExactAlarms():
                            manager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pending)
                        else:
                            manager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pending)
                        request_code += 1
        except Exception as error:
            Clock.schedule_once(lambda *_: self.alert("Alarm Planlama Hatası", str(error)))



    def permission_definitions(self):
        return [
            ("Bildirim izni", "notifications",
             "Namaz vakti, ön uyarı ve eksik izin bildirimlerinin görünmesini sağlar. "
             "Kapalıysa uygulama arka plandayken bildirim gösterilemez."),
            ("Konum izni", "location",
             "Kıble yönü ve konuma bağlı özelliklerin doğru çalışması için kullanılır."),
            ("Kesin alarm izni", "exact_alarm",
             "Namaz vakti ve ön bildirim alarmlarının seçilen dakikada çalışmasını sağlar. "
             "Kapalıysa Android alarmı geciktirebilir."),
            ("Pil optimizasyonu muafiyeti", "battery",
             "Android'in uygulamayı arka planda erken durdurmasını önlemeye yardımcı olur. "
             "Alarm ve kalıcı bildirim güvenilirliğini artırır."),
        ]

    def get_permission_states(self):
        states = {key: True for _, key, _ in self.permission_definitions()}
        if not self.is_android():
            return states
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Build = autoclass("android.os.Build")
            PackageManager = autoclass("android.content.pm.PackageManager")
            context = PythonActivity.mActivity

            states["location"] = True
            if Build.VERSION.SDK_INT >= 23:
                states["location"] = (
                    context.checkSelfPermission("android.permission.ACCESS_FINE_LOCATION")
                    == PackageManager.PERMISSION_GRANTED
                    or context.checkSelfPermission("android.permission.ACCESS_COARSE_LOCATION")
                    == PackageManager.PERMISSION_GRANTED
                )

            NotificationManagerCompat = autoclass("androidx.core.app.NotificationManagerCompat")
            states["notifications"] = bool(
                NotificationManagerCompat.from_(context).areNotificationsEnabled()
            )
            if Build.VERSION.SDK_INT >= 33:
                states["notifications"] = states["notifications"] and (
                    context.checkSelfPermission("android.permission.POST_NOTIFICATIONS")
                    == PackageManager.PERMISSION_GRANTED
                )

            AlarmManager = autoclass("android.app.AlarmManager")
            alarm_manager = context.getSystemService(context.ALARM_SERVICE)
            states["exact_alarm"] = (
                bool(alarm_manager.canScheduleExactAlarms())
                if Build.VERSION.SDK_INT >= 31 else True
            )

            NotificationManager = autoclass("android.app.NotificationManager")
            notification_manager = context.getSystemService(context.NOTIFICATION_SERVICE)
            states["notification_policy"] = bool(
                notification_manager.isNotificationPolicyAccessGranted()
            )

            PowerManager = autoclass("android.os.PowerManager")
            power_manager = context.getSystemService(context.POWER_SERVICE)
            states["battery"] = bool(
                power_manager.isIgnoringBatteryOptimizations(context.getPackageName())
            )
        except Exception:
            pass
        return states

    def show_permissions(self, *_):
        self.clear()
        content = self.scroll()
        content.add_widget(self.header("İzin Kontrolü"))

        states = self.get_permission_states()
        total = len(states)
        granted_count = sum(1 for value in states.values() if value)
        permission_percent = int(round((granted_count / total) * 100)) if total else 100

        summary = BoxLayout(orientation="vertical", size_hint_y=None,
                            height=dp(145), padding=dp(15), spacing=dp(7))
        rounded(summary, GREEN if granted_count == total else WHITE, 24, MINT)
        summary.add_widget(lbl(
            "[b]Tüm izinler hazır[/b]" if granted_count == total
            else "[b]Tamamlanması gereken izinler var[/b]",
            color=WHITE if granted_count == total else TEXT,
            size="20sp", markup=True, size_hint_y=None, height=dp(38)
        ))
        summary.add_widget(lbl(
            f"{granted_count} / {total} izin etkin   |   %{permission_percent}",
            color=WHITE if granted_count == total else MUTED,
            size="15sp", size_hint_y=None, height=dp(28)
        ))
        progress = FloatLayout(size_hint_y=None, height=dp(34))
        with progress.canvas.before:
            Color(.82, .88, .84, 1)
            progress._permission_bg = RoundedRectangle(
                pos=progress.pos, size=progress.size, radius=[dp(10)])
            Color(*GREEN)
            progress._permission_fg = RoundedRectangle(
                pos=progress.pos,
                size=(progress.width * granted_count / total, progress.height),
                radius=[dp(10)])
        def update_progress(*_):
            progress._permission_bg.pos = progress.pos
            progress._permission_bg.size = progress.size
            progress._permission_fg.pos = progress.pos
            progress._permission_fg.size = (
                progress.width * granted_count / total, progress.height)
        progress.bind(pos=update_progress, size=update_progress)
        percent_label = lbl(
            f"%{permission_percent}", color=WHITE,
            size="13sp", bold=True, size_hint=(1, 1),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        progress.add_widget(percent_label)
        summary.add_widget(progress)
        content.add_widget(summary)

        for title, key, description in self.permission_definitions():
            granted = bool(states.get(key, False))
            card = BoxLayout(orientation="horizontal", size_hint_y=None,
                             height=dp(166), padding=dp(12), spacing=dp(10))
            rounded(card, WHITE, 20,
                    (0.35, .82, .63, 1) if granted else (1, .47, .39, 1))

            card.add_widget(PermissionIcon(
                granted=granted, size_hint_x=None, width=dp(68)))

            text_area = BoxLayout(orientation="vertical", spacing=dp(3))
            text_area.add_widget(lbl(
                f"[b]{title}[/b]", color=TEXT, size="16sp", markup=True,
                size_hint_y=None, height=dp(30), halign="left"))
            text_area.add_widget(lbl(
                description, color=MUTED, size="12sp",
                size_hint_y=None, height=dp(74), halign="left", valign="middle"))
            text_area.add_widget(lbl(
                "Etkin" if granted else "İzin gerekli",
                color=(.02, .53, .29, 1) if granted else (.82, .10, .05, 1),
                size="13sp", bold=True, size_hint_y=None, height=dp(26),
                halign="left"))
            card.add_widget(text_area)

            action = FlatButton(
                text="AÇIK" if granted else "AYARI AÇ",
                color=WHITE, size_hint_x=None, width=dp(102),
                bg=(.10, .62, .39, 1) if granted else GREEN,
                font_size="12sp")
            if not granted:
                action.bind(
                    on_release=lambda _, permission_key=key:
                    self.open_permission_setting(permission_key))
            card.add_widget(action)
            content.add_widget(card)

        refresh = FlatButton(
            text="İZİNLERİ YENİDEN KONTROL ET",
            size_hint_y=None, height=dp(56), bg=GREEN)
        refresh.bind(on_release=self.show_permissions)
        content.add_widget(refresh)

        back = FlatButton(text="AYARLARA DÖN", size_hint_y=None,
                          height=dp(52), bg=DARK)
        back.bind(on_release=self.show_settings)
        content.add_widget(back)

    def check_permissions_on_start(self, *_):
        if not self.is_android():
            return
        states = self.get_permission_states()
        missing = [title for title, key, _ in self.permission_definitions()
                   if not states.get(key, False)]
        if not missing:
            return
        box = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        rounded(box, BG, 22)
        visual = PermissionIcon(granted=False, size_hint_y=None, height=dp(92))
        box.add_widget(visual)
        box.add_widget(lbl("[b]Eksik İzinler Var[/b]", color=TEXT,
                           size="21sp", markup=True,
                           size_hint_y=None, height=dp(40)))
        box.add_widget(lbl(
            "Aşağıdaki izinler tamamlanmalıdır:\n\n" +
            "\n".join("• " + item for item in missing),
            color=TEXT, size="14sp", halign="left", valign="middle"))
        buttons = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        later = FlatButton(text="DAHA SONRA", bg=(.45, .48, .45, 1))
        open_button = FlatButton(text="İZİNLERİ KONTROL ET", bg=GREEN)
        buttons.add_widget(later)
        buttons.add_widget(open_button)
        box.add_widget(buttons)
        popup = Popup(title="", separator_height=0, content=box,
                      size_hint=(.92, .76), auto_dismiss=False,
                      background_color=(0, 0, 0, 0))
        later.bind(on_release=popup.dismiss)
        open_button.bind(
            on_release=lambda *_: (popup.dismiss(), self.show_permissions()))
        popup.open()

    def open_permission_setting(self, permission_key):
        if not self.is_android():
            self.alert("Bilgi", "İzin ayarları Android cihazda kullanılabilir.")
            return
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            Settings = autoclass("android.provider.Settings")
            Uri = autoclass("android.net.Uri")
            Build = autoclass("android.os.Build")
            context = PythonActivity.mActivity
            package_name = context.getPackageName()

            if permission_key == "location":
                try:
                    from android.permissions import Permission, request_permissions
                    request_permissions([
                        Permission.ACCESS_FINE_LOCATION,
                        Permission.ACCESS_COARSE_LOCATION])
                    return
                except Exception:
                    pass
            elif permission_key == "notifications" and Build.VERSION.SDK_INT >= 33:
                try:
                    from android.permissions import Permission, request_permissions
                    request_permissions([Permission.POST_NOTIFICATIONS])
                    return
                except Exception:
                    pass

            if permission_key == "exact_alarm" and Build.VERSION.SDK_INT >= 31:
                intent = Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM)
                intent.setData(Uri.parse("package:" + package_name))
            elif permission_key == "notification_policy":
                intent = Intent(Settings.ACTION_NOTIFICATION_POLICY_ACCESS_SETTINGS)
            elif permission_key == "battery":
                intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)
                intent.setData(Uri.parse("package:" + package_name))
            else:
                intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                intent.setData(Uri.parse("package:" + package_name))
            context.startActivity(intent)
        except Exception as error:
            self.alert("İzin Ayarı Açılamadı", str(error))

    def on_pause(self):
        return True

    def on_resume(self):
        Clock.schedule_once(lambda *_: self.check_permissions_on_start(), .8)
        Clock.schedule_once(lambda *_: self.sync_android_surfaces(), 1.2)

    def setup_popup(self, *_):
        box = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(10))
        rounded(box, BG, 20)
        box.add_widget(lbl("[b]Miraç Ezan Vakti[/b]", color=TEXT, size="24sp", markup=True))
        city = Spinner(text=self.settings["city"], values=tuple(sorted(PROVINCES)),
                       background_normal="", background_color=WHITE, color=TEXT)
        districts = tuple(sorted(KAYSERI_DISTRICTS)) if city.text == "Kayseri" else ("Merkez",)
        district = Spinner(text=self.settings["district"], values=districts,
                           background_normal="", background_color=WHITE, color=TEXT)
        city.bind(text=lambda _, value: self.update_setup_district(district, value))
        box.add_widget(city)
        box.add_widget(district)
        done = FlatButton(text="Kurulumu Tamamla")
        box.add_widget(done)
        popup = Popup(title="", separator_height=0, content=box,
                      size_hint=(.9, .72), auto_dismiss=False,
                      background_color=(0, 0, 0, 0))
        done.bind(on_release=lambda *_: self.finish_setup(popup, city.text, district.text))
        popup.open()

    @staticmethod
    def update_setup_district(spinner, city):
        spinner.values = tuple(sorted(KAYSERI_DISTRICTS)) if city == "Kayseri" else ("Merkez",)
        spinner.text = spinner.values[0]

    def finish_setup(self, popup, city, district):
        self.settings["city"] = city
        self.settings["district"] = district if city == "Kayseri" else "Merkez"
        self.settings["first_run"] = True
        self.save(self.settings_file, self.settings)
        self.ensure_times(True)
        self.sync_android_surfaces()
        popup.dismiss()
        self.show_home()

    def ensure_times(self, force=False):
        if self.times and not force and self.today_record():
            return
        lat, lon = self.current_coords()
        self.times = [
            self.calculate_day(date.today() + timedelta(days=i), lat, lon)
            for i in range(-1, 63)
        ]
        self.save(self.times_file, self.times)
        self.schedule_all_alarms()
        Clock.schedule_once(lambda *_: self.sync_android_surfaces(), .5)

    @staticmethod
    def calculate_day(day, lat, lon):
        number = day.timetuple().tm_yday
        lng_hour = lon / 15
        def calc(sunrise, zenith):
            t = number + ((6-lng_hour)/24 if sunrise else (18-lng_hour)/24)
            mean = .9856*t - 3.289
            longitude = (mean + 1.916*math.sin(math.radians(mean)) +
                         .020*math.sin(math.radians(2*mean)) + 282.634) % 360
            ascension = math.degrees(math.atan(.91764*math.tan(math.radians(longitude)))) % 360
            ascension += math.floor(longitude/90)*90 - math.floor(ascension/90)*90
            ascension /= 15
            sin_dec = .39782*math.sin(math.radians(longitude))
            cos_dec = math.cos(math.asin(sin_dec))
            cos_hour = ((math.cos(math.radians(zenith)) - sin_dec*math.sin(math.radians(lat))) /
                        (cos_dec*math.cos(math.radians(lat))))
            hour = math.degrees(math.acos(max(-1, min(1, cos_hour))))
            hour = (360-hour if sunrise else hour) / 15
            return (hour+ascension-.06571*t-6.622-lng_hour+3) % 24
        sunrise = calc(True, 90.833)
        sunset = calc(False, 90.833)
        noon = (sunrise + sunset) / 2
        values = {
            "Imsak": calc(True, 108), "Gunes": sunrise, "Ogle": noon,
            "Ikindi": noon+(sunset-noon)*.55, "Aksam": sunset,
            "Yatsi": calc(False, 107),
        }
        def fmt(value):
            minutes = int(round(value*60)) % 1440
            return f"{minutes//60:02d}:{minutes%60:02d}"
        return {"date": day.isoformat(), **{key: fmt(value) for key, value in values.items()}}

    @staticmethod
    def alert(title, message):
        Popup(title=title, content=lbl(message, halign="center"),
              size_hint=(.85, .38)).open()


if __name__ == "__main__":
    EzanApp().run()
