import {BsMastodon} from "react-icons/bs";

export const code2lan = {
  "aa": "Afar",
  "ab": "Abkhazian",
  "ae": "Avestan",
  "af": "Afrikaans",
  "ak": "Akan",
  "am": "Amharic",
  "an": "Aragonese",
  "ar": "Arabic",
  "as": "Assamese",
  "av": "Avaric",
  "ay": "Aymara",
  "az": "Azerbaijani",
  "ba": "Bashkir",
  "be": "Belarusian",
  "bg": "Bulgarian",
  "bh": "Bihari languages",
  "bi": "Bislama",
  "bm": "Bambara",
  "bn": "Bengali",
  "bo": "Tibetan",
  "br": "Breton",
  "bs": "Bosnian",
  "ca": "Catalan",
  "ce": "Chechen",
  "ch": "Chamorro",
  "co": "Corsican",
  "cr": "Cree",
  "cs": "Czech",
  "cu": "Church",
  "cv": "Chuvash",
  "cy": "Welsh",
  "da": "Danish",
  "de": "German",
  "dv": "Divehi",
  "dz": "Dzongkha",
  "ee": "Ewe",
  "el": "Greek",
  "en": "English",
  "eo": "Esperanto",
  "es": "Spanish",
  "et": "Estonian",
  "eu": "Basque",
  "fa": "Persian",
  "ff": "Fulah",
  "fi": "Finnish",
  "fj": "Fijian",
  "fo": "Faroese",
  "fr": "French",
  "fy": "Western Frisian",
  "ga": "Irish",
  "gd": "Gaelic",
  "gl": "Galician",
  "gn": "Guarani",
  "gu": "Gujarati",
  "gv": "Manx",
  "ha": "Hausa",
  "he": "Hebrew",
  "hi": "Hindi",
  "ho": "Hiri Motu",
  "hr": "Croatian",
  "ht": "Haitian",
  "hu": "Hungarian",
  "hy": "Armenian",
  "hz": "Herero",
  "ia": "Interlingua ",
  "id": "Indonesian",
  "ie": "Interlingue",
  "ig": "Igbo",
  "ii": "Sichuan Yi",
  "ik": "Inupiaq",
  "io": "Ido",
  "is": "Icelandic",
  "it": "Italian",
  "iu": "Inuktitut",
  "ja": "Japanese",
  "jv": "Javanese",
  "ka": "Georgian",
  "kg": "Kongo",
  "ki": "Kikuyu",
  "kj": "Kuanyama",
  "kk": "Kazakh",
  "kl": "Kalaallisut",
  "km": "Central Khmer",
  "kn": "Kannada",
  "ko": "Korean",
  "kr": "Kanuri",
  "ks": "Kashmiri",
  "ku": "Kurdish",
  "kv": "Komi",
  "kw": "Cornish",
  "ky": "Kirghiz",
  "la": "Latin",
  "lb": "Luxembourgish",
  "lg": "Ganda",
  "li": "Limburgan",
  "ln": "Lingala",
  "lo": "Lao",
  "lt": "Lithuanian",
  "lu": "Luba-Katanga",
  "lv": "Latvian",
  "mg": "Malagasy",
  "mh": "Marshallese",
  "mi": "Maori",
  "mk": "Macedonian",
  "ml": "Malayalam",
  "mn": "Mongolian",
  "mr": "Marathi",
  "ms": "Malay",
  "mt": "Maltese",
  "my": "Burmese",
  "na": "Nauru",
  "nb": "Bokmål,",
  "nd": "Ndebele",
  "ne": "Nepali",
  "ng": "Ndonga",
  "nl": "Dutch",
  "nn": "Norwegian Nynorsk",
  "no": "Norwegian",
  "nr": "Ndebele",
  "nv": "Navajo",
  "ny": "Chichewa",
  "oc": "Occitan",
  "oj": "Ojibwa",
  "om": "Oromo",
  "or": "Oriya",
  "os": "Ossetian",
  "pa": "Panjabi",
  "pi": "Pali",
  "pl": "Polish",
  "ps": "Pushto",
  "pt": "Portuguese",
  "qu": "Quechua",
  "rm": "Romansh",
  "rn": "Rundi",
  "ro": "Romanian",
  "ru": "Russian",
  "rw": "Kinyarwanda",
  "sa": "Sanskrit",
  "sc": "Sardinian",
  "sd": "Sindhi",
  "se": "Northern Sami",
  "sg": "Sango",
  "si": "Sinhala",
  "sk": "Slovak",
  "sl": "Slovenian",
  "sm": "Samoan",
  "sn": "Shona",
  "so": "Somali",
  "sq": "Albanian",
  "sr": "Serbian",
  "ss": "Swati",
  "st": "Sotho",
  "su": "Sundanese",
  "sv": "Swedish",
  "sw": "Swahili",
  "ta": "Tamil",
  "te": "Telugu",
  "tg": "Tajik",
  "th": "Thai",
  "ti": "Tigrinya",
  "tk": "Turkmen",
  "tl": "Tagalog",
  "tn": "Tswana",
  "to": "Tonga",
  "tr": "Turkish",
  "ts": "Tsonga",
  "tt": "Tatar",
  "tw": "Twi",
  "ty": "Tahitian",
  "ug": "Uighur",
  "uk": "Ukrainian",
  "ur": "Urdu",
  "uz": "Uzbek",
  "ve": "Venda",
  "vi": "Vietnamese",
  "vo": "Volapük",
  "wa": "Walloon",
  "wo": "Wolof",
  "xh": "Xhosa",
  "yi": "Yiddish",
  "yo": "Yoruba",
  "za": "Zhuang; Chuang",
  "zh": "Chinese",
  "zu": "Zulu"
} as any

const CardLanMastodon = (props: { data: { text: string, value: number, }[], className?: string }) => {

  const data = [...props.data].sort((a, b) => b.value - a.value).slice(0, 9)
  const total = data.reduce((a, b) => a + b.value, 0)
  return (
    <div
      className={"rounded-sm border border-stroke bg-white py-6 px-6 shadow-default dark:border-strokedark dark:bg-boxdark overflow-hidden " + props.className}>
      <div className='flex items-center space-x-4'>
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4 ">
          <BsMastodon className="text-xl fill-primary dark:fill-white"/>
        </div>
        <div className='text-2xl font-medium text-black-2 dark:text-white'>
          Localization
        </div>
      </div>

      <div className="mt-4 flex items-end justify-between dark:bg-boxdark overflow-hidden">
        <div className='flex flex-col w-full'>
          <div className="flex justify-between  text-title-md font-bold text-black dark:text-white w-full pb-2">
            <div>
              {total}
            </div>
            <div className="flex items-center gap-1 text-md font-medium dark:text-meta-2">
              Total
            </div>
          </div>
          {data.map((item, index) => (
            <div className="flex justify-between text-title-sm font-bold text-black dark:text-white w-full"
                 key={index.toString() + item}>
              <div>
                {item.value}
              </div>
              <div className="flex items-center gap-1 text-normal font-medium text-meta-3">
                {code2lan[item.text]}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CardLanMastodon;
